## Fix: Public Infrastructure Exposure

### Before

```hcl
cidr_blocks = ["0.0.0.0/0"]
```

### After

```hcl
cidr_blocks = ["10.0.0.0/16"]
```

Restricting the CIDR is the minimal safe fix, but the stronger real-world improvement is removing public SSH entirely and using AWS Systems Manager Session Manager instead.
