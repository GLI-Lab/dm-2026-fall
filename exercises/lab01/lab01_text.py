"""
lab01_text.py

Helper functions for Lab 01 — Text Data.

Design rule
-----------
- .py  : load data and construct representations
- .qmd : inspect returned objects, visualize them, and interpret them

Dataset
-------
20 Newsgroups
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

import networkx as nx
import pandas as pd
from scipy import sparse
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from pathlib import Path

# exercises/lab01/thisfile.py → parents[2] is the project root
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_20NG_ROOT = _PROJECT_ROOT / "data" / "text" / "20newsgroups"


RANDOM_STATE = 42

DEFAULT_20NG_CATEGORIES = (
    "comp.graphics",
    "misc.forsale",
    "rec.sport.baseball",
    "sci.space",
)


def load_20newsgroups(
    *,
    root: str | Path = DEFAULT_20NG_ROOT,
    categories: Optional[Sequence[str]] = DEFAULT_20NG_CATEGORIES,
    subset: str = "train",
    n_per_class: Optional[int] = 100,
    remove: Sequence[str] = ("headers", "footers", "quotes"),
    random_state: int = RANDOM_STATE,
) -> pd.DataFrame:
    """Load 20 Newsgroups and cache the dataset under ``root``."""

    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)

    data = fetch_20newsgroups(
        data_home=root,
        subset=subset,
        categories=list(categories) if categories is not None else None,
        remove=tuple(remove),
        shuffle=True,
        random_state=random_state,
        download_if_missing=True,
    )

    label_names = dict(enumerate(data.target_names))

    df = pd.DataFrame(
        {
            "text": data.data,
            "label": [label_names[i] for i in data.target],
        }
    )

    df["text"] = df["text"].fillna("").astype(str)
    df = df[df["text"].str.strip().str.len() > 0].copy()

    if n_per_class is not None:
        sampled = []
        for _, group in df.groupby("label", sort=True):
            sampled.append(
                group.sample(
                    n=min(n_per_class, len(group)),
                    random_state=random_state,
                )
            )

        df = pd.concat(sampled, ignore_index=True)

    df = df.sample(
        frac=1.0,
        random_state=random_state,
    ).reset_index(drop=True)

    df.insert(
        0,
        "doc_id",
        [f"20ng_{i:04d}" for i in range(len(df))],
    )

    return df[["doc_id", "label", "text"]]


def tokenize_documents(texts: Iterable[str]) -> list[list[str]]:
    """Convert documents into ordered token sequences using Gensim."""
    try:
        from gensim.utils import simple_preprocess
    except ImportError as exc:
        raise ImportError("tokenize_documents() requires gensim.") from exc

    return [simple_preprocess(str(text), deacc=True) for text in texts]


def build_count_matrix(
    texts: Iterable[str],
    *,
    max_features: Optional[int] = 3000,
    min_df: int | float = 2,
    max_df: int | float = 0.95,
    stop_words: Optional[str | Sequence[str]] = "english",
    ngram_range: tuple[int, int] = (1, 1),
) -> tuple[sparse.csr_matrix, CountVectorizer]:
    """Construct a sparse document-term count matrix."""
    vectorizer = CountVectorizer(
        max_features=max_features,
        min_df=min_df,
        max_df=max_df,
        stop_words=stop_words,
        ngram_range=ngram_range,
    )
    X = vectorizer.fit_transform(list(texts)).tocsr()
    return X, vectorizer


def build_tfidf_matrix(
    texts: Iterable[str],
    *,
    max_features: Optional[int] = 3000,
    min_df: int | float = 2,
    max_df: int | float = 0.95,
    stop_words: Optional[str | Sequence[str]] = "english",
    ngram_range: tuple[int, int] = (1, 1),
) -> tuple[sparse.csr_matrix, TfidfVectorizer]:
    """Construct a sparse TF-IDF document-term matrix."""
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        min_df=min_df,
        max_df=max_df,
        stop_words=stop_words,
        ngram_range=ngram_range,
    )
    X = vectorizer.fit_transform(list(texts)).tocsr()
    return X, vectorizer


def compute_cosine_similarity(
    X: sparse.spmatrix,
    *,
    query_index: Optional[int] = None,
):
    """Compute pairwise cosine similarity or one query-to-all similarity vector."""
    if query_index is None:
        return cosine_similarity(X)
    return cosine_similarity(X[query_index], X).ravel()


def build_similarity_graph(
    X: sparse.spmatrix,
    *,
    doc_ids: Optional[Sequence[str]] = None,
    labels: Optional[Sequence[str]] = None,
    k: int = 3,
    max_docs: int = 80,
) -> nx.Graph:
    """Construct a k-nearest-neighbor document graph using cosine similarity."""
    X = sparse.csr_matrix(X)
    n_docs = min(max_docs, X.shape[0])
    X = X[:n_docs]

    if n_docs == 0:
        return nx.Graph()

    if doc_ids is None:
        doc_ids = [f"doc_{i}" for i in range(n_docs)]
    else:
        doc_ids = list(doc_ids)[:n_docs]

    if labels is not None:
        labels = list(labels)[:n_docs]

    G = nx.Graph()
    for i in range(n_docs):
        attrs = {"doc_id": str(doc_ids[i])}
        if labels is not None:
            attrs["label"] = str(labels[i])
        G.add_node(i, **attrs)

    model = NearestNeighbors(
        n_neighbors=min(k + 1, n_docs),
        metric="cosine",
    )
    model.fit(X)
    distances, indices = model.kneighbors(X)

    for i in range(n_docs):
        for distance, j in zip(distances[i, 1:], indices[i, 1:]):
            similarity = 1.0 - float(distance)
            G.add_edge(i, int(j), weight=similarity)

    return G
