---
type: regex
pattern: "^\\|[^|\\n]*\\|[^|\\n]*18\\s?%[^|\\n]*\\|\\s*RESULT\\s*\\|"
flags: m
match: contains
target: {source: file, path: eb/brand-core/facts.md}
---
