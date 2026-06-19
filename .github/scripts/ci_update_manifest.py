"""
CI helper: update esgvoc_manifest.yaml with new version info.

Usage:
  python .github/scripts/ci_update_manifest.py \
    --version 1.2.0 \
    --universe-version 1.0.3 \
    --changelog-file changelog.md
"""

import argparse
import sys

import yaml


def _literal_str_representer(dumper, data):
    """Force multi-line strings to use YAML literal block scalar (|)."""
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, _literal_str_representer)


def main():
    parser = argparse.ArgumentParser(description="Update esgvoc manifest")
    parser.add_argument("--version", required=True, help="New CV version")
    parser.add_argument("--universe-version", required=True, help="Universe version")
    parser.add_argument(
        "--changelog-file",
        default="-",
        help="Path to changelog file, or - for stdin (default: -)",
    )
    parser.add_argument(
        "--manifest",
        default="esgvoc_manifest.yaml",
        help="Path to manifest file (default: esgvoc_manifest.yaml)",
    )
    args = parser.parse_args()

    if args.changelog_file == "-":
        changelog = sys.stdin.read().strip()
    else:
        with open(args.changelog_file) as f:
            changelog = f.read().strip()

    with open(args.manifest) as f:
        manifest = yaml.safe_load(f)

    manifest["cv_version"] = args.version
    manifest["universe_version"] = args.universe_version
    manifest["release_notes"] = changelog + "\n"

    with open(args.manifest, "w") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Updated manifest to version {args.version}")


if __name__ == "__main__":
    main()
