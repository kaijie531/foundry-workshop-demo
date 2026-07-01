#!/usr/bin/env bash
# =============================================================================
# apply.sh — drop the agentic-DevOps kit into THIS repo and open a pull request.
#
# Run from the ROOT of your cloned repository, AFTER copying the kit's files in
# (the .github/ tree, AGENTS.md, SECURITY.md, docs/, branch-protection.json,
# PULL_REQUEST.md). Requires the GitHub CLI (`gh auth login` done once).
# =============================================================================
set -euo pipefail

BRANCH="agent/setup-agentic-devops"

echo "▶ Creating branch: $BRANCH"
git checkout -b "$BRANCH"

echo "▶ Staging DevOps files"
git add .github AGENTS.md SECURITY.md docs/agentic-devops-setup.md \
        branch-protection.json PULL_REQUEST.md 2>/dev/null || git add .github AGENTS.md SECURITY.md

echo "▶ Committing"
git commit -m "ci: add agentic DevOps pipeline, DevSecOps scaffolding, and agent crew"

echo "▶ Pushing"
git push -u origin "$BRANCH"

echo "▶ Opening pull request"
gh pr create \
  --base main \
  --head "$BRANCH" \
  --title "Set up agentic DevOps: CI/CD pipeline + DevSecOps + agent crew" \
  --body-file PULL_REQUEST.md

cat <<'NEXT'

✅ PR opened. Two manual follow-ups (server-side settings, not files):

1) Branch protection (require PR + the ci-success check + CODEOWNERS review):
     gh api -X PUT repos/OWNER/REPO/branches/main/protection \
       --input branch-protection.json

2) Enable Copilot as an automatic PR reviewer:
     Settings ▸ Rules ▸ Rulesets ▸ New branch ruleset ▸
       target main ▸ enable "Request pull request review from Copilot".

Then replace the @your-org/... placeholders in .github/CODEOWNERS.
NEXT
