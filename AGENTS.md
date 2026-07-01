# AGENTS.md

This repository is **agent-ready** for DevOps automation. Any AI agent operating
here — including the GitHub Copilot coding agent — must follow the operating
rules in [`.github/copilot-instructions.md`](.github/copilot-instructions.md),
and the workflow-specific rules in
[`.github/instructions/workflows.instructions.md`](.github/instructions/workflows.instructions.md).

Specialized agent profiles live in [`.github/agents/`](.github/agents/):
`pipeline-engineer`, `test-specialist`, `security-reviewer`, `release-manager`.

## TL;DR guardrails
- **Pull requests only** — never push to `main`; humans review and merge.
- **Stay in your lane** — change only the files your agent owns.
- **Least-privilege tokens** — workflow `permissions:` read-only by default.
- **No secrets in code** — use `${{ secrets.NAME }}`.
- **Comment every workflow step** you add or change.

## How work flows (the "communication bus" is GitHub itself)
1. A GitHub **Issue** (labeled by area) is the task message — assign it to
   `@copilot` and pick the right agent.
2. The coding agent works in an isolated Actions environment and opens a
   **draft pull request** (its plan + reasoning live in the PR description/logs).
3. **Copilot code review** and `@security-reviewer` respond with PR comments —
   the agent picks these up automatically and revises.
4. **Status checks** (`build` / `test` / `security-validation` → `ci-success`)
   are the signals; branch protection is the guardrail.
5. A human approves and merges. **Agents never self-merge or self-deploy.**

See [`docs/agentic-devops-setup.md`](docs/agentic-devops-setup.md) for the full
architecture and setup steps.
