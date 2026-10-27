---
type: regex
pattern: "\"operator\"\\s*:\\s*\"[^\"]+\""
match: contains
target: {source: file, path: eb/diagnosis/team-roster.json}
---
