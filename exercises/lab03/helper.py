"""Lab 03 helpers: path setup, figures, and graph summaries.

Data loading belongs in ``data.loader``.  This module keeps only reusable
visualization and summary code so that the student TODO functions stay in
``lab03_1.py`` and ``lab03_2.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


LAB_DIR = Path(__file__).resolve().parent
REPO_ROOT = LAB_DIR.parents[1]

for path in (REPO_ROOT, LAB_DIR):
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)


def graph_summary(adjacency) -> pd.Series:
    """Return a small structural summary of a Boolean adjacency matrix."""
    A = np.asarray(adjacency, dtype=bool)
    G = nx.from_numpy_array(A.astype(int))
    degrees = [degree for _, degree in G.degree()]

    return pd.Series({
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "components": nx.number_connected_components(G),
        "isolates": len(list(nx.isolates(G))),
        "mean_degree": float(np.mean(degrees)) if degrees else 0.0,
    })


def plot_user_similarity_graph(
    adjacency,
    user_ids,
    similarities=None,
    title="User Similarity kNN Graph",
):
    """Plot an undirected user-similarity graph with a fixed layout."""
    A = np.asarray(adjacency, dtype=bool)
    user_ids = list(user_ids)

    G = nx.Graph()
    G.add_nodes_from(range(len(user_ids)))

    rows, cols = np.where(np.triu(A, k=1))
    for i, j in zip(rows, cols):
        weight = 1.0
        if similarities is not None and np.isfinite(similarities[i, j]):
            weight = float(similarities[i, j])
        G.add_edge(int(i), int(j), weight=weight)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(8, 6))

    if G.number_of_edges() > 0:
        if similarities is None:
            widths = 0.8
        else:
            edge_values = np.array([
                max(0.0, G[u][v]["weight"])
                for u, v in G.edges()
            ])
            widths = 0.4 + 1.8 * edge_values

        nx.draw_networkx_edges(
            G,
            pos,
            width=widths,
            alpha=0.35,
            ax=ax,
        )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=280,
        alpha=0.85,
        ax=ax,
    )
    nx.draw_networkx_labels(
        G,
        pos,
        labels={i: str(user_ids[i]) for i in range(len(user_ids))},
        font_size=7,
        ax=ax,
    )

    ax.set_title(title)
    ax.axis("off")
    plt.tight_layout()
    plt.show()


def plot_mahalanobis_neighbors(
    X,
    species,
    query_index: int,
    euclidean_index: int,
    mahalanobis_index: int,
    xlabel: str,
    ylabel: str,
):
    """Scatter a 2D cloud and mark the Euclidean vs Mahalanobis neighbors."""
    X = np.asarray(X, dtype=float)
    species = np.asarray(species)

    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    for label in pd.unique(species):
        mask = species == label
        ax.scatter(
            X[mask, 0],
            X[mask, 1],
            s=28,
            alpha=0.45,
            label=str(label),
        )

    markers = [
        (query_index, "black", "o", 90, "Query"),
        (euclidean_index, "tab:red", "s", 90, "Euclidean NN"),
        (mahalanobis_index, "tab:blue", "D", 90, "Mahalanobis NN"),
    ]
    for index, color, marker, size, name in markers:
        ax.scatter(
            X[index, 0],
            X[index, 1],
            s=size,
            c=color,
            marker=marker,
            edgecolors="white",
            linewidths=0.8,
            zorder=3,
            label=name,
        )

    ax.set(xlabel=xlabel, ylabel=ylabel, title="Euclidean vs Mahalanobis neighbors")
    ax.legend(loc="best", fontsize=8)
    plt.tight_layout()
    plt.show()


def plot_distance_concentration(summary: pd.DataFrame):
    """Plot nearest, mean, and farthest distances against dimensionality."""
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    ax.plot(
        summary["dimension"],
        summary["nearest"],
        marker="o",
        label="Nearest",
    )
    ax.plot(
        summary["dimension"],
        summary["mean"],
        marker="o",
        label="Mean",
    )
    ax.plot(
        summary["dimension"],
        summary["farthest"],
        marker="o",
        label="Farthest",
    )

    ax.set_xscale("log")
    ax.set(
        xlabel="Dimension (log scale)",
        ylabel="Euclidean distance",
        title="Distance Concentration as Dimension Increases",
    )
    ax.legend()
    plt.tight_layout()
    plt.show()
