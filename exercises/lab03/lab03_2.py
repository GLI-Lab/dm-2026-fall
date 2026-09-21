"""Lab 03-2: functions you implement."""

from __future__ import annotations

import numpy as np


def simple_matching_similarity(a, b, universe) -> float:
    """Return Simple Matching Coefficient for two presence/absence sets.

    ``universe`` is the complete set of possible items.  Shared presences and
    shared absences both count as matches.

    >>> U = {"a", "b", "c", "d"}
    >>> simple_matching_similarity({"a"}, {"b"}, U)
    0.5
    >>> simple_matching_similarity({"a"}, {"a"}, U)
    1.0
    """
    # ========== TODO ==========
    # 1. Convert a, b, and universe to sets.
    # 2. Count shared presences and shared absences.
    # 3. Divide the total number of matches by |universe|.
    # 4. If the universe is empty, return 1.0.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def jaccard_similarity(a, b) -> float:
    """Return Jaccard similarity between two sets.

    J(A, B) = |A intersection B| / |A union B|.
    If both sets are empty, return 1.0.

    >>> round(jaccard_similarity({"milk", "bread"}, {"milk", "apple"}), 4)
    0.3333
    >>> jaccard_similarity({"milk"}, {"bread"})
    0.0
    >>> jaccard_similarity(set(), set())
    1.0
    """
    # ========== TODO ==========
    # Convert a and b to sets, then divide intersection size by union size.
    # If the union is empty, return 1.0.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def cosine_similarity(x, y) -> float:
    """Return cosine similarity using coordinates observed in both vectors.

    NaN values are treated as missing.  Return np.nan when there are no
    jointly observed coordinates or when either observed vector has zero norm.

    >>> x = np.array([2.0, 3.0, 4.0, 5.0])
    >>> y = np.array([1.0, 2.0, 3.0, 4.0])
    >>> round(cosine_similarity(x, y), 4)
    0.9938
    >>> cosine_similarity([5.0, np.nan], [np.nan, 4.0])
    nan
    """
    # ========== TODO ==========
    # 1. Keep only coordinates that are finite in both x and y.
    # 2. Compute dot(x, y) / (||x|| * ||y||) on those coordinates.
    # 3. Return np.nan if there is no overlap or either norm is zero.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def pearson_similarity(x, y) -> float:
    """Return Pearson correlation using coordinates observed in both vectors.

    NaN values are treated as missing.  Return np.nan when fewer than two
    jointly observed values remain or when either centered vector has zero
    norm.

    >>> x = np.array([2.0, 3.0, 4.0, 5.0])
    >>> y = np.array([1.0, 2.0, 3.0, 4.0])
    >>> round(pearson_similarity(x, y), 4)
    1.0
    >>> z = np.array([5.0, 4.0, 3.0, 2.0])
    >>> round(pearson_similarity(x, z), 4)
    -1.0
    """
    # ========== TODO ==========
    # 1. Keep only coordinates observed in both vectors.
    # 2. Subtract each observed vector's own mean.
    # 3. Compute cosine similarity between the centered vectors.
    # 4. Return np.nan for fewer than two common values or a zero centered norm.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================
