---
type: regex
pattern: "(снизил|сократил)[^\\n]{0,60}12\\s?%"
flags: i
match: not_contains
target: {source: file, path: post.md}
---
