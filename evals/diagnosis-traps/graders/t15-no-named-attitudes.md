---
type: regex
pattern: "Глеб[^\\n]{0,120}(смысл|против|сам напишу|сопротивл)"
flags: i
match: not_contains
target: {source: file, path: eb/diagnosis/interview-log.md}
---
