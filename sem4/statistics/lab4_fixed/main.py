from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOKS = [
    "01_coin_toss.ipynb.ipynb",
    "02_linear_regression.ipynb",
    "03_robust_linear_regression_anscombe.ipynb",
    "04_robust_linear_regression_own_data.ipynb",
    "05_logistic_regression_iris.ipynb",
    "06_ab_testing_book.ipynb",
    "07_ab_testing_custom.ipynb",
    "08_challenger_disaster.ipynb",
    "09_advanced_ab_testing.ipynb",
]


def run_jupyter_lab() -> int:
    os.chdir(ROOT)
    print(f"Working directory: {ROOT}")
    print("Opening JupyterLab. Use the notebooks folder and run files from top to bottom.")
    return subprocess.call([sys.executable, "-m", "jupyter", "lab"])


def run_check() -> int:
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("PYTHONIOENCODING", "utf-8")

    for notebook in NOTEBOOKS:
        notebook_path = Path("notebooks") / notebook
        print(f"Executing {notebook_path}", flush=True)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--output-dir",
                "_executed",
                str(notebook_path),
            ],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            return result.returncode

    print("All notebooks executed successfully. Results are in _executed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Launcher for lab4_fixed notebooks.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="execute all notebooks headlessly with nbconvert",
    )
    args = parser.parse_args()

    if args.check:
        return run_check()
    return run_jupyter_lab()


if __name__ == "__main__":
    raise SystemExit(main())
