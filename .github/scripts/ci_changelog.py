"""
CI helper: generate a markdown changelog from git diff.

Usage:
  python .github/scripts/ci_changelog.py <base_sha>
"""

import argparse
import collections
import subprocess
import sys

# Paths excluded from CV change detection (infrastructure, docs, etc.)
EXCLUDE_PATTERNS = [
    ":(exclude)_src",
    ":(exclude)_tests",
    ":(exclude)_archive",
    ":(exclude)scripts",
    ":(exclude)*.md",
    ":(exclude)*.toml",
    ":(exclude)*.lock",
    ":(exclude)*.py",
    ":(exclude).github",
    ":(exclude)LICENSE*",
    ":(exclude).gitignore",
    ":(exclude).pre-commit-config.yaml",
    ":(exclude)esgvoc_manifest.yaml",
]


def get_diff(base_sha):
    """Run git diff and return the name-status output."""
    cmd = [
        "git", "diff", "--name-status", "--diff-filter=ACDMR",
        f"{base_sha}..HEAD", "--",
    ] + EXCLUDE_PATTERNS

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def parse_diff(diff_output):
    """Parse git diff name-status output into categorized changes."""
    changes = collections.defaultdict(lambda: {"A": [], "M": [], "D": []})
    model_changes = []
    spec_changes = []

    for line in diff_output.split("\n"):
        if not line.strip():
            continue

        parts = line.split("\t")

        if parts[0].startswith(("R", "C")):
            # Renames/copies: "R100\told/path\tnew/path" — treat as add of the new path
            if len(parts) < 3:
                continue
            status = "A"
            path = parts[2]
        elif len(parts) >= 2:
            status = parts[0]
            path = parts[1]
        else:
            continue

        segments = path.split("/")
        filename = segments[-1]

        # Spec files at root level
        if len(segments) == 1 and filename.endswith("_specs.yaml"):
            action = "new" if status == "A" else "updated"
            spec_changes.append((filename, action))
            continue

        if len(segments) < 2:
            continue

        collection = segments[0]

        if filename == "000_context.jsonld":
            action = "new" if status == "A" else "updated"
            model_changes.append((collection, action))
        else:
            term_id = filename.replace(".json", "")
            changes[collection][status[0]].append(term_id)

    return spec_changes, model_changes, changes


def format_changelog(spec_changes, model_changes, term_changes):
    """Format changes into markdown."""
    lines = []

    for filename, action in spec_changes:
        lines.append(f"- {filename}: {action}")

    for collection, action in model_changes:
        lines.append(f"- {collection}: {action} collection model")

    for collection in sorted(term_changes):
        parts = []
        counts = term_changes[collection]
        if counts["A"]:
            parts.append(f'{len(counts["A"])} added')
        if counts["M"]:
            parts.append(f'{len(counts["M"])} modified')
        if counts["D"]:
            parts.append(f'{len(counts["D"])} removed')
        if parts:
            lines.append(f"- {collection}: {', '.join(parts)}")

    return "\n".join(lines) if lines else "No CV changes."


def main():
    parser = argparse.ArgumentParser(description="Generate changelog from git diff")
    parser.add_argument("base_sha", help="Base SHA to diff against")
    args = parser.parse_args()

    diff_output = get_diff(args.base_sha)
    if not diff_output:
        print("No CV changes.")
        sys.exit(0)

    spec_changes, model_changes, term_changes = parse_diff(diff_output)
    print(format_changelog(spec_changes, model_changes, term_changes))


if __name__ == "__main__":
    main()
