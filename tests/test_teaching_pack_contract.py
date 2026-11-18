#!/usr/bin/env python3
"""Contract fixtures exercise structural failures; they are not Unit acceptance."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("contract", ROOT / "tools/check_teaching_pack_contract.py")
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


class ContractTests(unittest.TestCase):
    def test_schema_definitions(self):
        contract.schema("input")
        contract.schema("output")

    def test_fixture_cases(self):
        fixtures = json.loads((ROOT / "tests/fixtures/teaching-pack-builder/cases.json").read_text())
        for case in fixtures["cases"]:
            with self.subTest(case=case["name"]):
                payload = copy.deepcopy(contract.default_payload())
                for change in case["changes"]:
                    parent = payload
                    for key in change["path"][:-1]:
                        parent = parent[key]
                    key = change["path"][-1]
                    if change["op"] == "delete":
                        del parent[key]
                    else:
                        parent[key] = change["value"]
                report = contract.check(payload)
                self.assertEqual(report["status"], case["expect_status"])
                self.assertFalse(report["release_authorized"])
                if report["status"] == "BLOCKED":
                    self.assertTrue(report["errors"])
                    self.assertEqual(report["artifact_names"], [])
                else:
                    self.assertEqual(len(report["artifact_names"]), 4)

    def test_forged_release_rejected_by_output_schema(self):
        report = contract.check(contract.default_payload())
        report["release_authorized"] = True
        with self.assertRaises(ValidationError):
            contract.schema("output").validate(report)

    def test_blocked_report_cannot_list_generated_artifacts(self):
        report = contract.check(None)
        report["artifact_names"] = ["student.html"]
        with self.assertRaises(ValidationError):
            contract.schema("output").validate(report)

    def test_cli_invalid_json_is_machine_readable_block(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.json"
            source.write_text("{invalid")
            result = subprocess.run([sys.executable, str(ROOT / "tools/check_teaching_pack_contract.py"),
                                     "--input", str(source)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "BLOCKED")

    def test_default_check_does_not_write_student_outputs(self):
        directory = ROOT / "examples/starter-be"
        before = {str(p): p.read_bytes() for p in directory.rglob("*") if p.is_file()}
        report = contract.check(contract.default_payload())
        after = {str(p): p.read_bytes() for p in directory.rglob("*") if p.is_file()}
        self.assertEqual(report["status"], "DRAFT_FOR_TEACHER_REVIEW")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
