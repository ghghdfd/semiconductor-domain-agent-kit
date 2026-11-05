"""저장소 내 Codex 스킬 포맷과 안전 설치의 회귀 테스트."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_codex_skills", ROOT / "scripts" / "install_codex_skills.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class CodexSkillsTests(unittest.TestCase):
    def test_entrypoints(self):
        self.assertEqual(len(mod.AVAILABLE), 3)
        for name in mod.AVAILABLE:
            with self.subTest(name=name):
                self.assertEqual(mod.skill_path(name).name, name)

    def test_install_twice(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "skills"
            first, same = mod.install(mod.AVAILABLE, dest)
            self.assertEqual(len(first), 3)
            self.assertEqual(same, [])
            second, same = mod.install(mod.AVAILABLE, dest)
            self.assertEqual(second, [])
            self.assertEqual(len(same), 3)

    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "skills"
            mod.install(["grill-me"], dest, dry_run=True)
            self.assertFalse(dest.exists())

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "skills" / "deep-plan"
            dest.mkdir(parents=True)
            (dest / "SKILL.md").write_text("기존 사용자 수정본", encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.install(["deep-plan"], dest.parent)
            self.assertEqual((dest / "SKILL.md").read_text(encoding="utf-8"), "기존 사용자 수정본")

    def test_project_target(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(mod.get_target("project", d), Path(d).resolve() / ".agents" / "skills")


if __name__ == "__main__":
    unittest.main()
