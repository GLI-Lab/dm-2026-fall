# Data Mining (dm-2026-fall)
 
> Hands-on labs and assignments
> Konkuk University
 
Public site: <https://gli.konkuk.ac.kr/board/lectures/dm-2026-fall>
  
---

## 브랜치

| 브랜치 | 역할 |
|---|---|
| `main` | `.qmd` 원본, `_freeze/`, 워크플로 |
| `gh-pages` | `quarto publish` 결과 (공개 사이트) |
| `students` | 학생용 `.ipynb` + `pixi.toml` + `data/` (`README-students.md` → `README.md`) |
| `data` | `data/` 미러 (`data/**` 변경 시에만 갱신) |

`main`에 push하면 `gh-pages`와 `students`가 자동 갱신됨. `data`는 `data/**`가 바뀔 때만 갱신됨.

---

## 1. 사전 요구사항
 
| 도구 | 용도 | 확인 |
|---|---|---|
| Git | 저장소 관리 | `git --version` |
| [pixi](https://pixi.sh) | Python 환경 및 의존성 | `pixi --version` |
| [Quarto](https://quarto.org) | `.qmd` 렌더링 | `quarto --version` |
| Node.js + PM2 | 서버 상시 프리뷰 (서버에서만) | `pm2 --version` |

## 2. 저장소 받기

```zsh
git clone git@github.com:GLI-Lab/dm-2026-fall.git
cd dm-2026-fall
 
# 이 저장소에서만 적용되는 커밋 정보 (--global 없이)
git config user.name "GLI-Lab" 
git config user.email "glilab509@gmail.com"
```

## 3. Quarto 설치
 
### macOS
 
```bash
brew install --cask quarto
quarto --version
```
 
### Ubuntu
 
```bash
# 최신 버전 확인: https://quarto.org/docs/download/
QUARTO_VERSION=1.6.42
wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb
sudo dpkg -i quarto-${QUARTO_VERSION}-linux-amd64.deb
rm quarto-${QUARTO_VERSION}-linux-amd64.deb
 
source ~/.zshrc
quarto --version
```

## 4. 로컬에서 작업하기

```bash
pixi install  # 최초 1회
pixi run quarto render
pixi run quarto preview
```

> `render` = `_site` 생성 후 바로 종료함
>
> - `quarto render`: 프로젝트 전체에 대해서 `_site` HTML 생성 (`freeze: auto`)
>   - qmd가 바뀐 파일: 셀을 다시 실행 → 갱신한 `_freeze`로 `_site` HTML 생성
>   - qmd가 안 바뀐 파일: 셀은 다시 실행하지 않음 → 기존 `_freeze`로 `_site` HTML만 생성
> - `quarto render -M freeze:false`: 프로젝트 전체에 대해서 freeze를 무시하고 전부 다시 실행하여 `_site` HTML 생성함 (CSV 등 외부 파일만 바뀐 경우)
>
> `preview` = `_site`를 서빙하기 위한 로컬 서버를 생성함. `--render` 기본값은 `none`
>
> - `quarto preview`: 시작 때 전체를 다시 실행하지 않음. 이미 있는 `_freeze`로 HTML을 맞춘 뒤 서빙. qmd 옆에 `*_files/`를 만들지 않음
> - `quarto preview --render all`: 시작할 때 프로젝트 전체 `render`를 한 번 한 뒤 preview. 그때 `*_files/`가 qmd 옆에 생겼다가 `_site`로 복사됨. 이때 `*_files/`를 지우지 않음
> - `quarto preview --render all -M freeze:false`: 시작할 때 freeze를 무시하고 전부 다시 실행한 뒤 preview (CSV 등 외부 파일만 바뀐 경우)

## 5. 서버에 상시 프리뷰 띄우기 (PM2)

터미널 종료 후에도 렌더링 결과를 계속 확인하고 싶을 때

```bash
# quarto preview
pm2 start pixi --name "dm-2026-fall" -- run quarto preview --port 4001 --host 0.0.0.0

# --render all (추천)
pm2 start pixi --name "dm-2026-fall" -- run quarto preview --port 4001 --host 0.0.0.0 --render all

# --render all -M freeze:false
pm2 start pixi --name "dm-2026-fall" -- run quarto preview --port 4001 --host 0.0.0.0 --render all -M freeze:false

# 기존 _site만 서빙. 변경 감지 없음 (저장해도 다시 그리지 않음)
pm2 start pixi --name "dm-2026-fall" -- run quarto preview --port 4001 --host 0.0.0.0 --no-watch-inputs
```

접속: `http://<서버IP>:4001`

```bash
# 재시작 / 제거
pm2 restart dm-2026-fall
pm2 delete dm-2026-fall

# 상태 확인
pm2 status
pm2 show dm-2026-fall
pm2 logs dm-2026-fall --lines 100
```

서버 재부팅 후에도 살아 있게 하려면:
 
```bash
pm2 save
pm2 startup
```


## GitHub Pages 배포

.github/workflows 활용

## Workflow

> `qmd` → (실행) → `_freeze` (셀 출력/그림 캐시) → `_site` (완성 HTML).
>
> | | `_freeze/` | `_site/` |
> |---|---|---|
> | 역할 | 코드 셀 실행 캐시 | 브라우저가 보는 사이트 |
> | `main`에 커밋 | 함. qmd와 짝이 맞아야 CI가 Python 없이 빌드함 | 안 함 (`.gitignore`). `gh-pages`에만 올라감 |
>
> **커밋:** `.qmd`, `_freeze/`, 워크플로, `data/` (일부), TODO `.py`
>
> **커밋 안 함:** `_site/`, `*-solution.py`, `*-solution.qmd`, `solution/`, `.pixi/`, `*.ipynb`

이 저장소는 `*.qmd` 원본과 `_freeze/` 아래의 렌더 결과를 함께 관리함. 따라서 문서를 수정한 뒤 `git push` 하기 전에는 보통 아래 순서로 작업하는 것이 안전함

```bash
pixi run quarto render
git status
git add ...
git commit -m "..."
git push
```

## Practice 결과를 사이트에 넣을 때

1. TODO `.py`와 `.qmd`를 먼저 커밋해 학생 과제를 만든 뒤
2. 마지막에 `_freeze`를 커밋하여 Practice 결과(셀 출력·그림)를 넣음

> `pixi run freeze-solutions`가 하는 일:
>
> 1. `#| eval: false`를 `.qmd`에서 제거함
> 2. gitignored `labXX_X-solution.py`를 `labXX_X.py` **위에 복사**함. 파일은 안 지워짐. 작업 트리의 `labXX_X.py` 내용만 풀이로 바뀜. `*-solution.py`는 그대로 남음. git에 커밋된 TODO `.py`도 그대로 있음
> 3. `quarto render -M freeze:false`로 그 `.qmd`를 실행해 `_freeze`를 갱신함
> 4. `git checkout -- labXX_X.py`로 TODO `.py`를 복구함. `_freeze`는 그대로 둠
> 5. 스크립트는 커밋하지 않음. 확인 후 **이번 커밋**에는 `.qmd`와 `_freeze`만 넣음. TODO `.py`는 이미 `main`에 있음. 여기서 다시 add하지 않음 (복구가 안 되면 풀이가 들어감). `*-solution.py`는 gitignore

```bash
pixi run freeze-solutions --dry-run          # 잡히는 파일 확인
pixi run freeze-solutions                    # 전체
pixi run freeze-solutions exercises/labXX    # 한 랩만
```

```bash
git add exercises/labXX/*.qmd _freeze/exercises/labXX
git status   # TODO .py 가 modified면 복구 실패. *-solution.py 가 잡히면 안 됨
git commit -m "..."
git push
```

## README·qmd 작성 가이드

- Think·Practice는 `::: {.callout-important}` 로 두며, 시험에는 코드 구현이 아닌 Think·Practice와 관련있음
  - Think: `title="Think"`. 질문 다음에 답을 바로 적음
  - Practice: `title="Q. Practice"`. 구현은 `labXX_*.py`. qmd 셀은 `#| eval: false`. 필요하면 Hint
- 데이터 원본은 `data/`에 두고 찾기·다운로드·가공은 `data.loader`에 둠. 각 lab helper.py에 넣지 않음
- 모든 README와 qmd 파일에서 한글은 **개조식**으로 씀 (`~함`, `~둠`, `~않음`). 긴 서술체(`~합니다`)는 쓰지 않음
