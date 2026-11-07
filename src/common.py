# Shared configuration, data loading, label mapping and cleaning for both datasets.
# The raw data folders (./data and ./data_lycos) are only ever read, never written.

import glob
import re
import os
import datetime

import numpy as np
import pandas as pd

# Project root = parent of this src/ folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
CACHE = os.path.join(ROOT, "cache")

# Minimum number of flows (after cleaning / de-duplication) a family needs to be kept
MIN_CLASS_FLOWS = 100

DATASETS = {
    "lycos": {
        "name": "LYCOS-IDS2017",
        "folder": os.path.join(ROOT, "data_lycos"),
        "pattern": "*.csv",
        "encoding": "utf-8",
        "label_col": "label",
        # Identifier columns: flow id, IPs, ports, timestamp
        "id_cols": ["flow_id", "src_addr", "src_port", "dst_addr", "dst_port", "timestamp"],
    },
    "cicids": {
        "name": "CIC-IDS2017",
        "folder": os.path.join(ROOT, "data"),
        "pattern": "*.csv",
        # 'Web Attack ? ...' labels contain a non-ASCII dash; labels are normalised by normalise_label()
        "encoding": "latin-1",
        "label_col": "Label",
        # Only identifier present in the MachineLearningCVE release is the destination port
        "id_cols": ["Flow ID", "Source IP", "Source Port", "Destination IP",
                    "Destination Port", "Timestamp"],
    },
}

# Raw label -> family mapping, one per dataset
LABEL_MAP = {
    "lycos": {
        "benign": "Benign",
        "dos_hulk": "DoS", "dos_goldeneye": "DoS", "dos_slowloris": "DoS", "dos_slowhttptest": "DoS",
        "ddos": "DDoS",
        "portscan": "PortScan",
        "ftp_patator": "BruteForce", "ssh_patator": "BruteForce",
        "webattack_bruteforce": "WebAttack", "webattack_xss": "WebAttack",
        "webattack_sql_injection": "WebAttack",
        "bot": "Bot",
        "heartbleed": "Heartbleed",
        "infiltration": "Infiltration",
    },
    "cicids": {
        "BENIGN": "Benign",
        "DoS Hulk": "DoS", "DoS GoldenEye": "DoS", "DoS slowloris": "DoS", "DoS Slowhttptest": "DoS",
        "DDoS": "DDoS",
        "PortScan": "PortScan",
        "FTP-Patator": "BruteForce", "SSH-Patator": "BruteForce",
        "Web Attack - Brute Force": "WebAttack", "Web Attack - XSS": "WebAttack",
        "Web Attack - Sql Injection": "WebAttack",
        "Bot": "Bot",
        "Heartbleed": "Heartbleed",
        "Infiltration": "Infiltration",
    },
}


def log_progress(msg):
    # Append one timestamped line to results/PROGRESS.md and echo it
    os.makedirs(RESULTS, exist_ok=True)
    line = f"- {datetime.datetime.now():%Y-%m-%d %H:%M:%S} | {msg}"
    with open(os.path.join(RESULTS, "PROGRESS.md"), "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def list_files(ds):
    cfg = DATASETS[ds]
    return sorted(glob.glob(os.path.join(cfg["folder"], cfg["pattern"])))


def read_raw_file(ds, path):
    # Read one CSV and strip leading/trailing spaces from column names
    cfg = DATASETS[ds]
    df = pd.read_csv(path, encoding=cfg["encoding"], low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    return df


def normalise_label(raw):
    # Replace any run of non-printable/non-ASCII characters by '-' and trim spaces
    return re.sub(r"[^ -~]+", "-", str(raw)).strip()


def map_label(ds, raw):
    # Map a raw label to its family; unknown labels raise so nothing is silently mislabelled
    m = LABEL_MAP[ds]
    if raw not in m:
        raise KeyError(f"Unmapped label {raw!r} in dataset {ds}")
    return m[raw]


def load_clean(ds, verbose=True):
    # Steps of spec item 6: load all CSVs, strip names, drop identifiers, inf->NaN,
    # drop duplicate rows, drop zero-variance columns. Result is cached as a pickle.
    os.makedirs(CACHE, exist_ok=True)
    cache_path = os.path.join(CACHE, f"{ds}_clean.pkl")
    info_path = os.path.join(CACHE, f"{ds}_clean_info.pkl")
    if os.path.exists(cache_path) and os.path.exists(info_path):
        if verbose:
            print(f"[{ds}] loading cleaned data from cache {os.path.relpath(cache_path, ROOT)}")
        return pd.read_pickle(cache_path), pd.read_pickle(info_path)

    cfg = DATASETS[ds]
    label_col = cfg["label_col"].strip()
    parts = []
    info = {"files": [], "dropped_id_cols": set(), "dropped_dup_cols": []}
    for f in list_files(ds):
        df = read_raw_file(ds, f)
        info["files"].append((os.path.basename(f), len(df)))
        ids = [c for c in cfg["id_cols"] if c in df.columns]
        info["dropped_id_cols"].update(ids)
        df = df.drop(columns=ids)
        y = df.pop(label_col).map(normalise_label)
        # Convert every remaining column to numeric; non-parsable cells become NaN
        df = df.apply(pd.to_numeric, errors="coerce").astype("float64")
        df["Label"] = y.map(lambda v: map_label(ds, v)).values
        df["RawLabel"] = y.values
        parts.append(df)
        if verbose:
            print(f"[{ds}] read {os.path.basename(f)}: {len(df)} rows")
    df = pd.concat(parts, ignore_index=True)
    del parts
    info["dropped_id_cols"] = sorted(info["dropped_id_cols"])
    info["rows_raw"] = len(df)

    # Exact duplicate columns (CIC-IDS2017 ships 'Fwd Header Length' twice -> '.1' suffix)
    feat = [c for c in df.columns if c not in ("Label", "RawLabel")]
    for c in feat:
        if c.endswith(".1") and c[:-2] in df.columns:
            if df[c].equals(df[c[:-2]]):
                info["dropped_dup_cols"].append(c)
    df = df.drop(columns=info["dropped_dup_cols"])

    # inf -> NaN
    feat = [c for c in df.columns if c not in ("Label", "RawLabel")]
    n_inf = int(np.isinf(df[feat].to_numpy()).sum())
    df[feat] = df[feat].replace([np.inf, -np.inf], np.nan)
    info["n_inf_cells"] = n_inf
    info["n_nan_cells_after_inf"] = int(df[feat].isna().sum().sum())

    # Duplicate rows (features + raw label)
    before = len(df)
    df = df.drop_duplicates(subset=feat + ["RawLabel"]).reset_index(drop=True)
    info["rows_dup_dropped"] = before - len(df)
    # Feature vectors that still appear with more than one family label (label conflicts)
    h = pd.util.hash_pandas_object(df[feat], index=False)
    n_lab = df["Label"].groupby(h.values).transform("nunique")
    info["rows_feature_dup_conflicting_label"] = int((n_lab.values > 1).sum())

    # Zero-variance columns (computed on the whole cleaned dataset; label-free)
    nun = df[feat].nunique(dropna=True)
    zv = sorted(nun[nun <= 1].index.tolist())
    info["dropped_zero_var_cols"] = zv
    df = df.drop(columns=zv)
    info["rows_clean"] = len(df)
    info["n_features"] = df.shape[1] - 2

    df.to_pickle(cache_path)
    pd.to_pickle(info, info_path)
    return df, info


def class_filter(df):
    # Keep only families with >= MIN_CLASS_FLOWS rows; return filtered df and dropped dict
    vc = df["Label"].value_counts()
    keep = vc[vc >= MIN_CLASS_FLOWS].index
    dropped = vc[vc < MIN_CLASS_FLOWS].to_dict()
    return df[df["Label"].isin(keep)].reset_index(drop=True), dropped
