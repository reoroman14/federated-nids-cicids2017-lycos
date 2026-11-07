# Diagnostic: how many test rows have a feature vector that also occurs exactly in the training split
# (possible after de-duplication when the same features carry different raw labels), and which
# single feature best separates each class (a hint of trivially separable classes).
# Usage: python src/leakage_check.py  -> results/leakage_check.md
import os
import sys

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_experiment as rx  # noqa: E402
from common import RESULTS, class_filter, load_clean  # noqa: E402

out = ["# Leakage / separability diagnostics (seed 0)", ""]
for ds in ["lycos", "cicids"]:
    df, _ = load_clean(ds, verbose=False)
    df, _ = class_filter(df)
    classes = sorted(df["Label"].unique())
    feat = [c for c in df.columns if c not in ("Label", "RawLabel")]
    d = rx.prepare(df, classes, 0, lambda m: None)
    tr = {r.tobytes() for r in d["Xtr"]}
    hit = np.array([r.tobytes() in tr for r in d["Xte"]])
    out.append(f"## {ds}")
    out.append(f"- Test rows whose exact (scaled) feature vector also occurs in train: {hit.sum()} of {len(hit)}")
    for i, c in enumerate(classes):
        out.append(f"  - {c}: {int(hit[d['yte'] == i].sum())} of {int((d['yte'] == i).sum())}")
    # Best single feature (depth-1 stump, one-vs-rest) per class, test F1-free: train accuracy of stump
    out.append("- Best single-feature one-vs-rest stump per class (balanced accuracy on test):")
    for i, c in enumerate(classes):
        ytr = (d["ytr"] == i).astype(int)
        yte = (d["yte"] == i).astype(int)
        best = (0, None)
        for j in range(d["Xtr"].shape[1]):
            s = DecisionTreeClassifier(max_depth=1, random_state=0, class_weight="balanced").fit(d["Xtr"][:, [j]], ytr)
            p = s.predict(d["Xte"][:, [j]])
            ba = 0.5 * ((p[yte == 1] == 1).mean() + (p[yte == 0] == 0).mean())
            if ba > best[0]:
                best = (ba, feat[j])
        out.append(f"  - {c}: {best[1]} -> {100 * best[0]:.2f}%")
    out.append("")
with open(os.path.join(RESULTS, "leakage_check.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
