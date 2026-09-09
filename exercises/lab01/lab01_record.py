"""
lab01_record.py

Helper functions for Lab 01 — Record Data.

Design rule
-----------
- .py  : load data and construct representations
- .qmd : inspect returned objects, visualize them, and interpret them

Dataset
-------
Titanic
"""

from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.preprocessing import MultiLabelBinarizer


def load_titanic() -> pd.DataFrame:
    """Load the Titanic dataset and keep the columns used in this lab."""
    titanic = sns.load_dataset("titanic")

    return titanic[
        [
            "survived",
            "pclass",
            "sex",
            "age",
            "fare",
            "embarked",
            "alone",
        ]
    ].copy()


def build_numeric_matrix(
    titanic: pd.DataFrame,
) -> pd.DataFrame:
    """Titanic records -> numerical feature matrix."""
    X = titanic[
        [
            "age",
            "fare",
            "pclass",
            "sex",
            "embarked",
            "alone",
        ]
    ].copy()

    X["age"] = X["age"].fillna(
        X["age"].median()
    )

    X["embarked"] = X["embarked"].fillna(
        X["embarked"].mode()[0]
    )

    X = pd.get_dummies(
        X,
        columns=[
            "pclass",
            "sex",
            "embarked",
            "alone",
        ],
        dtype=int,
    )

    return X


def build_transactions(
    titanic: pd.DataFrame,
) -> pd.Series:
    """Titanic records -> transaction representation."""
    data = titanic.copy()

    data["embarked"] = data["embarked"].fillna(
        data["embarked"].mode()[0]
    )

    data["age_group"] = pd.cut(
        data["age"],
        bins=[0, 12, 18, 35, 60, np.inf],
        labels=[
            "child",
            "teen",
            "young_adult",
            "adult",
            "senior",
        ],
    )

    data["fare_group"] = pd.qcut(
        data["fare"],
        q=4,
        labels=[
            "low",
            "medium",
            "high",
            "very_high",
        ],
    )

    def to_transaction(row):
        items = [
            f"pclass={row['pclass']}",
            f"sex={row['sex']}",
            f"embarked={row['embarked']}",
            f"alone={row['alone']}",
        ]

        if pd.notna(row["age_group"]):
            items.append(
                f"age_group={row['age_group']}"
            )

        if pd.notna(row["fare_group"]):
            items.append(
                f"fare_group={row['fare_group']}"
            )

        return items

    return data.apply(
        to_transaction,
        axis=1,
    )


def build_binary_item_matrix(
    transactions: pd.Series,
) -> pd.DataFrame:
    """Transaction representation -> binary item matrix."""
    mlb = MultiLabelBinarizer()

    X = mlb.fit_transform(
        transactions
    )

    return pd.DataFrame(
        X,
        index=transactions.index,
        columns=mlb.classes_,
    )


def build_bipartite_graph(
    transactions: pd.Series,
    *,
    n_show: int = 6,
) -> nx.Graph:
    """Transactions -> passenger-attribute bipartite graph."""
    G = nx.Graph()

    for i in range(min(n_show, len(transactions))):
        passenger = f"Passenger {i}"

        G.add_node(
            passenger,
            node_type="passenger",
        )

        for item in transactions.iloc[i]:
            G.add_node(
                item,
                node_type="attribute",
            )

            G.add_edge(
                passenger,
                item,
            )

    return G
