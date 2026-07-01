# Agentic DevOps on GitHub — Setup & Demo Guide

This repository is set up so a **crew of GitHub Copilot agents** can safely modify
and operate the CI/CD pipeline — always through pull requests, never by pushing to
`main`. This guide explains the architecture, how to apply the kit, how to set up
and manage each agent on GitHub, and a demo storyboard.

> Diagrams: `agentic-devops-architecture.png` (the layers) and
> `agentic-devops-sequence.png` (how the agents communicate).

---

## 1. The idea in one picture

Three layers, and GitHub itself as the message bus:

1. **Governance & wiring** — the files/settings that define and constrain each
   agent.
2. **The agent crew** — four custom agents, each owning one lane, plus built-in
   Copilot code review.
3. **The CI/CD pipeline** — one GitHub Actions workflow with separated stages.

**GitHub is the bus:** an **Issue** is the task, a **pull request + comments** is
the conversation, **status checks** are the signals, and **labels / assignment**
are the routing. There is no hidden orchestrator — every hand-off is a native,
auditable GitHub event.

---

## 2. The crew (`.github/agents/`)

| Agent | Owns | Tools |
|---|---|---|
| `@pipeline-engineer` | build stage + workflow health | read, edit, search, execute |
| `@test-specialist` | test stage + coverage gates | read, edit, search, execute |
| `@security-reviewer` | security stage + DevSecOps + PR security review | read, edit, search |
| `@release-manager` | versioning, changelog, deploy gates | read, edit, search |

Each agent is a Markdown file with YAML frontmatter (`name`, `description`,
`tools`, optional `model` / `mcp-servers`) and a body of guardrails. They stay in
their lane so you can *show* separation of duties in the demo.

---

## 3. Repository file map

```
.
├── .github/
│   ├── agents/
│   │   ├── pipeline-engineer.agent.md
│   │   ├── test-specialist.agent.md
│   │   ├── security-reviewer.agent.md
│   │   └── release-manager.agent.md
│   ├── instructions/
│   │   └── workflows.instructions.md      # rules scoped to workflows via applyTo
│   ├── workflows/
│   │   ├── ci.yml                          # build · test · security · ci-success gate
│   │   ├── codeql.yml                      # SAST
│   │   └── dependency-review.yml           # SCA on PRs
│   ├── ISSUE_TEMPLATE/agent-task.yml       # route a task to an agent
│   ├── copilot-instructions.md             # repo-wide agent rules
│   ├── copilot-setup-steps.yml             # bootstraps the coding agent env
│   ├── dependabot.yml                      # dependency updates
│   ├── CODEOWNERS                          # required reviewers
│   └── pull_request_template.md
├── AGENTS.md                               # agent entry point (root)
├── SECURITY.md                             # where security tools plug in
├── branch-protection.json                  # branch-protection payload for gh api
├── PULL_REQUEST.md                         # ready-to-use PR body
├── apply.sh                                # branch + commit + open PR
└── docs/agentic-devops-setup.md            # this file
```

---

## 4. Apply the kit (create the branch + open the PR)

From the root of your cloned repo, after copying the files in:

```bash
bash apply.sh
```

Or manually:

```bash
git checkout -b agent/setup-agentic-devops
git add .github AGENTS.md SECURITY.md docs branch-protection.json PULL_REQUEST.md
git commit -m "ci: add agentic DevOps pipeline, DevSecOps scaffolding, and agent crew"
git push -u origin agent/setup-agentic-devops
gh pr create --base main --title "Set up agentic DevOps" --body-file PULL_REQUEST.md
```

---

## 5. Enforce the PR-based workflow (branch protection)

Branch protection is a **server-side setting**, not a file. Apply it once:

```bash
gh api -X PUT repos/OWNER/REPO/branches/main/protection --input branch-protection.json
```

This requires: a pull request, **1 CODEOWNERS approval**, the **`ci-success`**
status check, linear history, resolved conversations, and blocks force-pushes and
direct pushes (admins included). Equivalent UI path: **Settings ▸ Branches ▸ Add
branch ruleset** (or classic **Branch protection rules**) targeting `main`.

> Tip: `ci-success` is the single required check on purpose — the individual
> stage jobs can change without breaking protection.

---

## 6. Set up & manage each agent on GitHub

**Custom agents** (public preview) are exactly the "set up each agent" capability:

1. **Define** — the `.github/agents/*.agent.md` files in this kit. Commit them and
   they travel with the repo. (Org-wide agents can live in a root `agents/` dir.)
2. **Select** — on github.com open the **Agents** panel and pick the agent from
   the dropdown, or mention it on an issue:
   `@copilot use the security-reviewer agent to tighten our SAST config`.
3. **Bootstrap the environment** — `.github/copilot-setup-steps.yml` installs
   deps / builds / tests so the agent starts from a working repo.
4. **Wire in tools (MCP)** — give agents external capabilities/data via MCP
   servers, configured in **Settings ▸ Copilot ▸ coding agent** (shared) and/or
   per-agent in the `mcp-servers:` block of an `.agent.md`. The official GitHub
   MCP server exposes your GitHub data to the agent.
5. **Constrain** — `copilot-instructions.md`, `AGENTS.md`, and the path-scoped
   `instructions/*.instructions.md` set the rules every agent must follow.
6. **Add the reviewer agent** — enable **Copilot code review** as an automatic
   reviewer: **Settings ▸ Rules ▸ Rulesets ▸ New branch ruleset**, target `main`,
   enable *Request pull request review from Copilot*.

---

## 7. How to trigger the coding agent

- **From an Issue:** create an issue (use the *DevOps agent task* template),
  assign it to **@copilot**, pick the agent. It works in an isolated Actions env
  and opens a **draft PR**.
- **From chat / the Agents tab / CLI / IDE:** ask Copilot to open a PR for a task.
- **From a workflow (automation):** create + assign an issue to `@copilot`. Note:
  you must use a **fine-grained PAT**, not the built-in `GITHUB_TOKEN` — GitHub's
  anti-loop safeguard stops `GITHUB_TOKEN`-created issues from triggering the
  agent. Give the PAT only `Issues: write` on the target repo, store it as a
  secret, and reference it via `GH_TOKEN`.

---

## 8. Demo storyboard (≈5 minutes)

1. **Show the crew** — open `.github/agents/`; point out four agents, each scoped
   to one lane. (Screen: architecture diagram.)
2. **File a task** — open an Issue from the template, label `area:ci`, assign
   **@copilot**, select `pipeline-engineer`. *"This issue is the task message."*
3. **Watch the hand-off** — the agent reacts, spins up on Actions, and opens a
   **draft PR** with its plan in the description. *"The PR is the conversation."*
4. **Agents talk to each other** — Copilot code review + `@security-reviewer`
   leave inline comments; the coding agent revises automatically. (Screen:
   sequence diagram.)
5. **Show the signals & guardrail** — the `build → test → security → ci-success`
   checks report on the PR; branch protection blocks merge until they pass and a
   human approves. *"Agents never self-merge."*
6. **Approve & merge** — you make the final call. Emphasize: every hop was a
   native GitHub event — visible, logged, auditable.

---

## 9. Safety model (why this is enterprise-safe)

- Agents propose via **pull requests only**; humans review and merge.
- **No CI/CD runs on an agent's PR until a human approves it.**
- Workflow tokens are **least-privilege** (`contents: read` by default).
- Branch protection + CODEOWNERS + `ci-success` gate every change.
- Secrets are referenced via `${{ secrets.* }}` — never committed.
