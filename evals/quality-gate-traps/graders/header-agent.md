---
type: regex
pattern: "^Agent:\\s*`?(eb-)?employee-stories"
flags: m
match: contains
target: {source: file, path: eb/work/quality-gate/2026-11-02-employee-stories-kran.md}
---
