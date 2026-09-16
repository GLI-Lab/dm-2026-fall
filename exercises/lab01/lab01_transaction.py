"""
lab01_transaction.py

Helper functions for Lab 01-5 — Transaction Data.

Original Groceries files are located, downloaded, and grouped by data.loader.
This helper constructs representations from the loaded baskets.
"""

from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.preprocessing import MultiLabelBinarizer

RANDOM_STATE = 42


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
