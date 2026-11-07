# PART E: turns the raw per-seed outputs of run_experiment.py into tables, figures and LaTeX.
# Usage: python src/report.py [--smoke]    (processes every dataset folder that has raw outputs)

import argparse
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({"font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "pdf.fonttype": 42})
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATASETS, RESULTS, log_progress  # noqa: E402

METRICS = ["accuracy", "balanced_accuracy", "precision", "recall", "f1"]
MODELS = ["RF", "DT", "KNN", "SVM", "MLP"]
# The "federated" regime of each model used in the headline table
FED_REGIME = {"RF": "fed_hard", "DT": "fed_hard", "KNN": "fed_hard", "SVM": "fed_hard", "MLP": "fed"}
# Categorical colours (reference palette order) + distinct line styles for print/greyscale
COLORS = {"MLP": "#2a78d6", "RF": "#eb6834", "DT": "#1baf7a", "KNN": "#eda100", "SVM": "#e87ba4"}
STYLES = {"RF": (0, (5, 2)), "DT": (0, (1, 1.5)), "KNN": (0, (6, 2, 1, 2)), "SVM": (0, (3, 1, 1, 1, 1, 1))}
PREFIX = {"lycos": "lycos", "cicids": "cicids"}
REGIME_TEX = {"central": "Cent", "fed_hard": "Fed", "fed_soft": "FedSoft", "fed": "Fed",
              "local_only": "Local", "bag5_dt": "Bag", "bag5_rf20": "Bag"}
METRIC_TEX = {"accuracy": "Acc", "balanced_accuracy": "BalAcc", "precision": "Prec", "recall": "Rec", "f1": "F"}


def pct(x):
    return 100.0 * x


def fmt(m, s):
    return f"{pct(m):.2f} ± {pct(s):.2f}"


def summarise(raw):
    # mean and sample std (ddof=1) over seeds
    g = raw.groupby(["model", "regime"])
    cols = METRICS + [c for c in ["train_f1", "vote_ties"] if c in raw.columns]
    t = g[cols].agg(["mean", "std"])
    t.columns = [f"{a}_{b}" for a, b in t.columns]
    t["n_seeds"] = g.size()
    return t.reset_index()


def paired(raw):
    # Paired (same seed, same data split) differences A - B
    comps = []
    for m in ["RF", "DT", "KNN", "SVM"]:
        comps += [(m, "fed_hard", "central"), (m, "fed_soft", "central"), (m, "local_only", "central"),
                  (m, "fed_hard", "local_only")]
    comps += [("MLP", "fed", "central"), ("MLP", "local_only", "central"), ("MLP", "fed", "local_only"),
              ("DT", "bag5_dt", "central"), ("DT", "fed_hard", "bag5_dt"),
              ("RF", "bag5_rf20", "central"), ("RF", "fed_hard", "bag5_rf20")]
    rows = []
    for m, a, b in comps:
        A = raw[(raw.model == m) & (raw.regime == a)].set_index("seed")
        B = raw[(raw.model == m) & (raw.regime == b)].set_index("seed")
        common = A.index.intersection(B.index)
        if len(common) == 0:
            continue
        row = {"model": m, "comparison": f"{a} - {b}", "n_seeds": len(common)}
        for k in METRICS:
            d = A.loc[common, k] - B.loc[common, k]
            row[f"{k}_diff_mean"] = d.mean()
            row[f"{k}_diff_std"] = d.std(ddof=1) if len(d) > 1 else np.nan
            if k == "f1":
                row["f1_seeds_positive"] = int((d > 0).sum())
                row["f1_seeds_negative"] = int((d < 0).sum())
        rows.append(row)
    return pd.DataFrame(rows)


def convergence_fig(conv, table, ds, out_base, ax=None, title=None):
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
    g = conv.groupby("round")
    r = g["mlp_fed_f1"].mean().index.values
    mu, sd = pct(g["mlp_fed_f1"].mean().values), pct(g["mlp_fed_f1"].std(ddof=1).fillna(0).values)
    ax.fill_between(r, mu - sd, mu + sd, color=COLORS["MLP"], alpha=0.18, linewidth=0)
    ax.plot(r, mu, color=COLORS["MLP"], lw=1.8, marker="o", ms=3.5, label="MLP FedAvg")
    for m in ["RF", "DT", "KNN", "SVM"]:
        row = table[(table.model == m) & (table.regime == "fed_hard")]
        if len(row):
            ax.axhline(pct(row["f1_mean"].iloc[0]), color=COLORS[m], lw=1.3, ls=STYLES[m],
                       label=f"{m} (fed., vote)")
    ax.set_xlabel("Communication round")
    ax.set_ylabel("Macro F1 (%)")
    ax.set_xticks(r)
    lo = min(mu.min() - sd.max(), pct(table[table.regime == "fed_hard"]["f1_mean"].min()))
    ax.set_ylim(max(0, np.floor(lo / 5) * 5), 100)
    ax.grid(True, color="#d9d9d6", lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    if title:
        ax.set_title(title, fontsize=8)
    if own:
        ax.legend(fontsize=6.5, loc="lower right", frameon=False, ncol=1)
        fig.tight_layout(pad=0.3)
        fig.savefig(out_base + ".png", dpi=300)
        fig.savefig(out_base + ".pdf")
        plt.close(fig)


def cm_fig(cms, classes, path):
    # cms: list of (title, matrix) -> grid of row-normalised confusion matrices
    n = len(cms)
    cols = 4
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(3.2 * cols, 3.0 * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax, (t, m) in zip(axes, cms):
        m = np.asarray(m, dtype=float)
        norm = m / np.maximum(m.sum(1, keepdims=True), 1)
        ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
        for i in range(len(classes)):
            for j in range(len(classes)):
                if m[i, j] > 0:
                    ax.text(j, i, f"{m[i, j]:.0f}", ha="center", va="center", fontsize=5.5,
                            color="white" if norm[i, j] > 0.6 else "black")
        ax.set_xticks(range(len(classes)))
        ax.set_yticks(range(len(classes)))
        ax.set_xticklabels(classes, rotation=60, fontsize=6)
        ax.set_yticklabels(classes, fontsize=6)
        ax.set_title(t, fontsize=7)
    for ax in axes[n:]:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def macro_name(prefix, model, regime, metric, stat=""):
    # LaTeX macro names may contain letters only
    name = prefix + model.capitalize() + REGIME_TEX[regime] + METRIC_TEX[metric] + stat
    assert name.isalpha(), name
    return name


def process(ds, base):
    d = os.path.join(base, ds)
    raw = pd.read_csv(os.path.join(d, "raw_metrics.csv"))
    meta = json.load(open(os.path.join(d, "meta.json"), encoding="utf-8"))
    classes = meta["classes"]

    table = summarise(raw)
    table.to_csv(os.path.join(d, "table.csv"), index=False)
    pr = paired(raw)
    pr.to_csv(os.path.join(d, "paired_differences.csv"), index=False)

    # Per-class metrics (mean/std over seeds) and per-class F1 deltas
    pc = pd.read_csv(os.path.join(d, "raw_per_class.csv"))
    pcs = pc.groupby(["model", "regime", "class"])[["precision", "recall", "f1", "support"]].agg(["mean", "std"])
    pcs.columns = [f"{a}_{b}" for a, b in pcs.columns]
    pcs.reset_index().to_csv(os.path.join(d, "per_class.csv"), index=False)
    drows = []
    for m in MODELS:
        for a, b in [(FED_REGIME[m], "central"), ("local_only", "central")] + \
                    ([("bag5_dt", "central")] if m == "DT" else []) + ([("bag5_rf20", "central")] if m == "RF" else []):
            A = pc[(pc.model == m) & (pc.regime == a)].set_index(["seed", "class"])
            B = pc[(pc.model == m) & (pc.regime == b)].set_index(["seed", "class"])
            idx = A.index.intersection(B.index)
            for k in ["precision", "recall", "f1"]:
                dd = (A.loc[idx, k] - B.loc[idx, k]).groupby(level="class")
                for c, v in dd:
                    drows.append({"model": m, "comparison": f"{a} - {b}", "class": c, "metric": k,
                                  "diff_mean": v.mean(), "diff_std": v.std(ddof=1)})
    pd.DataFrame(drows).to_csv(os.path.join(d, "per_class_differences.csv"), index=False)

    # Confusion matrices summed over seeds (one CSV per model/regime) + figure
    cmr = pd.read_csv(os.path.join(d, "raw_confusion.csv"))
    cdir = os.path.join(d, "confusion")
    os.makedirs(cdir, exist_ok=True)
    figs = []
    for (m, rg), g in cmr.groupby(["model", "regime"], sort=False):
        mat = g.groupby(["true", "pred"])["count"].sum().unstack().reindex(index=classes, columns=classes)
        mat.to_csv(os.path.join(cdir, f"cm_{m}_{rg}_sum_over_seeds.csv"))
        g0 = g[g.seed == g.seed.min()]
        g0.pivot_table(index="true", columns="pred", values="count", aggfunc="sum").reindex(
            index=classes, columns=classes).to_csv(os.path.join(cdir, f"cm_{m}_{rg}_seed{g.seed.min()}.csv"))
        figs.append((f"{m} {rg} (sum over seeds)", mat.values))
    cm_fig(figs, classes, os.path.join(cdir, "confusion_matrices.png"))

    # Convergence
    conv = pd.read_csv(os.path.join(d, "raw_convergence.csv"))
    cg = conv.groupby("round").agg(mlp_fed_f1_mean=("mlp_fed_f1", "mean"), mlp_fed_f1_std=("mlp_fed_f1", "std"),
                                   mlp_fed_acc_mean=("mlp_fed_acc", "mean"), mlp_fed_acc_std=("mlp_fed_acc", "std"),
                                   mlp_central_f1_same_epochs_mean=("mlp_central_f1_same_epochs", "mean"),
                                   mlp_central_f1_same_epochs_std=("mlp_central_f1_same_epochs", "std"),
                                   bytes_up_per_client=("bytes_per_client_round_up", "first"),
                                   bytes_down_per_client=("bytes_per_client_round_down", "first")).reset_index()
    wide = conv.pivot(index="round", columns="seed", values="mlp_fed_f1")
    wide.columns = [f"mlp_fed_f1_seed{c}" for c in wide.columns]
    cg = cg.merge(wide.reset_index(), on="round")
    cg.to_csv(os.path.join(d, "convergence.csv"), index=False)
    convergence_fig(conv, table, ds, os.path.join(d, f"convergence_{ds}"))

    # Rounds to convergence: first round whose mean macro F1 is within 1 point of the best mean round
    mean_curve = cg["mlp_fed_f1_mean"].values
    r_conv = int(np.argmax(mean_curve >= mean_curve.max() - 0.01)) + 1
    seeds_meta = meta["seeds"]
    es = [{"seed": s["seed"], "early_stop_trigger_round": s.get("mlp_early_stop_trigger_round"),
           "best_round": s.get("mlp_best_round")} for s in seeds_meta]
    from run_experiment import early_stop_round  # noqa: E402
    es_mean_trig, es_mean_best = early_stop_round(list(mean_curve), 3)

    # Controls
    ctrl_rows = []
    for m, rgs in [("DT", ["central", "fed_hard", "fed_soft", "bag5_dt", "local_only"]),
                   ("RF", ["central", "fed_hard", "fed_soft", "bag5_rf20", "local_only"]),
                   ("KNN", ["central", "fed_hard", "local_only"]), ("SVM", ["central", "fed_hard", "local_only"]),
                   ("MLP", ["central", "fed", "local_only"])]:
        for rg in rgs:
            r = table[(table.model == m) & (table.regime == rg)]
            if len(r):
                ctrl_rows.append(r.iloc[0])
    ctrl = pd.DataFrame(ctrl_rows)
    ctrl.to_csv(os.path.join(d, "controls.csv"), index=False)

    # LaTeX table: centralised vs federated
    lines = [r"% Generated by src/report.py -- values are mean $\pm$ std over seeds, in percent.",
             r"\begin{table*}[t]", r"\centering\footnotesize",
             rf"\caption{{Centralised vs.\ federated ($K=5$, IID) on {DATASETS[ds]['name']}: macro metrics on the held-out test set, mean$\pm$std over {len(meta['config']['seeds'])} seeds. Federated: FedAvg for MLP, hard majority vote of client models for RF/DT/KNN/SVM. $\Delta$F1 = paired difference federated $-$ centralised.}}",
             rf"\label{{tab:cent_vs_fed_{ds}}}",
             r"\begin{tabular}{l cccc cccc c}", r"\toprule",
             r" & \multicolumn{4}{c}{Centralised} & \multicolumn{4}{c}{Federated} & \\",
             r"\cmidrule(lr){2-5}\cmidrule(lr){6-9}",
             r"Model & Acc & Prec & Rec & F1 & Acc & Prec & Rec & F1 & $\Delta$F1 \\", r"\midrule"]
    for m in MODELS:
        c = table[(table.model == m) & (table.regime == "central")]
        f = table[(table.model == m) & (table.regime == FED_REGIME[m])]
        p = pr[(pr.model == m) & (pr.comparison == f"{FED_REGIME[m]} - central")]
        if not (len(c) and len(f) and len(p)):
            continue
        cells = [f"{pct(x[k + '_mean'].iloc[0]):.2f}$\\pm${pct(x[k + '_std'].iloc[0]):.2f}"
                 for x in (c, f) for k in ["accuracy", "precision", "recall", "f1"]]
        dm, dsd = pct(p["f1_diff_mean"].iloc[0]), pct(p["f1_diff_std"].iloc[0])
        lines.append(f"{m} & " + " & ".join(cells) + f" & {dm:+.2f}$\\pm${dsd:.2f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    with open(os.path.join(base, f"table_{ds}.tex"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    # LaTeX macros
    pref = PREFIX[ds]
    mac = [f"% ---- {DATASETS[ds]['name']} ({ds}); percentages with 2 decimals unless stated"]
    seen = set()
    for _, r in table.iterrows():
        for k in METRICS:
            for stat, col in [("", f"{k}_mean"), ("Std", f"{k}_std")]:
                n = macro_name(pref, r.model, r.regime, k, stat)
                if n in seen:
                    continue
                seen.add(n)
                mac.append(f"\\newcommand{{\\{n}}}{{{pct(r[col]):.2f}}}")
    for _, r in pr.iterrows():
        a, b = r.comparison.split(" - ")
        n = pref + r.model.capitalize() + "Delta" + REGIME_TEX[a] + "Minus" + REGIME_TEX[b] + "F"
        if a == "fed_soft":
            n = n.replace("DeltaFedSoft", "DeltaSoft")
        if n.isalpha() and n not in seen:
            seen.add(n)
            mac.append(f"\\newcommand{{\\{n}}}{{{pct(r.f1_diff_mean):+.2f}}}")
            mac.append(f"\\newcommand{{\\{n}Std}}{{{pct(r.f1_diff_std):.2f}}}")
    s0 = seeds_meta[0]
    sz = s0["sizes"]
    extra = {
        "RoundsToConv": r_conv,
        "EarlyStopRoundMeanCurve": es_mean_trig if es_mean_trig else "none",
        "BestRoundMeanCurve": es_mean_best,
        "MlpParams": f"{s0['mlp_params']:,}".replace(",", "{,}"),
        "MlpBytesRaw": f"{s0['mlp_bytes_per_model_raw']:,}".replace(",", "{,}"),
        "MlpBytesSer": f"{s0['mlp_bytes_per_model_serialized']:,}".replace(",", "{,}"),
        "MlpKBPerClientRound": f"{2 * s0['mlp_bytes_per_model_serialized'] / 1024:.1f}",
        "NTotal": sz["total"], "NTrain": sz["train"], "NTest": sz["test"],
        "NPerClient": sz["per_client"][0], "NFeatures": sz["n_features"], "NClasses": len(classes),
        "NSeeds": len(seeds_meta),
    }
    for k, v in extra.items():
        mac.append(f"\\newcommand{{\\{pref}{k}}}{{{v}}}")
    if ds == "lycos":
        # Short aliases for the primary dataset, e.g. \rfCentF, \dtFedF, \mlpFedF (mean values only)
        mac.append("% ---- short aliases (primary dataset LYCOS-IDS2017, mean values)")
        for _, r in table.iterrows():
            for k in METRICS:
                n = macro_name(pref, r.model, r.regime, k)
                a = r.model.lower() + n[len(pref) + len(r.model):]
                mac.append(f"\\newcommand{{\\{a}}}{{\\{n}}}")
        mac.append(f"\\newcommand{{\\roundsToConv}}{{\\{pref}RoundsToConv}}")

    # Markdown fragments for the summary
    md = [f"### {DATASETS[ds]['name']} (`{ds}`)", "",
          f"Classes ({len(classes)}): {', '.join(classes)}; dropped (<100 flows): {meta['dropped_classes']}", "",
          f"Sizes (seed 0): total {sz['total']}, train {sz['train']}, test {sz['test']}, per client {sz['per_client']}, features {sz['n_features']}", "",
          f"Per-class counts before undersampling: {s0['counts_before']}", "",
          f"Per-class counts after undersampling: {s0['counts_after']}", "",
          "#### All models and regimes (macro metrics, %, mean ± std over seeds)", "",
          "| Model | Regime | Accuracy | Bal. acc. | Precision | Recall | F1 | train F1 |", "|---|---|---|---|---|---|---|---|"]
    for _, r in table.sort_values(["model", "regime"]).iterrows():
        tf = fmt(r.train_f1_mean, r.train_f1_std) if "train_f1_mean" in r and not np.isnan(r.train_f1_mean) else ""
        md.append(f"| {r.model} | {r.regime} | " + " | ".join(fmt(r[k + '_mean'], r[k + '_std']) for k in METRICS)
                  + f" | {tf} |")
    md += ["", "#### Paired differences (same seed), percentage points, mean ± std over seeds", "",
           "| Model | A - B | ΔAcc | ΔPrec | ΔRec | ΔF1 | seeds ΔF1>0 / <0 |", "|---|---|---|---|---|---|---|"]
    for _, r in pr.iterrows():
        md.append(f"| {r.model} | {r.comparison} | " +
                  " | ".join(f"{pct(r[k + '_diff_mean']):+.2f} ± {pct(r[k + '_diff_std']):.2f}"
                             for k in ["accuracy", "precision", "recall", "f1"]) +
                  f" | {r.f1_seeds_positive} / {r.f1_seeds_negative} |")
    md += ["", "#### MLP FedAvg convergence (macro F1 %, mean ± std over seeds)", "",
           "| Round | FedAvg F1 | Central MLP F1 after same #epochs |", "|---|---|---|"]
    for _, r in cg.iterrows():
        md.append(f"| {int(r['round'])} | {fmt(r.mlp_fed_f1_mean, r.mlp_fed_f1_std)} | "
                  f"{fmt(r.mlp_central_f1_same_epochs_mean, r.mlp_central_f1_same_epochs_std)} |")
    md += ["", f"- Parameters: {s0['mlp_params']}; bytes per model: {s0['mlp_bytes_per_model_raw']} raw float32, "
               f"{s0['mlp_bytes_per_model_serialized']} serialised with Flower (`ndarrays_to_parameters`); "
               f"per client per round: {s0['mlp_bytes_per_model_serialized']} up + {s0['mlp_bytes_per_model_serialized']} down "
               f"= {2 * s0['mlp_bytes_per_model_serialized']} bytes; all {len(sz['per_client'])} clients: "
               f"{2 * len(sz['per_client']) * s0['mlp_bytes_per_model_serialized']} bytes/round.",
           f"- Rounds to convergence (first round with mean F1 within 1 point of the best mean round): {r_conv}",
           f"- Early stopping (patience 3, on the test-set macro F1 curve, diagnostic only): per seed {es}; "
           f"on the mean curve: trigger round {es_mean_trig}, best round {es_mean_best}.",
           f"- Hard-vote ties per seed (number of test samples): {[s['ties'] for s in seeds_meta]}",
           f"- Central DT depth / leaves (seed 0): {s0.get('central_dt_depth')} / {s0.get('central_dt_leaves')}; "
           f"client DT depths: {s0.get('client_dt_depths')}",
           f"- Determinism check: {meta['determinism']}",
           f"- Failures: {[f for s in seeds_meta for f in s['failures']] or 'none'}", ""]
    # Per-class F1 deltas
    pcd = pd.DataFrame(drows)
    md += ["#### Per-class F1 difference federated - centralised (pp, mean ± std over seeds)", "",
           "| Model | " + " | ".join(classes) + " |", "|---" * (len(classes) + 1) + "|"]
    for m in MODELS:
        sub = pcd[(pcd.model == m) & (pcd.metric == "f1") & (pcd.comparison == f"{FED_REGIME[m]} - central")]
        if len(sub):
            sub = sub.set_index("class")
            md.append(f"| {m} | " + " | ".join(f"{pct(sub.loc[c, 'diff_mean']):+.2f} ± {pct(sub.loc[c, 'diff_std']):.2f}"
                                               for c in classes) + " |")
    md += ["", "#### Per-class F1 (%, mean over seeds)", "", "| Model | Regime | " + " | ".join(classes) + " |",
           "|---|---" + "|---" * len(classes) + "|"]
    pcm = pc.groupby(["model", "regime", "class"])["f1"].mean()
    for m in MODELS:
        for rg in ["central", FED_REGIME[m], "fed_soft", "local_only", "bag5_dt", "bag5_rf20"]:
            if (m, rg, classes[0]) in pcm.index:
                md.append(f"| {m} | {rg} | " + " | ".join(f"{pct(pcm[(m, rg, c)]):.2f}" for c in classes) + " |")
    md.append("")
    return table, pr, mac, md, cg, conv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    base = os.path.join(RESULTS, "smoke") if args.smoke else RESULTS
    done = [ds for ds in ["lycos", "cicids"] if os.path.exists(os.path.join(base, ds, "raw_metrics.csv"))]
    allmac = ["% Generated by src/report.py. Do not edit by hand.",
              "% Naming: <dataset><Model><Regime><Metric>[Std]; Regime Cent/Fed/FedSoft/Local/Bag;",
              "% Metric Acc/BalAcc/Prec/Rec/F; values in percent (2 decimals); Delta macros are paired",
              "% differences in percentage points (A minus B, same seed)."]
    md_all = []
    tabs = {}
    convs = {}
    for ds in done:
        table, pr, mac, md, cg, conv = process(ds, base)
        tabs[ds] = (table, pr)
        convs[ds] = (conv, table)
        allmac += mac
        md_all += md
        log_progress(f"REPORT {'smoke ' if args.smoke else ''}{ds} | tables, figures, LaTeX written")
    with open(os.path.join(base, "numbers.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(allmac) + "\n")

    # Two-panel convergence figure (double-column width) when both datasets exist
    if len(convs) == 2:
        fig, axes = plt.subplots(1, 2, figsize=(7.16, 2.5), sharey=False)
        for ax, ds in zip(axes, ["lycos", "cicids"]):
            convergence_fig(convs[ds][0], convs[ds][1], ds, None, ax=ax, title=DATASETS[ds]["name"])
        h, lab = axes[0].get_legend_handles_labels()
        fig.legend(h, lab, loc="lower center", ncol=5, fontsize=7, frameon=False)
        fig.tight_layout(rect=(0, 0.1, 1, 1), pad=0.3)
        fig.savefig(os.path.join(base, "convergence_both.png"), dpi=300)
        fig.savefig(os.path.join(base, "convergence_both.pdf"))
        plt.close(fig)

    # Side-by-side comparison of the two datasets
    if len(tabs) == 2:
        md_all += ["### LYCOS-IDS2017 vs CIC-IDS2017 side by side (macro F1 %, mean ± std; ΔF1 paired, pp)", "",
                   "| Model | Regime | LYCOS F1 | CIC-IDS2017 F1 | LYCOS ΔF1 vs central | CIC ΔF1 vs central |",
                   "|---|---|---|---|---|---|"]
        tl, pl = tabs["lycos"]
        tc, pcc = tabs["cicids"]
        for m in MODELS:
            for rg in ["central", FED_REGIME[m], "fed_soft", "local_only", "bag5_dt", "bag5_rf20"]:
                a = tl[(tl.model == m) & (tl.regime == rg)]
                b = tc[(tc.model == m) & (tc.regime == rg)]
                if not (len(a) and len(b)):
                    continue
                da = pl[(pl.model == m) & (pl.comparison == f"{rg} - central")]
                db = pcc[(pcc.model == m) & (pcc.comparison == f"{rg} - central")]
                fa = lambda p: f"{pct(p.f1_diff_mean.iloc[0]):+.2f} ± {pct(p.f1_diff_std.iloc[0]):.2f}" if len(p) else ""
                md_all.append(f"| {m} | {rg} | {fmt(a.f1_mean.iloc[0], a.f1_std.iloc[0])} | "
                              f"{fmt(b.f1_mean.iloc[0], b.f1_std.iloc[0])} | {fa(da)} | {fa(db)} |")
        md_all.append("")
    with open(os.path.join(base, "summary_tables.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_all) + "\n")


if __name__ == "__main__":
    main()
