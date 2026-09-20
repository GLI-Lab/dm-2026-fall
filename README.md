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

`main`에 push하면 `gh-pages`와 `students`가 자동 갱신됩니다.

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
pixi install                 # 최초 1회

# 1. _freeze / _site 갱신. freeze: auto라 바뀐 qmd만 다시 실행 (마크다운만 바꿔도 해당 파일은 다시 그림)
pixi run quarto render
#    qmd는 그대로인데 CSV 등 외부 데이터만 바뀐 경우
pixi run quarto render -M freeze:false

# 2. 브라우저로 확인. 저장하면 그 .qmd만 다시 그림 (마크다운 포함)
pixi run quarto preview
```

## 5. 서버에 상시 프리뷰 띄우기 (PM2)

터미널을 종료해도 렌더링 결과를 계속 확인할 때

```bash
# 기존 _site를 띄움. 저장하면 그 .qmd만 다시 그림 (마크다운 포함). 시작 시 전체 재실행은 하지 않음
pm2 start pixi --name "dm-2026-fall" -- run quarto preview --port 4001 --host 0.0.0.0

# (추천) 시작할 때 사이트 전체를 한 번 render한 뒤 띄움 (freeze: auto라 안 바뀐 qmd는 _freeze 재사용). 이후 저장 시 해당 파일만 다시 그림
pm2 start pixi --name "dm-2026-fall" -- run quarto preview --port 4001 --host 0.0.0.0 --render all

# qmd는 그대로인데 CSV 등 외부 데이터만 바뀐 경우: 시작 시 freeze를 끄고 전부 다시 실행
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

이 저장소는 `*.qmd` 원본과 `_freeze/` 아래의 렌더 결과를 함께 관리합니다. 따라서 문서를 수정한 뒤 `git push` 하기 전에는 보통 아래 순서로 작업하는 것이 안전합니다.

```bash
pixi run quarto render
git status
git add ...
git commit -m "..."
git push
```

즉, `qmd`만 수정하고 렌더 결과를 갱신하지 않으면 원본과 산출물이 서로 어긋날 수 있습니다. CSV만 바뀐 경우에는 4절의 `quarto render -M freeze:false`를 쓰면 됩니다.
