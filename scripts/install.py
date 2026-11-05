#!/usr/bin/env python3
"""Install all six skills without overwriting existing work. Copy is the default."""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

NAMES = (
    "meeting-create-minutes", "meeting-transcript-to-minutes",
    "meeting-create-gmail-draft", "meeting-write-deal-history",
    "meeting-post-slack", "meeting-run-followup",
)


def contents(folder):
    return {p.relative_to(folder): p.read_bytes()
            for p in folder.rglob("*") if p.is_file()}


def install(args):
    workspace = args.workspace.expanduser().resolve()
    if not workspace.is_dir():
        raise ValueError("Workspace must be an existing directory.")
    source = Path(__file__).resolve().parents[1] / "skills"
    target = workspace / ".agents" / "skills"
    pending = []
    for name in NAMES:
        src, dst = source / name, target / name
        if not (src / "SKILL.md").is_file():
            raise ValueError(f"Missing source skill: {name}")
        if dst.is_symlink() and dst.resolve() == src.resolve():
            print(f"Already linked: {name}")
        elif dst.exists() and not dst.is_symlink() and dst.is_dir() and contents(dst) == contents(src):
            print(f"Already copied: {name}")
        elif dst.exists() or dst.is_symlink():
            raise ValueError(f"Existing skill will not be replaced: {dst}\n"
                             "Back up and inspect the existing version before replacing it.")
        else:
            pending.append((src, dst))
    if args.dry_run:
        for _, dst in pending:
            print(f"Would {args.mode}: {dst}")
        return
    if not pending:
        return
    target.mkdir(parents=True, exist_ok=True)
    # Prepare every skill before exposing any new skill to Codex.
    with tempfile.TemporaryDirectory(prefix=".meeting-skills-", dir=target.parent) as scratch:
        staged = Path(scratch)
        for src, dst in pending:
            if args.mode == "copy":
                shutil.copytree(src, staged / dst.name)
            else:
                (staged / dst.name).symlink_to(src, target_is_directory=True)
        for _, dst in pending:
            if dst.exists() or dst.is_symlink():
                raise ValueError(f"Destination changed during installation; not replacing: {dst}")
            (staged / dst.name).rename(dst)
            print(f"Installed ({args.mode}): {dst}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--mode", choices=("copy", "link"), default="copy",
                        help="copy works without symlink privileges; link tracks this checkout")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        install(args)
    except (OSError, ValueError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        if args.mode == "link":
            print("If link creation is restricted, rerun with --mode copy. "
                  "No administrator permission is needed for copying into a writable workspace.",
                  file=sys.stderr)
        else:
            print("Choose a workspace you can write to. Existing skills are never overwritten.",
                  file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
