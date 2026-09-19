# agentic-devsecops-demo

> A developer opens a pull request.  
> A security agent reviews the change.  
> A deterministic security check blocks unsafe code.  
> The developer fixes it.  
> The pull request becomes mergeable.

## DevOps

```text
Code → Build → Test → Deploy
```

## DevSecOps

```text
Code → Security Checks → Build → Deploy
```

## X as Code

This repository shows that more than application code can live in version control. Infrastructure can be described in Terraform. Security instructions can live in `agents/security.md`. Repository review guidance can live in `.github/copilot-instructions.md`. Deterministic security policy can live in `scripts/security_gate.py`. Each of these files becomes visible, reviewable, and repeatable.

## Security agent

The file `agents/security.md` gives the AI reviewer a focused security persona for pull requests. In this demo, that guidance is used through GitHub Copilot's pull request review feature so students can compare an AI review comment with the actual code diff.

## Deterministic enforcement

The file `scripts/security_gate.py` is the repeatable enforcement layer. It makes scriptable pass or fail decisions in CI based on known rules, independent of any AI judgment or wording.

## Human approval

The agent explains risk, but it does not approve or merge its own reviewed work. A human reviewer makes the final decision after reading the review and checking the required status checks.

## Demo flow

```text
Developer opens PR
Security agent reviews the diff
Security gate detects a known violation
GitHub blocks the merge
Developer fixes the issue
Checks pass
Human approves the PR
```

## Repository map

- `.github/` - GitHub workflows, pull request templates, and Copilot instructions
- `agents/` - the security agent persona used for reviews
- `src/DemoApi/` - the minimal Web API used in the demo
- `tests/` - xUnit tests
- `scripts/security_gate.py` - the deterministic security gate
- `infrastructure/` - placeholder Terraform that is never applied
- `examples/` - prepared expected reviews and fixes for the three demo pull requests
- `docs/` - the presenter demo guide and screenshot checklist

## Run it locally

Run the API tests:

```text
dotnet test tests/DemoApi.Tests
```

Run the deterministic security gate:

```text
python scripts/security_gate.py
```

## Screenshots

### 1. The vulnerable diff
Shows the insecure change introduced in the first demo pull request.  
_Screenshot pending: `docs/screenshots/01-vulnerable-diff.png`_

### 2. The agent review
Shows the GitHub Copilot security review comment on the pull request.  
_Screenshot pending: `docs/screenshots/02-agent-review.png`_

### 3. The failed security gate
Shows the deterministic check failing with the expected rule output.  
_Screenshot pending: `docs/screenshots/03-security-gate-failed.png`_

### 4. The blocked merge
Shows GitHub preventing merge while required checks are failing.  
_Screenshot pending: `docs/screenshots/04-merge-blocked.png`_

### 5. The fix commit
Shows the prepared fix commit that removes the unsafe change.  
_Screenshot pending: `docs/screenshots/05-fix-commit.png`_

### 6. Checks passed
Shows both required checks passing after the fix is pushed.  
_Screenshot pending: `docs/screenshots/06-checks-passed.png`_

For the full presenter walkthrough, see `docs/DEMO-GUIDE.md`.
