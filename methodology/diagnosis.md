# Function diagnosis (Phase 1)

How the system understands an Employer Brand function and decides where agents help. The output is a map of the function, a zone for every process, a proposed agent team and a one-page summary for the CHRO.

## 1. Order of work

1. **Intake.** Index the materials (`workspace.md` §3).
2. **Brand core.** Build it from the materials (`brand-core.md`). The confirmation round can run now or after the interview.
3. **Pre-read.** Read every indexed material and fill a draft function map with what the materials say. Every entry carries its source (`MATERIAL`, with file ID).
4. **Interview.** Ask only what the pre-read did not answer or what needs confirming (§4).
5. **Scoring.** Score every process (§6).
6. **Team proposal.** Waves, the agent roster and the pipelines that connect the agents (§7).
7. **Validation with the future owners.** Each proposed owner says whether the agent is needed and on which real tasks to try it (§7a).
8. **CHRO summary.** One page (§8).
9. **Review and approval with the EB lead.** Walk through the map, the zones, the proposal and the validation results; record changes and approval.
10. **Overview page.** A visual page for the EB lead and the CHRO (§8a).

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
9. **Delegated answers.** The EB lead may forward questions to team leads, and answers may arrive in parts. A block with missing answers is marked partly done (`workspace.md` §6) with who owes what; the interview moves on, and the answers are applied when they arrive. Scores that depend on missing answers are marked provisional.
10. **One-off requests.** If the user interrupts with an urgent task, handle it as a one-off request (`workspace.md` §7), note in the log which process it belongs to, and return to the block where the interview stopped.
11. **Security policy.** If an answer shows that the security policy does not allow sending such materials to an external model, follow `principles.md` P9.

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

Check coverage against the library domains (strategy, research, reputation, content, social, campaigns, creative, quality, analytics, operations). For an uncovered domain, ask once whether the function does anything there.

### Block D. Data and systems
- Where do the materials live (drives, wikis, task trackers)? What can be exported, by whom?
- Which external platforms matter (hh.ru, Dream Job, Habr Career, Telegram, VK, others)? Which statistics are available?
- Which systems hold funnel data (ATS, HCM), and can the team get aggregated exports?
- What does the security policy say about AI tools and about sending internal documents to an external model? Has it been approved, by whom?
- Who in the team has access to the AI tool the system runs on, and who does not? Is access paid personally or by the company?

### Block E. Goals and plans
- Top priorities for the next 6 to 12 months.
- Projects and campaigns planned.
- What has to be shown to the CHRO, and when?

### Block F. Change readiness and rituals
- Which rituals does the team already have: planning, stand-ups, reviews, reports? When and how long?
- What was tried before with AI or automation, and what happened?
- What would make the team resist, and what would make it want to use the agents? Where resistance is mentioned, find its root cause: not aware what it is for; disagrees with the change itself; fears for their role, value or mistakes; distrusts the initiative; sees a real execution problem; record the user's words.
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

**Volume without hours.** Teams often know frequencies but not hours. First ask once for a rough effort per cycle (under an hour; a few hours; a day or more). If there is still no answer, score V from frequency and the number of steps, labelled `ESTIMATE`:

| Frequency | Simple cycle (one person, a few steps) | Multi-step cycle (several people or contractors, rounds of approval) |
|---|---|---|
| Monthly or rarer | 1 | 1 |
| Several times a month to weekly | 1 | 2 |
| Several times a week or daily | 2 | 3 |

A process with X = 3 is never `AUTOMATE`. Zones say who leads the work; in every zone people approve what goes outside (`principles.md` P5).

**Priority** = V + P + T (3 to 9).

## 7. Team proposal

`eb/diagnosis/team-proposal.md`.

**Waves:**
- `WAVE 1`: processes in `AUTOMATE` or `AUGMENT` with D ≥ 2, X ≤ 2 and priority ≥ 6. Take the top 3 to 5 by priority; break ties by lower X, then higher T, then higher R, then a process of a team that no wave-1 agent covers yet. If a tie remains, choose and write the reason in the proposal.
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
| Tool access | Whether the owner has access to the AI tool. If not: who operates the agent for them (an operator with access runs it; the owner decides on the outputs), or the agent waits for access |
| Inputs from | People, agents and brand-core files that feed it |
| Outputs to | Agents and people that receive its results; external-facing results always go through the quality gate |
| Autonomy | Starting level: the library default, lowered if T = 1 or the owner prefers. External-facing agents are capped at `L1` (`autonomy.md`) |
| Ritual | An existing ritual from Block F where possible; a new ritual only if none fits |
| First metric | One metric from the library entry that the owner agrees to track |
| Needed to start | Data, access, templates, decisions |
| Why now | One line from the scores |

**Pipelines.** The team is a system, not a set of personal assistants. The proposal describes 3 to 5 pipelines of the first wave: real recurring tasks of this function, each as a sequence of steps from the person who starts it, through the coordinator and the agents, to the person who decides. Every pipeline that produces something external passes the quality gate. At least one pipeline shows how a correction to the brand core reaches all agents, and one how human decisions in the log reach the retro.

Start from the pipeline library (`library/pipelines/`): take the entries whose agents are all in the first wave, then adapt the steps to the client's people, rituals and roster IDs. Write a custom pipeline only for a recurring task no entry covers. The brand-core loop and the learning loop entries cover the two required loops.

**Machine-readable roster.** Together with the proposal, write `eb/diagnosis/team-roster.json` in the format of `templates/team-roster.sample.json`: the agents of every wave with all fields above, and the pipelines as lists of steps (`from`, `to`, `what`), each with the `library_id` of the pipeline entry it started from, or `CUSTOM`. Steps refer to agent IDs or to `owner`, `lead`, `coordinator`, `brand-core`, `log`. Team assembly (Phase 2) builds from this file, not from the prose.

The proposal ends with what the first two weeks look like for the team: who onboards when, which rituals start, when the first retro happens.

## 7a. Validation with the future owners

Before approval, every proposed owner of a first-wave agent is asked, in person or in writing, using `eb/diagnosis/validation.md`. The file has one section per owner, written for that owner in plain words: what the agent does, why it was proposed (with their own words where they gave them), and four questions:

1. Is the agent needed? (yes / rather yes / no)
2. Which part of the work can it really take, and which part stays manual?
3. On which two or three real tasks do we try it in the first two weeks?
4. Who owns it, and does the proposed first metric fit?

The file ends with a summary table to fill in. Answers change the proposal: a "no" removes or replaces the agent, and the next candidate of the same wave moves up. Approval by the EB lead comes after validation. If the EB lead approves first and asks for validation later, the proposal is marked approved pending validation.

## 8. CHRO summary

`eb/diagnosis/chro-summary.md`. One page, in the language of the conversation, for a reader who has not seen the diagnosis.

1. **Where the function is.** Three to five sentences: mandate, team, main pressure points, with sources.
2. **Where AI helps and where it does not.** Counts by zone and the processes behind them. Current time spent on wave-1 processes, as the team estimates it, labelled as an estimate.
3. **First wave as a system.** The agents, owners and rituals in one table, and the pipelines in one or two sentences each: how a task goes from a person through the agents and back to a person.
4. **What is needed from leadership.** Data access, security decisions, owners' time.
5. **Risks and how they are controlled.** At least: data leaving the company (P9), quality of external communication (P5, the quality gate), team resistance (owners, rituals, the adoption coach).
6. **How we will know it works.** The first metrics and the date of the first review.

No savings forecasts, percentages or ROI that are not measured. Every number in the summary is `CONFIRMED` or labelled as an estimate with its source; targets are written as targets (`brand-core.md` §4.1).

## 8a. Overview page

After approval, build `eb/diagnosis/overview.html` with `scripts/build_overview.py` from data in the format of `templates/overview.sample.json`: the pipelines as an interactive scheme, the first-wave agents as cards with their owners and partners, the processes by zone, readiness for Phase 2 (`workspace.md` §6). Rules:

- light background by default; the reader can switch to dark;
- reader-facing wording only, no internal identifiers (`principles.md` P11);
- no personal data, no `TO CONFIRM` or `EVIDENCE NEEDED` facts as facts;
- it stays a local file. Publishing it as a link, or sending it anywhere, happens only on the user's decision and only if the security policy allows it.

**Before approval:** the summary and the overview are drafts. Their numbers are checked against the fact registry before the user shows them to anyone (`brand-core.md` §6). The summary may say "the team spends about N hours a month on these processes (team estimate); the pilot will measure how much of that the agents take over".

## 9. Outputs

| File | Content |
|---|---|
| `eb/diagnosis/interview-log.md` | Questions, answers, sources; the "for the proposal" list |
| `eb/diagnosis/function-map.md` | §5 |
| `eb/diagnosis/ai-map.md` | Processes grouped by zone, with scores and one-line reasons |
| `eb/diagnosis/team-proposal.md` | §7 |
| `eb/diagnosis/team-roster.json` | §7, for Phase 2 |
| `eb/diagnosis/validation.md` | §7a |
| `eb/diagnosis/overview.html` | §8a |
| `eb/diagnosis/chro-summary.md` | §8 |
| `eb/diagnosis/open-questions.md` | What remains unknown, who can answer, what it blocks |

## 10. Quality check before presenting

- Every process has a source for frequency, effort and pain, or says "not known".
- Every score has a reason; every zone follows the rules in §6.
- No `TO CONFIRM` or `EVIDENCE NEEDED` fact appears as fact in the summary.
- Every proposed agent has an owner, a ritual, tool access or an operator, inputs and outputs.
- The first wave has 3 to 5 pipelines, and every external-facing pipeline passes the quality gate.
- `team-roster.json` matches the proposal.
- Validation answers are applied, or the proposal says it is approved pending validation.
- No invented savings, percentages or benchmarks.
- The CHRO summary and chat messages contain no internal identifiers (`principles.md` P11, `terminology.md`).
