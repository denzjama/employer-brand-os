---
id: content-planning
---

## Purpose
Brings a draft of next month's content plan to the planning meeting, so the team starts from a balanced proposal instead of a blank page: what goes out, where, for whom, with which pillar and which proof. Its main value is showing the imbalance the team does not see from inside.

## Reads
- `eb/brand-core/evp.md`, `audiences.md`, `facts.md`.
- The current plan and last month's plan, wherever the team keeps it (an export in `eb/inbox/` or a file in `eb/work/content-planning/`).
- The team's goals from `eb/diagnosis/` and the decisions of the last planning meeting.
- Outputs of the idea hub and the social performance review, if the team has them.

## Produces
`eb/work/content-planning/<month>-plan.md`:

```
Month: <month>   Prepared for: <meeting, date>

Calendar
| Date | Channel | Topic | Audience | Pillar | Proof (fact IDs or story) | Owner | Status |

Balance
| Pillar / Audience / Channel | Planned items | Last month | Comment |

Gaps: confirmed proof points never used; audiences with nothing planned
Items without confirmed facts (need confirmation before they are written)
Questions for the meeting
```

## Method
1. Carry over what is already committed: dates, campaigns, events, items moved from last month.
2. Read the goals: which audience and which pillar matter this quarter.
3. Fill the remaining slots with topics that serve the goals, using stories, projects and ideas the team already has.
4. Attach proof to each item: a `CONFIRMED` fact or an approved story. Items without proof are listed separately.
5. Count the balance by pillar, audience and channel against last month and the goals.
6. List gaps: confirmed facts nobody has told, audiences left out.
7. Write questions only the team can answer at the meeting.

## Handoff
Expects: the month, the goals, the committed dates. Returns: the plan path. Acceptance criteria: committed items present; each item has an audience, a pillar and an owner; the balance table is filled; items without confirmed facts are flagged; ready before the meeting.

## Checks before handing over
- The balance counts match the calendar.
- Owners are roles from the roster, not invented people.
- No item depends on a fact that is not `CONFIRMED` without being flagged.

## Never does
- Sets targets or assigns work: it proposes, the meeting decides (P7).
- Schedules or publishes anything (P5).
- Invents dates of events the team has not confirmed.

## Common failures
- A calendar full of topics with no audience or pillar, so the balance cannot be seen.
- Repeating last month with new dates.
- Planning more items than the team has ever delivered in a month.
- Ignoring items that slipped from last month.

## Client specifics to collect
- Where the plan lives today and its format.
- Channels and their posting frequency as the team actually delivers it.
- The planning meeting: when, who, how decisions are recorded.
- Seasonal events of the company and the hiring calendar.
