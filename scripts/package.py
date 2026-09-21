#!/usr/bin/env python3
"""Deterministic local tar builder and refusal-first staging; never installs profiles."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import tempfile
from validate import EXCLUDED_FILES, distribution_files, validate


def safe_new_path(path):
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("explicit absolute path without traversal required")
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError("symlink destination or ancestor")
    if path.exists():
        raise ValueError("refuse overwrite")
    if not path.parent.is_dir():
        raise ValueError("parent must already exist")
    return path


def build(root, output):
    root = Path(root)
    errors = validate(root)
    if errors:
        raise ValueError("invalid repository: " + "; ".join(errors))
    output = safe_new_path(output)
    if output.is_relative_to(root.resolve()):
        raise ValueError("archive must be outside source tree")
    files = distribution_files(root)
    payloads = [(p.relative_to(root).as_posix(), p.read_bytes()) for p in files]
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in payloads}
    payloads.append(("PACKAGE_MANIFEST.json", (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()))
    # Exclusive creation ensures existing files cannot be overwritten.
    with output.open("xb") as out:
        with tarfile.open(fileobj=out, mode="w", format=tarfile.USTAR_FORMAT) as tar:
            for name, data in sorted(payloads):
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(data), 0o644, 0
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                tar.addfile(info, io.BytesIO(data))
    return {"path": str(output), "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "files": len(payloads)}


def stage(archive, destination):
    destination = safe_new_path(destination)
    # Validation/extraction is in a fresh sibling; untrusted members are never extractall'ed.
    with tempfile.TemporaryDirectory(prefix=".hcp-stage-", dir=destination.parent) as temp:
        temp = Path(temp)
        with tarfile.open(archive, "r:") as tar:
            members = tar.getmembers()
            if len(members) > 5000 or sum(m.size for m in members) > 32 * 1024 * 1024:
                raise ValueError("archive budget exceeded")
            names = set()
            for member in members:
                name = PurePosixPath(member.name)
                if not member.isfile() or name.is_absolute() or ".." in name.parts or "\\" in member.name or name.as_posix() != member.name or member.name in names:
                    raise ValueError("unsafe/duplicate archive member")
                if member.name != "PACKAGE_MANIFEST.json" and (not name.parts or name.parts[0] not in {p.name for p in distribution_roots()}):
                    raise ValueError("unexpected distribution member")
                if member.name in EXCLUDED_FILES:
                    raise ValueError("excluded internal distribution member")
                names.add(member.name)
                target = temp / member.name
                target.parent.mkdir(parents=True, exist_ok=True)
                source = tar.extractfile(member)
                if source is None:
                    raise ValueError("unreadable member")
                with source, target.open("xb") as handle:
                    shutil.copyfileobj(source, handle)
            manifest = json.loads((temp / "PACKAGE_MANIFEST.json").read_text())
            if set(manifest) != names - {"PACKAGE_MANIFEST.json"}:
                raise ValueError("manifest member mismatch")
            for name, digest in manifest.items():
                if hashlib.sha256((temp / name).read_bytes()).hexdigest() != digest:
                    raise ValueError("manifest digest mismatch")
        errors = validate(temp)
        if errors:
            raise ValueError("invalid staged distribution: " + "; ".join(errors))
        # Reserve destination atomically; no overwriting even if another creator raced.
        destination.mkdir(mode=0o700)
        try:
            for child in temp.iterdir():
                shutil.move(str(child), destination / child.name)
        except Exception:
            # Leave partial stage for operator inspection; never claim it succeeded.
            raise
    return {"path": str(destination), "status": "staged-not-installed", "skills": len(list((destination / "skills").glob("*/SKILL.md")))}


def distribution_roots():
    from validate import ROOT_FILES, ROOT_DIRS
    return [Path(p) for p in ROOT_FILES | ROOT_DIRS]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build")
    build_parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    build_parser.add_argument("--output", type=Path, required=True)
    stage_parser = sub.add_parser("stage")
    stage_parser.add_argument("--archive", type=Path, required=True)
    stage_parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build(args.root, args.output) if args.command == "build" else stage(args.archive, args.destination)
        print(json.dumps(result, sort_keys=True))
    except (ValueError, OSError, tarfile.TarError, KeyError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
