---
applyTo: ".github/workflows/**"
---

# Path-specific rules — GitHub Actions workflows

These rules fire **only** when an agent is working on a file under
`.github/workflows/`. They are additive to `.github/copilot-instructions.md`.

## Security-first workflow edits
- **Default token is read-only.** Never set a top-level `permissions:` broader
  than `contents: read`. Elevate at the **job** level only, with a comment.
- **Pin actions.** Reference third-party actions by version tag at minimum; pin
  to a full commit SHA for production hardening.
- **No secret interpolation into `run:`** in a way that enables shell injection.
  Pass secrets via `env:` and reference the env var, not inline `${{ }}` in a
  shell string built from untrusted input.
- **No `pull_request_target`** with checkout of untrusted code unless you fully
  understand the risk and document it.

## Structure rules
- Keep `build`, `test`, and `security-validation` as **separate jobs**.
- Keep the `ci-success` gate job as the single required status check. Do not
  rename it without coordinating a branch-protection update in the PR body.
- Every step added or changed must carry a `# comment` explaining it.

## Validation before opening the PR
- Confirm YAML is valid and job dependencies (`needs:`) still form a DAG.
- Confirm artifacts produced by `build` are still consumed downstream.
