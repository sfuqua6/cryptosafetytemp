#!/usr/bin/env python3
"""Combine the summary column from weekly incident CSV files."""

import argparse
import csv
import re
import sys
from pathlib import Path


def week_sort_key(path: Path) -> tuple[int, int, int, str]:
    """Sort weekly directories by year and their first/last calendar week."""
    year_match = re.search(r"\d{4}", path.parent.parent.name)
    weeks = [int(value) for value in re.findall(r"\d+", path.parent.name)]

    year = int(year_match.group()) if year_match else 0
    first_week = weeks[0] if weeks else 0
    last_week = weeks[-1] if weeks else first_week
    return year, first_week, last_week, path.parent.as_posix().casefold()


def collect_summaries(weeks_dir: Path) -> list[str]:
    summaries = []
    csv_paths = sorted(weeks_dir.rglob("incidents.csv"), key=week_sort_key)

    for csv_path in csv_paths:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames is None or "summary" not in reader.fieldnames:
                raise ValueError(f"{csv_path} does not have a 'summary' column")

            for row in reader:
                summary = (row.get("summary") or "").strip()
                if summary:
                    summaries.append(summary)

    return summaries


def main() -> int:
    repository_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Combine summaries from every weekly incidents.csv file."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=repository_dir / "weekly_summaries.txt",
        help="output text file (default: weekly_summaries.txt in the repository root)",
    )
    parser.add_argument(
        "--weeks-dir",
        type=Path,
        default=repository_dir / "weeks",
        help="directory containing year/week folders (default: weeks)",
    )
    args = parser.parse_args()

    if not args.weeks_dir.is_dir():
        parser.error(f"weeks directory does not exist: {args.weeks_dir}")

    try:
        summaries = collect_summaries(args.weeks_dir)
        if not summaries:
            raise ValueError(f"No non-empty summaries found under {args.weeks_dir}")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(summaries) + "\n", encoding="utf-8")
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Wrote {len(summaries)} summaries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())