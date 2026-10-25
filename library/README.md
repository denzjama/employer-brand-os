# Process library

The catalogue of typical Employer Brand processes. Phase 1 (diagnosis) maps each client process to an entry here. Phase 2 (team assembly) generates one agent per selected entry. The library is model-independent: plain markdown that any runtime can read.

## Entry format

Every file in `processes/` has this frontmatter, checked by `scripts/validate_plugin.py`:

| Field | Values |
|---|---|
| `id` | kebab-case, equal to the file name without `.md` |
| `domain` | `strategy`, `research`, `reputation`, `content`, `social`, `creative`, `quality`, `analytics`, `adoption` |
| `name` | English name |
| `name_ru` | Russian name, shown to Russian-speaking readers |
| `default_autonomy` | `L0`, `L1` or `L2` (`methodology/autonomy.md`) |
| `external_facing` | `true` if the output can reach people outside the EB team |

And these sections, in this order:

1. **Purpose** — what the process is for, in one paragraph.
2. **Fits when** — signals in the client's materials or interview that this process exists or is needed.
3. **Triggers** — on request, ritual, schedule or event.
4. **Inputs** — what the agent reads. Workspace paths use the layout in `methodology/workspace.md`.
5. **Outputs** — what the agent produces and where it puts it.
6. **Human checkpoint** — who decides what, and when.
7. **Suggested ritual** — where the process lives in the team's week or month.
8. **Metrics** — how the owner and the CHRO see that it works.
9. **Risks and limits** — what can go wrong and what the agent must not do.

## Not in the library

- **Job ads.** Generation is already automated in HCM systems and job boards. A client who still writes ads by hand gets a custom process.
- **System agents.** The coordinator, the architect and the retro agent are part of the system, not processes of the function. Their roles are described in `ARCHITECTURE.md` §2; each gets its methodology file when its phase is built.

## Custom processes

A client process that maps to no entry is recorded in the function map as `CUSTOM` and gets the generic template in Phase 2. Custom processes seen at several clients are candidates for a new library entry.
