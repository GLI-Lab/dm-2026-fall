"""Lab 02 helpers: path setup, figures, and the generated Moons sample.

Importing this module puts the repository root and this lab folder on
sys.path so `data.loader` and `lab02_*.py` both work, whether Quarto
runs with execute-dir: file or Jupyter starts at the repo root.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from sklearn.datasets import make_moons


LAB_DIR = Path(__file__).resolve().parent
REPO_ROOT = LAB_DIR.parents[1]

for path in (REPO_ROOT, LAB_DIR):
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)


def load_moons_graph_data():
    X, y = make_moons(n_samples=140, noise=0.08, random_state=42)
    return X, y


def entropy(labels) -> float:
    """Shannon entropy of a label vector, using log base 2."""
    labels = np.asarray(labels)
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return float(-np.sum(p * np.log2(p)))


def plot_missing_counts(df, columns=("age", "embarked", "deck")):
    counts = df[list(columns)].isna().sum()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(counts.index, counts.values)
    ax.set(
        xlabel="Attribute",
        ylabel="Missing count",
        title="Missing Values in Titanic",
    )
    plt.tight_layout()
    plt.show()


def plot_fare_outliers(fare, lower, upper):
    values = fare.dropna().to_numpy(dtype=float)
    mask = (values < lower) | (values > upper)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(
        np.arange(len(values)),
        values,
        s=14,
        alpha=0.6,
        label="Fare",
    )
    ax.scatter(
        np.flatnonzero(mask),
        values[mask],
        s=28,
        marker="x",
        label="IQR outlier",
    )
    ax.axhline(lower, linestyle="--", linewidth=1, label="IQR bounds")
    ax.axhline(upper, linestyle="--", linewidth=1)
    ax.set(
        xlabel="Passenger",
        ylabel="Fare",
        title="Potential Fare Outliers",
    )
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_discretization(values, boundaries, title):
    x = np.asarray(values, dtype=float).ravel()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.hist(x, bins=24, alpha=0.65, edgecolor="black")
    line_styles = ["-", "--", ":"]
    for (name, edges), style in zip(boundaries.items(), line_styles):
        for i, boundary in enumerate(np.asarray(edges)[1:-1]):
            ax.axvline(
                boundary,
                linestyle=style,
                linewidth=1.7,
                label=name if i == 0 else None,
            )
    ax.set(
        xlabel="Petal length (cm)",
        ylabel="Count",
        title=title,
    )
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_entropy_thresholds(thresholds, scores, best_threshold):
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(thresholds, scores, marker=".", linewidth=1)
    ax.axvline(
        best_threshold,
        linestyle="--",
        linewidth=1.5,
        label="Best threshold",
    )
    ax.set(
        xlabel="Threshold",
        ylabel="Weighted entropy",
        title="Weighted Entropy by Threshold",
    )
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_log_transformation(original, transformed):
    original = pd.Series(original).dropna()
    transformed = pd.Series(transformed).dropna()
    fig, axes = plt.subplots(1, 2, figsize=(7, 3))
    axes[0].hist(original, bins=30, edgecolor="black", alpha=0.7)
    axes[0].set(xlabel="Fare", ylabel="Count", title="Original")
    axes[1].hist(transformed, bins=30, edgecolor="black", alpha=0.7)
    axes[1].set(
        xlabel="Transformed fare",
        ylabel="Count",
        title="Log Transformed",
    )
    plt.tight_layout()
    plt.show()


def plot_scaling(data_dict):
    names = list(data_dict.keys())
    fig, axes = plt.subplots(
        len(names), 1, figsize=(7.5, 2.3 * len(names)),
    )
    if len(names) == 1:
        axes = [axes]
    for ax, name in zip(axes, names):
        frame = data_dict[name]
        ax.boxplot(
            [
                frame[column].dropna().to_numpy()
                for column in frame.columns
            ],
            tick_labels=list(frame.columns),
            vert=False,
        )
        ax.set_title(name)
    plt.tight_layout()
    plt.show()


def _sample_indices_by_group(labels, per_group=12, random_state=0):
    """Return indices grouped by label, sampling at most `per_group` per group."""
    labels = np.asarray(labels)
    rng = np.random.default_rng(random_state)
    parts = []
    for group in pd.unique(labels):
        idx = np.flatnonzero(labels == group)
        if len(idx) > per_group:
            idx = np.sort(rng.choice(idx, size=per_group, replace=False))
        parts.append(idx)
    return np.concatenate(parts)


def plot_distance_matrix(
    D,
    title,
    labels=None,
    per_group=12,
):
    """Heatmap of a pairwise matrix. If `labels` is given, sample and group rows."""
    D = np.asarray(D, dtype=float)
    if labels is None:
        block = D
        group_note = ""
    else:
        idx = _sample_indices_by_group(labels, per_group=per_group)
        block = D[np.ix_(idx, idx)]
        group_note = f" ({per_group} sampled per group)"

    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    image = ax.imshow(block, aspect="auto")
    fig.colorbar(image, ax=ax, shrink=0.82)
    ax.set(
        xlabel="Object",
        ylabel="Object",
        title=title + group_note,
    )
    plt.tight_layout()
    plt.show()


def plot_similarity_graph(
    X,
    adjacency,
    weights=None,
    labels=None,
    title="Similarity Graph",
    xlabel="Feature 1",
    ylabel="Feature 2",
    ax=None,
):
    X = np.asarray(X, dtype=float)
    A = np.asarray(adjacency, dtype=bool)
    G = nx.Graph()
    G.add_nodes_from(range(len(X)))
    rows, cols = np.where(np.triu(A, k=1))
    for i, j in zip(rows, cols):
        weight = 1.0 if weights is None else float(weights[i, j])
        G.add_edge(int(i), int(j), weight=weight)

    pos = {i: X[i] for i in range(len(X))}
    created = ax is None
    if created:
        _, ax = plt.subplots(figsize=(7.2, 5.4))

    if G.number_of_edges() > 0:
        if weights is None:
            nx.draw_networkx_edges(
                G,
                pos,
                width=0.7,
                alpha=0.35,
                ax=ax,
            )
        else:
            edges = list(G.edges())
            edge_values = np.array(
                [G[u][v]["weight"] for u, v in edges],
                dtype=float,
            )
            order = np.argsort(edge_values)
            edges = [edges[i] for i in order]
            edge_values = edge_values[order]
            widths = 0.4 + 7.0 * edge_values
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=edges,
                width=widths,
                edge_color=edge_values,
                edge_cmap=plt.cm.Blues,
                edge_vmin=0.0,
                edge_vmax=1.0,
                alpha=0.95,
                ax=ax,
            )

    if labels is None:
        ax.scatter(X[:, 0], X[:, 1], s=32, alpha=0.8)
    else:
        labels = np.asarray(labels)
        for group in np.unique(labels):
            idx = labels == group
            ax.scatter(
                X[idx, 0],
                X[idx, 1],
                s=32,
                alpha=0.8,
                label=str(group),
            )

    isolates = [i for i, deg in G.degree() if deg == 0]
    if isolates:
        ax.scatter(
            X[isolates, 0],
            X[isolates, 1],
            s=90,
            facecolors="none",
            edgecolors="black",
            linewidths=1.4,
            zorder=4,
            label="isolate (degree 0)",
        )

    if labels is not None or isolates:
        ax.legend(title="Group")

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    if created:
        plt.tight_layout()
        plt.show()


def plot_graph_and_matrix(
    X,
    adjacency,
    matrix,
    labels=None,
    graph_title="Similarity Graph",
    matrix_title="Pairwise matrix",
    xlabel="Feature 1",
    ylabel="Feature 2",
    weights=None,
    per_group=12,
):
    """Graph in coordinate space (left) and a sampled pairwise matrix (right)."""
    fig, (ax_g, ax_m) = plt.subplots(1, 2, figsize=(12.6, 5.4))

    plot_similarity_graph(
        X,
        adjacency,
        weights=weights,
        labels=labels,
        title=graph_title,
        xlabel=xlabel,
        ylabel=ylabel,
        ax=ax_g,
    )

    matrix = np.asarray(matrix, dtype=float)
    if labels is None:
        idx = np.arange(len(matrix))
        note = ""
    else:
        idx = _sample_indices_by_group(labels, per_group=per_group)
        note = f" ({per_group} per group)"
    block = matrix[np.ix_(idx, idx)]

    image = ax_m.imshow(block, aspect="auto")
    fig.colorbar(image, ax=ax_m, shrink=0.82)
    ax_m.set(
        xlabel="Object",
        ylabel="Object",
        title=matrix_title + note,
    )
    fig.tight_layout()
    plt.show()


def graph_summary(adjacency):
    A = np.asarray(adjacency, dtype=bool)
    G = nx.from_numpy_array(A.astype(int))
    degrees = np.array([deg for _, deg in G.degree()])
    return pd.Series({
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "components": nx.number_connected_components(G),
        "isolates": int((degrees == 0).sum()),
        "min_degree": int(degrees.min()) if len(degrees) else 0,
        "max_degree": int(degrees.max()) if len(degrees) else 0,
        "mean_degree": float(degrees.mean()) if len(degrees) else 0.0,
    })
