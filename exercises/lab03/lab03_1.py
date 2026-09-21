"""Lab 03-1: functions you implement."""

from __future__ import annotations

import numpy as np


def euclidean_distance(x, y) -> float:
    """Return Euclidean (L2) distance between two numerical vectors.

    >>> euclidean_distance([0, 0], [3, 4])
    5.0
    >>> round(euclidean_distance([1, 2, 3], [1, 4, 6]), 4)
    3.6056
    """
    # ========== TODO ==========
    # Convert x and y to float arrays, square coordinate differences,
    # sum them, and take the square root.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def manhattan_distance(x, y) -> float:
    """Return Manhattan (L1) distance between two numerical vectors.

    >>> manhattan_distance([0, 0], [3, 4])
    7.0
    >>> manhattan_distance([1, 2, 3], [1, 4, 6])
    5.0
    """
    # ========== TODO ==========
    # Convert x and y to float arrays and sum absolute coordinate
    # differences.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def minkowski_distance(x, y, p: float) -> float:
    """Return Minkowski (Lp) distance for p >= 1.

    >>> minkowski_distance([0, 0], [3, 4], p=1)
    7.0
    >>> minkowski_distance([0, 0], [3, 4], p=2)
    5.0
    >>> round(minkowski_distance([0, 0], [3, 4], p=3), 4)
    4.4979
    """
    # ========== TODO ==========
    # 1. Reject p < 1 with ValueError.
    # 2. Compute (sum(|x_i - y_i| ** p)) ** (1 / p).
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def neighbor_ranking(
    X,
    query_index: int,
    distance_fn,
    k: int = 5,
    **distance_kwargs,
):
    """Return indices and distances of the k nearest other objects.

    ``distance_fn`` is called as ``distance_fn(query, row, **distance_kwargs)``.

    >>> X = np.array([[0.0, 0.0], [1.0, 0.0], [3.0, 0.0]])
    >>> idx, dist = neighbor_ranking(X, 0, euclidean_distance, k=2)
    >>> idx
    array([1, 2])
    >>> dist
    array([1., 3.])
    """
    # ========== TODO ==========
    # 1. Compute the distance from the query object to every other row.
    # 2. Put inf at the query object's own position.
    # 3. Sort the distances and return the first k indices and distances.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def mahalanobis_distance(x, y, cov_inv) -> float:
    """Return Mahalanobis distance using a supplied inverse covariance.

    d(x, y) = sqrt((x - y)^T Σ^{-1} (x - y)).
    If `cov_inv` is the identity matrix, this equals Euclidean distance.

    >>> VI = np.array([[0.75, -1.0], [-1.0, 2.0]])
    >>> round(mahalanobis_distance([2.0, 1.0], [0.0, 0.0], VI), 2)
    1.0
    >>> mahalanobis_distance([3.0, 4.0], [0.0, 0.0], np.eye(2))
    5.0
    """
    # ========== TODO ==========
    # 1. Convert x, y, and cov_inv to float arrays.
    # 2. Let diff = x - y.
    # 3. Return sqrt(diff @ cov_inv @ diff).
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def gower_distance(
    x,
    y,
    numeric_indices,
    categorical_indices,
    numeric_ranges,
) -> float:
    """Return Gower distance for complete mixed-type records.

    Numerical attributes use range-normalized absolute differences.
    Categorical attributes contribute 0 for a match and 1 for a mismatch.
    The final distance is the mean of the per-attribute distances.

    Missing values are intentionally excluded from this simplified exercise;
    the notebook first selects complete records.

    >>> x = np.array([20.0, 100.0, "F"], dtype=object)
    >>> y = np.array([30.0, 150.0, "F"], dtype=object)
    >>> round(gower_distance(x, y, [0, 1], [2], [100.0, 200.0]), 4)
    0.1167
    >>> z = np.array([20.0, 100.0, "M"], dtype=object)
    >>> round(gower_distance(x, z, [0, 1], [2], [100.0, 200.0]), 4)
    0.3333
    """
    # ========== TODO ==========
    # 1. For each numerical attribute, compute |x-y| / range.
    #    If a range is 0, use distance 0 for that attribute.
    # 2. For each categorical attribute, use 0 if the values match, else 1.
    # 3. Return the mean of all per-attribute distances.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================
