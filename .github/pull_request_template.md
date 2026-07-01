<!-- Pull request template — applies to human- and agent-authored PRs. -->
## What does this PR do?
<!-- One-line summary. If the DevOps agent opened this PR, it fills this in. -->

## Which agent / lane?
- [ ] `@pipeline-engineer` (build)
- [ ] `@test-specialist` (test)
- [ ] `@security-reviewer` (security / DevSecOps)
- [ ] `@release-manager` (release / deploy)
- [ ] Human

## Type of change
- [ ] CI/CD pipeline change
- [ ] Security / DevSecOps change
- [ ] Documentation
- [ ] Other

## Checklist
- [ ] Scoped to DevOps / automation (no unrelated app code)
- [ ] Build, test, and security-validation stages remain separated
- [ ] `ci-success` gate passes
- [ ] No secrets, tokens, or credentials committed
- [ ] Workflow `permissions:` remain least-privilege
- [ ] New third-party actions are version-pinned
- [ ] A CODEOWNERS reviewer is assigned

## Agent notes
<!-- If an agent opened this PR: what changed, why, and what it validated. -->
