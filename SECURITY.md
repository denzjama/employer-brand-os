# Security policy

## Reporting a vulnerability

Report privately through GitHub: the **Security** tab of this repository → **Report a vulnerability**. Do not open a public issue for a vulnerability.

Include the plugin version (`.claude-plugin/plugin.json`), the steps or the file that reproduces the problem, and what an attacker gains. Use fictional data in the report: never attach real client materials.

The project has one maintainer. Fixes go into the latest release; older versions are not patched.

## What counts

- A way to write outside an agent's own folder, into the brand core, the team descriptions or the decision log, past the write guard (`hooks/`, `scripts/eb_hooks.py`).
- A crafted client file (docx, pptx, xlsx, html) that makes text extraction read or write files outside the workspace, expand entities, or exhaust memory.
- A plugin script that reaches the network or sends workspace data anywhere.
- Instructions inside client materials that make the system publish or send something, change a fact's status, or bypass the quality gate, when the plugin's own rules should have stopped it.
- Personal data that the plugin writes into the brand core or into results against `methodology/principles.md`.

## What does not count

- How the model provider processes data. That depends on the client's Claude plan; see Anthropic's documentation.
- Vulnerabilities in Claude Code itself. Report them to Anthropic.
- A model producing a weak or wrong draft that the quality gate flags. That is a quality issue: open a normal issue.

For the client's information security team, the data flows and built-in limits are described in [`docs/security-ru.md`](docs/security-ru.md) (in Russian).
