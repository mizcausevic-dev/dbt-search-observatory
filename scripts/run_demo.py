from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
DBT = ROOT / ".venv" / "Scripts" / "dbt.exe"


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    os.makedirs(ROOT / "warehouse", exist_ok=True)
    run([str(DBT), "seed", "--profiles-dir", ".", "--full-refresh"])
    run([str(DBT), "run", "--profiles-dir", "."])
    run([str(DBT), "test", "--profiles-dir", "."])
    run([str(DBT), "docs", "generate", "--profiles-dir", "."])
    run([str(PYTHON), str(ROOT / "scripts" / "render_readme_assets.py")])


if __name__ == "__main__":
    main()
