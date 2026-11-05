import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
assignment = ROOT / "examples" / "or" / "assignment.json"
contract = ROOT / "examples" / "or" / "model-contract.json"

sys.path.insert(0, str(ROOT / "scripts"))
from check_or_contract import check
from solve_assignment import solve, verify, validate_input


class OrTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(assignment.read_text(encoding="utf-8"))

    def test_contract_valid(self):
        data = json.loads(contract.read_text(encoding="utf-8"))
        self.assertEqual(check(data), [])

    def test_contract_missing_objective(self):
        data = json.loads(contract.read_text(encoding="utf-8"))
        data.pop("objective")
        self.assertTrue(check(data))

    def test_example_optimal(self):
        result = solve(self.data)
        self.assertEqual(result["status"], "OPTIMAL")
        self.assertTrue(result["verified"])
        self.assertTrue(verify(self.data, result["assignment"], result["cost"]))

    def test_bad_assignment_fails(self):
        self.assertFalse(verify(self.data, {"T1": "A", "T2": "A", "T3": "B"}, 12))

    def test_forbidden_assignment_rejected(self):
        self.assertFalse(verify(self.data, {"T1": "B", "T2": "C", "T3": "A"}, 14))

    def test_infeasible(self):
        d = copy.deepcopy(self.data)
        d["forbidden"] = [[w, "T1"] for w in d["workers"]]
        self.assertEqual(solve(d)["status"], "INFEASIBLE")

    def test_invalid_cost_shape(self):
        d = copy.deepcopy(self.data)
        d["costs"] = [[1]]
        with self.assertRaises(ValueError):
            validate_input(d)

    def test_commandline(self):
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "solve_assignment.py"),
                            str(assignment)], encoding="utf-8", capture_output=True, check=True)
        self.assertIn("OPTIMAL", p.stdout)


if __name__ == "__main__":
    unittest.main()