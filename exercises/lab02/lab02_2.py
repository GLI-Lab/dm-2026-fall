"""Helper functions for Lab 02-2 — Data Transformation.

Iris is loaded from scikit-learn. Titanic is loaded by data.loader.
This module constructs figures and holds the functions you implement.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.preprocessing import KBinsDiscretizer


def load_iris_data() -> pd.DataFrame:
    iris = load_iris(
        as_frame=True
    )

    data = iris.frame.copy()

    data["species"] = (
        data["target"]
        .map(
            dict(
                enumerate(
                    iris.target_names
                )
            )
        )
    )

    return data.drop(
        columns=["target"]
    )


def entropy(labels) -> float:
    """Shannon entropy of a label vector, using log base 2."""
    labels = np.asarray(
        labels
    )

    _, counts = np.unique(
        labels,
        return_counts=True,
    )

    p = (
        counts
        / counts.sum()
    )

    return float(
        -np.sum(
            p * np.log2(p)
        )
    )


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
    # interval. Use entropy() from this module.
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


def plot_discretization(
    values,
    boundaries,
    title,
):
    x = np.asarray(
        values,
        dtype=float,
    ).ravel()

    fig, ax = plt.subplots(
        figsize=(7.5, 4.5)
    )

    ax.hist(
        x,
        bins=24,
        alpha=0.65,
        edgecolor="black",
    )

    line_styles = [
        "-",
        "--",
        ":",
    ]

    for (name, edges), style in zip(
        boundaries.items(),
        line_styles,
    ):
        for i, boundary in enumerate(
            np.asarray(edges)[1:-1]
        ):
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


def plot_entropy_thresholds(
    thresholds,
    scores,
    best_threshold,
):
    fig, ax = plt.subplots(
        figsize=(7.5, 4)
    )

    ax.plot(
        thresholds,
        scores,
        marker=".",
        linewidth=1,
    )

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


def plot_log_transformation(
    original,
    transformed,
):
    original = pd.Series(
        original
    ).dropna()

    transformed = pd.Series(
        transformed
    ).dropna()

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(7, 3),
    )

    axes[0].hist(
        original,
        bins=30,
        edgecolor="black",
        alpha=0.7,
    )
    axes[0].set(
        xlabel="Fare",
        ylabel="Count",
        title="Original",
    )

    axes[1].hist(
        transformed,
        bins=30,
        edgecolor="black",
        alpha=0.7,
    )
    axes[1].set(
        xlabel="Transformed fare",
        ylabel="Count",
        title="Log Transformed",
    )

    plt.tight_layout()
    plt.show()


def plot_scaling(
    data_dict,
):
    names = list(
        data_dict.keys()
    )

    fig, axes = plt.subplots(
        len(names),
        1,
        figsize=(7.5, 2.3 * len(names)),
    )

    if len(names) == 1:
        axes = [axes]

    for ax, name in zip(
        axes,
        names,
    ):
        frame = data_dict[name]

        ax.boxplot(
            [
                frame[column]
                .dropna()
                .to_numpy()
                for column in frame.columns
            ],
            tick_labels=list(frame.columns),
            vert=False,
        )

        ax.set_title(
            name
        )

    plt.tight_layout()
    plt.show()
