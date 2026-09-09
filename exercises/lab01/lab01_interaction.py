"""
lab01_interaction.py

Helper functions for Lab 01 — Interaction Data.

Design rule
-----------
- .py  : load data and construct representations
- .qmd : inspect returned objects, visualize them, and interpret them

Dataset
-------
MovieLens 100K (GroupLens, University of Minnesota)
100,000 ratings (1-5) from 943 users on 1,682 movies.

Place the unzipped files under the shared project ``data/`` folder:

    data/interaction/Movielens/u.data
    data/interaction/Movielens/u.item
    data/interaction/Movielens/u.user

Source: https://grouplens.org/datasets/movielens/100k/
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


RANDOM_STATE = 42

# exercises/lab01/thisfile.py → parents[2] is the project root
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = _PROJECT_ROOT / "data" / "interaction" / "Movielens"

ML100K_PAGE = "https://grouplens.org/datasets/movielens/100k/"

DOWNLOAD_HELP = f"""
MovieLens 100K was not found. Download it once, then re-run.

  1. Open

         {ML100K_PAGE}

  2. Download 'ml-100k.zip' (about 5 MB).
     If the browser shows a security warning, choose Advanced -> Proceed.

  3. Unzip it and put the files here:

         {{target}}

     u.data, u.item and u.user must be directly inside that folder
     (not nested one level deeper).

MovieLens is free for research and educational use, but redistribution
requires separate permission, so the data is not shipped with this lab.
"""


def movielens_dir(*, data_dir: Optional[Path | str] = None) -> Path:
    """Return the MovieLens folder, or explain how to download it."""
    target = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR

    if not (target / "u.data").exists():
        raise FileNotFoundError(DOWNLOAD_HELP.format(target=target))

    return target


def _resolve(data_dir: Optional[Path | str], filename: str) -> Path:
    """Return the path to a MovieLens file."""
    return movielens_dir(data_dir=data_dir) / filename

ML100K_GENRES = (
    "unknown",
    "Action",
    "Adventure",
    "Animation",
    "Children's",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western",
)


def load_movielens_100k(
    *,
    data_dir: Optional[Path | str] = None,
    min_user_ratings: int = 0,
    min_item_ratings: int = 0,
) -> pd.DataFrame:
    """Load the rating log and return one row per (user, item) interaction."""
    df = pd.read_csv(
        _resolve(data_dir, "u.data"),
        sep="\t",
        names=["user_id", "item_id", "rating", "timestamp"],
        engine="python",
    )

    if min_item_ratings > 0:
        keep = df["item_id"].value_counts()
        df = df[df["item_id"].isin(keep[keep >= min_item_ratings].index)]

    if min_user_ratings > 0:
        keep = df["user_id"].value_counts()
        df = df[df["user_id"].isin(keep[keep >= min_user_ratings].index)]

    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

    return df.reset_index(drop=True)


def load_movies(*, data_dir: Optional[Path | str] = None) -> pd.DataFrame:
    """Load movie metadata, returning one row per item with a genre list."""
    columns = ["item_id", "title", "release_date", "video_release", "imdb_url"]
    columns += list(ML100K_GENRES)

    df = pd.read_csv(
        _resolve(data_dir, "u.item"),
        sep="|",
        names=columns,
        encoding="latin-1",
        engine="python",
    )

    flags = df[list(ML100K_GENRES)].to_numpy(dtype=bool)
    df["genres"] = [
        [g for g, on in zip(ML100K_GENRES, row) if on] for row in flags
    ]

    return df[["item_id", "title", "release_date", "genres"]]


def load_users(*, data_dir: Optional[Path | str] = None) -> pd.DataFrame:
    """Load user demographics, returning one row per user."""
    return pd.read_csv(
        _resolve(data_dir, "u.user"),
        sep="|",
        names=["user_id", "age", "gender", "occupation", "zip_code"],
        engine="python",
    )


def sample_interactions(
    ratings: pd.DataFrame,
    *,
    n_items: int = 12,
    n_users: int = 10,
    min_overlap: int = 3,
    user_col: str = "user_id",
    item_col: str = "item_id",
    random_state: int = RANDOM_STATE,
) -> pd.DataFrame:
    """Take the most-rated items and a random sample of users who rated some of them.

    Produces a block small enough to print and draw in full, while keeping the
    gaps that make the full matrix sparse.
    """
    popular = ratings[item_col].value_counts().head(n_items).index
    subset = ratings[ratings[item_col].isin(popular)]

    counts = subset[user_col].value_counts()
    eligible = counts[(counts >= min_overlap) & (counts < n_items)].index

    rng = np.random.default_rng(random_state)
    chosen = rng.choice(eligible, size=min(n_users, len(eligible)), replace=False)
    subset = subset[subset[user_col].isin(chosen)]

    return subset.sort_values([user_col, item_col]).reset_index(drop=True)


def build_utility_matrix(
    ratings: pd.DataFrame,
    *,
    user_col: str = "user_id",
    item_col: str = "item_id",
    value_col: Optional[str] = "rating",
) -> tuple[sparse.csr_matrix, np.ndarray, np.ndarray]:
    """Construct a sparse user-item utility matrix from an interaction log."""
    users = np.sort(ratings[user_col].unique())
    items = np.sort(ratings[item_col].unique())

    user_pos = pd.Series(np.arange(len(users)), index=users)
    item_pos = pd.Series(np.arange(len(items)), index=items)

    rows = user_pos.loc[ratings[user_col]].to_numpy()
    cols = item_pos.loc[ratings[item_col]].to_numpy()
    vals = (
        np.ones(len(ratings), dtype=float)
        if value_col is None
        else ratings[value_col].to_numpy(dtype=float)
    )

    X = sparse.csr_matrix(
        (vals, (rows, cols)),
        shape=(len(users), len(items)),
    )

    return X, users, items


def binarize_utility_matrix(
    X: sparse.spmatrix,
    *,
    threshold: float = 4.0,
) -> sparse.csr_matrix:
    """Keep only interactions at or above ``threshold`` and set their value to 1."""
    X = sparse.csr_matrix(X, copy=True)
    X.data = (X.data >= threshold).astype(float)
    X.eliminate_zeros()
    return X


def matrix_density(X: sparse.spmatrix) -> float:
    """Return the fraction of observed entries in a sparse matrix."""
    n_rows, n_cols = X.shape
    return float(X.nnz) / float(n_rows * n_cols)


def build_bipartite_graph(
    ratings: pd.DataFrame,
    *,
    user_col: str = "user_id",
    item_col: str = "item_id",
    weight_col: Optional[str] = "rating",
    titles: Optional[pd.Series] = None,
    n_users: Optional[int] = 30,
    random_state: int = RANDOM_STATE,
) -> nx.Graph:
    """Construct a bipartite user-item graph from an interaction log."""
    if n_users is not None:
        rng = np.random.default_rng(random_state)
        chosen = rng.choice(
            ratings[user_col].unique(),
            size=min(n_users, ratings[user_col].nunique()),
            replace=False,
        )
        ratings = ratings[ratings[user_col].isin(chosen)]

    G = nx.Graph()

    for user in ratings[user_col].unique():
        G.add_node(f"u{user}", bipartite=0, kind="user", label=f"u{user}")

    for item in ratings[item_col].unique():
        title = None if titles is None else titles.get(item)
        G.add_node(
            f"i{item}",
            bipartite=1,
            kind="item",
            label=str(title) if title is not None else f"i{item}",
        )

    for row in ratings.itertuples(index=False):
        weight = 1.0 if weight_col is None else float(getattr(row, weight_col))
        G.add_edge(
            f"u{getattr(row, user_col)}",
            f"i{getattr(row, item_col)}",
            weight=weight,
        )

    return G


def biadjacency_matrix(
    G: nx.Graph,
    *,
    weight: Optional[str] = "weight",
) -> tuple[sparse.csr_matrix, list[str], list[str]]:
    """Return the users x items block of a bipartite graph's adjacency matrix."""
    users = sorted(n for n, d in G.nodes(data=True) if d.get("bipartite") == 0)
    items = sorted(n for n, d in G.nodes(data=True) if d.get("bipartite") == 1)

    B = nx.bipartite.biadjacency_matrix(
        G,
        row_order=users,
        column_order=items,
        weight=weight,
    )

    return sparse.csr_matrix(B), users, items


def project_onto_users(
    G: nx.Graph,
    *,
    min_shared: int = 1,
) -> nx.Graph:
    """Fold a bipartite graph into a user-user graph weighted by shared items."""
    users = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 0]
    P = nx.bipartite.weighted_projected_graph(G, users)

    if min_shared > 1:
        weak = [
            (u, v)
            for u, v, d in P.edges(data=True)
            if d.get("weight", 0) < min_shared
        ]
        P.remove_edges_from(weak)

    return P


def compute_item_similarity(
    X: sparse.spmatrix,
    *,
    query_index: Optional[int] = None,
):
    """Compute item-item cosine similarity from a user-item matrix."""
    X_items = sparse.csr_matrix(X).T.tocsr()

    if query_index is None:
        return cosine_similarity(X_items)
    return cosine_similarity(X_items[query_index], X_items).ravel()


def build_item_knn_graph(
    X: sparse.spmatrix,
    *,
    item_ids: Optional[Sequence[int]] = None,
    titles: Optional[pd.Series] = None,
    k: int = 3,
    max_items: int = 80,
) -> nx.Graph:
    """Construct a k-nearest-neighbor item graph using cosine similarity.

    Restricted to the ``max_items`` most-interacted items, so that the graph
    is built from columns that actually have enough signal to compare.
    """
    X_items = sparse.csr_matrix(X).T.tocsr()

    if item_ids is None:
        item_ids = np.arange(X_items.shape[0])
    item_ids = np.asarray(item_ids)

    popularity = np.asarray((X_items > 0).sum(axis=1)).ravel()
    keep = np.argsort(popularity)[::-1][:max_items]
    keep = np.sort(keep)

    X_items = X_items[keep]
    item_ids = item_ids[keep]
    n_items = X_items.shape[0]

    if n_items == 0:
        return nx.Graph()

    G = nx.Graph()
    for i in range(n_items):
        item_id = item_ids[i]
        title = None if titles is None else titles.get(item_id)
        G.add_node(
            i,
            item_id=int(item_id),
            title=str(title) if title is not None else str(item_id),
        )

    model = NearestNeighbors(
        n_neighbors=min(k + 1, n_items),
        metric="cosine",
    )
    model.fit(X_items)
    distances, indices = model.kneighbors(X_items)

    for i in range(n_items):
        for distance, j in zip(distances[i, 1:], indices[i, 1:]):
            similarity = 1.0 - float(distance)
            G.add_edge(i, int(j), weight=similarity)

    return G
