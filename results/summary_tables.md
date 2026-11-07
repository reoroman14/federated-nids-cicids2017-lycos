### LYCOS-IDS2017 (`lycos`)

Classes (7): Benign, Bot, BruteForce, DDoS, DoS, PortScan, WebAttack; dropped (<100 flows): {'Heartbleed': 11}

Sizes (seed 0): total 9735, train 7788, test 1947, per client [1558, 1558, 1558, 1557, 1557], features 73

Per-class counts before undersampling: {'Benign': 1259765, 'Bot': 735, 'BruteForce': 6957, 'DDoS': 95683, 'DoS': 175707, 'PortScan': 1671, 'WebAttack': 2033}

Per-class counts after undersampling: {'Benign': 1500, 'Bot': 735, 'BruteForce': 1500, 'DDoS': 1500, 'DoS': 1500, 'PortScan': 1500, 'WebAttack': 1500}

#### All models and regimes (macro metrics, %, mean ± std over seeds)

| Model | Regime | Accuracy | Bal. acc. | Precision | Recall | F1 | train F1 |
|---|---|---|---|---|---|---|---|
| DT | bag5_dt | 98.96 ± 0.12 | 99.04 ± 0.11 | 99.03 ± 0.11 | 99.04 ± 0.11 | 99.03 ± 0.11 |  |
| DT | central | 99.07 ± 0.15 | 99.13 ± 0.14 | 99.13 ± 0.15 | 99.13 ± 0.14 | 99.13 ± 0.15 | 99.76 ± 0.07 |
| DT | fed_hard | 99.07 ± 0.19 | 99.13 ± 0.18 | 99.12 ± 0.20 | 99.13 ± 0.18 | 99.12 ± 0.19 |  |
| DT | fed_soft | 99.02 ± 0.14 | 99.10 ± 0.13 | 99.08 ± 0.15 | 99.10 ± 0.13 | 99.09 ± 0.14 |  |
| DT | local_only | 98.07 ± 0.24 | 98.18 ± 0.23 | 98.17 ± 0.23 | 98.18 ± 0.23 | 98.16 ± 0.23 |  |
| KNN | central | 98.94 ± 0.30 | 99.02 ± 0.27 | 98.96 ± 0.35 | 99.02 ± 0.27 | 98.98 ± 0.31 | 99.26 ± 0.05 |
| KNN | fed_hard | 97.75 ± 0.24 | 97.91 ± 0.23 | 97.65 ± 0.30 | 97.91 ± 0.23 | 97.77 ± 0.26 |  |
| KNN | fed_soft | 97.85 ± 0.21 | 98.01 ± 0.19 | 97.79 ± 0.17 | 98.01 ± 0.19 | 97.89 ± 0.18 |  |
| KNN | local_only | 97.62 ± 0.35 | 97.78 ± 0.32 | 97.52 ± 0.39 | 97.78 ± 0.32 | 97.64 ± 0.36 |  |
| MLP | central | 99.29 ± 0.23 | 99.34 ± 0.21 | 99.34 ± 0.20 | 99.34 ± 0.21 | 99.34 ± 0.20 | 99.58 ± 0.06 |
| MLP | fed | 98.46 ± 0.31 | 98.53 ± 0.32 | 98.45 ± 0.36 | 98.53 ± 0.32 | 98.48 ± 0.35 |  |
| MLP | local_only | 98.14 ± 0.24 | 98.24 ± 0.23 | 98.10 ± 0.26 | 98.24 ± 0.23 | 98.16 ± 0.25 |  |
| RF | bag5_rf20 | 99.10 ± 0.23 | 99.16 ± 0.22 | 99.17 ± 0.21 | 99.16 ± 0.22 | 99.16 ± 0.22 |  |
| RF | central | 99.51 ± 0.16 | 99.54 ± 0.15 | 99.55 ± 0.15 | 99.54 ± 0.15 | 99.54 ± 0.15 | 99.95 ± 0.02 |
| RF | fed_hard | 99.20 ± 0.25 | 99.26 ± 0.23 | 99.25 ± 0.22 | 99.26 ± 0.23 | 99.25 ± 0.23 |  |
| RF | fed_soft | 99.21 ± 0.23 | 99.27 ± 0.21 | 99.27 ± 0.21 | 99.27 ± 0.21 | 99.27 ± 0.21 |  |
| RF | local_only | 99.02 ± 0.21 | 99.09 ± 0.19 | 99.09 ± 0.18 | 99.09 ± 0.19 | 99.09 ± 0.19 |  |
| SVM | central | 97.50 ± 0.35 | 97.69 ± 0.33 | 97.34 ± 0.32 | 97.69 ± 0.33 | 97.48 ± 0.32 | 97.65 ± 0.12 |
| SVM | fed_hard | 95.36 ± 0.56 | 95.70 ± 0.52 | 94.98 ± 0.55 | 95.70 ± 0.52 | 95.20 ± 0.53 |  |
| SVM | fed_soft | 96.48 ± 0.42 | 96.73 ± 0.39 | 96.53 ± 0.44 | 96.73 ± 0.39 | 96.55 ± 0.41 |  |
| SVM | local_only | 95.24 ± 0.46 | 95.58 ± 0.42 | 94.87 ± 0.45 | 95.58 ± 0.42 | 95.07 ± 0.43 |  |

#### Paired differences (same seed), percentage points, mean ± std over seeds

| Model | A - B | ΔAcc | ΔPrec | ΔRec | ΔF1 | seeds ΔF1>0 / <0 |
|---|---|---|---|---|---|---|
| RF | fed_hard - central | -0.31 ± 0.19 | -0.29 ± 0.18 | -0.29 ± 0.18 | -0.29 ± 0.18 | 0 / 5 |
| RF | fed_soft - central | -0.30 ± 0.14 | -0.27 ± 0.13 | -0.28 ± 0.13 | -0.28 ± 0.13 | 0 / 5 |
| RF | local_only - central | -0.49 ± 0.13 | -0.46 ± 0.12 | -0.45 ± 0.12 | -0.46 ± 0.12 | 0 / 5 |
| RF | fed_hard - local_only | +0.18 ± 0.08 | +0.16 ± 0.07 | +0.17 ± 0.07 | +0.17 ± 0.07 | 5 / 0 |
| DT | fed_hard - central | +0.00 ± 0.25 | -0.01 ± 0.25 | +0.00 ± 0.23 | -0.00 ± 0.24 | 3 / 2 |
| DT | fed_soft - central | -0.04 ± 0.18 | -0.05 ± 0.19 | -0.04 ± 0.17 | -0.04 ± 0.18 | 3 / 2 |
| DT | local_only - central | -0.99 ± 0.28 | -0.96 ± 0.26 | -0.95 ± 0.26 | -0.96 ± 0.26 | 0 / 5 |
| DT | fed_hard - local_only | +0.99 ± 0.17 | +0.95 ± 0.19 | +0.95 ± 0.15 | +0.96 ± 0.17 | 5 / 0 |
| KNN | fed_hard - central | -1.19 ± 0.40 | -1.31 ± 0.46 | -1.10 ± 0.37 | -1.21 ± 0.42 | 0 / 5 |
| KNN | fed_soft - central | -1.09 ± 0.31 | -1.16 ± 0.33 | -1.01 ± 0.29 | -1.09 ± 0.31 | 0 / 5 |
| KNN | local_only - central | -1.33 ± 0.38 | -1.43 ± 0.43 | -1.24 ± 0.35 | -1.35 ± 0.39 | 0 / 5 |
| KNN | fed_hard - local_only | +0.13 ± 0.16 | +0.13 ± 0.16 | +0.13 ± 0.15 | +0.14 ± 0.16 | 3 / 2 |
| SVM | fed_hard - central | -2.15 ± 0.34 | -2.36 ± 0.37 | -1.99 ± 0.31 | -2.29 ± 0.35 | 0 / 5 |
| SVM | fed_soft - central | -1.03 ± 0.26 | -0.81 ± 0.28 | -0.95 ± 0.24 | -0.93 ± 0.26 | 0 / 5 |
| SVM | local_only - central | -2.27 ± 0.26 | -2.47 ± 0.26 | -2.11 ± 0.24 | -2.41 ± 0.25 | 0 / 5 |
| SVM | fed_hard - local_only | +0.12 ± 0.17 | +0.12 ± 0.16 | +0.12 ± 0.15 | +0.12 ± 0.16 | 4 / 1 |
| MLP | fed - central | -0.83 ± 0.46 | -0.88 ± 0.48 | -0.81 ± 0.47 | -0.86 ± 0.48 | 0 / 5 |
| MLP | local_only - central | -1.15 ± 0.34 | -1.23 ± 0.35 | -1.10 ± 0.32 | -1.18 ± 0.34 | 0 / 5 |
| MLP | fed - local_only | +0.32 ± 0.17 | +0.35 ± 0.18 | +0.29 ± 0.19 | +0.32 ± 0.18 | 5 / 0 |
| DT | bag5_dt - central | -0.10 ± 0.10 | -0.10 ± 0.09 | -0.10 ± 0.10 | -0.10 ± 0.10 | 1 / 4 |
| DT | fed_hard - bag5_dt | +0.10 ± 0.22 | +0.09 ± 0.22 | +0.10 ± 0.20 | +0.09 ± 0.21 | 4 / 1 |
| RF | bag5_rf20 - central | -0.41 ± 0.12 | -0.38 ± 0.11 | -0.38 ± 0.11 | -0.38 ± 0.11 | 0 / 5 |
| RF | fed_hard - bag5_rf20 | +0.10 ± 0.18 | +0.09 ± 0.18 | +0.10 ± 0.17 | +0.09 ± 0.17 | 3 / 2 |

#### MLP FedAvg convergence (macro F1 %, mean ± std over seeds)

| Round | FedAvg F1 | Central MLP F1 after same #epochs |
|---|---|---|
| 1 | 86.14 ± 7.23 | 97.22 ± 0.43 |
| 2 | 94.46 ± 0.80 | 98.45 ± 0.27 |
| 3 | 95.73 ± 0.62 | 98.71 ± 0.25 |
| 4 | 96.66 ± 0.27 | 98.96 ± 0.12 |
| 5 | 97.46 ± 0.28 | 99.12 ± 0.17 |
| 6 | 97.67 ± 0.32 | 99.19 ± 0.20 |
| 7 | 97.93 ± 0.41 | 99.21 ± 0.18 |
| 8 | 98.28 ± 0.29 | 99.20 ± 0.22 |
| 9 | 98.45 ± 0.38 | 99.27 ± 0.20 |
| 10 | 98.48 ± 0.35 | 99.34 ± 0.20 |

- Parameters: 18183; bytes per model: 72732 raw float32, 73500 serialised with Flower (`ndarrays_to_parameters`); per client per round: 73500 up + 73500 down = 147000 bytes; all 5 clients: 735000 bytes/round.
- Rounds to convergence (first round with mean F1 within 1 point of the best mean round): 6
- Early stopping (patience 3, on the test-set macro F1 curve, diagnostic only): per seed [{'seed': 0, 'early_stop_trigger_round': None, 'best_round': 10}, {'seed': 1, 'early_stop_trigger_round': None, 'best_round': 9}, {'seed': 2, 'early_stop_trigger_round': None, 'best_round': 10}, {'seed': 3, 'early_stop_trigger_round': None, 'best_round': 10}, {'seed': 4, 'early_stop_trigger_round': None, 'best_round': 8}]; on the mean curve: trigger round None, best round 10.
- Hard-vote ties per seed (number of test samples): [{'RF': 0, 'DT': 5, 'KNN': 0, 'SVM': 7}, {'RF': 2, 'DT': 6, 'KNN': 1, 'SVM': 0}, {'RF': 0, 'DT': 13, 'KNN': 3, 'SVM': 5}, {'RF': 2, 'DT': 3, 'KNN': 2, 'SVM': 0}, {'RF': 0, 'DT': 3, 'KNN': 9, 'SVM': 4}]
- Central DT depth / leaves (seed 0): 10 / 61; client DT depths: [9, 10, 9, 10, 10]
- Determinism check: {'seed': 0, 'identical': True, 'n_compared_rows': 21, 'mismatches': [], 'curve_identical': True, 'central_curve_identical': True}
- Failures: none

#### Per-class F1 difference federated - centralised (pp, mean ± std over seeds)

| Model | Benign | Bot | BruteForce | DDoS | DoS | PortScan | WebAttack |
|---|---|---|---|---|---|---|---|
| RF | -0.90 ± 0.55 | -0.07 ± 0.15 | -0.34 ± 0.40 | +0.00 ± 0.00 | -0.37 ± 0.43 | -0.23 ± 0.25 | -0.13 ± 0.25 |
| DT | -0.43 ± 0.77 | -0.07 ± 0.15 | -0.03 ± 0.45 | +0.07 ± 0.09 | -0.14 ± 0.22 | +0.39 ± 0.47 | +0.17 ± 0.39 |
| KNN | -3.12 ± 1.23 | -1.39 ± 0.75 | -0.24 ± 0.26 | -0.10 ± 0.22 | -2.29 ± 0.61 | -1.11 ± 0.40 | -0.22 ± 0.55 |
| SVM | -3.10 ± 0.33 | -3.90 ± 0.43 | -1.28 ± 0.88 | -0.10 ± 0.22 | -0.95 ± 0.65 | -3.09 ± 0.48 | -3.61 ± 0.62 |
| MLP | -0.92 ± 0.85 | -1.15 ± 0.91 | -0.27 ± 0.32 | +0.00 ± 0.00 | -1.50 ± 0.82 | -1.81 ± 0.97 | -0.36 ± 0.32 |

#### Per-class F1 (%, mean over seeds)

| Model | Regime | Benign | Bot | BruteForce | DDoS | DoS | PortScan | WebAttack |
|---|---|---|---|---|---|---|---|---|
| RF | central | 98.94 | 100.00 | 99.63 | 100.00 | 99.57 | 99.50 | 99.16 |
| RF | fed_hard | 98.04 | 99.93 | 99.30 | 100.00 | 99.20 | 99.27 | 99.03 |
| RF | fed_soft | 98.14 | 100.00 | 99.36 | 100.00 | 99.20 | 99.20 | 98.97 |
| RF | local_only | 97.66 | 99.93 | 99.32 | 100.00 | 98.91 | 98.92 | 98.87 |
| RF | bag5_rf20 | 97.84 | 100.00 | 99.30 | 100.00 | 99.13 | 99.00 | 98.86 |
| DT | central | 98.04 | 99.93 | 99.30 | 99.93 | 99.03 | 98.97 | 98.69 |
| DT | fed_hard | 97.61 | 99.86 | 99.27 | 100.00 | 98.90 | 99.37 | 98.87 |
| DT | fed_soft | 97.61 | 99.86 | 99.20 | 100.00 | 98.83 | 99.23 | 98.87 |
| DT | local_only | 95.11 | 99.43 | 98.49 | 99.80 | 98.13 | 98.35 | 97.85 |
| DT | bag5_dt | 97.68 | 99.93 | 99.30 | 99.90 | 98.63 | 99.13 | 98.66 |
| KNN | central | 98.01 | 99.53 | 99.50 | 100.00 | 98.71 | 98.47 | 98.67 |
| KNN | fed_hard | 94.89 | 98.13 | 99.26 | 99.90 | 96.42 | 97.36 | 98.44 |
| KNN | fed_soft | 95.31 | 98.46 | 99.26 | 99.90 | 96.73 | 97.20 | 98.38 |
| KNN | local_only | 94.62 | 97.98 | 99.20 | 99.89 | 96.47 | 97.05 | 98.24 |
| SVM | central | 95.18 | 97.29 | 99.47 | 100.00 | 97.14 | 96.10 | 97.21 |
| SVM | fed_hard | 92.09 | 93.40 | 98.19 | 99.90 | 96.19 | 93.01 | 93.60 |
| SVM | fed_soft | 95.01 | 97.74 | 99.23 | 99.93 | 96.67 | 92.85 | 94.42 |
| SVM | local_only | 91.50 | 93.27 | 98.40 | 99.92 | 96.19 | 92.92 | 93.32 |
| MLP | central | 98.56 | 99.93 | 99.57 | 100.00 | 99.30 | 99.00 | 99.00 |
| MLP | fed | 97.64 | 98.79 | 99.30 | 100.00 | 97.80 | 97.19 | 98.64 |
| MLP | local_only | 96.68 | 98.40 | 99.39 | 99.98 | 97.47 | 96.88 | 98.31 |

### CIC-IDS2017 (`cicids`)

Classes (7): Benign, Bot, BruteForce, DDoS, DoS, PortScan, WebAttack; dropped (<100 flows): {'Infiltration': 36, 'Heartbleed': 11}

Sizes (seed 0): total 10441, train 8352, test 2089, per client [1671, 1671, 1670, 1670, 1670], features 68

Per-class counts before undersampling: {'Benign': 1897458, 'Bot': 1441, 'BruteForce': 9152, 'DDoS': 128016, 'DoS': 193748, 'PortScan': 1958, 'WebAttack': 2143}

Per-class counts after undersampling: {'Benign': 1500, 'Bot': 1441, 'BruteForce': 1500, 'DDoS': 1500, 'DoS': 1500, 'PortScan': 1500, 'WebAttack': 1500}

#### All models and regimes (macro metrics, %, mean ± std over seeds)

| Model | Regime | Accuracy | Bal. acc. | Precision | Recall | F1 | train F1 |
|---|---|---|---|---|---|---|---|
| DT | bag5_dt | 97.84 ± 0.44 | 97.85 ± 0.44 | 97.84 ± 0.43 | 97.85 ± 0.44 | 97.84 ± 0.44 |  |
| DT | central | 97.93 ± 0.39 | 97.94 ± 0.39 | 97.94 ± 0.38 | 97.94 ± 0.39 | 97.93 ± 0.39 | 99.29 ± 0.21 |
| DT | fed_hard | 98.05 ± 0.30 | 98.06 ± 0.30 | 98.05 ± 0.29 | 98.06 ± 0.30 | 98.04 ± 0.30 |  |
| DT | fed_soft | 97.99 ± 0.36 | 98.00 ± 0.36 | 97.99 ± 0.36 | 98.00 ± 0.36 | 97.98 ± 0.36 |  |
| DT | local_only | 96.21 ± 0.37 | 96.23 ± 0.37 | 96.26 ± 0.33 | 96.23 ± 0.37 | 96.19 ± 0.37 |  |
| KNN | central | 97.09 ± 0.39 | 97.10 ± 0.39 | 97.10 ± 0.39 | 97.10 ± 0.39 | 97.07 ± 0.40 | 98.02 ± 0.11 |
| KNN | fed_hard | 94.31 ± 0.72 | 94.34 ± 0.72 | 94.28 ± 0.72 | 94.34 ± 0.72 | 94.24 ± 0.71 |  |
| KNN | fed_soft | 94.59 ± 0.60 | 94.61 ± 0.60 | 94.58 ± 0.62 | 94.61 ± 0.60 | 94.50 ± 0.59 |  |
| KNN | local_only | 93.69 ± 0.26 | 93.72 ± 0.26 | 93.68 ± 0.26 | 93.72 ± 0.26 | 93.60 ± 0.25 |  |
| MLP | central | 96.80 ± 0.39 | 96.82 ± 0.39 | 96.84 ± 0.38 | 96.82 ± 0.39 | 96.79 ± 0.40 | 97.42 ± 0.21 |
| MLP | fed | 94.19 ± 0.96 | 94.21 ± 0.95 | 94.35 ± 0.85 | 94.21 ± 0.95 | 94.13 ± 0.99 |  |
| MLP | local_only | 93.52 ± 0.34 | 93.54 ± 0.34 | 93.66 ± 0.33 | 93.54 ± 0.34 | 93.45 ± 0.35 |  |
| RF | bag5_rf20 | 97.64 ± 0.40 | 97.65 ± 0.39 | 97.65 ± 0.40 | 97.65 ± 0.39 | 97.63 ± 0.40 |  |
| RF | central | 98.28 ± 0.28 | 98.28 ± 0.28 | 98.30 ± 0.28 | 98.28 ± 0.28 | 98.28 ± 0.28 | 99.20 ± 0.12 |
| RF | fed_hard | 97.80 ± 0.38 | 97.81 ± 0.38 | 97.81 ± 0.38 | 97.81 ± 0.38 | 97.79 ± 0.38 |  |
| RF | fed_soft | 97.79 ± 0.30 | 97.80 ± 0.30 | 97.81 ± 0.31 | 97.80 ± 0.30 | 97.79 ± 0.30 |  |
| RF | local_only | 97.36 ± 0.34 | 97.37 ± 0.34 | 97.38 ± 0.34 | 97.37 ± 0.34 | 97.35 ± 0.34 |  |
| SVM | central | 91.74 ± 0.34 | 91.77 ± 0.34 | 92.03 ± 0.26 | 91.77 ± 0.34 | 91.66 ± 0.32 | 91.85 ± 0.34 |
| SVM | fed_hard | 85.24 ± 0.46 | 85.31 ± 0.46 | 86.89 ± 0.35 | 85.31 ± 0.46 | 84.54 ± 0.56 |  |
| SVM | fed_soft | 90.23 ± 0.42 | 90.28 ± 0.42 | 90.69 ± 0.24 | 90.28 ± 0.42 | 90.14 ± 0.42 |  |
| SVM | local_only | 84.85 ± 0.73 | 84.92 ± 0.73 | 86.43 ± 0.63 | 84.92 ± 0.73 | 84.09 ± 0.85 |  |

#### Paired differences (same seed), percentage points, mean ± std over seeds

| Model | A - B | ΔAcc | ΔPrec | ΔRec | ΔF1 | seeds ΔF1>0 / <0 |
|---|---|---|---|---|---|---|
| RF | fed_hard - central | -0.48 ± 0.20 | -0.49 ± 0.20 | -0.48 ± 0.20 | -0.48 ± 0.20 | 0 / 5 |
| RF | fed_soft - central | -0.49 ± 0.09 | -0.49 ± 0.09 | -0.49 ± 0.09 | -0.49 ± 0.09 | 0 / 5 |
| RF | local_only - central | -0.92 ± 0.14 | -0.91 ± 0.14 | -0.91 ± 0.14 | -0.92 ± 0.14 | 0 / 5 |
| RF | fed_hard - local_only | +0.44 ± 0.08 | +0.43 ± 0.08 | +0.44 ± 0.08 | +0.44 ± 0.08 | 5 / 0 |
| DT | fed_hard - central | +0.11 ± 0.51 | +0.11 ± 0.50 | +0.11 ± 0.50 | +0.11 ± 0.50 | 3 / 2 |
| DT | fed_soft - central | +0.06 ± 0.58 | +0.05 ± 0.57 | +0.06 ± 0.57 | +0.05 ± 0.58 | 3 / 2 |
| DT | local_only - central | -1.72 ± 0.30 | -1.68 ± 0.29 | -1.71 ± 0.30 | -1.74 ± 0.30 | 0 / 5 |
| DT | fed_hard - local_only | +1.83 ± 0.29 | +1.79 ± 0.27 | +1.83 ± 0.29 | +1.85 ± 0.29 | 5 / 0 |
| KNN | fed_hard - central | -2.78 ± 0.52 | -2.82 ± 0.53 | -2.77 ± 0.51 | -2.83 ± 0.52 | 0 / 5 |
| KNN | fed_soft - central | -2.50 ± 0.36 | -2.52 ± 0.39 | -2.49 ± 0.35 | -2.57 ± 0.35 | 0 / 5 |
| KNN | local_only - central | -3.39 ± 0.27 | -3.42 ± 0.28 | -3.38 ± 0.26 | -3.47 ± 0.28 | 0 / 5 |
| KNN | fed_hard - local_only | +0.62 ± 0.52 | +0.60 ± 0.54 | +0.62 ± 0.51 | +0.64 ± 0.52 | 4 / 1 |
| SVM | fed_hard - central | -6.50 ± 0.57 | -5.14 ± 0.39 | -6.47 ± 0.56 | -7.12 ± 0.66 | 0 / 5 |
| SVM | fed_soft - central | -1.50 ± 0.55 | -1.33 ± 0.37 | -1.50 ± 0.54 | -1.52 ± 0.54 | 0 / 5 |
| SVM | local_only - central | -6.88 ± 0.87 | -5.60 ± 0.70 | -6.85 ± 0.86 | -7.57 ± 1.00 | 0 / 5 |
| SVM | fed_hard - local_only | +0.38 ± 0.39 | +0.46 ± 0.41 | +0.39 ± 0.39 | +0.45 ± 0.45 | 4 / 1 |
| MLP | fed - central | -2.61 ± 0.82 | -2.50 ± 0.72 | -2.60 ± 0.81 | -2.66 ± 0.86 | 0 / 5 |
| MLP | local_only - central | -3.28 ± 0.08 | -3.18 ± 0.09 | -3.27 ± 0.08 | -3.34 ± 0.10 | 0 / 5 |
| MLP | fed - local_only | +0.67 ± 0.83 | +0.68 ± 0.75 | +0.67 ± 0.83 | +0.68 ± 0.88 | 3 / 2 |
| DT | bag5_dt - central | -0.10 ± 0.59 | -0.09 ± 0.56 | -0.10 ± 0.58 | -0.10 ± 0.58 | 1 / 4 |
| DT | fed_hard - bag5_dt | +0.21 ± 0.35 | +0.20 ± 0.33 | +0.21 ± 0.34 | +0.20 ± 0.34 | 4 / 1 |
| RF | bag5_rf20 - central | -0.64 ± 0.25 | -0.64 ± 0.25 | -0.64 ± 0.25 | -0.65 ± 0.25 | 0 / 5 |
| RF | fed_hard - bag5_rf20 | +0.16 ± 0.07 | +0.16 ± 0.08 | +0.16 ± 0.07 | +0.16 ± 0.08 | 5 / 0 |

#### MLP FedAvg convergence (macro F1 %, mean ± std over seeds)

| Round | FedAvg F1 | Central MLP F1 after same #epochs |
|---|---|---|
| 1 | 73.46 ± 2.70 | 91.51 ± 0.14 |
| 2 | 81.08 ± 1.68 | 94.39 ± 0.90 |
| 3 | 84.14 ± 1.20 | 95.52 ± 0.47 |
| 4 | 89.91 ± 0.40 | 95.90 ± 0.55 |
| 5 | 90.89 ± 0.32 | 96.14 ± 0.41 |
| 6 | 91.63 ± 0.32 | 96.39 ± 0.44 |
| 7 | 92.08 ± 0.32 | 96.52 ± 0.46 |
| 8 | 92.74 ± 0.49 | 96.64 ± 0.33 |
| 9 | 93.48 ± 1.05 | 96.45 ± 0.59 |
| 10 | 94.13 ± 0.99 | 96.79 ± 0.40 |

- Parameters: 17543; bytes per model: 70172 raw float32, 70940 serialised with Flower (`ndarrays_to_parameters`); per client per round: 70940 up + 70940 down = 141880 bytes; all 5 clients: 709400 bytes/round.
- Rounds to convergence (first round with mean F1 within 1 point of the best mean round): 9
- Early stopping (patience 3, on the test-set macro F1 curve, diagnostic only): per seed [{'seed': 0, 'early_stop_trigger_round': None, 'best_round': 10}, {'seed': 1, 'early_stop_trigger_round': None, 'best_round': 10}, {'seed': 2, 'early_stop_trigger_round': None, 'best_round': 10}, {'seed': 3, 'early_stop_trigger_round': None, 'best_round': 10}, {'seed': 4, 'early_stop_trigger_round': None, 'best_round': 10}]; on the mean curve: trigger round None, best round 10.
- Hard-vote ties per seed (number of test samples): [{'RF': 1, 'DT': 16, 'KNN': 5, 'SVM': 1}, {'RF': 11, 'DT': 15, 'KNN': 12, 'SVM': 1}, {'RF': 4, 'DT': 10, 'KNN': 8, 'SVM': 3}, {'RF': 6, 'DT': 14, 'KNN': 14, 'SVM': 2}, {'RF': 6, 'DT': 10, 'KNN': 5, 'SVM': 0}]
- Central DT depth / leaves (seed 0): 10 / 99; client DT depths: [10, 10, 10, 10, 10]
- Determinism check: {'seed': 0, 'identical': True, 'n_compared_rows': 21, 'mismatches': [], 'curve_identical': True, 'central_curve_identical': True}
- Failures: none

#### Per-class F1 difference federated - centralised (pp, mean ± std over seeds)

| Model | Benign | Bot | BruteForce | DDoS | DoS | PortScan | WebAttack |
|---|---|---|---|---|---|---|---|
| RF | -1.71 ± 0.77 | -0.10 ± 0.29 | -0.30 ± 0.25 | +0.03 ± 0.07 | -0.67 ± 0.29 | -0.36 ± 0.48 | -0.27 ± 0.51 |
| DT | +0.25 ± 1.28 | -0.20 ± 0.52 | +0.42 ± 1.10 | -0.07 ± 0.15 | +0.00 ± 0.71 | -0.03 ± 0.48 | +0.40 ± 1.12 |
| KNN | -7.55 ± 1.24 | -1.97 ± 0.70 | -0.23 ± 0.42 | -1.35 ± 0.90 | -5.12 ± 2.14 | -2.83 ± 1.01 | -0.78 ± 0.48 |
| SVM | -3.82 ± 1.46 | -5.95 ± 0.54 | -2.91 ± 1.28 | -5.08 ± 0.65 | -1.51 ± 0.49 | -19.83 ± 3.07 | -10.75 ± 1.04 |
| MLP | -3.58 ± 0.66 | -2.96 ± 1.56 | -0.81 ± 1.18 | -1.89 ± 0.81 | -2.55 ± 1.13 | -4.96 ± 2.65 | -1.84 ± 1.13 |

#### Per-class F1 (%, mean over seeds)

| Model | Regime | Benign | Bot | BruteForce | DDoS | DoS | PortScan | WebAttack |
|---|---|---|---|---|---|---|---|---|
| RF | central | 95.64 | 98.70 | 98.82 | 99.87 | 98.63 | 99.00 | 97.28 |
| RF | fed_hard | 93.92 | 98.60 | 98.52 | 99.90 | 97.96 | 98.64 | 97.01 |
| RF | fed_soft | 94.29 | 98.57 | 98.55 | 99.90 | 97.99 | 98.51 | 96.69 |
| RF | local_only | 92.99 | 98.39 | 98.37 | 99.78 | 97.46 | 98.12 | 96.38 |
| RF | bag5_rf20 | 93.76 | 98.57 | 98.45 | 99.87 | 97.73 | 98.54 | 96.49 |
| DT | central | 94.81 | 98.73 | 98.12 | 99.87 | 97.81 | 98.51 | 97.67 |
| DT | fed_hard | 95.05 | 98.53 | 98.53 | 99.80 | 97.81 | 98.47 | 98.07 |
| DT | fed_soft | 94.98 | 98.47 | 98.57 | 99.80 | 97.71 | 98.38 | 97.97 |
| DT | local_only | 90.12 | 97.95 | 97.57 | 99.47 | 95.23 | 96.89 | 96.12 |
| DT | bag5_dt | 94.43 | 98.53 | 98.80 | 99.83 | 97.19 | 98.28 | 97.79 |
| KNN | central | 93.34 | 97.89 | 97.90 | 98.76 | 96.63 | 98.21 | 96.77 |
| KNN | fed_hard | 85.80 | 95.93 | 97.67 | 97.42 | 91.51 | 95.38 | 95.99 |
| KNN | fed_soft | 86.31 | 95.93 | 97.77 | 97.62 | 92.58 | 95.59 | 95.72 |
| KNN | local_only | 84.59 | 95.64 | 97.04 | 96.99 | 90.98 | 94.34 | 95.63 |
| SVM | central | 84.51 | 91.43 | 94.59 | 96.29 | 92.89 | 88.58 | 93.37 |
| SVM | fed_hard | 80.68 | 85.48 | 91.69 | 91.22 | 91.38 | 68.75 | 82.62 |
| SVM | fed_soft | 81.67 | 88.78 | 93.47 | 95.16 | 91.48 | 87.45 | 92.97 |
| SVM | local_only | 79.81 | 85.73 | 91.03 | 91.43 | 91.22 | 67.23 | 82.20 |
| MLP | central | 92.16 | 98.13 | 97.94 | 99.57 | 96.02 | 97.66 | 96.05 |
| MLP | fed | 88.58 | 95.17 | 97.13 | 97.67 | 93.47 | 92.70 | 94.21 |
| MLP | local_only | 86.72 | 94.67 | 96.66 | 97.40 | 92.62 | 92.16 | 93.92 |

### LYCOS-IDS2017 vs CIC-IDS2017 side by side (macro F1 %, mean ± std; ΔF1 paired, pp)

| Model | Regime | LYCOS F1 | CIC-IDS2017 F1 | LYCOS ΔF1 vs central | CIC ΔF1 vs central |
|---|---|---|---|---|---|
| RF | central | 99.54 ± 0.15 | 98.28 ± 0.28 |  |  |
| RF | fed_hard | 99.25 ± 0.23 | 97.79 ± 0.38 | -0.29 ± 0.18 | -0.48 ± 0.20 |
| RF | fed_soft | 99.27 ± 0.21 | 97.79 ± 0.30 | -0.28 ± 0.13 | -0.49 ± 0.09 |
| RF | local_only | 99.09 ± 0.19 | 97.35 ± 0.34 | -0.46 ± 0.12 | -0.92 ± 0.14 |
| RF | bag5_rf20 | 99.16 ± 0.22 | 97.63 ± 0.40 | -0.38 ± 0.11 | -0.65 ± 0.25 |
| DT | central | 99.13 ± 0.15 | 97.93 ± 0.39 |  |  |
| DT | fed_hard | 99.12 ± 0.19 | 98.04 ± 0.30 | -0.00 ± 0.24 | +0.11 ± 0.50 |
| DT | fed_soft | 99.09 ± 0.14 | 97.98 ± 0.36 | -0.04 ± 0.18 | +0.05 ± 0.58 |
| DT | local_only | 98.16 ± 0.23 | 96.19 ± 0.37 | -0.96 ± 0.26 | -1.74 ± 0.30 |
| DT | bag5_dt | 99.03 ± 0.11 | 97.84 ± 0.44 | -0.10 ± 0.10 | -0.10 ± 0.58 |
| KNN | central | 98.98 ± 0.31 | 97.07 ± 0.40 |  |  |
| KNN | fed_hard | 97.77 ± 0.26 | 94.24 ± 0.71 | -1.21 ± 0.42 | -2.83 ± 0.52 |
| KNN | fed_soft | 97.89 ± 0.18 | 94.50 ± 0.59 | -1.09 ± 0.31 | -2.57 ± 0.35 |
| KNN | local_only | 97.64 ± 0.36 | 93.60 ± 0.25 | -1.35 ± 0.39 | -3.47 ± 0.28 |
| SVM | central | 97.48 ± 0.32 | 91.66 ± 0.32 |  |  |
| SVM | fed_hard | 95.20 ± 0.53 | 84.54 ± 0.56 | -2.29 ± 0.35 | -7.12 ± 0.66 |
| SVM | fed_soft | 96.55 ± 0.41 | 90.14 ± 0.42 | -0.93 ± 0.26 | -1.52 ± 0.54 |
| SVM | local_only | 95.07 ± 0.43 | 84.09 ± 0.85 | -2.41 ± 0.25 | -7.57 ± 1.00 |
| MLP | central | 99.34 ± 0.20 | 96.79 ± 0.40 |  |  |
| MLP | fed | 98.48 ± 0.35 | 94.13 ± 0.99 | -0.86 ± 0.48 | -2.66 ± 0.86 |
| MLP | local_only | 98.16 ± 0.25 | 93.45 ± 0.35 | -1.18 ± 0.34 | -3.34 ± 0.10 |

