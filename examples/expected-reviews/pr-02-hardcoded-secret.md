## Security Agent Review

**Severity:** CRITICAL  
**Finding:** A demonstration database password is hardcoded in source control (`DEMO_DATABASE_PASSWORD=not-a-real-password`).

Even fake-looking secrets committed to source control teach a bad habit and normalize an unsafe delivery pattern.

In a real system, a hardcoded secret in a public or later-compromised repository could be extracted from git history forever.

### Suggested remediation

1. Remove the hardcoded value entirely.
2. Use GitHub Actions encrypted secrets (`${{ secrets.NAME }}`) for CI/CD or AWS Secrets Manager / Parameter Store for runtime configuration.
3. Rotate any credential that was ever committed, even to a private repo.

**Decision:** Request changes.
