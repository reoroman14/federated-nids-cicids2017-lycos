# PART C/D: full pipeline. Usage:
#   python src/run_experiment.py --dataset lycos [--smoke] [--seeds 0 1 2 3 4]
# Produces raw per-seed results in results/<dataset>/ (or results/smoke/<dataset>/ with --smoke).
# Tables, figures and LaTeX are produced afterwards by src/report.py from these files.

import argparse
import json
import os
import sys
import time
import traceback
import warnings

# Must be set before torch initialises cuBLAS, required for deterministic GPU matmuls
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import torch  # noqa: E402
from torch import nn  # noqa: E402
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
from sklearn.impute import SimpleImputer  # noqa: E402
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix,  # noqa: E402
                             f1_score, precision_recall_fscore_support)
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.neighbors import KNeighborsClassifier  # noqa: E402
from sklearn.preprocessing import MinMaxScaler  # noqa: E402
from sklearn.svm import SVC  # noqa: E402
from sklearn.tree import DecisionTreeClassifier  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RESULTS, class_filter, load_clean, log_progress  # noqa: E402

# Flower is used for the FedAvg aggregation rule and for parameter serialisation (byte count).
# If it is unavailable the identical weighted average is computed manually.
try:
    from flwr.server.strategy.aggregate import aggregate as flwr_aggregate
    from flwr.common import ndarrays_to_parameters
    HAVE_FLWR = True
except Exception:  # pragma: no cover
    HAVE_FLWR = False

# ---------------------------------------------------------------- configuration
K_CLIENTS = 5
CAP_PER_CLASS = 1500
TEST_SIZE = 0.2
FL_ROUNDS = 10
LOCAL_EPOCHS = 5
CENTRAL_EPOCHS = FL_ROUNDS * LOCAL_EPOCHS  # same number of passes over the data as FedAvg
BATCH_SIZE = 64
LR = 1e-3
PATIENCE = 3
SMOKE_FRAC = 0.05
SMOKE_SAMPLE_SEED = 12345
CLASSIC = ["RF", "DT", "KNN", "SVM"]
# SVC(probability=True) is deprecated in sklearn 1.9 but still supported in the pinned 1.9.1
warnings.filterwarnings("ignore", message=".*`probability` parameter was deprecated.*")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

torch.use_deterministic_algorithms(True)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


def make_classic(name, seed):
    # Same hyper-parameters in every regime (central, client, control)
    if name == "RF":
        return RandomForestClassifier(n_estimators=100, max_depth=10, criterion="gini",
                                      random_state=seed, n_jobs=-1)
    if name == "DT":
        return DecisionTreeClassifier(max_depth=10, criterion="gini", random_state=seed)
    if name == "KNN":
        return KNeighborsClassifier(n_neighbors=5, metric="euclidean", n_jobs=-1)
    if name == "SVM":
        # probability=True only adds Platt scaling for soft voting; predict() still uses the decision function
        return SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=seed)
    raise ValueError(name)


# ---------------------------------------------------------------- metrics
def evaluate(y_true, y_pred, n_classes):
    labels = np.arange(n_classes)
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "precision": float(np.mean(p)),
        "recall": float(np.mean(r)),
        "f1": float(np.mean(f)),
        "per_class": {"precision": p, "recall": r, "f1": f, "support": s},
        "cm": confusion_matrix(y_true, y_pred, labels=labels),
    }


def full_proba(model, X, n_classes):
    # predict_proba aligned to all classes (a client may miss a class)
    P = np.zeros((X.shape[0], n_classes))
    P[:, model.classes_.astype(int)] = model.predict_proba(X)
    return P


def hard_vote(preds, n_classes):
    # preds: (n_models, n_samples). Majority vote; ties -> lowest class index (same as sklearn VotingClassifier)
    counts = np.zeros((preds.shape[1], n_classes), dtype=int)
    for p in preds:
        counts[np.arange(preds.shape[1]), p] += 1
    top = counts.max(axis=1)
    n_ties = int(((counts == top[:, None]).sum(axis=1) > 1).sum())
    return counts.argmax(axis=1), n_ties


# ---------------------------------------------------------------- MLP (PyTorch)
class MLP(nn.Module):
    def __init__(self, d_in, n_classes):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(),
                                 nn.Linear(64, n_classes))

    def forward(self, x):
        return self.net(x)


def new_mlp(d_in, n_classes, seed):
    torch.manual_seed(seed)
    return MLP(d_in, n_classes).to(DEVICE)


def train_epochs(model, X, y, epochs, gen_seed):
    # Plain mini-batch Adam training; a fresh optimiser per call (per round for FedAvg clients)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.CrossEntropyLoss()
    g = torch.Generator().manual_seed(int(gen_seed))
    n = X.shape[0]
    model.train()
    for _ in range(epochs):
        perm = torch.randperm(n, generator=g).to(DEVICE)
        for i in range(0, n, BATCH_SIZE):
            idx = perm[i:i + BATCH_SIZE]
            opt.zero_grad()
            loss = loss_fn(model(X[idx]), y[idx])
            loss.backward()
            opt.step()


@torch.no_grad()
def mlp_predict(model, X):
    model.eval()
    return model(X).argmax(1).cpu().numpy()


def get_weights(model):
    return [v.detach().cpu().numpy().copy() for v in model.state_dict().values()]


def set_weights(model, weights):
    sd = model.state_dict()
    for k, w in zip(sd.keys(), weights):
        sd[k] = torch.as_tensor(w, device=DEVICE)
    model.load_state_dict(sd)


def fedavg(results):
    # results: list of (weights, n_samples). Weighted by client sample count.
    if HAVE_FLWR:
        return flwr_aggregate(results)
    tot = sum(n for _, n in results)
    return [sum(w[i] * n for w, n in results) / tot for i in range(len(results[0][0]))]


def early_stop_round(curve, patience):
    # Returns (round where patience-based stopping triggers or None, best round). Rounds are 1-based.
    best, best_r, wait = -np.inf, 0, 0
    for r, v in enumerate(curve, start=1):
        if v > best:
            best, best_r, wait = v, r, 0
        else:
            wait += 1
            if wait >= patience:
                return r, best_r
    return None, best_r


# ---------------------------------------------------------------- data preparation
def prepare(df_all, classes, seed, log):
    rng = np.random.RandomState(seed)
    before = df_all["Label"].value_counts().reindex(classes).fillna(0).astype(int)
    parts = []
    for c in classes:
        sub = df_all[df_all["Label"] == c]
        if len(sub) > CAP_PER_CLASS:
            sub = sub.iloc[rng.choice(len(sub), CAP_PER_CLASS, replace=False)]
        parts.append(sub)
    df = pd.concat(parts, ignore_index=True)
    after = df["Label"].value_counts().reindex(classes).fillna(0).astype(int)
    log(f"  per-class counts before undersampling: {before.to_dict()}")
    log(f"  per-class counts after  undersampling: {after.to_dict()}")

    feat = [c for c in df.columns if c not in ("Label", "RawLabel")]
    X = df[feat].to_numpy(dtype=np.float64)
    y = df["Label"].map({c: i for i, c in enumerate(classes)}).to_numpy()
    raw = df["RawLabel"].to_numpy()

    # Split first, then fit imputer and scaler on the training part only
    Xtr, Xte, ytr, yte, rtr, rte = train_test_split(X, y, raw, test_size=TEST_SIZE, stratify=y, random_state=seed)
    imp = SimpleImputer(strategy="median").fit(Xtr)
    sc = MinMaxScaler().fit(imp.transform(Xtr))
    Xtr = sc.transform(imp.transform(Xtr))
    Xte = sc.transform(imp.transform(Xte))

    # IID partition into K equal-size clients
    perm = rng.permutation(len(ytr))
    parts_idx = np.array_split(perm, K_CLIENTS)
    sizes = {"total": int(len(y)), "train": int(len(ytr)), "test": int(len(yte)),
             "per_client": [int(len(p)) for p in parts_idx], "n_features": int(X.shape[1])}
    log(f"  sizes: total={sizes['total']} train={sizes['train']} test={sizes['test']} "
        f"per_client={sizes['per_client']} features={sizes['n_features']}")
    return dict(Xtr=Xtr, Xte=Xte, ytr=ytr, yte=yte, rte=rte, parts=parts_idx, sizes=sizes,
                before=before.to_dict(), after=after.to_dict(),
                client_class_counts=[np.bincount(ytr[p], minlength=len(classes)).tolist() for p in parts_idx])


# ---------------------------------------------------------------- one seed
def run_seed(df_all, classes, seed, log, stage_log):
    C = len(classes)
    t0 = time.time()
    log(f"=== seed {seed} ===")
    d = prepare(df_all, classes, seed, log)
    stage_log(f"seed {seed}: data prepared ({d['sizes']})")
    Xtr, Xte, ytr, yte, parts = d["Xtr"], d["Xte"], d["ytr"], d["yte"], d["parts"]
    out = {"metrics": [], "meta": {"seed": seed, "sizes": d["sizes"], "counts_before": d["before"],
                                   "counts_after": d["after"], "client_class_counts": d["client_class_counts"],
                                   "ties": {}, "failures": []}, "curve": None, "preds": {}}

    def record(model, regime, ev, extra=None):
        row = {"seed": seed, "model": model, "regime": regime,
               **{k: ev[k] for k in ["accuracy", "balanced_accuracy", "precision", "recall", "f1"]}}
        if extra:
            row.update(extra)
        row["per_class"] = {k: np.asarray(v).tolist() for k, v in ev["per_class"].items()}
        row["cm"] = np.asarray(ev["cm"]).tolist()
        out["metrics"].append(row)

    def safe(label, fn):
        try:
            fn()
        except Exception as e:
            msg = f"seed {seed}: FAILED {label}: {type(e).__name__}: {e}"
            log(msg)
            log(traceback.format_exc())
            out["meta"]["failures"].append(msg)
            stage_log(msg)

    # ---------------- classical models: central, federated voting, local-only
    for name in CLASSIC:
        def central(name=name):
            m = make_classic(name, seed).fit(Xtr, ytr)
            ptr = m.predict(Xtr)
            pte = m.predict(Xte)
            out["preds"][(name, "central")] = pte
            record(name, "central", evaluate(yte, pte, C),
                   {"train_f1": f1_score(ytr, ptr, average="macro", labels=np.arange(C), zero_division=0)})
            if name == "DT":
                out["meta"]["central_dt_depth"] = int(m.get_depth())
                out["meta"]["central_dt_leaves"] = int(m.get_n_leaves())
        safe(f"{name} central", central)

        def federated(name=name):
            clients = [make_classic(name, seed * 100 + k).fit(Xtr[p], ytr[p]) for k, p in enumerate(parts)]
            preds = np.stack([m.predict(Xte) for m in clients])
            # Local-only baseline: each client model alone, metrics averaged over clients
            evs = [evaluate(yte, p, C) for p in preds]
            avg = {k: float(np.mean([e[k] for e in evs])) for k in ["accuracy", "balanced_accuracy",
                                                                     "precision", "recall", "f1"]}
            avg["per_class"] = {k: np.mean([e["per_class"][k] for e in evs], axis=0) for k in evs[0]["per_class"]}
            avg["cm"] = np.mean([e["cm"] for e in evs], axis=0)
            record(name, "local_only", avg, {"local_f1_min": float(min(e["f1"] for e in evs)),
                                             "local_f1_max": float(max(e["f1"] for e in evs))})
            # Hard voting
            hv, ties = hard_vote(preds, C)
            out["meta"]["ties"][name] = ties
            out["preds"][(name, "fed_hard")] = hv
            record(name, "fed_hard", evaluate(yte, hv, C), {"vote_ties": ties})
            # Soft voting (mean of predict_proba)
            P = np.mean([full_proba(m, Xte, C) for m in clients], axis=0)
            sv = P.argmax(1)
            out["preds"][(name, "fed_soft")] = sv
            record(name, "fed_soft", evaluate(yte, sv, C))
            if name == "DT":
                out["meta"]["client_dt_depths"] = [int(m.get_depth()) for m in clients]
        safe(f"{name} federated", federated)
        stage_log(f"seed {seed}: {name} central + federated + local-only done")

    # ---------------- controls: centralised bagging on random 1/5 subsets
    rng_c = np.random.RandomState(10_000 + seed)
    n_sub = len(ytr) // K_CLIENTS

    def bag(kind):
        preds = []
        for k in range(K_CLIENTS):
            idx = rng_c.choice(len(ytr), n_sub, replace=False)
            if kind == "DT":
                m = DecisionTreeClassifier(max_depth=10, criterion="gini", random_state=seed * 100 + 50 + k)
            else:
                m = RandomForestClassifier(n_estimators=20, max_depth=10, criterion="gini",
                                           random_state=seed * 100 + 50 + k, n_jobs=-1)
            preds.append(m.fit(Xtr[idx], ytr[idx]).predict(Xte))
        hv, ties = hard_vote(np.stack(preds), C)
        regime = "bag5_dt" if kind == "DT" else "bag5_rf20"
        out["preds"][(kind, regime)] = hv
        record(kind, regime, evaluate(yte, hv, C), {"vote_ties": ties})
    safe("bagging DT control", lambda: bag("DT"))
    safe("bagging RF control", lambda: bag("RF"))
    stage_log(f"seed {seed}: bagging controls done")

    # ---------------- MLP
    Xtr_t = torch.tensor(Xtr, dtype=torch.float32, device=DEVICE)
    ytr_t = torch.tensor(ytr, dtype=torch.long, device=DEVICE)
    Xte_t = torch.tensor(Xte, dtype=torch.float32, device=DEVICE)
    d_in = Xtr.shape[1]

    def mlp_central():
        m = new_mlp(d_in, C, seed)
        curve = []
        for blk in range(FL_ROUNDS):
            train_epochs(m, Xtr_t, ytr_t, LOCAL_EPOCHS, gen_seed=seed * 1000 + blk)
            curve.append(f1_score(yte, mlp_predict(m, Xte_t), average="macro", labels=np.arange(C),
                                  zero_division=0))
        pte = mlp_predict(m, Xte_t)
        out["preds"][("MLP", "central")] = pte
        ptr = mlp_predict(m, Xtr_t)
        record("MLP", "central", evaluate(yte, pte, C),
               {"train_f1": f1_score(ytr, ptr, average="macro", labels=np.arange(C), zero_division=0)})
        out["central_curve"] = curve
    safe("MLP central", mlp_central)

    def mlp_fed():
        g = new_mlp(d_in, C, seed)
        n_params = sum(p.numel() for p in g.parameters())
        w0 = get_weights(g)
        raw_bytes = int(sum(w.nbytes for w in w0))
        ser_bytes = int(sum(len(t) for t in ndarrays_to_parameters(w0).tensors)) if HAVE_FLWR else raw_bytes
        out["meta"]["mlp_params"] = int(n_params)
        out["meta"]["mlp_bytes_per_model_raw"] = raw_bytes
        out["meta"]["mlp_bytes_per_model_serialized"] = ser_bytes
        clients = [(Xtr_t[torch.as_tensor(p, device=DEVICE)], ytr_t[torch.as_tensor(p, device=DEVICE)])
                   for p in parts]
        curve, acc_curve = [], []
        for r in range(1, FL_ROUNDS + 1):
            gw = get_weights(g)
            results = []
            for k, (Xk, yk) in enumerate(clients):
                local = new_mlp(d_in, C, seed)
                set_weights(local, gw)
                train_epochs(local, Xk, yk, LOCAL_EPOCHS, gen_seed=seed * 100_000 + r * 100 + k)
                results.append((get_weights(local), int(len(yk))))
            set_weights(g, fedavg(results))
            p = mlp_predict(g, Xte_t)
            curve.append(f1_score(yte, p, average="macro", labels=np.arange(C), zero_division=0))
            acc_curve.append(accuracy_score(yte, p))
            log(f"  FedAvg round {r}: macro F1={curve[-1]:.4f} acc={acc_curve[-1]:.4f}")
        pte = mlp_predict(g, Xte_t)
        out["preds"][("MLP", "fed")] = pte
        record("MLP", "fed", evaluate(yte, pte, C))
        trig, best_r = early_stop_round(curve, PATIENCE)
        out["meta"]["mlp_early_stop_trigger_round"] = trig
        out["meta"]["mlp_best_round"] = best_r
        out["curve"] = {"f1": curve, "acc": acc_curve}
    safe("MLP FedAvg", mlp_fed)

    def mlp_local():
        evs = []
        for k, p in enumerate(parts):
            m = new_mlp(d_in, C, seed)
            pi = torch.as_tensor(p, device=DEVICE)
            train_epochs(m, Xtr_t[pi], ytr_t[pi], CENTRAL_EPOCHS, gen_seed=seed * 7919 + k)
            evs.append(evaluate(yte, mlp_predict(m, Xte_t), C))
        avg = {k: float(np.mean([e[k] for e in evs])) for k in ["accuracy", "balanced_accuracy",
                                                                 "precision", "recall", "f1"]}
        avg["per_class"] = {k: np.mean([e["per_class"][k] for e in evs], axis=0) for k in evs[0]["per_class"]}
        avg["cm"] = np.mean([e["cm"] for e in evs], axis=0)
        record("MLP", "local_only", avg, {"local_f1_min": float(min(e["f1"] for e in evs)),
                                          "local_f1_max": float(max(e["f1"] for e in evs))})
    safe("MLP local-only", mlp_local)
    stage_log(f"seed {seed}: MLP central + FedAvg + local-only done")

    out["test_raw_labels"] = d["rte"]
    out["yte"] = yte
    out["meta"]["seconds"] = round(time.time() - t0, 1)
    log(f"seed {seed} finished in {out['meta']['seconds']} s")
    return out


def metric_signature(o):
    # Everything numeric that must be bit-identical between two runs of the same seed
    sig = [(m["model"], m["regime"], m["accuracy"], m["precision"], m["recall"], m["f1"],
            json.dumps(m["cm"])) for m in o["metrics"]]
    return sig, (o["curve"] or {}).get("f1"), o.get("central_curve")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["lycos", "cicids"])
    ap.add_argument("--smoke", action="store_true", help="use a 5%% random sample of the cleaned data")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    ap.add_argument("--no-determinism-check", action="store_true")
    args = ap.parse_args()

    tag = f"{'SMOKE ' if args.smoke else ''}{args.dataset}"
    out_dir = os.path.join(RESULTS, "smoke", args.dataset) if args.smoke else os.path.join(RESULTS, args.dataset)
    os.makedirs(out_dir, exist_ok=True)
    log_file = open(os.path.join(out_dir, "run_log.txt"), "w", encoding="utf-8")

    def log(msg):
        print(msg, flush=True)
        log_file.write(msg + "\n")
        log_file.flush()

    def stage_log(msg):
        log_progress(f"RUN {tag} | {msg}")

    log(f"device={DEVICE} flwr={'yes' if HAVE_FLWR else 'NO (manual FedAvg)'} seeds={args.seeds}")
    df_all, info = load_clean(args.dataset)
    if args.smoke:
        df_all = df_all.sample(frac=SMOKE_FRAC, random_state=SMOKE_SAMPLE_SEED).reset_index(drop=True)
        log(f"SMOKE: using {len(df_all)} rows ({SMOKE_FRAC:.0%} of cleaned data)")
    df_all, dropped = class_filter(df_all)
    classes = sorted(df_all["Label"].unique())
    log(f"classes kept: {classes}; dropped (<100 flows): {dropped}")
    stage_log(f"data loaded: {len(df_all)} rows, classes={classes}, dropped={dropped}")

    all_metrics, metas, curves, central_curves, preds_rows = [], [], [], [], []
    seed0 = None
    for s in args.seeds:
        o = run_seed(df_all, classes, s, log, stage_log)
        if s == args.seeds[0]:
            seed0 = o
        all_metrics += o["metrics"]
        metas.append(o["meta"])
        if o["curve"]:
            for r, (f, a) in enumerate(zip(o["curve"]["f1"], o["curve"]["acc"]), start=1):
                curves.append({"seed": s, "round": r, "mlp_fed_f1": f, "mlp_fed_acc": a,
                               "mlp_central_f1_same_epochs": o.get("central_curve", [np.nan] * FL_ROUNDS)[r - 1],
                               "bytes_per_client_round_up": o["meta"]["mlp_bytes_per_model_serialized"],
                               "bytes_per_client_round_down": o["meta"]["mlp_bytes_per_model_serialized"]})
        # Test-set predictions per model/regime (for per-class difference analysis)
        for (mname, regime), p in o["preds"].items():
            preds_rows.append(pd.DataFrame({"seed": s, "model": mname, "regime": regime,
                                            "y_true": o["yte"], "y_pred": p, "raw_label": o["test_raw_labels"]}))
        stage_log(f"seed {s} complete ({o['meta']['seconds']} s, failures={len(o['meta']['failures'])})")

    # Determinism check: re-run the first seed in the same process and compare bit-for-bit
    det = None
    if not args.no_determinism_check:
        o2 = run_seed(df_all, classes, args.seeds[0], lambda m: log("[rerun] " + m), lambda m: None)
        a, b = metric_signature(seed0), metric_signature(o2)
        det = {"seed": args.seeds[0], "identical": a == b,
               "n_compared_rows": len(a[0]),
               "mismatches": [str((x, y)) for x, y in zip(a[0], b[0]) if x != y][:20],
               "curve_identical": a[1] == b[1], "central_curve_identical": a[2] == b[2]}
        log(f"determinism check: {det}")
        stage_log(f"determinism check seed {args.seeds[0]}: identical={det['identical']}")

    # ---------------- save raw outputs
    flat = []
    per_class_rows = []
    cm_rows = []
    for m in all_metrics:
        base = {k: v for k, v in m.items() if k not in ("per_class", "cm")}
        flat.append(base)
        for i, c in enumerate(classes):
            per_class_rows.append({"seed": m["seed"], "model": m["model"], "regime": m["regime"], "class": c,
                                   "precision": m["per_class"]["precision"][i],
                                   "recall": m["per_class"]["recall"][i],
                                   "f1": m["per_class"]["f1"][i], "support": m["per_class"]["support"][i]})
        cm = np.asarray(m["cm"])
        for i, ct in enumerate(classes):
            for j, cp in enumerate(classes):
                cm_rows.append({"seed": m["seed"], "model": m["model"], "regime": m["regime"],
                                "true": ct, "pred": cp, "count": cm[i, j]})
    pd.DataFrame(flat).to_csv(os.path.join(out_dir, "raw_metrics.csv"), index=False)
    pd.DataFrame(per_class_rows).to_csv(os.path.join(out_dir, "raw_per_class.csv"), index=False)
    pd.DataFrame(cm_rows).to_csv(os.path.join(out_dir, "raw_confusion.csv"), index=False)
    pd.DataFrame(curves).to_csv(os.path.join(out_dir, "raw_convergence.csv"), index=False)
    if preds_rows:
        pr = pd.concat(preds_rows, ignore_index=True)
        pr["y_true"] = pr["y_true"].map(dict(enumerate(classes)))
        pr["y_pred"] = pr["y_pred"].map(dict(enumerate(classes)))
        pr.to_csv(os.path.join(out_dir, "raw_test_predictions.csv.gz"), index=False, compression="gzip")
    meta = {"dataset": args.dataset, "smoke": args.smoke, "device": str(DEVICE),
            "torch": torch.__version__, "flwr_used": HAVE_FLWR, "classes": classes,
            "dropped_classes": dropped, "clean_info": {k: v for k, v in info.items()},
            "rows_after_class_filter": int(len(df_all)),
            "config": {"K": K_CLIENTS, "cap": CAP_PER_CLASS, "test_size": TEST_SIZE, "rounds": FL_ROUNDS,
                       "local_epochs": LOCAL_EPOCHS, "central_epochs": CENTRAL_EPOCHS, "batch": BATCH_SIZE,
                       "lr": LR, "patience": PATIENCE, "seeds": args.seeds},
            "seeds": metas, "determinism": det}
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    n_fail = sum(len(m["failures"]) for m in metas)
    stage_log(f"finished; raw outputs in {os.path.relpath(out_dir)}; failures={n_fail}")
    log_file.close()


if __name__ == "__main__":
    main()
