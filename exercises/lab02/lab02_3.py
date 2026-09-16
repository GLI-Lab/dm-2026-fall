"""Helper functions for Lab 02-3 — Similarity Graph Construction.

This module constructs figures and holds the functions you implement.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from sklearn.datasets import (
    load_iris,
    make_moons,
)


def load_iris_graph_data():
    iris = load_iris(
        as_frame=True
    )

    frame = iris.frame.copy()

    frame["species"] = (
        frame["target"]
        .map(
            dict(
                enumerate(
                    iris.target_names
                )
            )
        )
    )

    X = frame[[
        "petal length (cm)",
        "petal width (cm)",
    ]].to_numpy(
        dtype=float
    )

    return (
        X,
        frame["species"].to_numpy(),
        frame,
    )


def load_moons_graph_data():
    X, y = make_moons(
        n_samples=140,
        noise=0.08,
        random_state=42,
    )

    return X, y


def epsilon_graph(
    D,
    epsilon: float,
) -> np.ndarray:
    """Boolean adjacency for an undirected ε-graph, with no self-loops.

    Connect i and j when D[i, j] <= epsilon.

    >>> D = np.array([[0.0, 0.2, 0.8], [0.2, 0.0, 0.5], [0.8, 0.5, 0.0]])
    >>> epsilon_graph(D, 0.4)
    array([[False,  True, False],
           [ True, False, False],
           [False, False, False]])
    """
    # ========== TODO ==========
    # Compare D with epsilon, then set the diagonal to False.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def knn_graph(
    D,
    k: int,
) -> np.ndarray:
    """Undirected kNN adjacency from a distance matrix.

    For each row i, connect i to its k nearest neighbors (excluding i).
    Ignore direction by taking the OR of the directed matrix and its
    transpose.

    >>> D = np.array([[0.0, 0.2, 0.8], [0.2, 0.0, 0.5], [0.8, 0.5, 0.0]])
    >>> knn_graph(D, k=1)
    array([[False,  True, False],
           [ True, False,  True],
           [False,  True, False]])
    """
    # ========== TODO ==========
    # For each object, set its own distance to inf, then take the k
    # smallest remaining distances with np.argsort. Symmetrize at the end.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def apply_edge_weights(
    similarity,
    adjacency,
) -> np.ndarray:
    """Keep similarity values only on selected edges; put 0 elsewhere.

    >>> apply_edge_weights(
    ...     np.array([[1.0, 0.5], [0.5, 1.0]]),
    ...     np.array([[False, True], [True, False]]),
    ... )
    array([[0. , 0.5],
           [0.5, 0. ]])
    """
    # ========== TODO ==========
    # Use np.where(adjacency, similarity, 0.0).
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def plot_distance_matrix(
    D,
    title,
    n_show=25,
):
    block = np.asarray(
        D,
        dtype=float,
    )[:n_show, :n_show]

    fig, ax = plt.subplots(
        figsize=(6.2, 5.2)
    )

    image = ax.imshow(
        block,
        aspect="auto",
    )

    fig.colorbar(
        image,
        ax=ax,
        shrink=0.82,
    )

    ax.set(
        xlabel="Object",
        ylabel="Object",
        title=title,
    )

    plt.tight_layout()
    plt.show()


def plot_similarity_graph(
    X,
    adjacency,
    weights=None,
    labels=None,
    title="Similarity Graph",
):
    X = np.asarray(
        X,
        dtype=float,
    )

    A = np.asarray(
        adjacency,
        dtype=bool,
    )

    G = nx.Graph()
    G.add_nodes_from(
        range(len(X))
    )

    rows, cols = np.where(
        np.triu(
            A,
            k=1,
        )
    )

    for i, j in zip(
        rows,
        cols,
    ):
        weight = (
            1.0
            if weights is None
            else float(
                weights[i, j]
            )
        )

        G.add_edge(
            int(i),
            int(j),
            weight=weight,
        )

    pos = {
        i: X[i]
        for i in range(
            len(X)
        )
    }

    fig, ax = plt.subplots(
        figsize=(7.2, 5.4)
    )

    if G.number_of_edges() > 0:
        if weights is None:
            widths = 0.7
        else:
            edge_values = np.array([
                G[u][v]["weight"]
                for u, v
                in G.edges()
            ])

            widths = (
                0.3
                + 2.0 * edge_values
            )

        nx.draw_networkx_edges(
            G,
            pos,
            width=widths,
            alpha=0.35,
            ax=ax,
        )

    if labels is None:
        ax.scatter(
            X[:, 0],
            X[:, 1],
            s=32,
            alpha=0.8,
        )
    else:
        labels = np.asarray(
            labels
        )

        for group in np.unique(
            labels
        ):
            idx = (
                labels == group
            )

            ax.scatter(
                X[idx, 0],
                X[idx, 1],
                s=32,
                alpha=0.8,
                label=str(group),
            )

        ax.legend(
            title="Group"
        )

    ax.set(
        xlabel="Feature 1",
        ylabel="Feature 2",
        title=title,
    )

    plt.tight_layout()
    plt.show()


def graph_summary(
    adjacency,
):
    A = np.asarray(
        adjacency,
        dtype=bool,
    )

    G = nx.from_numpy_array(
        A.astype(int)
    )

    return pd.Series({
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "components": nx.number_connected_components(G),
        "isolates": len(
            list(
                nx.isolates(G)
            )
        ),
        "mean_degree": np.mean([
            degree
            for _, degree
            in G.degree()
        ]),
    })
