# Machine Learning Course

```zsh
git clone git@github.com:GLI-Lab/machine-learning-course.git
git config user.name "GLI-Lab" 
git config user.email "glilab509@gmail.com"
```

## 우분투에서 설치하기

```bash
# 최신 버전 확인: https://quarto.org/docs/download/
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.6.42/quarto-1.6.42-linux-amd64.deb
sudo dpkg -i quarto-1.6.42-linux-amd64.deb
rm quarto-1.6.42-linux-amd64.deb

source ~/.zshrc
quarto --version
```

## PM2 등록하기
```bash
# 수업서버 Preview 서버 시작 (자동 랜더링)
pm2 start pixi --name "ml-course" -- run quarto preview --port 4000 --host 0.0.0.0
# 수업서버 Preview 서버 시작
pm2 start pixi --name "ml-course" -- run quarto preview --port 4000 --host 0.0.0.0 --no-watch-inputs

# 재시작 / 제거
pm2 restart ml-course
pm2 delete ml-course

# 상태 확인
pm2 status
pm2 show ml-course
```

`<IP>:4000` 으로 접속 가능

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

