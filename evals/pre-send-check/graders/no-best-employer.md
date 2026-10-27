---
type: regex
pattern: "лучш(ий|им|его) работодател"
flags: i
match: not_contains
target: {source: file, path: post.md}
---
