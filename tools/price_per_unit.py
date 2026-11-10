#!/usr/bin/env python3
"""Check and rank the per-unit VPS price table.

Verifies that every $/GB RAM, $/vCPU and $/GB storage figure in
data/price-per-unit.csv really equals the published monthly price divided by
the published spec, then prints a sorted Markdown table.

Usage:
    python tools/price_per_unit.py
    python tools/price_per_unit.py --sort usd_per_gb_storage --tier mid --top 5
    python tools/price_per_unit.py --check-only
"""

import argparse
import csv
import sys

DEFAULT_CSV = "data/price-per-unit.csv"
METRICS = ("usd_per_gb_ram", "usd_per_vcpu", "usd_per_gb_storage")


def load(path):
    # utf-8-sig also tolerates files saved with a UTF-8 BOM.
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def check(rows):
    bad = []
    for row in rows:
        price = float(row["monthly_usd"])
        for metric, spec in (
            ("usd_per_gb_ram", "ram_gb"),
            ("usd_per_vcpu", "vcpu"),
            ("usd_per_gb_storage", "storage_gb"),
        ):
            divisor = float(row[spec])
            raw = row[metric].strip()
            stated = float(raw)
            # The published figures are rounded to a fixed number of decimals.
            # Compare at that same precision instead of imposing an arbitrary
            # epsilon that would reject legitimate rounding.
            decimals = len(raw.split(".")[1]) if "." in raw else 0
            expected = round(price / divisor, decimals)
            if abs(expected - stated) > 1e-9:
                bad.append(
                    "%s %s: %s states %s, computed %s"
                    % (row["tier"], row["provider"], metric, raw, expected)
                )
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--sort", choices=METRICS, default="usd_per_gb_ram")
    ap.add_argument("--tier", choices=("entry", "mid", "high"), default="")
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    rows = load(args.csv)
    bad = check(rows)
    if bad:
        print("CHECK FAILED (%d mismatch(es)):" % len(bad))
        for line in bad:
            print("  " + line)
        return 1
    print("CHECK OK: %d rows, all per-unit figures recompute correctly." % len(rows))

    if args.check_only:
        return 0

    if args.tier:
        rows = [r for r in rows if r["tier"] == args.tier]
    rows.sort(key=lambda r: float(r[args.sort]))
    if args.top:
        rows = rows[: args.top]

    print("\n| Tier | Provider | vCPU | RAM (GB) | Storage (GB) | $/mo | $/GB RAM | $/vCPU | $/GB storage |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        print(
            "| {tier} | {provider} | {vcpu} | {ram_gb} | {storage_gb} | {monthly_usd} | "
            "{usd_per_gb_ram} | {usd_per_vcpu} | {usd_per_gb_storage} |".format(**r)
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
