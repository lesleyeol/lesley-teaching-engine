#!/usr/bin/env python3
# Source / item-map checks; no external package or network access required.
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pkg = json.loads((root / "tools/full_starter_u2/unit_scope_item_bank.json").read_text(encoding="utf8"))
old = json.loads((root / "tools/full_starter_u2/legacy_subject_be.items.json").read_text(encoding="utf8"))
kp = {x["id"]: x for x in pkg["knowledge_points"]}
items = pkg["items"]
sources = pkg["sources"]
assert pkg["status"] == "DRAFT_FOR_TEACHER_REVIEW"
assert pkg["source_status"] == "READY_WITH_LIMITS"
assert set(pkg["scope"]) >= {"Starter", "Unit 1", "Unit 2"}
assert len(kp) == 46, len(kp)
assert len(items) == 185, len(items)
assert len({x["id"] for x in items}) == len(items)
assert all(i["kp"] in kp for i in items)
assert all(i["answer"] and i["rationale"] and set(i["source_refs"]) <= set(sources) for i in items)
assert all(any(x["kp"] == k for x in items) for k in kp)
assert len(pkg["word_banks"]["Unit 1"]) == 29
assert len(pkg["word_banks"]["Unit 2"]) == 36
assert all(x["state"] == "AUDIO_PENDING" for x in pkg["audio_gaps"])
assert all(not x.get("hint") for x in items if x["stage"] in ("check", "delayed"))
legacy = {i["id"]: i for i in items if i.get("legacy_preserved")}
assert len(legacy) == 16
for x in old["items"]:
    y = legacy["LEG-" + x["id"]]
    assert y["prompt"] == x["prompt"]
    assert y["legacy_original"] == x
    assert y["answer"] == " / ".join(x["answers"])
print("PASS: 46 knowledge points / 185 items / 65 vocabulary items / 16 legacy preserved")
print("NOTE: source validity, teacher approval, formal Release QA, real oral/listening and student mastery are NOT certified.")
