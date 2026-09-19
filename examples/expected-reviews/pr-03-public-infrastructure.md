## Security Agent Review

**Severity:** HIGH  
**Finding:** The Terraform security group allows SSH (port 22) from `0.0.0.0/0`, i.e. the entire internet.

This exposes SSH to brute-force and credential-stuffing attacks from any IP address worldwide, which is a very common real-world breach vector.

### Suggested remediation

1. Restrict `cidr_blocks` to a specific known/trusted range (e.g. a VPN or office CIDR).
2. Prefer eliminating public SSH entirely in favor of AWS Systems Manager Session Manager or a bastion host.
3. Keep the security gate's SEC003 check as a required status check.

**Decision:** Request changes.
