# Data Mining Course (for students)

Konkuk University, Fall 2026.

Hands-on labs and homework starter code. The lab environment is set up with **pixi**.

Course site: <https://gli.konkuk.ac.kr/board/lectures/dm-2026-fall>

This branch (`students`) contains Jupyter notebooks (`.ipynb`), helper `.py` files, shared datasets, and the pixi environment. Lab contents, deadlines, and policies are on the course site.

## Repository layout

```
dm-2026-fall/                 # clone of the students branch
├── pixi.toml                 # dependency declarations
├── pixi.lock                 # exact pinned versions
├── data/                     # shared datasets (paths are from the repo root)
├── exercises/                # lab notebooks
└── assignments/              # homework starter code
```

Always start Jupyter **from the repository root** so that `data/` paths resolve correctly.

## 1. First-time setup

Install Pixi: <https://pixi.sh/latest/getting_started/installation/>

Windows: use **WSL2**, then follow the Linux steps inside Ubuntu. See the [environment setup](https://gli.konkuk.ac.kr/board/lectures/dm-2026-fall/exercises/environment-setup.html) page for details.

Clone this branch and enter the repo:

```bash
git clone -b students https://github.com/GLI-Lab/dm-2026-fall.git
cd dm-2026-fall
```

Install the environment. Pixi reads `pixi.toml` and `pixi.lock` and installs the pinned packages:

```bash
pixi install
```

Start JupyterLab (defined as the `lab` task in `pixi.toml`):

```bash
pixi run lab
```

Copy the URL printed in the terminal into your browser (port 8888). In VS Code, open the repo folder and select the kernel at `.pixi/envs/default/bin/python`.

## 2. Update course materials

From the repo root, on the `students` branch:

```bash
git pull
```

If `pixi.toml` or `pixi.lock` changed, run `pixi install` again.
