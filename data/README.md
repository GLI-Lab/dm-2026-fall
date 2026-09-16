# Course datasets

원본 데이터는 이 폴더에 둡니다. `data.loader`가 파일을 찾고, 없으면 받은 뒤 로드합니다.

로컬에 파일이 있으면 다시 받지 않습니다. 빠진 파일만 자동으로 받습니다.

```bash
pixi run python -m data
```

또는 Python에서:

```python
from data.loader import check_datasets
check_datasets()          # 없으면 다운로드 후 로드
check_datasets(download=False)  # 로컬만 검사
```

## 데이터 타입과 파일

| 타입 | 데이터 | 경로 | 자동 다운로드 |
|:---|:---|:---|:---|
| Record | Titanic | `record/titanic.csv` | 없으면 seaborn `sns.load_dataset("titanic")` |
| Text | 20 Newsgroups | `text/20newsgroups/` | 없으면 `sklearn.datasets.fetch_20newsgroups` |
| Graph | Zachary's Karate Club | `graph/karate/` (`nodes.csv`, `edges.csv`) | 없으면 NetworkX `karate_club_graph()`로 저장 |
| Graph | Cora | `graph/cora/` (`nodes.csv`, `edges.csv`) | 없으면 [temprl.com/nodes.csv](https://temprl.com/nodes.csv), [temprl.com/edges.csv](https://temprl.com/edges.csv) ([Cora 설명](https://graphsandnetworks.com/the-cora-dataset/)) |
| Interaction | MovieLens 100K | `interaction/Movielens/` (`u.data`, `u.item`, `u.user`) | 없으면 kagglehub [`trishna8/movielens-100k-dataset`](https://www.kaggle.com/datasets/trishna8/movielens-100k-dataset) |
| Transaction | Groceries (arules) | `transaction/groceries.csv` | 저장소에 포함. 없으면 GitHub [`stedy/Machine-Learning-with-R-datasets`](https://github.com/stedy/Machine-Learning-with-R-datasets/blob/master/groceries.csv) |
| Transaction | Groceries Kaggle (raw) | `transaction/groceries_kaggle(raw).csv` | 없으면 kagglehub [`heeraldedhia/groceries-dataset`](https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset) |
| Transaction | Groceries Kaggle (baskets) | `transaction/groceries_kaggle.csv` | raw를 `Member_number`, `Date`로 묶어 생성 |

개별로 브라우저에서 받을 파일은 없습니다. kagglehub가 인증을 요구하면 [Kaggle Settings](https://www.kaggle.com/settings)에서 API 토큰을 받아 `~/.kaggle/kaggle.json`에 두면 됩니다.

MovieLens 100K는 GroupLens 재배포 허가가 따로 필요합니다. 저장소에는 코드만 배포하고 데이터는 각자 받게 하는 것이 원칙입니다.

## 로더

| 함수 | 역할 |
|:---|:---|
| `load_titanic()` | Titanic 표 |
| `load_20newsgroups()` | 20 Newsgroups 문서 |
| `ensure_karate()` / `load_karate()` | Karate Club 노드·엣지와 그래프 |
| `ensure_cora()` / `load_cora()` | Cora 인용 네트워크 |
| `ensure_movielens()` / `load_movielens_100k()` / `load_movies()` / `load_users()` | MovieLens 폴더와 표 |
| `ensure_groceries()` / `load_groceries(path)` | arules 장바구니 CSV |
| `ensure_groceries_kaggle_raw()` | Kaggle 긴 형식 CSV |
| `ensure_groceries_kaggle()` | Kaggle 장바구니 CSV |
| `check_datasets()` | 위 데이터를 모두 로드해 상태표 반환 |
