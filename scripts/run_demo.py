from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# Platform-aware venv paths: Windows uses Scripts/, POSIX uses bin/.
# Fall back to the current interpreter / PATH-resolved dbt when no venv
# exists (e.g. CI where deps are installed system-wide via pip).
_VENV_BIN = ROOT / ".venv" / ("Scripts" if os.name == "nt" else "bin")
_PY_NAME = "python.exe" if os.name == "nt" else "python"
_DBT_NAME = "dbt.exe" if os.name == "nt" else "dbt"
PYTHON = (_VENV_BIN / _PY_NAME) if (_VENV_BIN / _PY_NAME).exists() else Path(sys.executable)
DBT = (_VENV_BIN / _DBT_NAME) if (_VENV_BIN / _DBT_NAME).exists() else Path("dbt")


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
