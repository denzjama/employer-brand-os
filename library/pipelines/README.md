# Pipeline library

A pipeline is a recurring task of the function that goes from the person who starts it, through the coordinator and the agents, to the person who decides. The team proposal in Phase 1 starts its pipelines from these entries when the agents they need are in the wave, and adapts the steps to the client (`methodology/diagnosis.md` §7). Team assembly turns each roster pipeline into a command.

## Format

Frontmatter, checked by `scripts/validate_plugin.py`:

| Field | Values |
|---|---|
| `id` | kebab-case, equal to the file name without `.md` |
| `name` | English name |
| `name_ru` | Russian name, shown to Russian-speaking readers |
| `agents` | The library processes the pipeline needs, comma-separated |
| `external_facing` | `true` if the result can leave the EB team |

Sections, in this order:

1. **Purpose** — the task the pipeline does and the result the person gets.
2. **Fits when** — signals in the diagnosis that the team needs it.
3. **Trigger** — what starts it and who.
4. **Steps** — a table with the columns `From`, `To`, `What`. `From` and `To` are library process IDs from `agents`, or `owner`, `lead`, `coordinator`, `brand-core`, `log`. The table is copied into the roster as the pipeline's steps.
5. **Decision** — who decides on the result and what is recorded.
6. **Variants** — common adaptations: an extra agent, an operator, a shorter path.
7. **Risks and limits** — what goes wrong in this pipeline and how the steps prevent it.

Rules for every entry:

- An external-facing pipeline passes the quality gate, and the gate's result goes to the person who decides (`owner` or `lead`), never straight out.
- The last step records the person's decision in the `log`.
- No step publishes or sends anything: people do, after the pipeline (`methodology/principles.md` P5).

## In the roster

A roster pipeline built from an entry keeps its ID in `library_id`. It may rename the pipeline, add or drop steps, and use the client's roster IDs for the agents; the rules above still hold. A pipeline that matches no entry has `library_id: CUSTOM`.
