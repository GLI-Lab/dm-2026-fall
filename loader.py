"""Locate, download, and load original course datasets under data/.

Lab helpers import these functions and then construct representations.
"""

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd


DATA_ROOT = Path(__file__).resolve().parent
LAB_DATA_ROOT = DATA_ROOT.parent / "exercises" / "lab01" / "data"

MOVIELENS_FILES = ("u.data", "u.item", "u.user")
MOVIELENS_DIR = DATA_ROOT / "interaction" / "Movielens"
MOVIELENS_HANDLE = "trishna8/movielens-100k-dataset"
MOVIELENS_PAGE = f"https://www.kaggle.com/datasets/{MOVIELENS_HANDLE}"

GROCERIES_ARULES_NAME = "groceries.csv"
GROCERIES_ARULES_URL = (
    "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/groceries.csv"
)
GROCERIES_RAW_NAME = "groceries_kaggle(raw).csv"
GROCERIES_BASKET_NAME = "groceries_kaggle.csv"
GROCERIES_DOWNLOAD_NAME = "Groceries_dataset.csv"
GROCERIES_DIR = DATA_ROOT / "transaction"
GROCERIES_HANDLE = "heeraldedhia/groceries-dataset"
GROCERIES_PAGE = f"https://www.kaggle.com/datasets/{GROCERIES_HANDLE}"
GROCERIES_LONG_COLUMNS = {"Member_number", "Date", "itemDescription"}

TITANIC_CSV = DATA_ROOT / "record" / "titanic.csv"
IRIS_CSV = DATA_ROOT / "record" / "iris.csv"
TEXT_DIR = DATA_ROOT / "text" / "20newsgroups"
KARATE_DIR = DATA_ROOT / "graph" / "karate"
KARATE_NODES = KARATE_DIR / "nodes.csv"
KARATE_EDGES = KARATE_DIR / "edges.csv"
CORA_DIR = DATA_ROOT / "graph" / "cora"
CORA_NODES = CORA_DIR / "nodes.csv"
CORA_EDGES = CORA_DIR / "edges.csv"
CORA_PAGE = "https://graphsandnetworks.com/the-cora-dataset/"
CORA_NODES_URL = "https://temprl.com/nodes.csv"
CORA_EDGES_URL = "https://temprl.com/edges.csv"

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


def _kaggle_download(handle: str, page: str, filename: str) -> Path:
    try:
        import kagglehub
    except ImportError as exc:
        raise FileNotFoundError(
            f"{filename} is missing and kagglehub is not installed.\n{page}"
        ) from exc

    try:
        downloaded = Path(kagglehub.dataset_download(handle))
    except Exception as exc:
        raise FileNotFoundError(
            f"Could not download {handle} with kagglehub.\n{exc}\n{page}"
        ) from exc

    matches = list(downloaded.rglob(filename))
    if not matches:
        raise FileNotFoundError(
            f"Downloaded {handle} to {downloaded} but {filename} was not inside.\n{page}"
        )
    return matches[0]


def _has_movielens_files(folder: Path) -> bool:
    return folder.is_dir() and all((folder / name).is_file() for name in MOVIELENS_FILES)


def _find_in_tree(root: Path, *, max_depth: int = 3) -> Optional[Path]:
    if not root.is_dir():
        return None
    if _has_movielens_files(root):
        return root
    if max_depth <= 0:
        return None
    try:
        children = sorted(
            p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
        )
    except OSError:
        return None
    for child in children:
        found = _find_in_tree(child, max_depth=max_depth - 1)
        if found is not None:
            return found
    return None


def _search_roots(*folders: Optional[Path]) -> list[Path]:
    roots: list[Path] = []
    for folder in folders:
        if folder is not None and folder not in roots:
            roots.append(folder)
    return roots


def ensure_movielens(*, data_dir: Optional[Path | str] = None) -> Path:
    """Return the MovieLens folder, downloading it into data/interaction/ if needed."""
    roots = _search_roots(
        Path(data_dir) if data_dir is not None else None,
        MOVIELENS_DIR.parent,
        LAB_DATA_ROOT / "interaction",
    )

    for root in roots:
        found = _find_in_tree(root)
        if found is not None:
            return found

    src = _kaggle_download(MOVIELENS_HANDLE, MOVIELENS_PAGE, "u.data").parent
    found = _find_in_tree(src, max_depth=4)
    if found is None:
        raise FileNotFoundError(
            f"Downloaded MovieLens files were not found under {src}.\n{MOVIELENS_PAGE}"
        )
    MOVIELENS_DIR.mkdir(parents=True, exist_ok=True)
    for name in MOVIELENS_FILES:
        shutil.copy2(found / name, MOVIELENS_DIR / name)
    return MOVIELENS_DIR


movielens_dir = ensure_movielens


def _movielens_file(filename: str, *, data_dir: Optional[Path | str] = None) -> Path:
    return ensure_movielens(data_dir=data_dir) / filename


def load_movielens_100k(
    *,
    data_dir: Optional[Path | str] = None,
    min_user_ratings: int = 0,
    min_item_ratings: int = 0,
) -> pd.DataFrame:
    """Load the rating log and return one row per (user, item) interaction."""
    df = pd.read_csv(
        _movielens_file("u.data", data_dir=data_dir),
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
        _movielens_file("u.item", data_dir=data_dir),
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
        _movielens_file("u.user", data_dir=data_dir),
        sep="|",
        names=["user_id", "age", "gender", "occupation", "zip_code"],
        engine="python",
    )


def _groceries_search_dirs() -> list[Path]:
    return _search_roots(GROCERIES_DIR, LAB_DATA_ROOT / "transaction")


def ensure_groceries() -> Path:
    """Return the arules Groceries CSV, downloading it from GitHub if missing."""
    for folder in _groceries_search_dirs():
        path = folder / GROCERIES_ARULES_NAME
        if path.is_file():
            return path

    import urllib.request

    GROCERIES_DIR.mkdir(parents=True, exist_ok=True)
    dest = GROCERIES_DIR / GROCERIES_ARULES_NAME
    urllib.request.urlretrieve(GROCERIES_ARULES_URL, dest)
    return dest


def ensure_groceries_kaggle_raw() -> Path:
    """Download the Kaggle Groceries file into data/transaction/groceries_kaggle(raw).csv."""
    for folder in _groceries_search_dirs():
        raw_path = folder / GROCERIES_RAW_NAME
        if raw_path.is_file():
            return raw_path

    src = _kaggle_download(GROCERIES_HANDLE, GROCERIES_PAGE, GROCERIES_DOWNLOAD_NAME)
    GROCERIES_DIR.mkdir(parents=True, exist_ok=True)
    dest = GROCERIES_DIR / GROCERIES_RAW_NAME
    if src.resolve() != dest.resolve():
        shutil.copy2(src, dest)
    return dest


def _group_kaggle_long(raw: pd.DataFrame) -> list[list[str]]:
    grouped = (
        raw.groupby(["Member_number", "Date"], sort=False)["itemDescription"]
        .apply(lambda s: [x for x in dict.fromkeys(s.dropna().astype(str).str.strip()) if x])
        .tolist()
    )
    return [items for items in grouped if items]


def _write_baskets(baskets: list[list[str]], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for items in baskets:
            writer.writerow(items)
    return dest


def ensure_groceries_kaggle() -> Path:
    """Group the Kaggle raw file by (Member_number, Date) into groceries_kaggle.csv."""
    for folder in _groceries_search_dirs():
        basket = folder / GROCERIES_BASKET_NAME
        if basket.is_file():
            return basket

    raw_path = ensure_groceries_kaggle_raw()
    raw = pd.read_csv(raw_path)
    if not GROCERIES_LONG_COLUMNS.issubset(raw.columns):
        raise ValueError(f"{raw_path} is not the Kaggle Groceries long-format file.")

    dest = GROCERIES_DIR / GROCERIES_BASKET_NAME
    return _write_baskets(_group_kaggle_long(raw), dest)


def groceries_csv(path: Optional[Path | str] = None) -> Path:
    """Return a Groceries file path, preparing the Kaggle baskets if needed."""
    if path is not None:
        target = Path(path)
        if target.is_file():
            return target
    return ensure_groceries_kaggle()


def load_groceries(path: Optional[str | Path] = None) -> pd.DataFrame:
    """Load Groceries and return one row per transaction."""
    path = groceries_csv(path)

    try:
        raw = pd.read_csv(path)
        if GROCERIES_LONG_COLUMNS.issubset(raw.columns):
            grouped = (
                raw.groupby(["Member_number", "Date"], sort=False)["itemDescription"]
                .apply(lambda s: list(dict.fromkeys(s.dropna().astype(str))))
                .reset_index()
            )
            grouped["transaction_id"] = [
                f"txn_{i:05d}" for i in range(len(grouped))
            ]
            grouped = grouped.rename(columns={"itemDescription": "items"})
            return grouped[["transaction_id", "items"]]
    except Exception:
        pass

    transactions = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            items = [
                item.strip()
                for item in row
                if item is not None and item.strip() != ""
            ]
            if items:
                transactions.append(items)

    if not transactions:
        raise ValueError(f"No transactions could be read from: {path}")

    return pd.DataFrame(
        {
            "transaction_id": [f"txn_{i:05d}" for i in range(len(transactions))],
            "items": transactions,
        }
    )


def load_titanic() -> pd.DataFrame:
    """Load Titanic from data/record/titanic.csv, downloading via seaborn if missing."""
    if TITANIC_CSV.is_file():
        return pd.read_csv(TITANIC_CSV)

    import seaborn as sns

    df = sns.load_dataset("titanic")
    TITANIC_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(TITANIC_CSV, index=False)
    return df


def load_iris() -> pd.DataFrame:
    """Load Iris from data/record/iris.csv, writing sklearn's table if missing."""
    if IRIS_CSV.is_file():
        return pd.read_csv(IRIS_CSV)

    from sklearn.datasets import load_iris as _sklearn_iris

    bunch = _sklearn_iris(as_frame=True)
    df = bunch.frame.copy()
    df["species"] = df["target"].map(dict(enumerate(bunch.target_names)))
    df = df.drop(columns=["target"])
    IRIS_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(IRIS_CSV, index=False)
    return df


def load_20newsgroups(
    *,
    root: str | Path | None = None,
    categories: Optional[Sequence[str]] = None,
    subset: str = "train",
    remove: Sequence[str] = ("headers", "footers", "quotes"),
    random_state: int = 42,
    download_if_missing: bool = True,
) -> pd.DataFrame:
    """Load 20 Newsgroups and cache the dataset under data/text/20newsgroups."""
    from sklearn.datasets import fetch_20newsgroups

    root = Path(root) if root is not None else TEXT_DIR
    root.mkdir(parents=True, exist_ok=True)

    data = fetch_20newsgroups(
        data_home=root,
        subset=subset,
        categories=list(categories) if categories is not None else None,
        remove=tuple(remove),
        shuffle=True,
        random_state=random_state,
        download_if_missing=download_if_missing,
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
    df = df.reset_index(drop=True)
    df.insert(0, "doc_id", [f"20ng_{i:04d}" for i in range(len(df))])
    return df[["doc_id", "label", "text"]]


def ensure_karate() -> Path:
    """Write Zachary's Karate Club under data/graph/karate/ if the files are missing."""
    if KARATE_NODES.is_file() and KARATE_EDGES.is_file():
        return KARATE_DIR

    import networkx as nx

    G = nx.karate_club_graph()
    KARATE_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [{"node": n, "club": d["club"]} for n, d in G.nodes(data=True)]
    ).to_csv(KARATE_NODES, index=False)
    pd.DataFrame(
        [{"source": u, "target": v} for u, v in G.edges()]
    ).to_csv(KARATE_EDGES, index=False)
    return KARATE_DIR


def load_karate():
    """Load Zachary's Karate Club from data/graph/karate/, creating the files if needed."""
    import networkx as nx

    ensure_karate()
    nodes = pd.read_csv(KARATE_NODES)
    edges = pd.read_csv(KARATE_EDGES)
    G = nx.Graph()
    for row in nodes.itertuples(index=False):
        G.add_node(int(row.node), club=str(row.club))
    for row in edges.itertuples(index=False):
        G.add_edge(int(row.source), int(row.target))
    return G


def _http_download(url: str, dest: Path) -> Path:
    import urllib.request

    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    return dest


def ensure_cora() -> Path:
    """Download Cora nodes.csv and edges.csv from temprl.com if missing."""
    if CORA_NODES.is_file() and CORA_EDGES.is_file():
        return CORA_DIR
    _http_download(CORA_NODES_URL, CORA_NODES)
    _http_download(CORA_EDGES_URL, CORA_EDGES)
    return CORA_DIR


def load_cora():
    """Load Cora as a directed citation graph with a subject on each paper."""
    import networkx as nx

    ensure_cora()
    nodes = pd.read_csv(CORA_NODES, index_col=0)
    edges = pd.read_csv(CORA_EDGES, index_col=0)
    G = nx.DiGraph()
    for row in nodes.itertuples(index=False):
        G.add_node(int(row.nodeId), subject=str(row.subject))
    for row in edges.itertuples(index=False):
        G.add_edge(int(row.sourceNodeId), int(row.targetNodeId))
    return G


def check_datasets(*, download: bool = True) -> pd.DataFrame:
    """Load every course dataset and return a status table.

    If the files are already under data/, nothing is downloaded.
    Pass download=False to report missing files instead of fetching them.
    """
    rows: list[dict[str, object]] = []

    def add(
        kind: str,
        name: str,
        path: Path | str,
        *,
        local: bool,
        source: str,
        status: str,
        detail: str,
    ) -> None:
        rows.append(
            {
                "type": kind,
                "dataset": name,
                "path": str(path),
                "local": local,
                "source": source,
                "status": status,
                "detail": detail,
            }
        )

    def run(kind: str, name: str, path: Path, source: str, local: bool, load) -> None:
        if not local and not download:
            add(kind, name, path, local=False, source=source, status="missing",
                detail="Not on disk; re-run with download=True.")
            return
        try:
            detail = load()
            add(kind, name, path, local=local, source=source, status="ok", detail=detail)
        except Exception as exc:
            add(kind, name, path, local=local, source=source, status="error", detail=str(exc))

    titanic_local = TITANIC_CSV.is_file()
    run(
        "record", "Titanic", TITANIC_CSV,
        "seaborn (sns.load_dataset) if missing",
        titanic_local,
        lambda: f"{load_titanic().shape[0]} rows × {load_titanic().shape[1]} columns",
    )

    iris_local = IRIS_CSV.is_file()
    run(
        "record", "Iris", IRIS_CSV,
        "sklearn.datasets.load_iris if missing",
        iris_local,
        lambda: f"{load_iris().shape[0]} rows × {load_iris().shape[1]} columns",
    )

    text_local = TEXT_DIR.is_dir() and any(TEXT_DIR.rglob("*.pkz"))
    def _load_text() -> str:
        df = load_20newsgroups(
            categories=["sci.space"],
            download_if_missing=download,
        )
        return f"{df.shape[0]} documents (sci.space sample)"
    run(
        "text", "20 Newsgroups", TEXT_DIR,
        "sklearn.datasets.fetch_20newsgroups",
        text_local,
        _load_text,
    )

    karate_local = KARATE_NODES.is_file() and KARATE_EDGES.is_file()
    run(
        "graph", "Zachary's Karate Club", KARATE_DIR,
        "networkx.karate_club_graph if missing",
        karate_local,
        lambda: f"{load_karate().number_of_nodes()} nodes, {load_karate().number_of_edges()} edges",
    )

    cora_local = CORA_NODES.is_file() and CORA_EDGES.is_file()
    run(
        "graph", "Cora", CORA_DIR,
        CORA_PAGE,
        cora_local,
        lambda: f"{load_cora().number_of_nodes()} nodes, {load_cora().number_of_edges()} edges",
    )

    ml_dir = _find_in_tree(MOVIELENS_DIR.parent) or _find_in_tree(LAB_DATA_ROOT / "interaction")
    run(
        "interaction", "MovieLens 100K", ml_dir or MOVIELENS_DIR,
        f"kagglehub:{MOVIELENS_HANDLE}",
        ml_dir is not None,
        lambda: (
            f"{len(load_movielens_100k())} ratings, "
            f"{len(load_movies())} movies, {len(load_users())} users"
        ),
    )

    arules_path = next(
        (folder / GROCERIES_ARULES_NAME for folder in _groceries_search_dirs()
         if (folder / GROCERIES_ARULES_NAME).is_file()),
        GROCERIES_DIR / GROCERIES_ARULES_NAME,
    )
    run(
        "transaction", "Groceries (arules)", arules_path,
        GROCERIES_ARULES_URL,
        arules_path.is_file(),
        lambda: f"{len(load_groceries(ensure_groceries() if download else arules_path))} baskets",
    )

    raw_path = next(
        (folder / GROCERIES_RAW_NAME for folder in _groceries_search_dirs()
         if (folder / GROCERIES_RAW_NAME).is_file()),
        GROCERIES_DIR / GROCERIES_RAW_NAME,
    )
    run(
        "transaction", "Groceries Kaggle (raw)", raw_path,
        f"kagglehub:{GROCERIES_HANDLE}",
        raw_path.is_file(),
        lambda: f"{len(pd.read_csv(ensure_groceries_kaggle_raw() if download else raw_path))} item rows",
    )

    basket_path = next(
        (folder / GROCERIES_BASKET_NAME for folder in _groceries_search_dirs()
         if (folder / GROCERIES_BASKET_NAME).is_file()),
        GROCERIES_DIR / GROCERIES_BASKET_NAME,
    )
    run(
        "transaction", "Groceries Kaggle (baskets)", basket_path,
        "grouped from groceries_kaggle(raw).csv by Member_number, Date",
        basket_path.is_file(),
        lambda: f"{len(load_groceries(ensure_groceries_kaggle() if download else basket_path))} baskets",
    )

    result = pd.DataFrame(rows)
    return result

