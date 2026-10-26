---
id: contractor-operations
domain: operations
name: Contractor and paperwork operations
name_ru: Подрядчики и документооборот
default_autonomy: L1
external_facing: true
---

## Purpose
Keeps the routine of working with contractors under control: task statements for contractors from approved briefs, a tracker of what was ordered, delivered and accepted, document checklists for each stage, and reminders of deadlines. Contracts, prices and legal terms stay with people and the procurement and legal functions.

## Fits when
- The team works with many contractors and loses time tracking deliveries and documents.
- The same document packages are assembled again and again for procurement.

## Triggers
An approved project brief; the weekly tracker review; a delivery or a document arriving.

## Inputs
Approved briefs; the tracker `eb/work/contractor-operations/tracker.md`; the client's procurement checklists in `eb/team/procurement.md`.

## Outputs
Task statement drafts for contractors; the updated tracker with overdue items flagged; per-stage document checklists.

## Human checkpoint
The project owner approves and sends every task statement; procurement and legal handle contracts and payments.

## Suggested ritual
The weekly team meeting: the tracker's overdue list is one agenda item.

## Metrics
Overdue deliveries and documents; time spent on contractor routine, as the team reports it.

## Risks and limits
Never drafts contract terms, prices or legal clauses, never commits the company to anything, never contacts contractors. Commercial terms of contractors stay out of the workspace unless the user decides otherwise.
