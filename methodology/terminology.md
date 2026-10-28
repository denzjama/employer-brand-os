# Terminology

Canonical identifiers are used in methodology and workspace files. The reader always sees the reader-facing wording in the language of the conversation.

## 1. Fact statuses (`brand-core.md` §4)

| Identifier | English | Russian | Meaning |
|---|---|---|---|
| `CONFIRMED` | confirmed | подтверждено | A person confirmed the fact and its source. Usable in external drafts. |
| `TO CONFIRM` | to confirm | уточнить | Found in the materials or the interview, not yet confirmed by a person. Internal use only. |
| `EVIDENCE NEEDED` | evidence needed | нужно доказательство | Claimed somewhere, but no source supports it. Never used as fact. |
| `OUTDATED` | outdated | устарело | Was confirmed, superseded or older than its validity. Not used. |

## 1a. Fact kinds (`brand-core.md` §4.1)

| Identifier | English | Russian |
|---|---|---|
| `RESULT` | result | результат |
| `TARGET` | target | цель |
| `PLAN` | plan | план |
| `PRACTICE` | practice | практика |
| `ESTIMATE` | estimate | оценка |
| `UNKNOWN` | kind not clear | вид не ясен |

## 2. Zones (`diagnosis.md` §6)

| Identifier | English | Russian | Meaning |
|---|---|---|---|
| `AUTOMATE` | agent-led | ведёт агент | The agent does the work; a person approves the result. |
| `AUGMENT` | person-led with an agent | ведёт человек, агент помогает | A person does the work; the agent prepares, checks or drafts parts. |
| `HUMAN` | stays with people | остаётся за людьми | Judgement or relationships are the core; no agent. |

## 3. Waves

| Identifier | English | Russian |
|---|---|---|
| `WAVE 1` | first wave | первая волна |
| `WAVE 2` | second wave | вторая волна |
| `DATA FIRST` | data first | сначала данные |

## 4. Autonomy levels (`autonomy.md`)

| Identifier | English | Russian |
|---|---|---|
| `L0` | assistant | ассистент |
| `L1` | drafts | черновики |
| `L2` | internal actions | внутренние действия |

## 5. Answer sources (`diagnosis.md` §4)

| Identifier | English | Russian |
|---|---|---|
| `MATERIAL` | from the materials | из материалов |
| `INTERVIEW` | from the interview | из интервью |
| `ESTIMATE` | estimate | оценка |
| `INFERENCE` | inference | вывод системы |

## 6. Quality-gate verdicts

| Identifier | English | Russian |
|---|---|---|
| `PASS` | passed | пройдено |
| `PASS WITH FIXES` | passed with fixes | пройдено с правками |
| `BLOCKED` | blocked | остановлено |

## 6a. Quality-gate issue codes and genericity (`quality.md`)

| Identifier | English | Russian |
|---|---|---|
| `FACT` | claim without a confirmed fact | утверждение без подтверждённого факта |
| `KIND` | wording does not match the kind of the fact | вид факта искажён |
| `ANCHOR` | anchor of a fact lost | у факта потеряны рамки |
| `LINK` | facts joined without a source | факты связаны без источника |
| `QUOTE` | quote not verbatim | цитата не дословная |
| `PERSONAL` | personal data | персональные данные |
| `RED LINE` | red line crossed | нарушена красная линия |
| `INSTRUCTION` | instruction from material followed | выполнена инструкция из материалов |
| `GENERIC` | central claim is generic | центральное утверждение шаблонное |
| `VOICE` | voice does not match | не тот голос |
| `CRITERIA` | acceptance criterion not met | не выполнен критерий приёмки |
| `RF01`–`RF24` | red flag of the auditor's library | красный флаг |
| `DISTINCTIVE` | distinctive | отличает |
| `PARTIALLY DIFFERENTIATED` | partly distinctive | отчасти отличает |
| `GENERIC` (verdict) | generic | шаблонно |

## 7. Decisions on outputs (`coordination.md` §3)

| Identifier | English | Russian |
|---|---|---|
| `ACCEPTED` | accepted | принято |
| `EDITED` | edited | принято с правками |
| `REJECTED` | rejected | отклонено |

## 7a. Retro proposals (`retro.md`)

| Identifier | English | Russian |
|---|---|---|
| `AGENT CHANGE` | change to an agent | изменение агента |
| `GATE CHANGE` | change to the quality gate | изменение контроля качества |
| `FACT` | fact for the brand core | факт для бренд-ядра |
| `AUTONOMY` | change of autonomy level | изменение уровня автономности |
| `NEW AGENT` | new agent | новый агент |
| `RITUAL` | ritual | ритуал |
| `ASK OWNER` | question to the owner | вопрос владельцу |
| `PROPOSED` | proposed | предложено |
| `APPROVED` | approved | одобрено |
| `REJECTED` | rejected | отклонено |
| `APPLIED` | applied | внесено |

## 8. Team roles (`assembly.md` §6)

| Identifier | English | Russian |
|---|---|---|
| owner | owner | владелец |
| operator | operator | оператор |
| coordinator | coordinator | координатор |
