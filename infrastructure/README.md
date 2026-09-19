# Infrastructure (reference only)

This directory is reference-quality Terraform. **Nothing in this
directory is ever applied to a real AWS account as part of this demo.**
`terraform fmt`, `terraform init`, and `terraform validate` are safe and
run in CI (`.github/workflows/terraform-validate.yml`). `terraform plan`
and `terraform apply` are not part of that workflow, and should not be
run against these files without first treating them as a starting point
for a real environment, not a finished one.

## What this stack describes

| File | Purpose |
| --- | --- |
| `main.tf` | Standalone placeholder security group used only by the `security-gate` demo (PR #3 / SEC003). Unrelated to the stack below. |
| `versions.tf` | Provider requirements and provider configuration. |
| `variables.tf` | Every input, each with a sensible default so the config is self-contained. |
| `vpc.tf` | A small two-AZ VPC (`terraform-aws-modules/vpc/aws`). |
| `eks.tf` | A single EKS cluster with one managed node group (`terraform-aws-modules/eks/eks`), private API endpoint only. |
| `iam.tf` | An IRSA role so the demo API can read a secret from AWS Secrets Manager instead of hardcoding it (see `examples/fixes/hardcoded-secret.md`). |
| `argocd.tf` | Installs ArgoCD with Helm, then applies the `AppProject` and root `Application` in `gitops/`, handing continuous deployment over to GitOps. |
| `outputs.tf` | Cluster name/endpoint, VPC ID, ArgoCD namespace, and the IRSA role ARN. |

## If you ever wanted to actually run this

1. You would need real AWS credentials with permission to create a VPC,
   an EKS cluster, IAM roles, and to install Helm releases.
2. You would reconsider `cluster_endpoint_public_access = false` if you
   were not already on a VPN or Direct Connect path to the private
   endpoint.
3. You would run `terraform init`, `terraform plan`, review the plan
   carefully, and only then `terraform apply`.
4. An EKS cluster and its NAT gateway both cost money for every hour
   they exist, whether or not you use them. This is exactly why the
   demo never does step 3.

## Why this exists

The talk's premise is that a secure supply chain includes infrastructure,
not just application code. This stack is the "to ArgoCD stuff" half of
that story: Terraform provisions the platform once, then ArgoCD takes
over continuous delivery by watching `gitops/manifests/demo-api` in this
same Git repository. See `gitops/README.md` for the other half.
