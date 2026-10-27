# Reference agents

A reference agent is a tested description of a good agent for one library process: how it works step by step, what its result looks like, what the owner accepts and what the owner usually rejects. Team assembly (Phase 2) starts every canonical agent description from its reference, when one exists, and adapts it to the client (`methodology/assembly.md` §2). A process without a reference starts from its library entry alone.

A reference is client-neutral. It holds no client facts, names, numbers or templates; those go into the canonical description's "Client specifics", each with its source.

## Format

Frontmatter: `id`, equal to the file name and to an entry in `../processes/`. Sections, in this order (checked by `scripts/validate_plugin.py`):

1. **Purpose** — what the agent is for, sharper than the library entry: the one job it does well.
2. **Reads** — workspace paths and brand-core files.
3. **Produces** — the path and the structure of the result as a template. Headings in the template are written in the team's language in the canonical description.
4. **Method** — numbered steps from the task to the result.
5. **Handoff** — what the agent expects from the coordinator, what it returns, and the acceptance criteria the coordinator checks.
6. **Checks before handing over** — the checks the agent runs on its own result.
7. **Never does** — the limits, with the principles they come from (`methodology/principles.md`).
8. **Common failures** — what owners reject most often in this kind of work, and how the agent avoids it.
9. **Client specifics to collect** — what assembly looks for in the materials, the interview and the brand core to fill the canonical "Client specifics". What is not found is listed as missing, never invented.

## How a reference becomes a canonical description

| Reference section | Canonical section |
|---|---|
| Purpose | Purpose, rewritten in the client's words |
| Reads, Produces | Reads, Produces, with the client's real paths and channels |
| Method and Common failures | Method: the steps, then the failures to avoid |
| Handoff | Handoff, plus acceptance criteria the owner adds |
| Checks before handing over | Checks before handing over |
| Never does | Never does, plus the client's red lines |
| Client specifics to collect | Client specifics: what was found, with sources, and what is missing |

## Coverage

References exist for the processes most clients start with: `quality-gate`, `employee-stories`, `review-monitoring`, `review-response-drafting`, `project-briefs`, `social-adaptation`, `content-planning`, `eb-metrics-report`, `evp-guardian`, `adoption-coach`. A new reference is added when a process has run at least at one client and its owners' decisions show what a good result is.
