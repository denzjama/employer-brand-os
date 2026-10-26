# Changelog

## 0.1.1 — fixes after the first pilot

The first real diagnosis of an Employer Brand function (51 materials, six interview blocks, a 27-process map) left 25 notes on the plugin. This release addresses those that concern Phase 1.

**Facts**
- A fact is confirmed only by an explicit answer about that fact. A text the user already sent to colleagues does not confirm its numbers.
- The fact registry has a Kind column: result, target, plan, practice, estimate, or unclear. A target is never written as a result; numbers of unclear kind are asked about first.
- Every number in anything that leaves the workspace is listed with its status and kind before the user sends it.
- Minors and credentials found in materials are covered by the personal-data rules.
- Consent to the data notice is given in the conversation that reads the files; a relayed consent is asked again.
- A conflict with the client's security policy is said once, recorded, and left to the user to decide.

**Intake**
- New `scripts/inventory.py`: sizes, pages, PDF text layer (scans), byte-identical duplicates, file names in NFD or with non-breaking spaces.
- `scripts/extract_text.py` reads HTML, keeps scripted counter values (`data-*` attributes), drops inline images and scripts, names extracts by NFC-normalised path.
- Index columns for format, pages and duplicates or versions; a Decisions section for sensitive files, credentials and embedded instructions.
- Extracts of sensitive files are deleted until the user decides.
- Note batches are sized by volume (about 100 pages), not by file count; the core is built in groups and merged when the notes do not fit in one context.

**Diagnosis**
- Interview blocks can be partly done while answers from team leads are awaited; `eb/status.md` has "Waiting for" and "Readiness for Phase 2".
- Volume can be scored from frequency when nobody knows the hours.
- Full tie-break order for the first wave.
- Every proposed agent has tool access (or an operator), inputs and outputs; the first wave is described as 3 to 5 pipelines.
- New `eb/diagnosis/team-roster.json` for Phase 2, in the format of `templates/team-roster.sample.json`.
- New validation step with the future owners before approval (`eb/diagnosis/validation.md`).
- Block D asks about tool access; Block F looks for the root cause of resistance.
- One-off requests during the interview are handled, logged and the interview resumes.
- New overview page: `templates/overview.html` and `scripts/build_overview.py`, light by default with a dark switch, data rendered as text only.

**Library**
- Four new processes: design production, ambassador programme, recruitment campaigns, contractor and paperwork operations. Two new domains: campaigns and operations.

**Not in this release:** the shared team workspace and team assembly (Phase 2).

## 0.1.0

First version: architecture, methodology, a library of 17 processes, and the Phase 1 skills `eb-setup`, `brand-core` and `function-diagnosis`.
