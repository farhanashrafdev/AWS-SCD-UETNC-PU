output "vpc_id" {
  description = "ID of the reference VPC."
  value       = module.vpc.vpc_id
}

output "cluster_name" {
  description = "Name of the reference EKS cluster."
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Private API endpoint of the reference EKS cluster."
  value       = module.eks.cluster_endpoint
}

output "argocd_namespace" {
  description = "Namespace ArgoCD is installed into."
  value       = helm_release.argocd.namespace
}

output "demo_api_irsa_role_arn" {
  description = "IAM role the demo-api pod assumes via IRSA."
  value       = aws_iam_role.demo_api.arn
}
