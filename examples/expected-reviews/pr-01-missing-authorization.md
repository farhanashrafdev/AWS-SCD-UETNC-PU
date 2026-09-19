## Security Agent Review

**Severity:** HIGH  
**Finding:** The user-data endpoint does not require authorization.

The endpoint returns user information but does not verify that the caller is authenticated or permitted to access the requested user ID.

An attacker could request another user's identifier and retrieve information without authorization.

### Suggested remediation

1. Add `[Authorize]` to the endpoint.
2. Verify resource-level access before returning the user.
3. Keep the authorization test as a required check.

**Decision:** Request changes.
