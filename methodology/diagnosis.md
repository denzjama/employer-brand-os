# Function diagnosis (Phase 1)

How the system understands an Employer Brand function and decides where agents help. The output is a map of the function, a zone for every process, a proposed agent team and a one-page summary for the CHRO.

## 1. Order of work

1. **Intake.** Index the materials (`workspace.md` §3).
2. **Brand core.** Build it from the materials (`brand-core.md`). The confirmation round can run now or after the interview.
3. **Pre-read.** Read every indexed material and fill a draft function map with what the materials say. Every entry carries its source (`MATERIAL`, with file ID).
4. **Interview.** Ask only what the pre-read did not answer or what needs confirming (§4).
5. **Scoring.** Score every process (§6).
6. **Team proposal.** Build waves and the agent roster (§7).
7. **CHRO summary.** One page (§8).
8. **Review with the EB lead.** Walk through the map, the zones and the proposal; record changes and approval.

Read first, ask second. The EB lead's time is the scarcest resource in the diagnosis.

## 2. Pre-read

From the materials, extract into `eb/diagnosis/function-map.md` (draft):

- the mandate of the function and its stated goals and KPIs;
- the team: structure, roles, headcount, who owns what;
- processes and recurring activities, with any frequency, volume or effort stated;
- channels, tools and systems mentioned;
- results reported, with periods;
- plans and strategic priorities;
- any statement about AI use, past attempts or constraints.

Each item is tagged `MATERIAL (M0x, location)`. Where the material only implies something, tag it `INFERENCE` and add it to the interview questions as a hypothesis to check.

## 3. Interview rules

1. **One block at a time.** At most four questions per message.
2. **Start from what is known.** Open each block with a short summary of what the materials say, then ask what is missing: "From the strategy deck I understood X. Is that still current? What is missing?"
3. **Hypotheses, not quizzes.** Where an `INFERENCE` exists, state it and ask to confirm or correct.
4. **"Don't know" is an answer.** Record it as an open question, do not push.
5. **Record as you go.** After each answer, append to `eb/diagnosis/interview-log.md`: date, block, question, answer summary in the user's terms, source `INTERVIEW`. Numbers the user estimates are recorded as `ESTIMATE`.
6. **Pausable.** The user can stop at any point. `eb/status.md` records which block is next. A new session resumes from there with a one-line recap.
7. **No advice during the interview.** Ideas that come up go to a "for the proposal" list in the log; the interview stays an interview.
8. **Sensitive answers.** If the user shares something about named people (performance, conflicts), record only what matters for the process ("the owner of X is overloaded"), not the person's details.

## 4. Interview blocks

Skip any question the pre-read already answered with a current source.

### Block A. Mandate and expectations
- What is the function accountable for, and to whom? What does the CHRO expect this year?
- Which goals and KPIs are formal, and which ones does the function itself consider important?
- Which stakeholders matter most: talent acquisition, internal communications, HR business partners, marketing, business units, agencies?
- What would make this year a success for the function?

### Block B. Team
- Structure, roles and headcount; who owns which area.
- Where is the team overloaded, and where are there gaps in skills?
- Who already uses AI, for what, and how often? Who is curious, who is sceptical, and why?
- Which agencies and contractors work with the team, and on what?

### Block C. Processes
Walk through the team's year, month and week. For each recurring activity:
- What is it, who does it, how often?
- How long does it take per cycle (estimate)?
- What goes in, what comes out, which tools?
- What is painful: volume, waiting, quality, rework, coordination?
- What would "better" look like?

Check coverage against the library domains (strategy, research, reputation, content, social, creative, quality, analytics). For an uncovered domain, ask once whether the function does anything there.

### Block D. Data and systems
- Where do the materials live (drives, wikis, task trackers)? What can be exported, by whom?
- Which external platforms matter (hh.ru, Dream Job, Habr Career, Telegram, VK, others)? Which statistics are available?
- Which systems hold funnel data (ATS, HCM), and can the team get aggregated exports?
- What does the security policy say about AI tools and about sending internal documents to an external model?

### Block E. Goals and plans
- Top priorities for the next 6 to 12 months.
- Projects and campaigns planned.
- What has to be shown to the CHRO, and when?

### Block F. Change readiness and rituals
- Which rituals does the team already have: planning, stand-ups, reviews, reports? When and how long?
- What was tried before with AI or automation, and what happened?
- What would make the team resist, and what would make it want to use the agents?
- How much time can owners give to onboarding in the first month?

## 5. Function map

`eb/diagnosis/function-map.md` lists every process, one section each:

| Field | Content |
|---|---|
| ID | `P01`, `P02`, … |
| Name | In the client's words |
| Library match | A library `id`, or `CUSTOM` |
| Owner | Role (and name only if the user gave it) |
| Frequency | As stated, with source |
| Effort | Hours per cycle and per month, with source; `ESTIMATE` where estimated |
| Inputs and tools | |
| Outputs | |
| Pain | In the client's words, with source |
| AI today | What is already used, if anything |
| Scores | §6 |
| Zone | §6 |

A process can map to several library entries, or several processes to one entry. Record both directions.

## 6. Scoring and zones

Score each process on six axes, 1 to 3. When between two scores, choose the lower one and note why. Every score has a one-line reason tied to a source.

| Axis | 1 | 2 | 3 |
|---|---|---|---|
| **V Volume** | A few hours a month | Several hours a week | A day a week or more, or many repetitions |
| **P Pain** | Works fine | Noticeable friction: delays, rework, quality complaints | A recognised problem the EB lead raised unprompted, or a blocker for goals |
| **R Repeatability** | Every cycle is different; the value is judgement or relationships | Common structure with significant case-by-case judgement | Same structure each time; clear inputs and outputs |
| **D Data readiness** | Inputs are not available or not accessible to the system | Inputs exist and can be exported or copied by hand | Inputs are already in the workspace or easy to provide regularly |
| **X Exposure** | Output is used only inside the EB team | Output goes outside after human approval | Legal, safety, personal-data or crisis sensitivity |
| **T Team appetite** | The owner is sceptical or has no time | Neutral, or willing with support | The owner asked for help with it |

**Zone** (apply in order):
1. `HUMAN` if R = 1.
2. `AUTOMATE` if R = 3, D ≥ 2 and X ≤ 2.
3. `AUGMENT` otherwise.

A process with X = 3 is never `AUTOMATE`. Zones say who leads the work; in every zone people approve what goes outside (`principles.md` P5).

**Priority** = V + P + T (3 to 9).

## 7. Team proposal

`eb/diagnosis/team-proposal.md`.

**Waves:**
- `WAVE 1`: processes in `AUTOMATE` or `AUGMENT` with D ≥ 2, X ≤ 2 and priority ≥ 6. Take the top 3 to 5 by priority; break ties by lower X, then higher T.
- `WAVE 2`: the remaining `AUTOMATE` and `AUGMENT` processes with D ≥ 2.
- `DATA FIRST`: processes with D = 1. For each, state what data access would unlock it.
- `HUMAN` processes are listed with a sentence on why they stay with people and, where useful, which agent can feed them (for example a digest that prepares a meeting).

**Always in wave 1:** the quality gate, if any wave-1 agent is external-facing, and the adoption coach.

**For each proposed agent:**

| Field | Content |
|---|---|
| Agent | Library `id` (or `CUSTOM`) and reader-facing name |
| Covers | Function-map process IDs |
| Owner | Role from the function map. An agent without an owner is not proposed (`principles.md` P6) |
| Autonomy | Starting level: the library default, lowered if T = 1 or the owner prefers. External-facing agents are capped at `L1` (`autonomy.md`) |
| Ritual | An existing ritual from Block F where possible; a new ritual only if none fits |
| First metric | One metric from the library entry that the owner agrees to track |
| Needed to start | Data, access, templates, decisions |
| Why now | One line from the scores |

The proposal ends with what the first two weeks look like for the team: who onboards when, which rituals start, when the first retro happens.

## 8. CHRO summary

`eb/diagnosis/chro-summary.md`. One page, in the language of the conversation, for a reader who has not seen the diagnosis.

1. **Where the function is.** Three to five sentences: mandate, team, main pressure points, with sources.
2. **Where AI helps and where it does not.** Counts by zone and the processes behind them. Current time spent on wave-1 processes, as the team estimates it, labelled as an estimate.
3. **First wave.** The agents, owners and rituals, in one table.
4. **What is needed from leadership.** Data access, security decisions, owners' time.
5. **Risks and how they are controlled.** At least: data leaving the company (P9), quality of external communication (P5, the quality gate), team resistance (owners, rituals, the adoption coach).
6. **How we will know it works.** The first metrics and the date of the first review.

No savings forecasts, percentages or ROI that are not measured. The summary may say "the team spends about N hours a month on these processes (team estimate); the pilot will measure how much of that the agents take over".

## 9. Outputs

| File | Content |
|---|---|
| `eb/diagnosis/interview-log.md` | Questions, answers, sources; the "for the proposal" list |
| `eb/diagnosis/function-map.md` | §5 |
| `eb/diagnosis/ai-map.md` | Processes grouped by zone, with scores and one-line reasons |
| `eb/diagnosis/team-proposal.md` | §7 |
| `eb/diagnosis/chro-summary.md` | §8 |
| `eb/diagnosis/open-questions.md` | What remains unknown, who can answer, what it blocks |

## 10. Quality check before presenting

- Every process has a source for frequency, effort and pain, or says "not known".
- Every score has a reason; every zone follows the rules in §6.
- No `TO CONFIRM` or `EVIDENCE NEEDED` fact appears as fact in the summary.
- Every proposed agent has an owner and a ritual.
- No invented savings, percentages or benchmarks.
- The CHRO summary and chat messages contain no internal identifiers (`principles.md` P11, `terminology.md`).
