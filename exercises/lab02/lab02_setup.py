"""Put the course repo root and this lab folder on sys.path.

Notebooks import this first so `data.loader` and `lab02_*.py` both work,
whether Quarto runs with execute-dir: file or Jupyter starts at the repo root.
"""

from __future__ import annotations

import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent
REPO_ROOT = LAB_DIR.parents[1]

for path in (REPO_ROOT, LAB_DIR):
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)
