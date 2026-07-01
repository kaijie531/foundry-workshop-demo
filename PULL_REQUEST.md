# Set up agentic DevOps: CI/CD pipeline + DevSecOps + agent crew

## Summary
This PR turns the repository into an **agent-operated DevOps environment**. It adds
a CI/CD pipeline with clearly separated build / test / security stages, DevSecOps
scanning scaffolding, and the configuration that lets a crew of GitHub Copilot
agents safely modify and operate that pipeline **through pull requests only**.

No application code is changed — this is pipeline and automation setup.

## What's included
**Pipeline (GitHub Actions)**
- `.github/workflows/ci.yml` — build, test, and security-validation as separate
  jobs, plus a single stable `ci-success` gate to use as the required check.
- `.github/workflows/codeql.yml` — code scanning (SAST) plug-in point.
- `.github/workflows/dependency-review.yml` — dependency/SCA check on PRs.
- `.github/dependabot.yml` — automated dependency updates.
- `.github/copilot-setup-steps.yml` — bootstraps the coding agent's environment.

**The agent crew (custom agents)**
- `.github/agents/pipeline-engineer.agent.md` — owns the build stage.
- `.github/agents/test-specialist.agent.md` — owns the test stage.
- `.github/agents/security-reviewer.agent.md` — owns DevSecOps + PR security review.
- `.github/agents/release-manager.agent.md` — owns versioning + deploy gates.

**Governance & guardrails**
- `.github/copilot-instructions.md` + root `AGENTS.md` — repo-wide agent rules.
- `.github/instructions/workflows.instructions.md` — security rules scoped to
  `.github/workflows/**` (via `applyTo`).
- `.github/CODEOWNERS` — required reviewers for pipeline/security files.
- `.github/pull_request_template.md` + `.github/ISSUE_TEMPLATE/agent-task.yml`.
- `SECURITY.md` — where each security tool plugs in.
- `docs/agentic-devops-setup.md` — architecture, setup, and demo storyboard.

## Why it's safe for agents
- Agents propose changes **only via pull requests** — they never push to `main`
  and never self-merge or self-deploy.
- Workflow tokens are **least-privilege** (`contents: read` by default).
- Branch protection (see `branch-protection.json`) requires a PR, a CODEOWNERS
  review, and the `ci-success` check before merge.

## Follow-up after merge (not done by this PR)
1. Apply branch protection: `gh api -X PUT repos/OWNER/REPO/branches/main/protection --input branch-protection.json`
2. Replace `@your-org/...` placeholders in `CODEOWNERS`.
3. Enable Copilot code review as an automatic reviewer (Settings ▸ Rules ▸ Rulesets).
4. Set real build/test/scan commands in the placeholder steps.

## How to review
Start with `docs/agentic-devops-setup.md`, then skim `ci.yml`. Every step is
commented to explain what the DevOps agent is doing and why.
