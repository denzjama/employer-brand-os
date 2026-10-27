---
type: regex
pattern: "AUTOMATE|AUGMENT|TO CONFIRM|EVIDENCE NEEDED|WAVE 1|ESTIMATE"
match: not_contains
target: {source: file, path: eb/diagnosis/overview.html}
---
