"""전역 Codex Router 설치의 비파괴성 테스트."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "install_codex_router", ROOT / "scripts" / "install_codex_router.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class RouterTests(unittest.TestCase):
    def make_repo(self, root):
        (root / "docs").mkdir(parents=True, exist_ok=True)
        for name in ("README.md", "AGENTS.md", "docs/00-index.md"):
            (root / name).write_text("테스트", encoding="utf-8")

    def test_install_and_reinstall_are_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "kit"
            self.make_repo(root)
            target = Path(d) / "codex" / "AGENTS.md"
            self.assertEqual(mod.install_router(root, target), "INSTALLED")
            self.assertIn(str(root.resolve()), target.read_text(encoding="utf-8"))
            self.assertEqual(mod.install_router(root, target), "ALREADY_INSTALLED")

    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "kit"
            self.make_repo(root)
            target = Path(d) / "codex" / "AGENTS.md"
            self.assertEqual(mod.install_router(root, target, dry_run=True), "DRY_RUN")
            self.assertFalse(target.exists())

    def test_existing_file_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "kit"
            self.make_repo(root)
            target = Path(d) / "codex" / "AGENTS.md"
            target.parent.mkdir()
            target.write_text("사용자의 기존 지침", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                mod.install_router(root, target)
            self.assertEqual(target.read_text(encoding="utf-8"), "사용자의 기존 지침")

    def test_missing_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "kit"
            root.mkdir()
            target = Path(d) / "codex" / "AGENTS.md"
            with self.assertRaises(ValueError):
                mod.install_router(root, target)
            self.assertFalse(target.exists())

    def test_codex_home_env(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.dict(os.environ, {"CODEX_HOME": d}):
                self.assertEqual(mod.codex_home(), Path(d))
            with patch.dict(os.environ, {"CODEX_HOME": "relative/path"}):
                with self.assertRaises(ValueError):
                    mod.codex_home()

    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "kit"
            self.make_repo(root)
            existing = Path(d) / "existing.md"
            existing.write_text("기존 지침", encoding="utf-8")
            target = Path(d) / "AGENTS.md"
            try:
                target.symlink_to(existing)
            except (OSError, NotImplementedError):
                self.skipTest("이 환경에서 심볼릭 링크를 생성할 수 없음")
            with self.assertRaises(FileExistsError):
                mod.install_router(root, target)
            self.assertEqual(existing.read_text(encoding="utf-8"), "기존 지침")


if __name__ == "__main__":
    unittest.main()
