from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re


SKIP_DIRS = {".git", "bin", "obj", "node_modules", ".terraform", ".vs"}
SEC002_PATTERN = re.compile(r"DEMO_(AWS_SECRET|DATABASE_PASSWORD)\s*=\s*\S+")
INGRESS_START_PATTERN = re.compile(r"\bingress\b\s*\{", re.MULTILINE)


@dataclass
class Finding:
    rule_id: str
    severity: str
    path: str
    line: int
    message: str


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _build_message(rule_id: str, severity: str, title: str, path: str, remediation: str) -> str:
    return (
        f"{rule_id} {severity}: {title}\n"
        f"File: {path}\n"
        f"Remediation: {remediation}"
    )


def check_sec001(path: str, text: str) -> list[Finding]:
    """Deterministic check for a missing authorization attribute on the demo user endpoint."""
    if Path(path).suffix.lower() != ".cs":
        return []

    basename = Path(path).name
    looks_like_controller = bool(re.match(r"^users.*controller\.cs$", basename, re.IGNORECASE))
    looks_like_users_route = 'route("api/users' in text.lower()
    has_http_action = "[http" in text.lower()
    has_authorize = "[authorize" in text.lower()

    if (looks_like_controller or looks_like_users_route) and has_http_action and not has_authorize:
        marker = text.lower().find("[http")
        line = _line_number(text, marker if marker >= 0 else 0)
        return [
            Finding(
                rule_id="SEC001",
                severity="HIGH",
                path=path,
                line=line,
                message=_build_message(
                    "SEC001",
                    "HIGH",
                    "User-data endpoint does not require authorization.",
                    path,
                    "Add [Authorize] and verify resource-level access.",
                ),
            )
        ]
    return []


def check_sec002(path: str, text: str) -> list[Finding]:
    """Deterministic check for the demo's intentionally hardcoded secret patterns."""
    path_segments = [segment.lower() for segment in re.split(r"[\\/]+", path) if segment]
    if Path(path).suffix.lower() == ".md" or "scripts" in path_segments:
        return []

    findings: list[Finding] = []
    for match in SEC002_PATTERN.finditer(text):
        findings.append(
            Finding(
                rule_id="SEC002",
                severity="CRITICAL",
                path=path,
                line=_line_number(text, match.start()),
                message=_build_message(
                    "SEC002",
                    "CRITICAL",
                    "Hardcoded credential detected.",
                    path,
                    "Remove the secret and use a secret-management mechanism.",
                ),
            )
        )
    return findings


def check_sec003(path: str, text: str) -> list[Finding]:
    """Deterministic Terraform check for public SSH access in ingress blocks."""
    if Path(path).suffix.lower() != ".tf":
        return []

    findings: list[Finding] = []
    for match in INGRESS_START_PATTERN.finditer(text):
        open_brace_index = text.find("{", match.start())
        if open_brace_index < 0:
            continue

        depth = 1
        index = open_brace_index + 1
        while index < len(text) and depth > 0:
            char = text[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            index += 1

        if depth != 0:
            continue

        body = text[open_brace_index + 1 : index - 1]
        if (
            re.search(r"from_port\s*=\s*22\b", body)
            and re.search(r"to_port\s*=\s*22\b", body)
            and re.search(r'cidr_blocks\s*=\s*\[[^\]]*0\.0\.0\.0/0[^\]]*\]', body)
        ):
            line = _line_number(text, match.start())
            findings.append(
                Finding(
                    rule_id="SEC003",
                    severity="HIGH",
                    path=path,
                    line=line,
                    message=_build_message(
                        "SEC003",
                        "HIGH",
                        "SSH is exposed to the entire internet.",
                        path,
                        "Restrict the CIDR range or use a private access mechanism.",
                    ),
                )
            )
    return findings


def _scan_text(display_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(check_sec001(display_path, text))
    findings.extend(check_sec002(display_path, text))
    findings.extend(check_sec003(display_path, text))
    return findings


def _scan_path(display_path: str, actual_path: Path) -> list[Finding]:
    try:
        text = actual_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    return _scan_text(display_path, text)


def scan_file(path: str) -> list[Finding]:
    """Read one UTF-8 text file and run the deterministic demo checks."""
    return _scan_path(path, Path(path))


def scan(root: str) -> list[Finding]:
    """Walk a directory tree and run the deterministic demo checks on each file."""
    findings: list[Finding] = []
    root_path = Path(root)
    for current_root, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        for filename in filenames:
            full_path = Path(current_root) / filename
            display_path = os.path.relpath(full_path, root_path)
            findings.extend(_scan_path(display_path, full_path))
    return findings


def main(argv: list[str]) -> int:
    """CLI entry point for the deterministic CI security gate used in the demo."""
    repo_root = Path(__file__).resolve().parent.parent
    targets = argv or [str(repo_root)]

    findings: list[Finding] = []
    for target in targets:
        target_path = Path(target)
        if target_path.is_dir():
            findings.extend(scan(target))
        else:
            findings.extend(scan_file(target))

    for finding in findings:
        print(finding.message)
        print(
            f"::error file={finding.path},line={finding.line},title={finding.rule_id}::"
            f"{finding.message.splitlines()[0]}"
        )

    if findings:
        print(f"Security gate failed: {len(findings)} violation(s) found.")
        return 1

    print("Security gate passed: no violations found.")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv[1:]))
