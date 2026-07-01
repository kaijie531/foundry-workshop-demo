# Copilot Instructions — Agentic DevOps repository

This repository is operated by a **crew of DevOps agents** (GitHub Copilot custom
agents) working alongside humans. These instructions apply to **every** Copilot
request in this repo. Path-specific rules for workflow files live in
`.github/instructions/workflows.instructions.md`.

## The crew (see `.github/agents/`)
| Agent | Owns |
|---|---|
| `@pipeline-engineer` | build stage + Actions workflow health |
| `@test-specialist` | test stage + coverage gates |
| `@security-reviewer` | security-validation stage + DevSecOps scanners + PR security review |
| `@release-manager` | versioning, changelog, deploy gates |

Select an agent from the **Agents** panel, or mention it on an issue:
`@copilot use the pipeline-engineer agent to …`.

## Golden rules (all agents, all requests)
1. **Pull requests only.** Never push to `main`. Use a feature branch
   (`agent/<area>-<slug>`). A human reviews and merges — agents never self-merge.
2. **Least privilege.** Workflow `permissions:` are read-only by default;
   elevate one job only when it truly needs write scope, and comment why.
3. **No secrets in code.** Use `${{ secrets.NAME }}` only. Never inline tokens,
   keys, or credentials.
4. **Stay in your lane.** Change only files your agent owns. If a task spans
   lanes, open a focused PR and hand off (comment/mention the right agent).
5. **Keep the gate stable.** `ci-success` is the single required status check.
   Don't rename it without updating branch protection.
6. **Comment your work.** Every workflow step you add or change carries a comment
   describing what it does and why.
7. **DevOps scope only.** This repo's automation kit is about the pipeline —
   don't rewrite application code to make a pipeline task pass.

## Where things live
| Concern | File |
|---|---|
| Build / test / security stages + gate | `.github/workflows/ci.yml` |
| Code scanning (SAST) | `.github/workflows/codeql.yml` |
| Dependency review (SCA) | `.github/workflows/dependency-review.yml` |
| Dependency updates | `.github/dependabot.yml` |
| Coding-agent environment bootstrap | `.github/copilot-setup-steps.yml` |
| Where to plug in security tools | `SECURITY.md` |
| Review ownership | `.github/CODEOWNERS` |
| How it all fits + how to apply | `docs/agentic-devops-setup.md` |

## Definition of done for any pipeline change
- [ ] Change is in a PR, not a direct push.
- [ ] Build / test / security stages remain clearly separated.
- [ ] New third-party actions are version-pinned.
- [ ] `ci-success` still passes.
- [ ] Docs updated if behavior changed.
