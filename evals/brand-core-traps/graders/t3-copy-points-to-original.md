---
type: regex
pattern: "копия\\)[^\\n]*\\|\\s*M\\d+"
match: contains
target: {source: file, path: eb/inbox/_index.md}
---
