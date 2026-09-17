"""Lab 02-3 — functions you implement.

Loaders and figures live in helper.py.
"""

from __future__ import annotations

import numpy as np


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
