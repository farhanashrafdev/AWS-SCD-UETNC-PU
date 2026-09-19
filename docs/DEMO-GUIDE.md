# Demo Guide

This runbook is written for presenters delivering the live university talk.

## Repository setup

1. Clone the repository to your demo machine.
2. Open the repository in your editor or terminal.
3. Confirm your local branch is up to date with the remote branch you plan to present from.
4. Open the GitHub repository page and confirm the **Actions** tab is enabled and visible.
5. Open the **Pull requests** tab and make sure the three prepared demo branches are available on the remote.

## Ruleset configuration

These protections are **not active by default**. The repository content alone cannot self-enforce branch protection. The repository owner must manually create the ruleset in GitHub.

1. Open the repository on GitHub.
2. Go to **Settings**.
3. Select **Rules**.
4. Select **Rulesets**.
5. Click **New branch ruleset**.
6. Give it a clear name such as `Main branch protection`.
7. Set the target branch to `main`.
8. Enable **Require a pull request before merging** and require at least **1 approval**.
9. Enable **Require conversation resolution before merging**.
10. Enable **Require status checks to pass**.
11. Add both required checks:
    - `build-and-test`
    - `security-gate`
12. Enable **Block force pushes**.
13. Save the ruleset.

## How to open each demo PR

Use these prepared branches:

1. `demo/01-missing-authorization` - demonstrates **SEC001**.
2. `demo/02-hardcoded-secret` - demonstrates **SEC002**.
3. `demo/03-public-ssh` - demonstrates **SEC003**.

For each one:

1. Open **Pull requests** on GitHub.
2. Click **New pull request**.
3. Set the base branch to `main`.
4. Set the compare branch to the demo branch.
5. Create the pull request with a short title that matches the scenario.

## How to request a GitHub Copilot code review

On the pull request page:

1. Click **Reviewers** using the gear icon.
2. Select **Copilot**.

Alternative:

1. Add a PR comment containing `@copilot review`.

## What to explain while checks run

Use these talking points:

- Both checks run in parallel.
- `build-and-test` compiles the API and runs its tests.
- `security-gate` runs the deterministic Python scanner.
- The AI review is advisory: it explains risk and suggests fixes.
- The deterministic gate is authoritative: it returns a pass or fail result that can block merge.

## When to capture screenshots

Use `docs/screenshots/README.md` as the checklist during rehearsal or the live demo.

- Capture **01-vulnerable-diff.png** immediately after opening PR 1 and showing the changed code.
- Capture **02-agent-review.png** after Copilot posts its review comment.
- Capture **03-security-gate-failed.png** when the failed `security-gate` check shows **SEC001**.
- Capture **04-merge-blocked.png** when the merge button is disabled because required checks have not passed.
- Capture **05-fix-commit.png** after you push the prepared fix commit and show it in the PR timeline or commit list.
- Capture **06-checks-passed.png** once both required checks turn green.
- Capture **07-merge-ready.png** when the pull request is ready for human approval and merge.
- Optionally capture **08-optional-hardcoded-secret.png** and **09-optional-public-infrastructure.png** when showing PR 2 and PR 3.

## How to push the prepared fix

Each demo branch already has a prepared fix commit locally, but it is **not pushed yet**. After showing the failing pull request, push the matching branch live.

Command pattern:

```text
git push origin demo/01-missing-authorization
git push origin demo/02-hardcoded-secret
git push origin demo/03-public-ssh
```

Run only the command that matches the branch you are currently demonstrating.

## How to recover if Copilot review is unavailable

Fallback plan:

1. Open the matching file in `examples/expected-reviews/`.
2. Copy or read the prepared review text.
3. Paste it as a manual PR comment or read it aloud.
4. Tell the audience clearly: **this is a prepared demonstration, not a live AI review**.

Do not present the prepared text as if Copilot generated it live.

## How to demonstrate the deterministic security gate locally

On the secure `main` branch:

```text
python scripts/security_gate.py
echo $LASTEXITCODE
```

In PowerShell, a secure branch should return exit code `0`.

On a demo branch with a known violation:

```text
python scripts/security_gate.py
echo $LASTEXITCODE
```

Expected result in PowerShell:

- exit code `1`
- printed rule output such as `SEC001`

If you are using bash instead, show the exit code with:

```text
python scripts/security_gate.py
echo $?
```

## Touring the infrastructure and GitOps layer (reference only)

This part of the repository is for discussion, not execution. Never run
`terraform apply` or `kubectl apply` against these files during the
talk.

1. Open `infrastructure/README.md` and explain the reference-only rule
   up front, before showing any code.
2. Open `infrastructure/vpc.tf` and `infrastructure/eks.tf` and point out
   the secure default: `cluster_endpoint_public_access = false`.
3. Open `infrastructure/iam.tf` and connect it back to PR 2: this IRSA
   role is the real fix for the hardcoded secret, not just deleting the
   line from source.
4. Open `infrastructure/argocd.tf` and explain the handoff: Terraform
   installs ArgoCD with Helm and applies one root `Application`, then
   ArgoCD takes over.
5. Open `gitops/apps/demo-api-application.yaml` and
   `gitops/manifests/demo-api/deployment.yaml` and explain that this is
   what ArgoCD would continuously reconcile against the cluster.
6. Show the `terraform-validate` check passing on GitHub Actions and
   explain that this is the one part of this layer that is real: syntax
   and type validation with no credentials and no real resources.

### Optional extension if time allows

Add two to three minutes after the ten-minute version to walk through
the section above. Keep it conceptual: no terminal commands are run
against AWS or a cluster.

## Five-minute version of the demo

1. **0:00-1:00** - Introduce the repository, the pull request, and the idea of AI review plus deterministic policy.
2. **1:00-3:00** - Open PR 1, show the vulnerable diff, request Copilot review, and show the failing `security-gate` result.
3. **3:00-4:00** - Push the prepared fix for PR 1 and refresh the pull request.
4. **4:00-5:00** - Show green checks, explain that a human still approves the change, and close with the key lesson.

## Ten-minute version of the demo

1. **0:00-1:30** - Introduce the repository structure and explain the difference between AI review and deterministic enforcement.
2. **1:30-4:00** - Walk through PR 1 in detail: vulnerable diff, Copilot review, failed `security-gate`, and blocked merge.
3. **4:00-5:30** - Push the prepared fix for PR 1 and show the checks passing.
4. **5:30-7:30** - Open PR 2 and explain how the same pattern applies to **SEC002** for hardcoded secrets.
5. **7:30-9:00** - Open PR 3 and explain how **SEC003** covers public infrastructure exposure such as public SSH access.
6. **9:00-10:00** - Summarize the lesson: AI explains risk, deterministic checks enforce policy, and humans decide whether code merges.
