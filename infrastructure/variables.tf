variable "region" {
  description = "AWS region for the reference infrastructure."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name prefix applied to every resource in this reference stack."
  type        = string
  default     = "agentic-devsecops-demo"
}

variable "vpc_cidr" {
  description = "CIDR block for the reference VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "cluster_version" {
  description = "Kubernetes version for the reference EKS cluster."
  type        = string
  default     = "1.30"
}

variable "node_instance_types" {
  description = "Instance types for the single managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  description = "Desired node count for the managed node group."
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum node count for the managed node group."
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum node count for the managed node group."
  type        = number
  default     = 3
}
