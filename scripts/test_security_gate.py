import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unittest

from security_gate import check_sec001, check_sec002, check_sec003


SECURE_USERS_CONTROLLER = """[ApiController]
[Route("api/users")]
public class UsersController(UserService users) : ControllerBase
{
    [HttpGet("{id:int}")]
    [Authorize]
    public ActionResult<UserDto> GetUser(int id)
    {
        var callerId = User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (callerId != id.ToString())
        {
            return Forbid();
        }
        var user = users.GetById(id);
        return user is null ? NotFound() : Ok(user);
    }
}
"""

VULNERABLE_USERS_CONTROLLER = SECURE_USERS_CONTROLLER.replace("    [Authorize]\n", "")

UNRELATED_HEALTH_CONTROLLER = """[ApiController]
[Route("api/health")]
public class HealthController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok();
}
"""

SECURE_TERRAFORM = """resource "aws_security_group" "demo_ssh" {
  name        = "demo-ssh-access"
  description = "Placeholder security group for the DevSecOps demo"

  ingress {
    description = "SSH access restricted to the demo VPC"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
"""

VULNERABLE_TERRAFORM = SECURE_TERRAFORM.replace('["10.0.0.0/16"]', '["0.0.0.0/0"]')

PUBLIC_HTTPS_TERRAFORM = """resource "aws_security_group" "demo_https" {
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
"""


class Sec001Tests(unittest.TestCase):
    def test_sec001_flags_users_controller_without_authorize(self) -> None:
        findings = check_sec001(r"src\DemoApi\Controllers\UsersController.cs", VULNERABLE_USERS_CONTROLLER)
        self.assertEqual(1, len(findings))
        self.assertEqual("SEC001", findings[0].rule_id)
        self.assertIn("User-data endpoint does not require authorization.", findings[0].message)

    def test_sec001_does_not_flag_secure_users_controller(self) -> None:
        findings = check_sec001(r"src\DemoApi\Controllers\UsersController.cs", SECURE_USERS_CONTROLLER)
        self.assertEqual([], findings)

    def test_sec001_does_not_flag_unrelated_controller(self) -> None:
        findings = check_sec001(r"src\DemoApi\Controllers\HealthController.cs", UNRELATED_HEALTH_CONTROLLER)
        self.assertEqual([], findings)


class Sec002Tests(unittest.TestCase):
    def test_sec002_flags_demo_database_password(self) -> None:
        findings = check_sec002(r"config\demo.env", "DEMO_DATABASE_PASSWORD=not-a-real-password")
        self.assertEqual(1, len(findings))
        self.assertEqual("SEC002", findings[0].rule_id)
        self.assertIn("Hardcoded credential detected.", findings[0].message)

    def test_sec002_ignores_markdown_files(self) -> None:
        findings = check_sec002(r"docs\demo.md", "DEMO_DATABASE_PASSWORD=not-a-real-password")
        self.assertEqual([], findings)

    def test_sec002_ignores_unrelated_variables(self) -> None:
        findings = check_sec002(r"config\demo.env", "SOME_OTHER_VAR=value")
        self.assertEqual([], findings)


class Sec003Tests(unittest.TestCase):
    def test_sec003_flags_public_ssh_ingress(self) -> None:
        findings = check_sec003(r"infrastructure\main.tf", VULNERABLE_TERRAFORM)
        self.assertEqual(1, len(findings))
        self.assertEqual("SEC003", findings[0].rule_id)
        self.assertIn("SSH is exposed to the entire internet.", findings[0].message)

    def test_sec003_ignores_secure_restricted_cidr(self) -> None:
        findings = check_sec003(r"infrastructure\main.tf", SECURE_TERRAFORM)
        self.assertEqual([], findings)

    def test_sec003_ignores_public_non_ssh_port(self) -> None:
        findings = check_sec003(r"infrastructure\main.tf", PUBLIC_HTTPS_TERRAFORM)
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
