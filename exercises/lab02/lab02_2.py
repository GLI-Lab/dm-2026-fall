"""Lab 02-2 — functions you implement.

Iris and figures live in helper.py. Titanic is loaded by data.loader.
"""

from __future__ import annotations

import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

from helper import entropy


def equal_frequency_discretize(
    values: pd.DataFrame,
    n_bins: int = 3,
):
    """Fit an equal-frequency discretizer and transform `values`.

    Return `(discretizer, bins)`, where `bins` is the output of
    `fit_transform()`.

    >>> values = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
    >>> discretizer, bins = equal_frequency_discretize(values, n_bins=3)
    >>> discretizer.strategy
    'quantile'
    >>> bins.shape
    (6, 1)
    """
    # ========== TODO ==========
    # Create KBinsDiscretizer with strategy="quantile", encode="ordinal",
    # subsample=None, then call fit_transform(values).
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def weighted_split_entropy(
    left_labels,
    right_labels,
) -> float:
    """Weighted average of the two interval entropies.

    >>> weighted_split_entropy(["A", "A"], ["A", "B"])
    0.5
    """
    # ========== TODO ==========
    # Weight each interval's entropy by the proportion of objects in that
    # interval. Use entropy() from helper.py.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def binarize_categorical(
    series: pd.Series,
    prefix: str,
) -> pd.DataFrame:
    """One-hot encode a categorical Series with integer 0/1 columns.

    >>> out = binarize_categorical(pd.Series(["male", "female", "male"]), "sex")
    >>> sorted(out.columns.tolist())
    ['sex_female', 'sex_male']
    >>> out["sex_male"].tolist()
    [1, 0, 1]
    """
    # ========== TODO ==========
    # Use pd.get_dummies(..., prefix=prefix, dtype=int).
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def minmax_scale(
    X: pd.DataFrame,
) -> pd.DataFrame:
    """Scale each column to [0, 1] with min-max normalization.

    >>> scaled = minmax_scale(pd.DataFrame({"a": [0.0, 5.0, 10.0]}))
    >>> scaled["a"].tolist()
    [0.0, 0.5, 1.0]
    """
    # ========== TODO ==========
    # (X - X.min()) / (X.max() - X.min())
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def robust_scale(
    X: pd.DataFrame,
) -> pd.DataFrame:
    """Scale each column with the median and IQR.

    >>> scaled = robust_scale(pd.DataFrame({"a": [0.0, 5.0, 10.0]}))
    >>> round(float(scaled["a"].iloc[1]), 6)
    0.0
    """
    # ========== TODO ==========
    # (X - X.median()) / (X.quantile(0.75) - X.quantile(0.25))
    raise NotImplementedError("Remove this line and implement above")
    # ==========================
