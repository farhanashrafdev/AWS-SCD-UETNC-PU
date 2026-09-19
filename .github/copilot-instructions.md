# GitHub Copilot review instructions

Use these instructions when performing pull request reviews in this repository for the university demo. Keep comments focused, evidence-based, and easy for students to understand.

- Read and follow `agents/security.md` during security reviews.
- Focus on the changed code in the pull request diff instead of producing a generic whole-repository audit.
- Review specifically for authentication, authorization, hardcoded secrets or credentials, unsafe handling of user input, Terraform or infrastructure public exposure, and excessive permissions.
- Explain findings in clear language suitable for university students and avoid unnecessary jargon.
- Do not report speculative issues unless there is concrete evidence in the diff.
- Provide a concrete, specific fix suggestion for every finding you raise.
- Never suggest bypassing tests, branch protection rules, or security checks.
- Treat deterministic workflow failures from `security-gate` and `build-and-test` as authoritative facts when they fail.
- Clearly distinguish between an AI recommendation and a policy-enforced failure that blocks merge.
