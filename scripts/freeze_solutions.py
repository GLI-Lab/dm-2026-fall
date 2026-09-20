#!/usr/bin/env python3
"""Freeze Practice output using local *-solution.py files.

gh-pages CI has no Python. Freeze hashes the .qmd only, so committed
starter .py files may stay as TODO. This script:

1. Copies each gitignored *-solution.py over the matching starter .py
2. Strips `#| eval: false` from .qmd files that import those modules
   (the committed .qmd must match the one used to write freeze)
3. Renders those .qmd files with freeze:false so cells actually run
4. Restores tracked starter .py files from git (TODO). Freeze stays.

Does not commit. Does not put `#| eval: false` back.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_NAMES = {
    ".git",
    ".pixi",
    ".quarto",
    "_freeze",
    "_site",
    "__pycache__",
    ".ipynb_checkpoints",
    "node_modules",
}

EVAL_FALSE_RE = re.compile(
    r"^[ \t]*#\|[ \t]*eval:[ \t]*false[ \t]*\n?",
    re.MULTILINE,
)


def skip_path(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def iter_solution_py(root: Path) -> list[Path]:
    found = []
    for path in root.rglob("*-solution.py"):
        if skip_path(path):
            continue
        found.append(path)
    return sorted(found)


def starter_for(solution: Path) -> Path:
    name = solution.name
    suffix = "-solution.py"
    if not name.endswith(suffix):
        raise ValueError(f"not a solution file: {solution}")
    return solution.with_name(name[: -len(suffix)] + ".py")


def import_pattern(module: str) -> re.Pattern[str]:
    name = re.escape(module)
    return re.compile(
        rf"(?:^|\n)(?:from[ \t]+{name}[ \t]+import|import[ \t]+{name}\b)"
    )


def qmd_imports_module(text: str, module: str) -> bool:
    return import_pattern(module).search(text) is not None


def heuristic_qmds(starter: Path) -> list[Path]:
    stem = starter.stem
    variants = {stem.lower(), stem.lower().replace("_", "-")}
    match = re.match(r"^(.*)_(\d+)$", stem)
    if match:
        variants.add(f"{match.group(1)}-{match.group(2)}".lower())

    found = []
    for qmd in starter.parent.glob("*.qmd"):
        if skip_path(qmd) or qmd.name.endswith("-solution.qmd"):
            continue
        qstem = qmd.stem.lower()
        if any(variant == qstem or variant in qstem for variant in variants):
            found.append(qmd)
    return found


def find_qmds(root: Path, starters: list[Path]) -> list[Path]:
    modules = {starter.stem: starter for starter in starters}
    found: dict[Path, None] = {}

    for qmd in root.rglob("*.qmd"):
        if skip_path(qmd) or qmd.name.endswith("-solution.qmd"):
            continue
        text = qmd.read_text(encoding="utf-8")
        if any(qmd_imports_module(text, module) for module in modules):
            found[qmd] = None

    for starter in starters:
        for qmd in heuristic_qmds(starter):
            found[qmd] = None

    return sorted(found)


def count_eval_false(path: Path) -> int:
    return len(EVAL_FALSE_RE.findall(path.read_text(encoding="utf-8")))


def strip_eval_false(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, n = EVAL_FALSE_RE.subn("", text)
    if n:
        path.write_text(new_text, encoding="utf-8")
    return n


def git_tracked(path: Path) -> bool:
    relative = path.resolve().relative_to(REPO_ROOT)
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "--error-unmatch", str(relative)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def restore_starters(starters: list[Path], backups: dict[Path, bytes]) -> None:
    tracked = [path for path in starters if git_tracked(path)]
    if tracked:
        rels = [str(path.resolve().relative_to(REPO_ROOT)) for path in tracked]
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "checkout", "--", *rels],
            check=True,
        )
    for path in starters:
        if path in tracked:
            continue
        path.write_bytes(backups[path])


def freeze_dir_for(qmd: Path) -> Path:
    relative = qmd.resolve().relative_to(REPO_ROOT)
    return REPO_ROOT / "_freeze" / relative.with_suffix("")


def collect_solutions(paths: list[Path]) -> list[Path]:
    if not paths:
        return iter_solution_py(REPO_ROOT)

    found: dict[Path, None] = {}
    for raw in paths:
        path = raw if raw.is_absolute() else (REPO_ROOT / raw)
        path = path.resolve()
        if path.is_dir():
            for solution in iter_solution_py(path):
                found[solution] = None
        elif path.name.endswith("-solution.py"):
            found[path] = None
        elif path.suffix == ".py":
            solution = path.with_name(f"{path.stem}-solution.py")
            if solution.exists():
                found[solution] = None
        else:
            raise SystemExit(f"not a lab directory or starter/solution .py: {raw}")
    return sorted(found)


def require_quarto() -> str:
    quarto = shutil.which("quarto")
    if quarto is None:
        raise SystemExit("quarto not on PATH. Install Quarto, then retry.")
    return quarto


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy *-solution.py over starters, render matching .qmd, "
            "restore TODO .py, leave _freeze in place."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional lab dirs or starter/solution .py files (default: whole repo)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print pairs and .qmd files; do not copy, strip, or render",
    )
    parser.add_argument(
        "--keep-eval-false",
        action="store_true",
        help="Do not strip #| eval: false (Practice cells will stay skipped)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    solutions = collect_solutions(args.paths)
    if not solutions:
        print("No *-solution.py files found.", file=sys.stderr)
        return 1

    pairs: list[tuple[Path, Path]] = []
    for solution in solutions:
        starter = starter_for(solution)
        if not starter.exists():
            print(f"skip {solution}: missing starter {starter}", file=sys.stderr)
            continue
        pairs.append((solution, starter))

    if not pairs:
        print("No starter/solution pairs to freeze.", file=sys.stderr)
        return 1

    starters = [starter for _, starter in pairs]
    qmds = find_qmds(REPO_ROOT, starters)
    if not qmds:
        print("No .qmd files import the solution-backed modules.", file=sys.stderr)
        return 1

    print("Solution pairs:")
    for solution, starter in pairs:
        rel_sol = solution.relative_to(REPO_ROOT)
        rel_starter = starter.relative_to(REPO_ROOT)
        print(f"  {rel_sol} -> {rel_starter}")

    print("Notebooks:")
    for qmd in qmds:
        n_eval_false = count_eval_false(qmd)
        note = f"  ({n_eval_false} eval: false)" if n_eval_false else ""
        print(f"  {qmd.relative_to(REPO_ROOT)}{note}")

    if args.dry_run:
        return 0

    if not args.keep_eval_false:
        for qmd in qmds:
            n = strip_eval_false(qmd)
            if n:
                print(f"stripped {n} eval: false from {qmd.relative_to(REPO_ROOT)}")
    else:
        leftover = [qmd for qmd in qmds if count_eval_false(qmd)]
        if leftover:
            print(
                "warning: eval: false left in place; Practice cells will not run:",
                file=sys.stderr,
            )
            for qmd in leftover:
                print(f"  {qmd.relative_to(REPO_ROOT)}", file=sys.stderr)

    quarto = require_quarto()
    backups = {starter: starter.read_bytes() for starter in starters}

    try:
        for solution, starter in pairs:
            shutil.copyfile(solution, starter)
            print(f"copied {solution.relative_to(REPO_ROOT)} -> {starter.relative_to(REPO_ROOT)}")

        for qmd in qmds:
            relative = qmd.relative_to(REPO_ROOT)
            print(f"render {relative}")
            subprocess.run(
                [quarto, "render", str(relative), "-M", "freeze:false"],
                cwd=REPO_ROOT,
                check=True,
            )
    finally:
        restore_starters(starters, backups)
        print("restored starter .py from git (or pre-run copy)")

    print("Freeze written. Starter .py files are TODO again.")
    print("Commit matching .qmd + _freeze only (not *-solution.py):")
    for qmd in qmds:
        freeze_dir = freeze_dir_for(qmd)
        print(f"  git add {qmd.relative_to(REPO_ROOT)} {freeze_dir.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
