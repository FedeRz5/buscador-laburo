#!/usr/bin/env python3
"""Revisa archivos publicables; no sustituye una auditoría del historial."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMAIL = re.compile(r"[\w.+-]+@([\w.-]+\.[A-Za-z]{2,})")
SECRET = re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}")
MARKERS = {
    "CLAUDE.md": "[YOUR_NAME]",
    "cv/main_example.tex": "[YOUR_NAME]",
    "cover_letters/cover_example.tex": "[YOUR NAME]",
    ".claude/skills/job-application-assistant/01-candidate-profile.md": "[NOMBRE]",
    ".claude/skills/job-application-assistant/02-behavioral-profile.md": "[FORTALEZAS]",
    ".claude/skills/job-application-assistant/04-job-evaluation.md": "[YOUR_PRIMARY_SKILLS]",
}

def findings(name, data):
    issues = []
    if SECRET.search(data):
        issues.append("posible credencial")
    if any(domain.lower() not in {"example.com", "example.org", "example.net"} for domain in EMAIL.findall(data)):
        issues.append("correo fuera de los dominios de ejemplo; revisar")
    if name in MARKERS and MARKERS[name] not in data:
        issues.append("plantilla pública personalizada")
    return issues

def main():
    errors = []
    if (ROOT / ".git").exists():
        raw = subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT)
        paths = {ROOT / name for name in raw.decode("utf-8").split("\0") if name}
    else:
        paths = {p for p in ROOT.rglob("*") if p.is_file() and "node_modules" not in p.parts}
    for path in sorted(paths):
        if not path.is_file():
            continue
        name = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv", ".zip"}:
            errors.append(f"{name}: documento o archivo de datos que requiere revisión")
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        errors.extend(f"{name}: {issue}" for issue in findings(name, data))
    for error in errors:
        print(error)
    print(f"Publicación: {len(errors)} hallazgos en archivos actuales. El historial requiere revisión separada.")
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(main())
