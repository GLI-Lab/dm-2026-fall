"""
lab01_graph.py

Helper functions for Lab 01 — Graph Data.

Design rule
-----------
- .py  : load data and construct representations
- .qmd : inspect returned objects, visualize them, and interpret them

Datasets
--------
Zachary's Karate Club (34 nodes, NetworkX built-in)
Cora citation network (2,708 nodes, PyTorch Geometric)
ogbn-arxiv citation network (169,343 nodes, Open Graph Benchmark)

Notes
-----
Cora and ogbn-arxiv require extra packages::

    pip install torch torch_geometric ogb

The first call downloads each dataset (about 1-2 minutes).
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

# exercises/lab01/thisfile.py → parents[2] is the project root
_PROJECT_ROOT = Path(__file__).resolve().parents[2]


RANDOM_STATE = 42


def _allow_pyg_globals() -> None:
    """Allowlist PyG classes for torch.load (required since PyTorch 2.6).

    PyTorch 2.6 changed the default of ``torch.load`` to weights-only safe
    mode, which rejects the PyG classes used inside saved dataset files.
    """
    try:
        import torch
        from torch_geometric.data.data import DataEdgeAttr, DataTensorAttr
        from torch_geometric.data.storage import GlobalStorage
    except ImportError as exc:
        raise ImportError(
            "Loading Cora / ogbn-arxiv requires torch and torch_geometric. "
            "Install them with: pip install torch torch_geometric"
        ) from exc

    torch.serialization.add_safe_globals(
        [DataEdgeAttr, DataTensorAttr, GlobalStorage]
    )


def load_karate() -> nx.Graph:
    """Load Zachary's Karate Club graph (34 nodes, 78 edges)."""
    return nx.karate_club_graph()


def build_edge_list(
    G: nx.Graph,
) -> pd.DataFrame:
    """Graph -> edge-list representation."""
    return pd.DataFrame(
        G.edges(),
        columns=["source", "target"],
    )


def build_adjacency_list(
    G: nx.Graph,
) -> dict:
    """Graph -> adjacency-list representation."""
    return {
        node: list(G.neighbors(node))
        for node in G.nodes()
    }


def adjacency(
    G: nx.Graph,
) -> np.ndarray:
    """Graph -> binary adjacency matrix (nodes x nodes)."""
    return nx.to_numpy_array(
        G,
        weight=None,
        dtype=int,
    )


def load_cora(
    *,
    root: str = str(_PROJECT_ROOT / "data" / "graph" / "Cora"),
):
    """Load the Cora citation network.

    Returns
    -------
    (dataset, data) : PyG ``Planetoid`` dataset and its single graph object.
    """
    _allow_pyg_globals()
    from torch_geometric.datasets import Planetoid

    dataset = Planetoid(
        root=root,
        name="Cora",
    )

    return dataset, dataset[0]


def load_arxiv(
    *,
    root: str = str(_PROJECT_ROOT / "data" / "graph" / "OGB"),
):
    """Load the ogbn-arxiv citation network.

    Returns
    -------
    (dataset, data) : OGB node-property-prediction dataset and its graph.
    """
    _allow_pyg_globals()

    try:
        from ogb.nodeproppred import PygNodePropPredDataset
    except ImportError as exc:
        raise ImportError(
            "load_arxiv() requires ogb. Install it with: pip install ogb"
        ) from exc

    dataset = PygNodePropPredDataset(
        name="ogbn-arxiv",
        root=root,
    )

    return dataset, dataset[0]


def to_networkx_undirected(
    data,
) -> nx.Graph:
    """Convert a PyG graph object into an undirected NetworkX graph."""
    import torch_geometric.utils as pyg_utils

    return pyg_utils.to_networkx(
        data,
        to_undirected=True,
    )


def largest_component(
    G: nx.Graph,
) -> nx.Graph:
    """Return the subgraph induced by the largest connected component.

    Useful for whole-graph layouts of networks like Cora, where many small
    disconnected fragments would otherwise clutter the drawing.
    """
    largest_cc = max(
        nx.connected_components(G),
        key=len,
    )

    return G.subgraph(largest_cc)


def khop_subgraph(
    data,
    *,
    center: int = 0,
    hops: int = 2,
) -> tuple[nx.Graph, list]:
    """Extract the k-hop neighborhood of one node as a NetworkX graph.

    ``hops=2`` keeps the center node, its neighbors, and their neighbors
    ("friends of friends"), so a huge graph can be inspected locally.

    Returns
    -------
    (G_sub, labels) : the subgraph and per-node class labels for coloring.
    """
    from torch_geometric.utils import k_hop_subgraph

    sub_nodes, sub_edge_index, _, _ = k_hop_subgraph(
        center,
        hops,
        data.edge_index,
        relabel_nodes=True,
    )

    G_sub = nx.Graph()
    G_sub.add_nodes_from(
        range(sub_nodes.size(0))
    )
    G_sub.add_edges_from(
        sub_edge_index.t().tolist()
    )

    labels = data.y[
        sub_nodes
    ].squeeze().tolist()

    return G_sub, labels
