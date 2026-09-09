# Machine Learning Course (for students)

The lab environment is set up with **pixi**.

## Workflow

### 1. First-time setup

Install Pixi:

- https://pixi.sh/latest/getting_started/installation/

Clone the student branch and enter the repo:

```bash
git clone -b students https://github.com/GLI-Lab/machine-learning-course.git
cd machine-learning-course
```

Install the environment:

Pixi reads the project configuration from `pixi.toml` (and the lock file, if present) and installs the required packages automatically.

```bash
pixi install
```

Run Jupyter Lab:

This runs the `jupyter` task defined in the Pixi project and starts Jupyter Lab with the course environment activated.

```bash
pixi run jupyter
```

Open the URL shown in the terminal in your browser.

### 2. Update course materials

From the repo root, run:

```bash
git pull   # updates from origin/students when you're on the students branch
```
