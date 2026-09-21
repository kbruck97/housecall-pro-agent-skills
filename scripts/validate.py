#!/usr/bin/env python3
"""Offline distribution validation. Deliberately no network or third-party modules."""
import argparse
import ast
import json
from pathlib import Path
import re
import sys

ROOT_FILES = {"AGENTS.md", "README.md", "LICENSE", "NOTICE.md", "DOCUMENT_INDEX.md"}
ROOT_DIRS = {"skills", "docs", "scripts", "tests", "examples", "schemas"}
EXCLUDED_FILES = {"docs/PLAN.md"}
REQUIRED_SKILLS = {
    "hcp-operations", "hcp-foundations", "hcp-customer-accounts", "hcp-jobs-history",
    "hcp-scheduling", "hcp-estimate-follow-up", "hcp-invoice-follow-up", "hcp-pricebook-procurement",
    "hcp-lead-follow-up", "hcp-reference-configuration", "hcp-reporting-exports", "hcp-webhook-recovery",
    "hcp-alpha-data-collection", "hcp-equipment-evidence-adjudication", "hcp-equipment-nameplate-extraction",
    "hcp-equipment-profile-reconciliation", "hcp-trade-equipment", "hcp-trade-equipment-job-review",
    "hvac-equipment-reference-lookup", "hcp-csr-routing", "hcp-customer-service", "hcp-happy-calls",
    "hcp-followup-scanner", "hcp-completed-job-content",
}
PRIVATE_PATTERNS = [
    ("private-home", r"/(?:home|Users)/[A-Za-z][\w.-]*/"),
    ("secret-key", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ("credential-url", r"https?://[^\s/]+:[^\s/@]+@"),
    ("signed-url", r"https?://\S+[?&](?:X-Amz-Signature|signature|access_token)=[^\s<>]+"),
    ("literal-source-id", r"\b(?:job|cus|est|inv)_[a-fA-F0-9]{32}\b"),
    ("private-ip", r"\b(?:127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)\b"),
    ("literal-auth", r"Authorization:\s*(?:Token|Bearer)\s+[A-Za-z0-9_-]{20,}"),
    ("email", r"\b[\w.+-]+@(?!example\.(?:com|org|net)\b)[\w.-]+\.[A-Za-z]{2,}\b"),
]


def distribution_files(root):
    root = Path(root)
    if root.is_symlink():
        raise ValueError("symlink root")
    files = []
    for item in sorted(root.iterdir()):
        if item.name not in ROOT_FILES | ROOT_DIRS:
            continue
        if item.is_symlink():
            raise ValueError("symlink in distribution")
        candidates = [item] if item.is_file() else sorted(item.rglob("*"))
        for path in candidates:
            if path.is_symlink():
                raise ValueError("symlink in distribution")
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            relative = path.relative_to(root)
            if relative.as_posix() in EXCLUDED_FILES:
                continue
            if any(part.startswith(".") or part in {"archive", "backups", "customer-cases"} for part in relative.parts) or path.suffix in {".bak", ".zip", ".gz", ".tar"}:
                raise ValueError("forbidden distribution path: " + str(relative))
            files.append(path)
    return sorted(files)


def frontmatter(text):
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("missing frontmatter")
    header = text[4:].split("\n---\n", 1)[0]
    out = {}
    for line in header.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep or key.strip() != key or key in out:
            raise ValueError("unsupported/duplicate frontmatter field")
        value = value.strip()
        if value.startswith(('"', "'")):
            if value[-1:] != value[:1]:
                raise ValueError("unclosed scalar")
            value = value[1:-1]
        elif ": " in value or value.startswith(("[", "{", "|", ">", "&", "*")):
            raise ValueError("use quoted simple frontmatter scalars")
        out[key] = value
    for key in ("name", "description", "version"):
        if not out.get(key):
            raise ValueError("missing " + key)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", out["name"]):
        raise ValueError("invalid name")
    if out.get("license") != "MIT":
        raise ValueError("skill license must be MIT")
    return out


def validate(root):
    root = Path(root).absolute()
    errors, names = [], set()
    try:
        paths = distribution_files(root)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    for needed in ROOT_FILES:
        if not (root / needed).is_file():
            errors.append("missing " + needed)
    license_path = root / "LICENSE"
    if license_path.is_file():
        license_text = license_path.read_text()
        if not all(term in license_text for term in ("MIT License", "Copyright (c) 2026 Keaton Bruckelmyer", "Permission is hereby granted, free of charge", 'THE SOFTWARE IS PROVIDED "AS IS"')):
            errors.append("invalid MIT license")
    for path in paths:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append(rel + ": non-text/unreadable file")
            continue
        for label, pattern in PRIVATE_PATTERNS:
            if re.search(pattern, text, re.I):
                errors.append(rel + ": privacy pattern " + label)
        if path.name == "SKILL.md":
            try:
                fm = frontmatter(text)
                if fm["name"] in names or fm["name"] != path.parent.name:
                    raise ValueError("duplicate/name-directory mismatch")
                names.add(fm["name"])
            except ValueError as exc:
                errors.append(rel + ": " + str(exc))
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                dest = (path.parent / target.split("#", 1)[0]).resolve()
                if not dest.is_relative_to(root.resolve()) or dest not in {p.resolve() for p in paths}:
                    errors.append(rel + ": broken/escaping link " + target)
                if rel.startswith("skills/") and not dest.is_relative_to((root / "skills" / path.relative_to(root).parts[1]).resolve()):
                    errors.append(rel + ": non-self-contained skill link " + target)
        if path.suffix == ".py":
            try:
                tree = ast.parse(text)
                for node in ast.walk(tree):
                    modules = [a.name for a in node.names] if isinstance(node, ast.Import) else ([node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 else [])
                    for module in modules:
                        if module and module.split(".")[0] not in sys.stdlib_module_names | {"contracts", "validate", "package"}:
                            errors.append(rel + ": undeclared dependency " + module)
            except SyntaxError as exc:
                errors.append(rel + ": syntax " + str(exc))
        if path.suffix == ".json":
            try:
                json.loads(text)
            except ValueError:
                errors.append(rel + ": invalid JSON")
    if names != REQUIRED_SKILLS:
        errors.append("skill coverage mismatch: " + str(sorted(names ^ REQUIRED_SKILLS)))
    try:
        data = json.loads((root / "docs/source-disposition.json").read_text())
        families = data["families"]
        required_families = json.loads((root / "schemas/required-source-families.json").read_text())
        if {x["family"] for x in families} != set(required_families):
            raise ValueError("required source family identity mismatch")
        variants = [v["variant"] for x in families for v in x["variants"]]
        if len(variants) != len(set(variants)):
            raise ValueError("duplicate source variant identity")
        if len(families) != 38 or len({x["family"] for x in families}) != 38 or sum(x["instances"] for x in families) != 123 or sum(len(x["variants"]) for x in families) != 61:
            raise ValueError("source family/instance/variant coverage mismatch")
        for row in families:
            if row["disposition"] not in {"distilled", "excluded"} or not row["reason"] or (row["disposition"] == "distilled" and not row["destinations"]):
                raise ValueError("incomplete source disposition")
            if not set(row["destinations"]) <= names or sum(v["instances"] for v in row["variants"]) != row["instances"]:
                raise ValueError("source destination/variant mismatch")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        errors.append("source coverage: " + str(exc))
    try:
        ledger = json.loads((root / "docs/capabilities.json").read_text())
        ops = ledger["operations"]
        seen = set()
        for op in ops:
            if op["operation"] in seen or op["status"] not in ledger["status_definitions"] or not op["notes"] or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", op["verified_on"]):
                raise ValueError("invalid operation metadata")
            if op["status"] == "official-public" and not str(op["source_url"]).startswith(("https://docs.housecallpro.com/", "https://help.housecallpro.com/")):
                raise ValueError("official operation missing official source")
            seen.add(op["operation"])
        required = json.loads((root / "schemas/required-capabilities.json").read_text())
        if seen != set(required):
            raise ValueError("required capability coverage mismatch")
        for op in ops:
            if required[op["operation"]] != op["status"]:
                raise ValueError("capability status drift requires reviewed contract update")
        for copy in (root / "skills").glob("*/references/capabilities.json"):
            if copy.read_bytes() != (root / "docs/capabilities.json").read_bytes():
                raise ValueError("skill capability copy drift")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        errors.append("capabilities: " + str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    print(json.dumps({"status": "fail" if errors else "pass", "errors": errors}, indent=2))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
