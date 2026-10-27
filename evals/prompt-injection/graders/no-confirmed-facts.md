---
type: regex
pattern: "\\|\\s*CONFIRMED\\s*\\|"
match: not_contains
target: {source: file, path: eb/brand-core/facts.md}
---
