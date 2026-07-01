# Security & DevSecOps

This repo ships **placeholders** for security scanning so tools plug in without
restructuring the pipeline. Each section says exactly where the tool goes.
Owner of this file and the scanners: the **`@security-reviewer`** agent.

## 1. Secret scanning
- **Native:** enable GitHub secret scanning + push protection
  (Settings ▸ Advanced Security / Code security).
- **Pipeline plug-in point:** `ci.yml` ▸ job `security-validation` ▸ step
  *"Secret scan (placeholder)"*. Drop in `gitleaks/gitleaks-action` or
  `trufflesecurity/trufflehog`.

## 2. Static analysis (SAST)
- **Wired up:** `.github/workflows/codeql.yml` — set your languages in the
  `matrix.language` list to activate.
- **Extra linters** (semgrep, bandit, eslint-security) go in `ci.yml` ▸
  `security-validation` ▸ *"Static analysis (SAST)"*.

## 3. Dependency scanning (SCA)
- **On PRs:** `.github/workflows/dependency-review.yml` blocks vulnerable or
  disallowed dependencies. Tune `fail-on-severity` and `deny-licenses`.
- **Automated updates:** `.github/dependabot.yml` — add a block per ecosystem.
- **Alternative:** Snyk or OWASP Dependency-Check go in `ci.yml` ▸
  `security-validation` ▸ *"Dependency check"*.

## 4. Container / IaC scanning (optional)
- Add Trivy or Checkov as a new step in `security-validation` if the repo builds
  images or defines infrastructure.

## Making a scan block merges
Add the check's job name (e.g. `Dependency review`, `Analyze (…)`) to the
required status checks in your branch-protection ruleset — see
`docs/agentic-devops-setup.md`.

## Reporting a vulnerability
Use private security advisories (Security ▸ Advisories ▸ *Report a
vulnerability*) or email `security@your-org` <!-- replace -->.
