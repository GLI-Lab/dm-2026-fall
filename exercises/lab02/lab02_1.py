"""Lab 02-1 — functions you implement.

Titanic is loaded by data.loader. Figures live in helper.py.
"""

from __future__ import annotations

import pandas as pd


def fill_missing_with_mode(
    df: pd.DataFrame,
    column: str = "embarked",
) -> tuple[pd.DataFrame, str]:
    """Fill missing values in `column` with its most frequent category.

    Returns a copy of `df` and the mode used for filling.

    >>> data = pd.DataFrame({"embarked": ["S", None, "S", "C"]})
    >>> filled, mode = fill_missing_with_mode(data)
    >>> mode
    'S'
    >>> filled["embarked"].tolist()
    ['S', 'S', 'S', 'C']
    """
    # ========== TODO ==========
    # Replace missing values in `column` with its mode.
    # Hint: Series.mode() and Series.fillna().
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def drop_duplicate_rows(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:
    """Count duplicate rows and return a DataFrame with them removed.

    The first occurrence of each duplicated row is kept.

    >>> data = pd.DataFrame({"a": [1, 2, 2, 3], "b": [1, 2, 2, 3]})
    >>> cleaned, n_duplicates = drop_duplicate_rows(data)
    >>> int(n_duplicates)
    1
    >>> len(cleaned)
    3
    """
    # ========== TODO ==========
    # Store the duplicate count and the DataFrame after drop_duplicates().
    # Hint: duplicated().sum() and drop_duplicates().
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def iqr_outlier_bounds(
    q1: float,
    q3: float,
) -> tuple[float, float]:
    """Return (lower, upper) fences using the 1.5 IQR rule.

    >>> iqr_outlier_bounds(1.0, 3.0)
    (-2.0, 6.0)
    """
    # ========== TODO ==========
    # lower = Q1 - 1.5 IQR, upper = Q3 + 1.5 IQR, where IQR = Q3 - Q1.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def summarize_by_class_and_sex(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Group by pclass and sex; mean of survived and median of fare.

    >>> data = pd.DataFrame({
    ...     "pclass": [1, 1, 3, 3],
    ...     "sex": ["male", "female", "male", "female"],
    ...     "survived": [0, 1, 0, 1],
    ...     "fare": [50.0, 70.0, 8.0, 12.0],
    ... })
    >>> out = summarize_by_class_and_sex(data)
    >>> set(out.columns) == {"pclass", "sex", "survived", "fare"}
    True
    >>> len(out)
    4
    """
    # ========== TODO ==========
    # groupby(["pclass", "sex"]) then agg({"survived": "mean", "fare": "median"}).
    # Reset the index so pclass and sex are columns.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================


def stratified_sample_by_class(
    df: pd.DataFrame,
    n_per_group: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Sample up to `n_per_group` rows from each pclass group.

    >>> data = pd.DataFrame({
    ...     "pclass": [1, 1, 1, 2, 2, 3],
    ...     "fare": [10, 20, 30, 40, 50, 60],
    ... })
    >>> sample = stratified_sample_by_class(data, n_per_group=2)
    >>> sample["pclass"].value_counts().sort_index().tolist()
    [2, 2, 1]
    """
    # ========== TODO ==========
    # For each pclass group, sample min(len(group), n_per_group) rows and
    # concatenate the groups. Pass random_state so the sample is reproducible.
    raise NotImplementedError("Remove this line and implement above")
    # ==========================
