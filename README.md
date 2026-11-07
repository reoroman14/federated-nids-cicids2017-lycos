# Federated versus Centralised NIDS on Original and Corrected CIC-IDS2017

This repository contains the code and final results for the paper "Federated versus Centralised Network Intrusion
Detection on Original and Corrected CIC-IDS2017: Does Data Quality or Ensembling Explain the Gap?". The same
pipeline is run on two versions of the same traffic: the original CIC-IDS2017 CSV files and the corrected
LYCOS-IDS2017 release. On each, it compares centralised training with federated training on K=5 clients for five
classifiers: random forest (RF), decision tree (DT), k-nearest neighbours (KNN), support vector machine (SVM) and a
multi-layer perceptron (MLP). The paper asks three research questions:

* **RQ1:** Does the gap between centralised and federated training change when moving from original CIC-IDS2017 to LYCOS-IDS2017?
* **RQ2:** Is any federated gain for tree-based models explained by ensembling rather than by federation? Bagging controls and a local-only baseline test this.
* **RQ3:** How many communication rounds does a federated MLP need, and at what communication cost?

Every number in `results/` is produced by the code in `src/`.

## Data (not included)

Neither dataset is redistributed here. Download them from the official sources and place the CSV files in two folders
next to `src/`, using exactly these folder names. The code only reads these folders and never writes to them.

| Folder the code expects | Dataset | Official source | Files used |
|---|---|---|---|
| `data/` | Original CIC-IDS2017 (Sharafaldin et al., ICISSP 2018) | Canadian Institute for Cybersecurity, University of New Brunswick: https://www.unb.ca/cic/datasets/ids-2017.html (archive `MachineLearningCSV.zip`, folder `MachineLearningCVE`) | the 8 `*.pcap_ISCX.csv` files |
| `data_lycos/` | LYCOS-IDS2017 (Rosay et al., WI-IAT 2021, doi:10.1145/3486622.3493973) | https://lycos-ids.univ-lemans.fr/ | the 5 `*.pcap_lycos.csv` files |

These are the files and row counts we observed (from `results/inspect_log.txt`). Row counts exclude the header line.

**`data/` (CIC-IDS2017): 8 files, 2,830,743 rows, 79 columns**

| File | Rows |
|---|---|
| Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv | 225,745 |
| Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv | 286,467 |
| Friday-WorkingHours-Morning.pcap_ISCX.csv | 191,033 |
| Monday-WorkingHours.pcap_ISCX.csv | 529,918 |
| Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv | 288,602 |
| Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv | 170,366 |
| Tuesday-WorkingHours.pcap_ISCX.csv | 445,909 |
| Wednesday-workingHours.pcap_ISCX.csv | 692,703 |

**`data_lycos/` (LYCOS-IDS2017): 5 files, 1,837,498 rows, 83 columns**

| File | Rows |
|---|---|
| Friday-WorkingHours.pcap_lycos.csv | 542,962 |
| Monday-WorkingHours.pcap_lycos.csv | 367,181 |
| Thursday-WorkingHours.pcap_lycos.csv | 112,481 |
| Tuesday-WorkingHours.pcap_lycos.csv | 319,637 |
| Wednesday-WorkingHours.pcap_lycos.csv | 495,237 |

If your copies have different row counts, the results will differ. Run the inspection step first and compare with
`results/dataset_inspection.md`.

## Environment

* Python 3.12 (we used 3.12.10 on Windows 11).
* GPU used: NVIDIA GeForce RTX 4060 Laptop GPU with the CUDA 12.8 build of PyTorch. Only the MLP uses the GPU. The code also runs on a CPU without changes: it selects `cuda` when available and `cpu` otherwise, and enforces deterministic algorithms in both cases. Floating-point results on CPU may differ slightly from the GPU numbers in `results/`.

Create the environment from the repository root:

```bash
# Windows
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt

# Linux / macOS
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`requirements.txt` pins every package exactly. Its first line adds the PyTorch CUDA 12.8 wheel index. On a machine without
an NVIDIA GPU, install the CPU build of the same torch version first (`pip install torch==2.11.0 --index-url
https://download.pytorch.org/whl/cpu`), then remove the `torch==2.11.0+cu128` line from `requirements.txt` and install
the rest. These are the main packages and versions used:

| Package | Version |
|---|---|
| numpy | 2.5.4 |
| pandas | 3.1.1 |
| scikit-learn | 1.9.1 |
| matplotlib | 3.11.2 |
| torch | 2.11.0+cu128 |
| flwr (Flower) | 1.43.0 |

## How to run

Run all commands from the repository root with the virtual environment active. They are listed in the order we ran them.

```bash
# 1. Data inspection: files, columns, labels, family mapping, cleaning summary
#    -> results/dataset_inspection.md (the first run also builds the cleaned-data cache in cache/)
python src/inspect_data.py

# 2. Smoke test: the whole pipeline on a 5 % sample, all 5 seeds -> results/smoke/<dataset>/
python src/run_experiment.py --dataset lycos --smoke
python src/run_experiment.py --dataset cicids --smoke
python src/report.py --smoke

# 3. Full experiment: seeds 0 to 4 plus a determinism re-run of seed 0 -> results/<dataset>/raw_*, meta.json
python src/run_experiment.py --dataset lycos
python src/run_experiment.py --dataset cicids

# 4. Report: tables, figures, LaTeX -> results/<dataset>/, results/*.tex, results/convergence_both.*
python src/report.py
```

Optional extras (their outputs are not part of this release):

```bash
# Train/test exact-overlap and single-feature separability diagnostic -> results/leakage_check.md
python src/leakage_check.py

# Non-IID run (Dirichlet alpha = 0.5), MLP FedAvg only, on LYCOS -> results/lycos_noniid/
python src/noniid.py --dataset lycos --alpha 0.5
```

`python src/run_experiment.py --help` lists every option (`--dataset`, `--smoke`, `--seeds`, `--no-determinism-check`).
Each stage appends a timestamped line to `results/PROGRESS.md`.

### Run time

These times were measured on the machine above (RTX 4060 Laptop GPU, 32 logical CPU cores, 32 GB RAM). They come from
`results/PROGRESS.md` and from the fresh-copy verification described in `RELEASE_CHECK.md`.

| Step | Wall time |
|---|---|
| `inspect_data.py` (reads about 1.7 GB of CSV, builds the cache) | about 1 min (62 s) |
| Smoke test, both datasets | about 4 min (113 s LYCOS + 122 s CIC-IDS2017 + 10 s report) |
| Full run, LYCOS (5 seeds + determinism re-run) | about 3.5 min (210 s) |
| Full run, CIC-IDS2017 (5 seeds + determinism re-run) | about 4 min (234 s) |
| `report.py` | under 10 s |
| `pip install -r requirements.txt` (with a warm pip cache) | about 2 min |

The whole sequence from inspection to report takes about 13 minutes. If the smoke or full run is started without
running `inspect_data.py` first, it builds the cache itself on first use.

## Expected outputs

| Path | Content |
|---|---|
| `results/dataset_inspection.md`, `results/inspect_log.txt` | files, columns, row counts, label values, mapping to families, dropped classes, cleaning summary |
| `results/<dataset>/table.csv` | mean and std over seeds of accuracy, balanced accuracy, macro precision, recall and F1 for every model and regime |
| `results/<dataset>/paired_differences.csv` | paired (same seed) differences, for example federated minus centralised |
| `results/<dataset>/per_class.csv`, `per_class_differences.csv` | per-class precision, recall and F1 and their differences |
| `results/<dataset>/controls.csv` | bagging controls and local-only baselines next to centralised and federated |
| `results/<dataset>/confusion/` | confusion matrices (CSV, summed over seeds and for seed 0) and `confusion_matrices.png` |
| `results/<dataset>/convergence.csv`, `convergence_<dataset>.png/.pdf` | MLP FedAvg macro F1 per round |
| `results/<dataset>/raw_*.csv`, `raw_test_predictions.csv.gz`, `meta.json`, `run_log.txt` | per-seed raw metrics, test predictions, sizes, class counts, vote ties, determinism check |
| `results/convergence_both.png/.pdf` | convergence figure for both datasets |
| `results/numbers.tex` | one `\newcommand` per reported number, for example `\lycosDtFedF`, `\cicidsRfCentF` |
| `results/table_lycos.tex`, `results/table_cicids.tex` | booktabs tables, centralised versus federated |
| `results/summary_tables.md` | every table above in Markdown |

The determinism check in `meta.json` should report `"identical": true`.

## Key settings

| Setting | Value |
|---|---|
| Seeds | 5 (0 to 4); each seed controls undersampling, split, partition, model initialisation and shuffling |
| Classes | Benign plus attack families (DoS, DDoS, PortScan, BruteForce, WebAttack, Bot); families with fewer than 100 flows after cleaning are dropped (Heartbleed in both datasets, Infiltration in CIC-IDS2017) |
| Cleaning | strip column names, drop identifier columns (IPs, ports, timestamp, flow id), replace inf with NaN, drop duplicate rows and zero-variance columns |
| Class cap | at most 1,500 flows per family (random undersampling; smaller families keep all flows) |
| Split | stratified 80/20 train/test split, done before any fitting |
| Preprocessing | median imputer and MinMaxScaler fitted on the training split only |
| Clients | K = 5 IID clients of equal size (random partition of the training split) |
| Models | RF (100 trees, max depth 10, Gini); DT (max depth 10, Gini); KNN (k = 5, Euclidean); SVM (RBF, C = 1.0, gamma = scale); MLP (128, 64, ReLU, Adam, lr = 1e-3, batch 64). Same hyperparameters in every regime. |
| MLP federated | FedAvg, 10 rounds, 5 local epochs per round, clients weighted by sample count; the centralised MLP trains for the same 50 epochs |
| Aggregation | `flwr.server.strategy.aggregate.aggregate` called in-process; the Flower simulation engine is not used; message sizes are measured with `flwr.common.ndarrays_to_parameters` |
| Non-parametric models | RF, DT, KNN and SVM are trained locally on each client and combined by voting (hard voting is the main result; soft voting is also reported) |
| Controls | centralised bagging of 5 DTs, and of 5 RFs with 20 trees, each on a random 1/5 of the training data; local-only single-client models |
| Metrics | accuracy, balanced accuracy, macro precision, recall and F1, per-class scores and confusion matrices on the held-out test set; mean and std over seeds plus paired differences |

## Limitations

* **IID clients only.** The main results use an IID partition with equal client sizes. Real deployments are usually non-IID. The optional non-IID script is included, but its results are not part of the paper's main tables.
* **Undersampling and a balanced test set.** Each family is capped at 1,500 flows, so the test set is roughly class-balanced. The scores do not reflect performance at real-world class prevalence, where benign traffic dominates. At real prevalence, precision for attack classes would be lower.
* **No significance tests.** We report mean, standard deviation and paired differences over 5 seeds, with the number of seeds in which a difference is positive. No formal statistical test was run, and with 5 seeds small differences (for example the DT and bagging comparisons) should not be read as significant.
* **Voting is not federated learning in the FedAvg sense.** For RF, DT, KNN and SVM the federated model is an ensemble of five local models sent once to the server. A federated KNN shares its training data, so it gives no privacy.
* **Simulated communication.** All clients run in one process. Byte counts come from serialised message sizes, not from network measurements.
* **Fixed budget and hyperparameters.** No hyperparameter tuning was done, and the MLP gets a fixed budget of 10 rounds. Its curve is still rising at round 10, especially on CIC-IDS2017. Early stopping (patience 3) is reported on the test curve for information only and is never applied.
* **Two datasets with different feature sets** (73 features for LYCOS-IDS2017 and 68 for CIC-IDS2017 after cleaning). Differences between the datasets cannot be attributed to a single cause.

## Citation and license

See `CITATION.cff` for how to cite this work. The code is released under the MIT License (`LICENSE`). The datasets
keep their own licences and terms of use from their providers.
