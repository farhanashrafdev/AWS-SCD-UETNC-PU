# Reference-only: shows the secure alternative to the hardcoded secret
# demonstrated in PR #2 (see examples/fixes/hardcoded-secret.md). Instead
# of baking a database password into source code, the demo-api pod
# assumes this role via IRSA and reads the secret from AWS Secrets
# Manager at runtime.

data "aws_iam_policy_document" "demo_api_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [module.eks.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${module.eks.oidc_provider}:sub"
      values   = ["system:serviceaccount:demo-api:demo-api"]
    }
  }
}

resource "aws_iam_role" "demo_api" {
  name               = "${var.project_name}-demo-api-irsa"
  assume_role_policy = data.aws_iam_policy_document.demo_api_assume_role.json

  tags = {
    Project = var.project_name
  }
}

data "aws_iam_policy_document" "demo_api_secrets" {
  statement {
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:${var.region}:*:secret:${var.project_name}/*"]
  }
}

resource "aws_iam_role_policy" "demo_api_secrets" {
  name   = "read-demo-secrets"
  role   = aws_iam_role.demo_api.id
  policy = data.aws_iam_policy_document.demo_api_secrets.json
}
