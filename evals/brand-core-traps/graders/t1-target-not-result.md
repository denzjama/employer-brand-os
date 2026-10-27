---
type: regex
pattern: "^\\|[^|\\n]*\\|[^|\\n]*12\\s?%[^|\\n]*\\|\\s*RESULT\\s*\\|"
flags: m
match: not_contains
target: {source: file, path: eb/brand-core/facts.md}
---
