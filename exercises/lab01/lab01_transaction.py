"""
lab01_transaction.py

Helper functions for Lab 01 — Transaction Data.

Design rule
-----------
- .py  : load data and construct representations
- .qmd : inspect returned objects, visualize them, and interpret them

Dataset
-------
Groceries Market Basket Dataset

The loader supports two common Kaggle-style forms:
1) basket format: one transaction per CSV row, items spread across columns
2) long format: Member_number, Date, itemDescription
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import csv

import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.preprocessing import MultiLabelBinarizer

# exercises/lab01/thisfile.py → parents[2] is the project root
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GROCERIES_PATH = _PROJECT_ROOT / "data" / "transaction" / "groceries.csv"


def load_groceries(path: str | Path | None = None) -> pd.DataFrame:
    """
    Load Groceries data and return one row per transaction.

    Returns
    -------
    pandas.DataFrame
        Columns:
        - transaction_id
        - items : list[str]
    """
    path = Path(path) if path is not None else DEFAULT_GROCERIES_PATH

    if not path.exists():
        raise FileNotFoundError(f"Groceries file not found: {path}")

    # First try the common long-format Kaggle version.
    try:
        raw = pd.read_csv(path)

        required = {"Member_number", "Date", "itemDescription"}
        if required.issubset(raw.columns):
            grouped = (
                raw.groupby(["Member_number", "Date"], sort=False)["itemDescription"]
                .apply(lambda s: list(dict.fromkeys(s.dropna().astype(str))))
                .reset_index()
            )

            grouped["transaction_id"] = [
                f"txn_{i:05d}" for i in range(len(grouped))
            ]
            grouped = grouped.rename(columns={"itemDescription": "items"})

            return grouped[["transaction_id", "items"]]
    except Exception:
        pass

    # Basket format: one CSV row = one transaction, variable number of items.
    transactions = []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            items = [
                item.strip()
                for item in row
                if item is not None and item.strip() != ""
            ]

            if items:
                transactions.append(items)

    if not transactions:
        raise ValueError(f"No transactions could be read from: {path}")

    return pd.DataFrame(
        {
            "transaction_id": [
                f"txn_{i:05d}" for i in range(len(transactions))
            ],
            "items": transactions,
        }
    )


def to_long_table(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Convert one-row-per-basket data into one-row-per-item data.

    The same transaction_id therefore appears multiple times.
    """
    long_df = transactions[["transaction_id", "items"]].explode(
        "items",
        ignore_index=True,
    )
    return long_df.rename(columns={"items": "item"})


def build_transaction_item_matrix(
    transactions: pd.DataFrame,
) -> tuple[sparse.csr_matrix, np.ndarray]:
    """
    Construct a sparse binary transaction × item matrix.

    X[t, i] = 1 if item i occurs in transaction t, otherwise 0.
    """
    encoder = MultiLabelBinarizer(sparse_output=True)
    X = encoder.fit_transform(transactions["items"]).tocsr()

    return X, np.asarray(encoder.classes_)


def compute_item_support(
    X: sparse.spmatrix,
    item_names: np.ndarray,
) -> pd.DataFrame:
    """
    Compute support for each item.

    support(item) = number of transactions containing the item
                    / total number of transactions
    """
    X = sparse.csr_matrix(X)

    counts = np.asarray(X.sum(axis=0)).ravel()
    support = counts / X.shape[0]

    result = pd.DataFrame(
        {
            "item": item_names,
            "count": counts.astype(int),
            "support": support,
        }
    )

    return result.sort_values(
        ["support", "item"],
        ascending=[False, True],
        ignore_index=True,
    )


def build_item_cooccurrence_graph(
    X: sparse.spmatrix,
    item_names: np.ndarray,
    *,
    top_n_items: int = 15,
    k: int = 2,
) -> nx.Graph:
    """
    Build an item-item graph using Jaccard similarity.

    Node = item
    Edge = relationship between two items
    Edge weight = Jaccard similarity

    J(i, j)
      = (# transactions containing both i and j)
        / (# transactions containing i or j)
    """
    X = sparse.csr_matrix(X)

    item_counts = np.asarray(X.sum(axis=0)).ravel()

    # Select the most frequent items for visualization.
    top_n_items = min(top_n_items, X.shape[1])
    top_idx = item_counts.argsort()[-top_n_items:][::-1]

    X_top = X[:, top_idx]
    counts_top = item_counts[top_idx]

    # Number of transactions containing both items.
    cooccurrence = (X_top.T @ X_top).toarray()

    # Jaccard denominator:
    # |A union B| = |A| + |B| - |A intersection B|
    union = (
        counts_top[:, None]
        + counts_top[None, :]
        - cooccurrence
    )

    # Jaccard similarity.
    jaccard = np.divide(
        cooccurrence,
        union,
        out=np.zeros_like(cooccurrence, dtype=float),
        where=union > 0,
    )

    np.fill_diagonal(jaccard, 0)

    G = nx.Graph()

    # Add item nodes.
    for local_i, global_i in enumerate(top_idx):
        G.add_node(
            local_i,
            item=str(item_names[global_i]),
            count=int(item_counts[global_i]),
        )

    # Connect each item to its k highest-Jaccard neighbors.
    for i in range(top_n_items):
        row = jaccard[i]

        candidate_idx = np.flatnonzero(row > 0)

        if len(candidate_idx) == 0:
            continue

        ranked = candidate_idx[
            np.argsort(row[candidate_idx])[::-1]
        ]

        neighbors = ranked[: min(k, len(ranked))]

        for j in neighbors:
            G.add_edge(
                int(i),
                int(j),
                weight=float(jaccard[i, j]),
            )

    return G
