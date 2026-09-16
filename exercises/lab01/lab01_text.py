"""
lab01_text.py

Helper functions for Lab 01-2 — Text Data.

Original 20 Newsgroups documents are loaded by data.loader.
This helper constructs representations from the loaded documents.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

import networkx as nx
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


RANDOM_STATE = 42


def tokenize_documents(texts: Iterable[str]) -> list[list[str]]:
    """Convert documents into ordered token sequences using Gensim."""
    try:
        from gensim.utils import simple_preprocess
    except ImportError as exc:
        raise ImportError("tokenize_documents() requires gensim.") from exc

    return [simple_preprocess(str(text), deacc=True) for text in texts]


def build_count_matrix(
    texts: Iterable[str],
    **kwargs,
) -> tuple[sparse.csr_matrix, CountVectorizer]:
    """Construct a sparse document-term count matrix."""
    vectorizer = CountVectorizer(
        **kwargs
    )

    X = vectorizer.fit_transform(list(texts)).tocsr()
    return X, vectorizer


def build_tfidf_matrix(
    texts: Iterable[str],
    **kwargs,
) -> tuple[sparse.csr_matrix, TfidfVectorizer]:
    """Construct a sparse TF-IDF document-term matrix."""
    vectorizer = TfidfVectorizer(
        **kwargs
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


def categorical_node_colors(
    G: nx.Graph,
    attribute: str = "label",
):
    """
    Convert categorical node attributes into numeric color indices.

    This is a visualization helper, not part of graph construction.
    """

    values = [
        G.nodes[node].get(attribute)
        for node in G.nodes
    ]

    return pd.Categorical(values).codes