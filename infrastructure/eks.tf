# Reference-only: one managed EKS cluster with a single managed node
# group. The API endpoint is private-only by default, matching the
# secure-by-default posture used everywhere else in this repository
# (compare infrastructure/main.tf and SEC003 in scripts/security_gate.py).

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.project_name}-cluster"
  cluster_version = var.cluster_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Secure baseline: no public API endpoint. A real rollout would reach
  # this cluster over a VPN, Direct Connect, or a bastion, not the
  # public internet.
  cluster_endpoint_public_access  = false
  cluster_endpoint_private_access = true

  enable_irsa = true

  eks_managed_node_groups = {
    default = {
      instance_types = var.node_instance_types
      desired_size   = var.node_desired_size
      min_size       = var.node_min_size
      max_size       = var.node_max_size
    }
  }

  tags = {
    Project = var.project_name
  }
}
