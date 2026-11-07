# Release check

Prepared on 2026-11-08. Nothing was pushed, no remote was added, no commit was made and no credentials were used.
`paper/` was only read, never modified.

## Summary

| Check | Result |
|---|---|
| A. Layout | `release/` contains `src/`, `requirements.txt`, trimmed `results/`, `README.md`, `.gitignore`, `LICENSE` (MIT), `CITATION.cff`. No file is larger than 20 MB (the largest is 771 KB). |
| B. README | Written in English with no em or en dashes. Every command in it was run in a fresh copy, and all exited with code 0. |
| C1. Fresh-copy run | **PASSED.** A new venv, `pip install -r requirements.txt`, inspection, both smoke tests, both full runs, the report and the optional scripts all completed with exit code 0 and 0 failures. Determinism is identical for both datasets. **All 21 regenerated result files are byte-identical to the shipped ones.** |
| C2. Paper vs results | **56 of 56 numbers in Table III and Table IV match. There are no mismatches.** |
| C3. Sensitive data | One absolute path was found and fixed (details below). No usernames, emails, API keys or tokens were found. |
| C4. git dry run | `git init` was run in `release/` only and 136 files (2.85 MB) are staged. There is no commit and no remote. |

## A. Files in the release

`results/` has only the final results: `lycos/`, `cicids/`, `numbers.tex`, `table_*.tex`, `summary_tables.md`,
`convergence_both.pdf/png`, `dataset_inspection.md`, `inspect_log.txt` and `PROGRESS.md`. These are excluded:
`results/smoke/`, `results/lycos_noniid/`, `SUMMARY_FOR_REVIEW.md`, the stdout logs, `.venv/`, `cache/`, `data/`,
`data_lycos/`, `.idea/` and `paper/`. All of `src/` is included, which covers the optional `noniid.py` and
`leakage_check.py`; the README lists them as optional.

| Folder | Files | Size |
|---|---|---|
| (root) | 5 | 15.8 KB |
| results (top level) | 9 | 213.0 KB |
| results/cicids | 58 | 1,370.4 KB |
| results/lycos | 58 | 1,248.5 KB |
| src | 6 | 67.6 KB |
| **Total** | **136** | **2.85 MB** |

<details><summary>Full file list with sizes (bytes)</summary>

| File | Bytes |
|---|---|
| .gitignore | 335 |
| CITATION.cff | 1,057 |
| LICENSE | 1,094 |
| README.md | 12,319 |
| requirements.txt | 1,338 |
| results/PROGRESS.md | 19,680 |
| results/cicids/confusion/cm_DT_bag5_dt_seed0.csv | 323 |
| results/cicids/confusion/cm_DT_bag5_dt_sum_over_seeds.csv | 339 |
| results/cicids/confusion/cm_DT_central_seed0.csv | 323 |
| results/cicids/confusion/cm_DT_central_sum_over_seeds.csv | 338 |
| results/cicids/confusion/cm_DT_fed_hard_seed0.csv | 323 |
| results/cicids/confusion/cm_DT_fed_hard_sum_over_seeds.csv | 337 |
| results/cicids/confusion/cm_DT_fed_soft_seed0.csv | 323 |
| results/cicids/confusion/cm_DT_fed_soft_sum_over_seeds.csv | 338 |
| results/cicids/confusion/cm_DT_local_only_seed0.csv | 324 |
| results/cicids/confusion/cm_DT_local_only_sum_over_seeds.csv | 385 |
| results/cicids/confusion/cm_KNN_central_seed0.csv | 323 |
| results/cicids/confusion/cm_KNN_central_sum_over_seeds.csv | 341 |
| results/cicids/confusion/cm_KNN_fed_hard_seed0.csv | 327 |
| results/cicids/confusion/cm_KNN_fed_hard_sum_over_seeds.csv | 346 |
| results/cicids/confusion/cm_KNN_fed_soft_seed0.csv | 326 |
| results/cicids/confusion/cm_KNN_fed_soft_sum_over_seeds.csv | 345 |
| results/cicids/confusion/cm_KNN_local_only_seed0.csv | 328 |
| results/cicids/confusion/cm_KNN_local_only_sum_over_seeds.csv | 462 |
| results/cicids/confusion/cm_MLP_central_seed0.csv | 324 |
| results/cicids/confusion/cm_MLP_central_sum_over_seeds.csv | 340 |
| results/cicids/confusion/cm_MLP_fed_seed0.csv | 327 |
| results/cicids/confusion/cm_MLP_fed_sum_over_seeds.csv | 349 |
| results/cicids/confusion/cm_MLP_local_only_seed0.csv | 329 |
| results/cicids/confusion/cm_MLP_local_only_sum_over_seeds.csv | 404 |
| results/cicids/confusion/cm_RF_bag5_rf20_seed0.csv | 323 |
| results/cicids/confusion/cm_RF_bag5_rf20_sum_over_seeds.csv | 339 |
| results/cicids/confusion/cm_RF_central_seed0.csv | 323 |
| results/cicids/confusion/cm_RF_central_sum_over_seeds.csv | 338 |
| results/cicids/confusion/cm_RF_fed_hard_seed0.csv | 323 |
| results/cicids/confusion/cm_RF_fed_hard_sum_over_seeds.csv | 338 |
| results/cicids/confusion/cm_RF_fed_soft_seed0.csv | 323 |
| results/cicids/confusion/cm_RF_fed_soft_sum_over_seeds.csv | 339 |
| results/cicids/confusion/cm_RF_local_only_seed0.csv | 323 |
| results/cicids/confusion/cm_RF_local_only_sum_over_seeds.csv | 366 |
| results/cicids/confusion/cm_SVM_central_seed0.csv | 330 |
| results/cicids/confusion/cm_SVM_central_sum_over_seeds.csv | 347 |
| results/cicids/confusion/cm_SVM_fed_hard_seed0.csv | 333 |
| results/cicids/confusion/cm_SVM_fed_hard_sum_over_seeds.csv | 353 |
| results/cicids/confusion/cm_SVM_fed_soft_seed0.csv | 332 |
| results/cicids/confusion/cm_SVM_fed_soft_sum_over_seeds.csv | 353 |
| results/cicids/confusion/cm_SVM_local_only_seed0.csv | 333 |
| results/cicids/confusion/cm_SVM_local_only_sum_over_seeds.csv | 353 |
| results/cicids/confusion/confusion_matrices.png | 771,165 |
| results/cicids/controls.csv | 4,716 |
| results/cicids/convergence.csv | 2,551 |
| results/cicids/convergence_cicids.pdf | 14,957 |
| results/cicids/convergence_cicids.png | 72,109 |
| results/cicids/meta.json | 9,466 |
| results/cicids/paired_differences.csv | 5,888 |
| results/cicids/per_class.csv | 21,557 |
| results/cicids/per_class_differences.csv | 20,204 |
| results/cicids/raw_confusion.csv | 175,781 |
| results/cicids/raw_convergence.csv | 3,807 |
| results/cicids/raw_metrics.csv | 13,498 |
| results/cicids/raw_per_class.csv | 58,663 |
| results/cicids/raw_test_predictions.csv.gz | 203,542 |
| results/cicids/run_log.txt | 5,983 |
| results/cicids/table.csv | 5,156 |
| results/convergence_both.pdf | 16,736 |
| results/convergence_both.png | 105,534 |
| results/dataset_inspection.md | 11,062 |
| results/inspect_log.txt | 12,637 |
| results/lycos/confusion/cm_DT_bag5_dt_seed0.csv | 323 |
| results/lycos/confusion/cm_DT_bag5_dt_sum_over_seeds.csv | 333 |
| results/lycos/confusion/cm_DT_central_seed0.csv | 323 |
| results/lycos/confusion/cm_DT_central_sum_over_seeds.csv | 332 |
| results/lycos/confusion/cm_DT_fed_hard_seed0.csv | 323 |
| results/lycos/confusion/cm_DT_fed_hard_sum_over_seeds.csv | 332 |
| results/lycos/confusion/cm_DT_fed_soft_seed0.csv | 323 |
| results/lycos/confusion/cm_DT_fed_soft_sum_over_seeds.csv | 332 |
| results/lycos/confusion/cm_DT_local_only_seed0.csv | 323 |
| results/lycos/confusion/cm_DT_local_only_sum_over_seeds.csv | 381 |
| results/lycos/confusion/cm_KNN_central_seed0.csv | 323 |
| results/lycos/confusion/cm_KNN_central_sum_over_seeds.csv | 332 |
| results/lycos/confusion/cm_KNN_fed_hard_seed0.csv | 324 |
| results/lycos/confusion/cm_KNN_fed_hard_sum_over_seeds.csv | 336 |
| results/lycos/confusion/cm_KNN_fed_soft_seed0.csv | 324 |
| results/lycos/confusion/cm_KNN_fed_soft_sum_over_seeds.csv | 335 |
| results/lycos/confusion/cm_KNN_local_only_seed0.csv | 324 |
| results/lycos/confusion/cm_KNN_local_only_sum_over_seeds.csv | 394 |
| results/lycos/confusion/cm_MLP_central_seed0.csv | 323 |
| results/lycos/confusion/cm_MLP_central_sum_over_seeds.csv | 329 |
| results/lycos/confusion/cm_MLP_fed_seed0.csv | 323 |
| results/lycos/confusion/cm_MLP_fed_sum_over_seeds.csv | 334 |
| results/lycos/confusion/cm_MLP_local_only_seed0.csv | 323 |
| results/lycos/confusion/cm_MLP_local_only_sum_over_seeds.csv | 363 |
| results/lycos/confusion/cm_RF_bag5_rf20_seed0.csv | 323 |
| results/lycos/confusion/cm_RF_bag5_rf20_sum_over_seeds.csv | 331 |
| results/lycos/confusion/cm_RF_central_seed0.csv | 323 |
| results/lycos/confusion/cm_RF_central_sum_over_seeds.csv | 330 |
| results/lycos/confusion/cm_RF_fed_hard_seed0.csv | 323 |
| results/lycos/confusion/cm_RF_fed_hard_sum_over_seeds.csv | 331 |
| results/lycos/confusion/cm_RF_fed_soft_seed0.csv | 323 |
| results/lycos/confusion/cm_RF_fed_soft_sum_over_seeds.csv | 331 |
| results/lycos/confusion/cm_RF_local_only_seed0.csv | 323 |
| results/lycos/confusion/cm_RF_local_only_sum_over_seeds.csv | 345 |
| results/lycos/confusion/cm_SVM_central_seed0.csv | 324 |
| results/lycos/confusion/cm_SVM_central_sum_over_seeds.csv | 337 |
| results/lycos/confusion/cm_SVM_fed_hard_seed0.csv | 326 |
| results/lycos/confusion/cm_SVM_fed_hard_sum_over_seeds.csv | 341 |
| results/lycos/confusion/cm_SVM_fed_soft_seed0.csv | 326 |
| results/lycos/confusion/cm_SVM_fed_soft_sum_over_seeds.csv | 337 |
| results/lycos/confusion/cm_SVM_local_only_seed0.csv | 326 |
| results/lycos/confusion/cm_SVM_local_only_sum_over_seeds.csv | 340 |
| results/lycos/confusion/confusion_matrices.png | 686,214 |
| results/lycos/controls.csv | 4,755 |
| results/lycos/convergence.csv | 2,569 |
| results/lycos/convergence_lycos.pdf | 14,915 |
| results/lycos/convergence_lycos.png | 66,041 |
| results/lycos/meta.json | 9,009 |
| results/lycos/paired_differences.csv | 5,919 |
| results/lycos/per_class.csv | 19,916 |
| results/lycos/per_class_differences.csv | 19,394 |
| results/lycos/raw_confusion.csv | 175,515 |
| results/lycos/raw_convergence.csv | 3,807 |
| results/lycos/raw_metrics.csv | 13,424 |
| results/lycos/raw_per_class.csv | 52,519 |
| results/lycos/raw_test_predictions.csv.gz | 179,406 |
| results/lycos/run_log.txt | 5,939 |
| results/lycos/table.csv | 5,199 |
| results/numbers.tex | 27,751 |
| results/summary_tables.md | 21,663 |
| results/table_cicids.tex | 1,512 |
| results/table_lycos.tex | 1,513 |
| src/common.py | 7,094 |
| src/inspect_data.py | 6,119 |
| src/leakage_check.py | 2,243 |
| src/noniid.py | 6,550 |
| src/report.py | 22,658 |
| src/run_experiment.py | 24,591 |

</details>

## C1. Fresh-copy verification

Procedure: `release/` was copied to `C:\Roman\Magidah\Conference\_release_verify\`. The existing `data\` and `data_lycos\`
folders were linked into it as directory junctions, so they stayed read-only and were not copied. A new venv was
created with `py -3.12 -m venv .venv`, and every README command was then run in order with that venv's Python. Logs
are in `_release_verification_logs/` in the project root (outside `release/`).

| Step | Command | Exit code | Time |
|---|---|---|---|
| venv | `py -3.12 -m venv .venv` | 0 | 3 s |
| install | `python -m pip install -r requirements.txt` | 0 | 122 s (warm pip cache) |
| imports | numpy 2.5.4, pandas 3.1.1, scikit-learn 1.9.1, matplotlib 3.11.2, torch 2.11.0+cu128, flwr 1.43.0, CUDA available | 0 | 6 s |
| help | `python src/run_experiment.py --help` | 0 | 5 s |
| inspection | `python src/inspect_data.py` | 0 | 62 s |
| smoke LYCOS | `python src/run_experiment.py --dataset lycos --smoke` | 0 | 113 s |
| smoke CIC | `python src/run_experiment.py --dataset cicids --smoke` | 0 | 122 s |
| smoke report | `python src/report.py --smoke` | 0 | 10 s |
| full LYCOS | `python src/run_experiment.py --dataset lycos` | 0 | 210 s |
| full CIC | `python src/run_experiment.py --dataset cicids` | 0 | 234 s |
| report | `python src/report.py` | 0 | 8 s |
| optional | `python src/leakage_check.py` | 0 | 8 s |
| optional | `python src/noniid.py --dataset lycos --alpha 0.5` | 0 | 42 s |

Both smoke tests completed (0 failures, determinism identical). Both full runs reported `failures=0` and
`determinism check seed 0: identical=True`.

Reproducibility: these regenerated files are byte-identical to the copies in `release/results/`:
* `numbers.tex`, `table_lycos.tex`, `table_cicids.tex`, `summary_tables.md`, `dataset_inspection.md`
* for each dataset: `table.csv`, `paired_differences.csv`, `raw_metrics.csv`, `raw_confusion.csv`, `raw_convergence.csv`, `per_class.csv`, `controls.csv`, `convergence.csv`

The optional non-IID metrics and `leakage_check.md` also match the original project run byte for byte. This was all on
the same machine and GPU. Another GPU or a CPU may give small floating-point differences.

## C2. Paper (`paper/main.tex`) vs `results/`

Table III is `tab:main` (lines 144 to 148) and Table IV is `tab:ctrl` (lines 166 to 169). Each paper value was compared
with the value computed from `results/<dataset>/table.csv` and `paired_differences.csv`, rounded to 2 decimals.

**Result: 56 / 56 match, 0 mismatches.**

| Table | paper line | Dataset | Model | Quantity | Paper | Results | Match |
|---|---|---|---|---|---|---|---|
| III | 144 | cicids | RF | Cent. F1 | 98.28 | 98.28 | yes |
| III | 144 | cicids | RF | Fed. F1 | 97.79 | 97.79 | yes |
| III | 144 | cicids | RF | Delta F1 mean | -0.48 | -0.48 | yes |
| III | 144 | cicids | RF | Delta F1 std | 0.20 | 0.20 | yes |
| III | 144 | lycos | RF | Cent. F1 | 99.54 | 99.54 | yes |
| III | 144 | lycos | RF | Fed. F1 | 99.25 | 99.25 | yes |
| III | 144 | lycos | RF | Delta F1 mean | -0.29 | -0.29 | yes |
| III | 144 | lycos | RF | Delta F1 std | 0.18 | 0.18 | yes |
| III | 145 | cicids | DT | Cent. F1 | 97.93 | 97.93 | yes |
| III | 145 | cicids | DT | Fed. F1 | 98.04 | 98.04 | yes |
| III | 145 | cicids | DT | Delta F1 mean | +0.11 | +0.11 | yes |
| III | 145 | cicids | DT | Delta F1 std | 0.50 | 0.50 | yes |
| III | 145 | lycos | DT | Cent. F1 | 99.13 | 99.13 | yes |
| III | 145 | lycos | DT | Fed. F1 | 99.12 | 99.12 | yes |
| III | 145 | lycos | DT | Delta F1 mean | -0.00 | -0.00 | yes |
| III | 145 | lycos | DT | Delta F1 std | 0.24 | 0.24 | yes |
| III | 146 | cicids | KNN | Cent. F1 | 97.07 | 97.07 | yes |
| III | 146 | cicids | KNN | Fed. F1 | 94.24 | 94.24 | yes |
| III | 146 | cicids | KNN | Delta F1 mean | -2.83 | -2.83 | yes |
| III | 146 | cicids | KNN | Delta F1 std | 0.52 | 0.52 | yes |
| III | 146 | lycos | KNN | Cent. F1 | 98.98 | 98.98 | yes |
| III | 146 | lycos | KNN | Fed. F1 | 97.77 | 97.77 | yes |
| III | 146 | lycos | KNN | Delta F1 mean | -1.21 | -1.21 | yes |
| III | 146 | lycos | KNN | Delta F1 std | 0.42 | 0.42 | yes |
| III | 147 | cicids | SVM | Cent. F1 | 91.66 | 91.66 | yes |
| III | 147 | cicids | SVM | Fed. F1 | 84.54 | 84.54 | yes |
| III | 147 | cicids | SVM | Delta F1 mean | -7.12 | -7.12 | yes |
| III | 147 | cicids | SVM | Delta F1 std | 0.66 | 0.66 | yes |
| III | 147 | lycos | SVM | Cent. F1 | 97.48 | 97.48 | yes |
| III | 147 | lycos | SVM | Fed. F1 | 95.20 | 95.20 | yes |
| III | 147 | lycos | SVM | Delta F1 mean | -2.29 | -2.29 | yes |
| III | 147 | lycos | SVM | Delta F1 std | 0.35 | 0.35 | yes |
| III | 148 | cicids | MLP | Cent. F1 | 96.79 | 96.79 | yes |
| III | 148 | cicids | MLP | Fed. F1 | 94.13 | 94.13 | yes |
| III | 148 | cicids | MLP | Delta F1 mean | -2.66 | -2.66 | yes |
| III | 148 | cicids | MLP | Delta F1 std | 0.86 | 0.86 | yes |
| III | 148 | lycos | MLP | Cent. F1 | 99.34 | 99.34 | yes |
| III | 148 | lycos | MLP | Fed. F1 | 98.48 | 98.48 | yes |
| III | 148 | lycos | MLP | Delta F1 mean | -0.86 | -0.86 | yes |
| III | 148 | lycos | MLP | Delta F1 std | 0.48 | 0.48 | yes |
| IV | 166 | cicids | RF | Cent. F1 | 98.28 | 98.28 | yes |
| IV | 166 | cicids | RF | Fed. F1 | 97.79 | 97.79 | yes |
| IV | 166 | cicids | RF | Bag. F1 | 97.63 | 97.63 | yes |
| IV | 166 | cicids | RF | Local F1 | 97.35 | 97.35 | yes |
| IV | 167 | cicids | DT | Cent. F1 | 97.93 | 97.93 | yes |
| IV | 167 | cicids | DT | Fed. F1 | 98.04 | 98.04 | yes |
| IV | 167 | cicids | DT | Bag. F1 | 97.84 | 97.84 | yes |
| IV | 167 | cicids | DT | Local F1 | 96.19 | 96.19 | yes |
| IV | 168 | lycos | RF | Cent. F1 | 99.54 | 99.54 | yes |
| IV | 168 | lycos | RF | Fed. F1 | 99.25 | 99.25 | yes |
| IV | 168 | lycos | RF | Bag. F1 | 99.16 | 99.16 | yes |
| IV | 168 | lycos | RF | Local F1 | 99.09 | 99.09 | yes |
| IV | 169 | lycos | DT | Cent. F1 | 99.13 | 99.13 | yes |
| IV | 169 | lycos | DT | Fed. F1 | 99.12 | 99.12 | yes |
| IV | 169 | lycos | DT | Bag. F1 | 99.03 | 99.03 | yes |
| IV | 169 | lycos | DT | Local F1 | 98.16 | 98.16 | yes |

Extra checks, not requested and done by hand:
* Table I (family counts raw/clean, lines 82 to 92) matches `results/dataset_inspection.md` in all 38 cells.
* The numbers in the result text (lines 101, 130, 154, 175 and 186) also agree with `results/`: per-client sizes, tie counts, soft-voting gaps, fed minus local, fed minus bagging, rounds to convergence, parameters, bytes, duplicates removed, label conflicts and feature counts.

## C3. Sensitive-data scan

All 136 files in `release/` were scanned, including the decompressed content of `raw_test_predictions.csv.gz` and the
raw bytes of the PDF and PNG files. The scan looked for absolute Windows and Unix paths, the local username and home
directory, `AppData`, email addresses, and API key or token words and key shapes (`sk-`, `ghp_`, `AKIA`, `xoxb-`).
The patterns were self-tested before the scan.

| Finding | Action |
|---|---|
| `results/inspect_log.txt` contained the absolute local path of the cache file | The path prefix was removed in the release copy. `src/common.py` now prints the cache path relative to the project root, in both `src/` and `release/src/`, so new logs are clean. |
| 2 hits of the drive-letter pattern in `confusion_matrices.png` | False positives: random bytes inside compressed image data |
| Usernames, emails, keys, tokens | None found |

The code has no hard-coded absolute paths. Every path is built from the repository root (`src/common.py`, `ROOT`).

## C4. git dry run (in `release/` only)

```
git init                  -> release/.git created
git add -A                -> 136 files staged (2.85 MB of tracked content)
git status --short        -> 136 x "A" (new file); nothing ignored was staged
git ls-files | wc -l      -> 136
git remote -v             -> (empty, no remote)
git log                   -> (no commits)
```

Git printed "LF will be replaced by CRLF" warnings. That is Git for Windows' normal line-ending handling and is harmless.
`RELEASE_CHECK.md` itself was written after the staging, so the `git add -A` below will add it as file 137.

## Commands for you to run yourself

Your global git configuration already has a name and email. A commit records that email publicly on GitHub. If you
prefer, set a repository-local identity first, for example the GitHub no-reply address from
github.com > Settings > Emails.

```bash
cd C:\Roman\Magidah\Conference\release

# optional: identity for this repository only
git config user.name  "Your Name"
git config user.email "ID+username@users.noreply.github.com"

# 1. stage and commit
git add -A
git status
git commit -m "Code and results for: Federated versus Centralised Network Intrusion Detection on Original and Corrected CIC-IDS2017"

# 2. create the repository on github.com:
#    New repository > name, e.g. fl-nids-cicids2017 > Public >
#    do NOT add a README, .gitignore or license (they already exist here) > Create repository

# 3. connect and push (replace <user> and <repo>)
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

Git will ask you to sign in through the browser or Git Credential Manager on the first push.

## Open items for you

1. **CITATION.cff** contains placeholders (`collection-title`, `doi`, `url`). Fill them in once the paper is published, before or soon after release.
2. **Dataset links.** The UNB page for CIC-IDS2017 is the official source. For LYCOS-IDS2017, the README gives `https://lycos-ids.univ-lemans.fr/`, the site named by the dataset authors in their papers. I could not confirm that its download page is still live, so please open both links once before publishing.
3. **Temporary verification copy removed.** After the checks, the directory junctions were removed first with a link-only `rmdir`. The original `data\` and `data_lycos\` were confirmed intact (unchanged listing, 8 + 6 files), and only then was `_release_verify\` deleted. Logs and the paper comparison are kept in `_release_verification_logs/` in the project root, not in `release/`.
