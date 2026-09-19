## Fix: Hardcoded Secret

### Before

```text
DEMO_DATABASE_PASSWORD=not-a-real-password
```

### After

```text
(the line is deleted entirely - no secret value lives in source control)
```

Remove the value entirely and inject it at runtime instead. In GitHub Actions, reference `${{ secrets.DATABASE_PASSWORD }}` in a workflow step's `env:` block; for an application deployed to AWS, use AWS Secrets Manager or SSM Parameter Store for the runtime equivalent.
