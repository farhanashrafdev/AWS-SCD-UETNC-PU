# Reference-only: installs ArgoCD via Helm, then hands continuous
# deployment over to GitOps by applying the AppProject and root
# Application from gitops/. From that point forward, ArgoCD - not
# Terraform - keeps gitops/manifests/demo-api in sync with the cluster.
# This is the "Terraform to ArgoCD" handoff.

resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "7.6.12"
  namespace        = "argocd"
  create_namespace = true

  # Kept deliberately small: no ingress, no SSO, no HA. A real install
  # would layer those on top of this reference baseline.
  set {
    name  = "configs.params.server\\.insecure"
    value = "false"
  }

  depends_on = [module.eks]
}

# ArgoCD's AppProject and Application are CRDs whose schema ArgoCD itself
# defines. Applying them with kubectl here - rather than a Terraform
# Kubernetes resource - avoids requiring a live cluster connection just
# to run `terraform validate` in CI, and mirrors how real platform teams
# often hand this exact last step off to kubectl or a bootstrap script.
resource "null_resource" "bootstrap_gitops" {
  provisioner "local-exec" {
    command = join(" && ", [
      "kubectl apply -f ${path.module}/../gitops/projects/appproject.yaml",
      "kubectl apply -f ${path.module}/../gitops/apps/demo-api-application.yaml",
    ])
  }

  depends_on = [helm_release.argocd]
}
