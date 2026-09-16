"""
lab01_graph.py

Helper functions for Lab 01-3 — Graph Data.

Original Karate Club files are stored by data.loader.
This helper draws figures from the loaded graph.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from matplotlib.colors import ListedColormap

RANDOM_STATE = 42


def plot_karate_graph(
    G: nx.Graph,
) -> None:
    """Visualize the graph with node layout and club membership colors."""
    node_colors = [
        "skyblue"
        if G.nodes[node]["club"] == "Mr. Hi"
        else "salmon"
        for node in G.nodes()
    ]

    pos = nx.spring_layout(
        G,
        seed=RANDOM_STATE,
    )

    plt.figure(
        figsize=(8, 6)
    )

    nx.draw(
        G,
        pos,
        node_color=node_colors,
        with_labels=True,
        node_size=500,
        edge_color="gray",
    )

    plt.show()


def plot_adjacency_matrix(
    A: np.ndarray,
    *,
    n: int = 12,
) -> None:
    """Visualize a binary adjacency matrix."""
    n = min(
        n,
        A.shape[0],
        A.shape[1],
    )

    A_small = A[:n, :n]

    cmap = ListedColormap(
        [
            "#F7F7F7",
            "#87CEEB",
        ]
    )

    fig, ax = plt.subplots(
        figsize=(7, 7)
    )

    ax.imshow(
        A_small,
        cmap=cmap,
        vmin=0,
        vmax=1,
        interpolation="nearest",
    )

    for i in range(n):
        for j in range(n):
            ax.text(
                j,
                i,
                str(A_small[i, j]),
                ha="center",
                va="center",
                fontsize=8,
            )

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))

    ax.set_xticklabels(
        [f"N{i}" for i in range(n)]
    )
    ax.set_yticklabels(
        [f"N{i}" for i in range(n)]
    )

    ax.set_xticks(
        np.arange(-0.5, n, 1),
        minor=True,
    )
    ax.set_yticks(
        np.arange(-0.5, n, 1),
        minor=True,
    )

    ax.grid(
        which="minor",
        color="#D9D9D9",
        linewidth=0.6,
    )

    ax.tick_params(
        which="minor",
        bottom=False,
        left=False,
    )

    ax.set_xlabel("Node")
    ax.set_ylabel("Node")

    plt.tight_layout()
    plt.show()
