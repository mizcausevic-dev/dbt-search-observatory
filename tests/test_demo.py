from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"


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
