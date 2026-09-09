# Data Mining (dm-2026-fall)
 
> Hands-on labs and assignments
> Konkuk University
 
Public site: <https://gli.konkuk.ac.kr/board/lectures/dm-2026-fall>
  
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
git clone git@github.com:GLI-Lab/{{COURSE_SLUG}}.git
cd {{COURSE_SLUG}}
 
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
pixi run quarto preview      # 파일을 저장하면 해당 문서만 다시 렌더링 + 브라우저 자동 새로고침
```

## 5. 서버에 상시 프리뷰 띄우기 (PM2)

터미널을 종료해도 렌더링 결과를 계속 확인할 때

```bash
# 수업서버 Preview 서버 시작 (파일 변경 시 자동 렌더링)
pm2 start pixi --name "{{COURSE_SLUG}}" -- run quarto preview --port 4000 --host 0.0.0.0
# 수업서버 Preview 서버 시작 (변경 감지 없음)
pm2 start pixi --name "{{COURSE_SLUG}}" -- run quarto preview --port 4000 --host 0.0.0.0 --no-watch-inputs
```

접속: `http://<서버IP>:{{PORT}}`

```bash
# 재시작 / 제거
pm2 restart {{COURSE_SLUG}}
pm2 delete {{COURSE_SLUG}}

# 상태 확인
pm2 status
pm2 show {{COURSE_SLUG}}
pm2 logs {{COURSE_SLUG}} --lines 100
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

즉, `qmd`만 수정하고 렌더 결과를 갱신하지 않으면 원본과 산출물이 서로 어긋날 수 있습니다.

