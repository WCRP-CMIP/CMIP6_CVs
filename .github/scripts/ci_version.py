"""
CI helper: version management for CV releases.

Subcommands:
  fetch-current   Read registry JSON from stdin, print current stable version.
  fetch-universe  Read registry JSON from stdin, print current universe version.
  compute-next    Given --current and --bump, print the next semver version.
"""

import argparse
import json
import sys


def fetch_version(data):
    """Extract the latest non-prerelease, non-dev version from a registry index."""
    for release in data.get("releases", []):
        version = release.get("version", "")
        if version == "dev-latest" or release.get("is_prerelease"):
            continue
        return version.lstrip("v")
    return "0.0.0"


def cmd_fetch_current(args):
    data = json.load(sys.stdin)
    print(fetch_version(data))


def cmd_fetch_universe(args):
    data = json.load(sys.stdin)
    print(fetch_version(data))


def cmd_compute_next(args):
    parts = [int(x) for x in args.current.split(".")]
    if len(parts) != 3:
        print(f"error: invalid version '{args.current}'", file=sys.stderr)
        sys.exit(1)

    if args.bump == "major":
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif args.bump == "minor":
        parts[1] += 1
        parts[2] = 0
    elif args.bump == "patch":
        parts[2] += 1
    else:
        print(f"error: invalid bump type '{args.bump}'", file=sys.stderr)
        sys.exit(1)

    print(".".join(str(p) for p in parts))


def main():
    parser = argparse.ArgumentParser(description="CI version helper")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("fetch-current", help="Read registry JSON from stdin, print current version")
    sub.add_parser("fetch-universe", help="Read registry JSON from stdin, print universe version")

    next_parser = sub.add_parser("compute-next", help="Compute next semver version")
    next_parser.add_argument("--current", required=True, help="Current version (e.g. 1.2.3)")
    next_parser.add_argument("--bump", required=True, choices=["major", "minor", "patch"])

    args = parser.parse_args()

    commands = {
        "fetch-current": cmd_fetch_current,
        "fetch-universe": cmd_fetch_universe,
        "compute-next": cmd_compute_next,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
