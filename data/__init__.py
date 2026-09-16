"""Original course datasets live in this folder.

Use `data.loader` to locate, download, and load the source files.
"""

from data.loader import (
    DATA_ROOT,
    check_datasets,
    ensure_groceries,
    ensure_groceries_kaggle,
    ensure_groceries_kaggle_raw,
    ensure_karate,
    ensure_cora,
    ensure_movielens,
    groceries_csv,
    load_20newsgroups,
    load_cora,
    load_groceries,
    load_karate,
    load_movies,
    load_movielens_100k,
    load_titanic,
    load_users,
    movielens_dir,
)

__all__ = [
    "DATA_ROOT",
    "check_datasets",
    "ensure_groceries",
    "ensure_groceries_kaggle",
    "ensure_groceries_kaggle_raw",
    "ensure_karate",
    "ensure_cora",
    "ensure_movielens",
    "groceries_csv",
    "load_20newsgroups",
    "load_cora",
    "load_groceries",
    "load_karate",
    "load_movies",
    "load_movielens_100k",
    "load_titanic",
    "load_users",
    "movielens_dir",
]
