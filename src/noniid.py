# OPTIONAL (spec item 17): non-IID FedAvg for the MLP only on LYCOS.
# Training clients receive a Dirichlet(alpha=0.5) label partition of the same training set that the
# IID run uses (same seed -> same undersampling, split, imputer and scaler). Everything else is unchanged.
# Usage: python src/noniid.py [--dataset lycos] [--alpha 0.5] [--seeds 0 1 2 3 4]

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_experiment as rx  # noqa: E402
from common import RESULTS, class_filter, load_clean, log_progress  # noqa: E402


def dirichlet_partition(y, k, alpha, rng, min_size=10):
    # Per class, split its indices among k clients with proportions ~ Dir(alpha); retry until every
    # client has at least min_size samples
    n_classes = int(y.max()) + 1
    for _ in range(1000):
        parts = [[] for _ in range(k)]
        for c in range(n_classes):
            idx = np.where(y == c)[0]
            rng.shuffle(idx)
            p = rng.dirichlet(alpha * np.ones(k))
            cuts = (np.cumsum(p) * len(idx)).astype(int)[:-1]
            for j, chunk in enumerate(np.split(idx, cuts)):
                parts[j] += chunk.tolist()
        if min(len(p) for p in parts) >= min_size:
            return [np.array(sorted(p)) for p in parts]
    raise RuntimeError("could not build a Dirichlet partition with the minimum client size")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="lycos", choices=["lycos", "cicids"])
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = ap.parse_args()
    out_dir = os.path.join(RESULTS, f"{args.dataset}_noniid")
    os.makedirs(out_dir, exist_ok=True)
    df_all, _ = load_clean(args.dataset)
    df_all, _ = class_filter(df_all)
    classes = sorted(df_all["Label"].unique())
    C = len(classes)
    rows, curves, client_counts = [], [], {}
    for seed in args.seeds:
        d = rx.prepare(df_all, classes, seed, print)
        Xtr, Xte, ytr, yte = d["Xtr"], d["Xte"], d["ytr"], d["yte"]
        parts = dirichlet_partition(ytr, rx.K_CLIENTS, args.alpha, np.random.RandomState(20_000 + seed))
        client_counts[seed] = [np.bincount(ytr[p], minlength=C).tolist() for p in parts]
        print(f"seed {seed}: client class counts {client_counts[seed]}")
        Xtr_t = torch.tensor(Xtr, dtype=torch.float32, device=rx.DEVICE)
        ytr_t = torch.tensor(ytr, dtype=torch.long, device=rx.DEVICE)
        Xte_t = torch.tensor(Xte, dtype=torch.float32, device=rx.DEVICE)
        g = rx.new_mlp(Xtr.shape[1], C, seed)
        clients = [(Xtr_t[torch.as_tensor(p, device=rx.DEVICE)], ytr_t[torch.as_tensor(p, device=rx.DEVICE)])
                   for p in parts]
        f1s = []
        for r in range(1, rx.FL_ROUNDS + 1):
            gw = rx.get_weights(g)
            res = []
            for k, (Xk, yk) in enumerate(clients):
                local = rx.new_mlp(Xtr.shape[1], C, seed)
                rx.set_weights(local, gw)
                rx.train_epochs(local, Xk, yk, rx.LOCAL_EPOCHS, gen_seed=seed * 100_000 + r * 100 + k)
                res.append((rx.get_weights(local), int(len(yk))))
            rx.set_weights(g, rx.fedavg(res))
            p = rx.mlp_predict(g, Xte_t)
            f1s.append(f1_score(yte, p, average="macro", labels=np.arange(C), zero_division=0))
            curves.append({"seed": seed, "round": r, "mlp_fed_noniid_f1": f1s[-1],
                           "mlp_fed_noniid_acc": accuracy_score(yte, p)})
            print(f"  seed {seed} round {r}: F1={f1s[-1]:.4f}")
        ev = rx.evaluate(yte, rx.mlp_predict(g, Xte_t), C)
        trig, best = rx.early_stop_round(f1s, rx.PATIENCE)
        rows.append({"seed": seed, **{k: ev[k] for k in ["accuracy", "balanced_accuracy", "precision", "recall", "f1"]},
                     "early_stop_trigger_round": trig, "best_round": best,
                     **{f"f1_{c}": v for c, v in zip(classes, ev["per_class"]["f1"])}})
        log_progress(f"OPTIONAL non-IID {args.dataset} | seed {seed} done (macro F1 {ev['f1']:.4f})")
    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(out_dir, "noniid_metrics.csv"), index=False)
    pd.DataFrame(curves).to_csv(os.path.join(out_dir, "noniid_convergence.csv"), index=False)
    with open(os.path.join(out_dir, "noniid_client_class_counts.json"), "w") as f:
        json.dump({"classes": classes, "alpha": args.alpha, "counts": client_counts}, f, indent=1)

    # Paired comparison with the IID FedAvg MLP of the main run (same seeds)
    iid_path = os.path.join(RESULTS, args.dataset, "raw_metrics.csv")
    md = [f"# OPTIONAL non-IID run ({args.dataset}, Dirichlet alpha={args.alpha}, MLP FedAvg only)", ""]
    md.append("| Metric | non-IID mean ± std (%) | IID mean ± std (%) | paired non-IID - IID (pp) |")
    md.append("|---|---|---|---|")
    if os.path.exists(iid_path):
        iid = pd.read_csv(iid_path)
        iid = iid[(iid.model == "MLP") & (iid.regime == "fed")].set_index("seed")
        nn_ = res.set_index("seed")
        common = nn_.index.intersection(iid.index)
        for k in ["accuracy", "balanced_accuracy", "precision", "recall", "f1"]:
            dlt = nn_.loc[common, k] - iid.loc[common, k]
            md.append(f"| {k} | {100 * nn_[k].mean():.2f} ± {100 * nn_[k].std(ddof=1):.2f} | "
                      f"{100 * iid.loc[common, k].mean():.2f} ± {100 * iid.loc[common, k].std(ddof=1):.2f} | "
                      f"{100 * dlt.mean():+.2f} ± {100 * dlt.std(ddof=1):.2f} |")
    md += ["", "Per-class F1 (%, mean over seeds): " +
           ", ".join(f"{c}: {100 * res[f'f1_{c}'].mean():.2f}" for c in classes), "",
           f"Early stopping (patience 3, test curve, diagnostic): {res[['seed', 'early_stop_trigger_round', 'best_round']].to_dict('records')}",
           "", "Per-round mean macro F1 (%): " + ", ".join(
               f"r{r}: {100 * v:.2f}" for r, v in pd.DataFrame(curves).groupby('round')['mlp_fed_noniid_f1'].mean().items()),
           "", f"Client class counts per seed (classes {classes}): see noniid_client_class_counts.json", ""]
    with open(os.path.join(out_dir, "noniid_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    log_progress(f"OPTIONAL non-IID {args.dataset} | finished, outputs in results/{args.dataset}_noniid")


if __name__ == "__main__":
    main()
