# Starter Unit｜Source → Item Map → Printable Pack（Controlled Draft）

**Mode:** SOURCE-BOUND GENERATION → teacher review → not yet PRODUCTION release  
**Status:** DRAFT_FOR_TEACHER_REVIEW / READY WITH LIMITS  
**Policy:** `LESLEY_TEACHING_ENGINE_v2.4_STABLE.md`  
**Content basis:** uploaded photographed original textbook pages, **not** previously corrected homework as evidence of mastery.

## 1. Why this exists

The Adaptive Lesson Designer v0.1 chose appropriate activities but did **not** author valid questions or trace a source. This next-stage pilot adds:

1. a narrow content Source Lock + lexical allowlist;
2. one structured question/answer/diagnosis item map;
3. Student / Teacher / Answer / Delayed outputs generated from **that same map**;
4. build-time guards against unknown vocabulary, missing source references, duplicate questions, answer-count mismatch, and unauthorized formal release.

This is **not** a general-purpose AI source recognizer or a verified textbook database.

## 2. Actual source verified for this pilot

| Basis | Verified from the uploaded file | Limit |
|---|---|---|
| `學校課本Starter & Unit 1.pdf` PDF page **7**, book page **5** | Starter subject pronouns `I, you, he, she, it, we, they`; forms `am, is, are`; names from the textbook's practice table | Source is photographed and already annotated; textbook edition / official current-version confirmation still required |
| Same PDF page **7**, book page **6** | Comparison with subject and possessive pronouns | Only verifies seen forms, **not** permission to assess possessives |

The original scan is **not committed** into this public repository. All questions in `subject-be.items.json` are teacher-created synthetic variations; the original student's corrected answers are not Independent Evidence.

**Locked pilot scope:** affirmative pronoun + be concord only. No formal claim regarding Starter's other lessons, Unit 1, Unit 2, age questions, possessives, spelling, or actual school exam coverage.

## 3. Source readiness and release boundary

| Aspect | Current status |
|---|---|
| Source authenticity | User-provided photographed textbook pages; original complete edition not yet independently verified |
| Source completeness | Partial (pilot subsections only) |
| Answer exposure | YES on some original pages; original answered items are not reused as mastery evidence |
| Curricular / lexical Source Lock | Scoped to visible items on printed page 5; machine allowlist explicitly recorded |
| Pedagogy Lock | Drafted for pronoun-be and traceable in manifest; teacher approval outstanding |
| Item-map static consistency | Tested with Node (29 assertions) |
| Student / Teacher / Answer versions | Derived from same map, no independent re-authoring |
| Formal Independent Gate | Not approved; no mastery pass claim |
| Formal release | **NOT READY** until teacher content checks and full v2.4 Release QA |

### The generator cannot authorize release

`--release` is rejected. Even a successful `--check` or perfect PDF does not certify curriculum authenticity, mastery, or classroom effectiveness. If the source readiness is `BLOCKED`, all output generation stops.

## 4. How to run

Use Node.js 18+; no npm packages, network calls, API keys, or student records are needed:

```sh
node tools/build-starter-pack.cjs --check
node tests/starter-pack.test.cjs
node tools/build-starter-pack.cjs
```

The last command builds `examples/starter-be/`:

| File | What it contains |
|---|---|
| `student.html` | Page 1 guided learning; page 2 no-hint new-item practice and perspective transfer |
| `teacher.html` | Source provenance, support removal, teacher record, item-level diagnosis |
| `answer.html` | Answer + Chinese rationale, including teacher-held delayed answers |
| `delayed.html` | Separate delayed no-cue new-item card; do not distribute with immediate booklet |
| `qa-report.json` | Build guard results + unresolved human-review warnings |

All generated HTML files are **standalone** and have A4 print CSS. In a mobile browser, use Share → Print / Save PDF where available, but verify print margins and fonts on the device before classroom distribution.

For repeatable local QA with a browser, export each HTML to PDF, inspect page counts, check no clipped lines or overlapping footer, and test mobile width. The standalone CLI deliberately does not require any browser.

## 5. How to use with an individual learner

1. Teacher uses the visible rule-card + `G01–G03` as guided instruction. This is **supported practice**.
2. Remove / cover the first page. Present `I01–I07` as **new no-target-hint attempts**; record any teacher cues separately.
3. Present `T01–T02` in the named-speaker context to test a different skill dimension: **pronoun perspective plus be**. Do not classify all transfer errors as pure be-rule failure.
4. If a cue was given, do not mark an independent pass. After support removal, use another **previously unseen** question, not simply retry the exposed item.
5. Give `D01–D04` at a later lesson, record the **actual days elapsed** and whether hints were used. A future task schedule is not itself retention evidence.

The system does not know whether any particular student has learned or retained the target; only actual teacher-observed results can establish that.

## 6. Change control and next gate

Teacher review should check each item for lexeme provenance, meaningful novelty, perspective, answer uniqueness, and classroom suitability. If issues are found, **revise only failed items** and regenerate all outputs from the same single item map. Before formal release, separately confirm current textbook edition / authorized Source Matrix, approved Unit Scope, required learning Gates, all Source + Pedagogy Locks, QA and Red Team, and print proof. This PR intentionally **does not** alter the existing PWA, change its learning-evidence database, or claim official student release.
