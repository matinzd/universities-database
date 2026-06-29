#!/usr/bin/env python3
"""Check universities/*.json for duplicate domains and university names across all country files."""

import argparse
import glob
import json
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--universities-dir", default="universities")
    args = parser.parse_args()

    country_files = sorted(glob.glob(f"{args.universities_dir}/*.json"))
    if not country_files:
        print(f"No JSON files found in {args.universities_dir}/", file=sys.stderr)
        sys.exit(1)

    all_universities = []
    for path in country_files:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        all_universities.extend(data["universities"])

    errors = []

    seen_domains = {}
    for uni in all_universities:
        for domain in uni["domains"]:
            if domain in seen_domains:
                errors.append(
                    f"Duplicate domain '{domain}': appears in both "
                    f"'{seen_domains[domain]}' and '{uni['name']}'"
                )
            else:
                seen_domains[domain] = uni["name"]

    seen_names = {}
    for uni in all_universities:
        key = uni["name"].strip().lower()
        if key in seen_names:
            errors.append(
                f"Duplicate name '{uni['name']}': already exists as '{seen_names[key]}'"
            )
        else:
            seen_names[key] = uni["name"]

    if errors:
        print("Duplicate check failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"No duplicates found ({len(all_universities)} universities, {len(seen_domains)} domains)")


if __name__ == "__main__":
    main()
