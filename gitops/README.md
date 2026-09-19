# GitOps manifests (reference only)

This directory is never applied to a real cluster as part of this demo.
It exists to show what ArgoCD would watch once `infrastructure/argocd.tf`
installed it.

## Layout

- `projects/appproject.yaml` - the ArgoCD `AppProject` that scopes what
  the demo is allowed to deploy: one source repository, one destination
  namespace, a small allow-list of resource kinds.
- `apps/demo-api-application.yaml` - the ArgoCD `Application` (the "root"
  app) that points at `manifests/demo-api` in this repository and keeps
  it continuously synced.
- `manifests/demo-api/` - plain Kubernetes manifests for the demo API:
  namespace, service account (annotated for the IRSA role from
  `infrastructure/iam.tf`), deployment, and service.

## The handoff from Terraform

`infrastructure/argocd.tf` installs ArgoCD with Helm and then applies
`projects/appproject.yaml` and `apps/demo-api-application.yaml` directly,
as its last step. From that point on, ArgoCD - not Terraform - is what
keeps the cluster in sync with `manifests/demo-api`. Terraform manages
the platform; ArgoCD manages what runs on it.

## Container image

`gitops/manifests/demo-api/deployment.yaml` references an image that is
never built or pushed as part of this demo. `src/DemoApi/Dockerfile`
shows how that image would be built. A real pipeline would build, scan,
and push it to a registry (ECR, GHCR, ...) and pin an immutable digest
in the manifest instead of a floating tag.
