"""페르소나 카탈로그 및 생성기의 기본 동작 검증."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compose_personas.py"
CATALOG = ROOT / "catalog" / "personas.json"


class PersonaTests(unittest.TestCase):
    def test_catalog_has_unique_ids(self):
        roles = json.loads(CATALOG.read_text(encoding="utf-8"))["roles"]
        self.assertEqual(len(roles), len({x["id"] for x in roles}))
        self.assertGreaterEqual(len(roles), 8)

    def test_all_knowledge_paths_exist(self):
        roles = json.loads(CATALOG.read_text(encoding="utf-8"))["roles"]
        for role in roles:
            for doc in role["knowledge"]:
                with self.subTest(role=role["id"], doc=doc):
                    self.assertTrue((ROOT / doc).is_file())

    def test_generate_two(self):
        with tempfile.TemporaryDirectory() as d:
            done = subprocess.run(
                [sys.executable, str(SCRIPT), "--roles", "memory-market,photo-overlay", "--out", d],
                text=True, capture_output=True, check=True
            )
            self.assertEqual(len(list(Path(d).glob("*.md"))), 2)
            self.assertIn("memory-market.md", done.stdout)
            self.assertIn("Overlay", (Path(d) / "photo-overlay.md").read_text(encoding="utf-8"))

    def test_custom(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--catalog", str(ROOT / "examples" / "custom-personas.json"),
             "--roles", "custom-sustainability"],
            text=True, capture_output=True, check=True
        )
        self.assertIn("지속가능성", proc.stdout)

    def test_unknown_role_fails(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--roles", "does-not-exist"],
            text=True, capture_output=True
        )
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()