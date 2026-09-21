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


def plot_distance_matrix(D, title, n_show=25):
    block = np.asarray(D, dtype=float)[:n_show, :n_show]
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    image = ax.imshow(block, aspect="auto")
    fig.colorbar(image, ax=ax, shrink=0.82)
    ax.set(xlabel="Object", ylabel="Object", title=title)
    plt.tight_layout()
    plt.show()


def plot_similarity_graph(
    X,
    adjacency,
    weights=None,
    labels=None,
    title="Similarity Graph",
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
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    if G.number_of_edges() > 0:
        if weights is None:
            widths = 0.7
        else:
            edge_values = np.array(
                [G[u][v]["weight"] for u, v in G.edges()]
            )
            widths = 0.3 + 2.0 * edge_values
        nx.draw_networkx_edges(G, pos, width=widths, alpha=0.35, ax=ax)

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
        ax.legend(title="Group")

    ax.set(xlabel="Feature 1", ylabel="Feature 2", title=title)
    plt.tight_layout()
    plt.show()


def graph_summary(adjacency):
    A = np.asarray(adjacency, dtype=bool)
    G = nx.from_numpy_array(A.astype(int))
    return pd.Series({
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "components": nx.number_connected_components(G),
        "isolates": len(list(nx.isolates(G))),
        "mean_degree": np.mean([degree for _, degree in G.degree()]),
    })
