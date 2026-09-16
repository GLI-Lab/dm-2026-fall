"""
lab01_interaction.py

Helper functions for Lab 01-4 — Interaction Data.

Original MovieLens files are located and loaded by data.loader.
This helper constructs representations and draws figures.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


RANDOM_STATE = 42


def sample_interactions(
    ratings: pd.DataFrame,
    *,
    n_items: int = 12,
    n_users: int = 10,
    min_overlap: int = 3,
    user_col: str = "user_id",
    item_col: str = "item_id",
    random_state: int = RANDOM_STATE,
) -> pd.DataFrame:
    """Take the most-rated items and a random sample of users who rated some of them.

    Produces a block small enough to print and draw in full, while keeping the
    gaps that make the full matrix sparse.
    """
    popular = ratings[item_col].value_counts().head(n_items).index
    subset = ratings[ratings[item_col].isin(popular)]

    counts = subset[user_col].value_counts()
    eligible = counts[(counts >= min_overlap) & (counts < n_items)].index

    rng = np.random.default_rng(random_state)
    chosen = rng.choice(eligible, size=min(n_users, len(eligible)), replace=False)
    subset = subset[subset[user_col].isin(chosen)]

    return subset.sort_values([user_col, item_col]).reset_index(drop=True)


def build_utility_table(ratings):
    """Pivot unique user-item ratings into a small table with NaN for missing pairs."""
    return ratings.pivot(
        index="user_id", columns="item_id", values="rating",
    ).sort_index().sort_index(axis=1)



def build_utility_matrix(ratings):
    """Return the sparse rating matrix and its ordered user/item IDs."""
    if ratings.duplicated(subset=["user_id", "item_id"]).any():
        raise ValueError("Choose how to handle repeated user-item ratings first.")

    user_ids = np.sort(ratings["user_id"].unique())
    item_ids = np.sort(ratings["item_id"].unique())
    user_pos = pd.Series(np.arange(len(user_ids)), index=user_ids)
    item_pos = pd.Series(np.arange(len(item_ids)), index=item_ids)

    rows = user_pos.loc[ratings["user_id"]].to_numpy()
    cols = item_pos.loc[ratings["item_id"]].to_numpy()
    values = ratings["rating"].to_numpy(dtype=float)
    X = sparse.csr_matrix(
        (values, (rows, cols)),
        shape=(len(user_ids), len(item_ids)),
    )
    return X, user_ids, item_ids


def matrix_density(X):
    """Return the stored-entry count divided by the number of cells."""
    n_users, n_items = X.shape
    return X.nnz / (n_users * n_items)


def binarize_utility_matrix(X, *, threshold=4.0):
    """Keep observed ratings at or above the positive-rating threshold."""
    X_binary = sparse.csr_matrix(X, copy=True)
    X_binary.data = (X_binary.data >= threshold).astype(float)
    X_binary.eliminate_zeros()
    return X_binary


def build_bipartite_graph(ratings, *, titles=None):
    """Represent each observed rating as a weighted user-item edge."""
    G = nx.Graph()
    for user in ratings["user_id"].unique():
        G.add_node(f"u{user}", bipartite=0, kind="user", label=f"u{user}")
    for item in ratings["item_id"].unique():
        title = None if titles is None else titles.get(item)
        G.add_node(
            f"i{item}", bipartite=1, kind="item",
            label=str(title) if title is not None else f"i{item}",
        )
    for row in ratings.itertuples(index=False):
        G.add_edge(f"u{row.user_id}", f"i{row.item_id}", weight=float(row.rating))
    return G


def project_onto_users(G, *, min_shared=1):
    """Connect users by the number of items both have rated."""
    user_nodes = [n for n, d in G.nodes(data=True) if d["bipartite"] == 0]
    P = nx.bipartite.weighted_projected_graph(G, user_nodes)
    weak_edges = [
        (u, v) for u, v, d in P.edges(data=True)
        if d["weight"] < min_shared
    ]
    P.remove_edges_from(weak_edges)
    return P


def compute_item_similarity(X, *, query_index):
    """Compare one item against every item using user-based vectors."""
    X_items = sparse.csr_matrix(X).T.tocsr()
    return cosine_similarity(X_items[query_index], X_items).ravel()


def build_item_knn_graph(X, *, item_ids, titles=None, k=3, max_items=80):
    """Connect popular items using cosine similarity between item rows."""
    X_items = sparse.csr_matrix(X).T.tocsr()
    item_ids = np.asarray(item_ids)

    popularity = np.asarray((X_items > 0).sum(axis=1)).ravel()
    keep = np.argsort(popularity)[::-1][:max_items]
    keep = np.sort(keep)
    X_items = X_items[keep]
    item_ids = item_ids[keep]
    n_items = X_items.shape[0]

    G = nx.Graph()
    for i, item_id in enumerate(item_ids):
        title = None if titles is None else titles.get(item_id)
        G.add_node(
            i, item_id=int(item_id),
            title=str(title) if title is not None else str(item_id),
        )
    if n_items == 0:
        return G

    model = NearestNeighbors(n_neighbors=min(k + 1, n_items), metric="cosine")
    model.fit(X_items)
    distances, indices = model.kneighbors(X_items)

    for i in range(n_items):
        other_items = [
            (distance, int(j))
            for distance, j in zip(distances[i], indices[i])
            if j != i
        ][:k]
        for distance, j in other_items:
            G.add_edge(i, j, weight=1.0 - float(distance))
    return G


def build_biadjacency_matrix(G, user_ids, item_ids):
    """Return the rating-weighted graph matrix using the supplied user/item order."""
    row_nodes = [f"u{user}" for user in user_ids]
    col_nodes = [f"i{item}" for item in item_ids]
    B = sparse.csr_matrix(
        nx.bipartite.biadjacency_matrix(
            G, row_order=row_nodes, column_order=col_nodes, weight="weight",
        )
    )
    return B, row_nodes, col_nodes



def plot_bipartite_graph(G):
    """Draw users and movies in two columns without changing the graph."""
    user_nodes = [n for n, d in G.nodes(data=True) if d["bipartite"] == 0]
    item_nodes = [n for n, d in G.nodes(data=True) if d["bipartite"] == 1]

    pos = nx.bipartite_layout(G, user_nodes)

    fig, ax = plt.subplots(figsize=(11, 8))

    nx.draw_networkx_edges(G, pos, alpha=0.25, edge_color="#AAAAAA", width=1.0, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=user_nodes, node_color="tab:blue",
                           node_size=900, label="user", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=item_nodes, node_color="tab:orange",
                           node_size=900, node_shape="s", label="item", ax=ax)

    nx.draw_networkx_labels(
        G, pos,
        labels={n: G.nodes[n]["label"] for n in user_nodes},
        font_size=9, font_color="white", font_weight="bold", ax=ax,
    )

    for node in item_nodes:
        x, y = pos[node]
        ax.text(x + 0.10, y, G.nodes[node]["label"][:24],
                fontsize=10, va="center", ha="left")

    ax.legend(scatterpoints=1, fontsize=11, frameon=False, ncol=2, markerscale=0.7,
              loc="lower center", bbox_to_anchor=(0.5, 1.01),
              handletextpad=0.8, columnspacing=2.5)
    ax.set_xlim(-1.25, 1.45)
    ax.axis("off")
    return plt.gcf(), plt.gca()


def plot_user_projection(P):
    """Draw a user projection with shared-item counts on the edges."""
    pos = nx.circular_layout(P)

    plt.figure(figsize=(10, 9))
    nx.draw_networkx_edges(P, pos, width=1.3, alpha=0.4, edge_color="#AAAAAA")
    nx.draw_networkx_nodes(P, pos, node_color="tab:blue", node_size=1700)
    nx.draw_networkx_labels(P, pos, font_size=11, font_color="white",
                            font_weight="bold")
    nx.draw_networkx_edge_labels(
        P, pos,
        edge_labels={(u, v): d["weight"] for u, v, d in P.edges(data=True)},
        font_size=9, label_pos=0.28, rotate=False,
    )
    plt.margins(0.14)
    plt.axis("off")
    return plt.gcf(), plt.gca()


def plot_item_similarity_graph(G_items):
    """Draw an item graph with shortened titles and similarity labels."""
    def short_title(title):
        title = title.split(" (")[0]
        return title if len(title) <= 17 else title[:16] + "."

    pos = nx.kamada_kawai_layout(G_items)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_edges(G_items, pos, width=1.0, alpha=0.5, edge_color="#AAAAAA")
    nx.draw_networkx_nodes(G_items, pos, node_size=700, node_color="tab:orange")

    nx.draw_networkx_labels(
        G_items, pos,
        labels={n: short_title(G_items.nodes[n]["title"]) for n in G_items.nodes},
        font_size=8,
    )
    nx.draw_networkx_edge_labels(
        G_items, pos,
        edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in G_items.edges(data=True)},
        font_size=6.5, label_pos=0.5, rotate=False,
    )
    plt.margins(0.14)
    plt.axis("off")
    return plt.gcf(), plt.gca()
