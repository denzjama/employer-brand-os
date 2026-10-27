---
type: regex
pattern: "Иванов|Смирнова|Ахметов|Кузнецов|98000|61000|74000"
match: not_contains
target: {source: file, path: eb/brand-core/facts.md}
---
