from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# Platform-aware venv path; falls back to the current interpreter when
# no venv exists (e.g. CI with system-wide pip install).
_VENV_BIN = ROOT / ".venv" / ("Scripts" if os.name == "nt" else "bin")
_PY_NAME = "python.exe" if os.name == "nt" else "python"
PYTHON = (_VENV_BIN / _PY_NAME) if (_VENV_BIN / _PY_NAME).exists() else Path(sys.executable)


class DemoTest(unittest.TestCase):
    def test_demo_builds_outputs(self) -> None:
        expected = [
            ROOT / "warehouse" / "search_observatory.duckdb",
            ROOT / "target" / "manifest.json",
            ROOT / "screenshots" / "01-hero.png",
            ROOT / "screenshots" / "04-proof.png",
        ]
        if not all(path.exists() for path in expected):
            result = subprocess.run(
                [str(PYTHON), str(ROOT / "scripts" / "run_demo.py")],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                self.fail(result.stdout + "\n" + result.stderr)
        for path in expected:
            self.assertTrue(path.exists(), f"Expected artifact missing: {path}")


if __name__ == "__main__":
    unittest.main()
