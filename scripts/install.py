#!/usr/bin/env python3
"""Link all shared skills into a workspace; never replace existing skills."""
import argparse
from pathlib import Path

NAMES = (
    "meeting-create-minutes", "meeting-transcript-to-minutes",
    "meeting-create-gmail-draft", "meeting-write-deal-history",
    "meeting-post-slack", "meeting-run-followup",
)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace.expanduser().resolve()
    if not workspace.is_dir():
        parser.error("workspace must be an existing directory")
    source = Path(__file__).resolve().parents[1] / "skills"
    target = workspace / ".agents" / "skills"
    pending = []
    for name in NAMES:
        src, dst = source / name, target / name
        if not (src / "SKILL.md").is_file():
            parser.error(f"missing skill: {name}")
        if dst.is_symlink() and dst.resolve() == src.resolve():
            print(f"Already linked: {name}")
        elif dst.exists() or dst.is_symlink():
            parser.error(f"existing skill will not be replaced: {dst}")
        else:
            pending.append((src, dst))
    # Preflight all six before making any changes.
    for src, dst in pending:
        if not args.dry_run:
            target.mkdir(parents=True, exist_ok=True)
            dst.symlink_to(src, target_is_directory=True)
        print(f"{'Would link' if args.dry_run else 'Linked'}: {dst}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
