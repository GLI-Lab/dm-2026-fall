"""
lab01_record.py

Helper functions for Lab 01-1 — Record Data.

Original Titanic rows are loaded by data.loader.
This helper constructs representations and draws figures.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def fill_titanic_missing_values(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Fill missing values used in this lab."""
    data = df.copy()

    if "age" in data.columns:
        data["age"] = data["age"].fillna(
            data["age"].median()
        )

    if "embarked" in data.columns:
        data["embarked"] = data["embarked"].fillna(
            data["embarked"].mode()[0]
        )

    return data


def build_transactions(
    data: pd.DataFrame,
) -> pd.Series:
    """Convert passenger rows into transaction items."""

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


def plot_bipartite_graph(
    G: nx.Graph,
) -> None:
    """Visualize a passenger-attribute bipartite graph."""
    passenger_nodes = [
        node
        for node, data in G.nodes(data=True)
        if data["node_type"] == "passenger"
    ]

    attribute_nodes = [
        node
        for node, data in G.nodes(data=True)
        if data["node_type"] == "attribute"
    ]

    attribute_order = [
        "pclass",
        "sex",
        "embarked",
        "alone",
        "age_group",
        "fare_group",
    ]

    def attribute_key(node):
        prefix = node.split("=")[0]
        if prefix in attribute_order:
            group = attribute_order.index(prefix)
        else:
            group = len(attribute_order)
        return (group, node)

    attribute_nodes = sorted(
        attribute_nodes,
        key=attribute_key,
    )

    pos = {}

    passenger_y = np.linspace(
        0.9,
        -0.9,
        len(passenger_nodes),
    )

    for y, node in zip(
        passenger_y,
        passenger_nodes,
    ):
        pos[node] = (-0.5, y)

    attribute_y = np.linspace(
        0.95,
        -0.95,
        len(attribute_nodes),
    )

    for y, node in zip(
        attribute_y,
        attribute_nodes,
    ):
        pos[node] = (0.5, y)

    fig, ax = plt.subplots(
        figsize=(7, 5.5)
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="lightgray",
        alpha=0.6,
        ax=ax,
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=passenger_nodes,
        node_size=340,
        node_color="skyblue",
        ax=ax,
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=attribute_nodes,
        node_size=340,
        node_color="salmon",
        node_shape="s",
        ax=ax,
    )

    passenger_label_pos = {
        node: (-0.44, pos[node][1])
        for node in passenger_nodes
    }

    attribute_label_pos = {
        node: (0.44, pos[node][1])
        for node in attribute_nodes
    }

    nx.draw_networkx_labels(
        G,
        passenger_label_pos,
        labels={
            node: node
            for node in passenger_nodes
        },
        font_size=7,
        horizontalalignment="left",
        ax=ax,
    )

    nx.draw_networkx_labels(
        G,
        attribute_label_pos,
        labels={
            node: node
            for node in attribute_nodes
        },
        font_size=7,
        horizontalalignment="right",
        ax=ax,
    )

    ax.text(
        -0.5,
        1.05,
        "Passengers",
        ha="center",
        fontsize=9,
    )

    ax.text(
        0.5,
        1.05,
        "Attribute-value items",
        ha="center",
        fontsize=9,
    )

    ax.set_xlim(-0.78, 0.78)
    ax.set_ylim(-1.05, 1.1)
    ax.axis("off")

    plt.tight_layout()
    plt.show()
