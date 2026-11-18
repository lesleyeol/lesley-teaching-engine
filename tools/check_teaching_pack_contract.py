#!/usr/bin/env python3
"""Check the existing Starter pilot; never authorize release or write lesson files."""
import argparse
import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCOPE = "starter-subject-be-contract-only"


def schema(name):
    result = json.loads((ROOT / f"schemas/teaching-pack-builder.{name}.schema.json").read_text())
    Draft202012Validator.check_schema(result)
    return Draft202012Validator(result)


def default_payload():
    return {
        "manifest": json.loads((ROOT / "curriculum/starter/subject-be.manifest.json").read_text()),
        "item_map": json.loads((ROOT / "curriculum/starter/subject-be.items.json").read_text()),
    }


def check(payload):
    report = {
        "validation_scope": SCOPE,
        "status": "BLOCKED",
        "release_authorized": False,
        "errors": [],
        "warnings": [],
        "counts": dict.fromkeys(["guided", "independent", "transfer", "delayed"], 0),
        "artifact_names": [],
    }
    for error in schema("input").iter_errors(payload):
        location = "/" + "/".join(str(p) for p in error.absolute_path)
        report["errors"].append(f"INPUT_SCHEMA {location}: {error.message}")
    if not report["errors"]:
        # Pass JSON on stdin; item strings cannot become shell or executable code.
        bridge = """
const fs=require('node:fs');
const {build}=require('./tools/build-starter-pack.cjs');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const result=build(input.manifest,input.item_map);
process.stdout.write(JSON.stringify({qa:result.qa,names:Object.keys(result.files||{})}));
"""
        try:
            process = subprocess.run(
                ["node", "-e", bridge], cwd=ROOT,
                input=json.dumps(payload, ensure_ascii=False),
                capture_output=True, text=True, timeout=30, check=False,
            )
            if process.returncode:
                report["errors"].append("ENGINE_EXECUTION_FAILED: existing builder returned a nonzero status")
            else:
                result = json.loads(process.stdout)
                qa = result["qa"]
                report.update({key: qa[key] for key in ["status", "errors", "warnings", "counts"]})
                report["artifact_names"] = result["names"]
        except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError):
            report["errors"].append("ENGINE_EXECUTION_FAILED: no valid builder result")
        if report["errors"]:
            report["status"] = "BLOCKED"
            report["artifact_names"] = []
    # A passing structural check is always a draft, including when input flags say PASS.
    report["release_authorized"] = False
    schema("output").validate(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON containing manifest and item_map; omit for existing pilot")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text()) if args.input else default_payload()
    except (OSError, ValueError):
        # Invalid/missing input is run through the same machine-readable blocked path.
        payload = None
    report = check(payload)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if report["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
