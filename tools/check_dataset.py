#!/usr/bin/env python3
"""Validate the shipped open-data CSVs without network access."""

import csv
import hashlib
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "open" / "manifest.json"
DATA = ROOT / "data" / "open"


def fail(message):
    raise SystemExit(f"FAIL: {message}")


def load_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            fail(f"{path.name}: missing header")
        rows = list(reader)
        return reader.fieldnames, rows


def check_manifest():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for item in manifest:
        path = DATA / item["file"]
        if not path.is_file():
            fail(f"manifest file missing: {item['file']}")
        raw = path.read_bytes()
        headers, rows = load_csv(path)
        if len(rows) != item["rows"]:
            fail(f"{item['file']}: row count {len(rows)} != {item['rows']}")
        if len(headers) != item["columns"]:
            fail(f"{item['file']}: column count {len(headers)} != {item['columns']}")
        if len(raw) != item["bytes"]:
            fail(f"{item['file']}: byte count {len(raw)} != {item['bytes']}")
        digest = hashlib.md5(raw).hexdigest()
        if digest != item["md5"]:
            fail(f"{item['file']}: MD5 mismatch")
        print(f"OK manifest: {item['file']} ({len(rows)} rows, {len(headers)} columns)")


def rounded_like(value, published):
    """Round a recomputed value to the precision used in the published cell."""
    quantum = Decimal(1).scaleb(published.as_tuple().exponent)
    return value.quantize(quantum, rounding=ROUND_HALF_UP)


def check_unit_prices():
    path = DATA / "vps-plan-pricing.csv"
    _, rows = load_csv(path)
    checked = 0
    for line, row in enumerate(rows, start=2):
        try:
            price = Decimal(row["price_usd_per_month"])
            vcpu = Decimal(row["vcpu"])
            ram = Decimal(row["ram_gb"])
            storage = Decimal(row["storage_gb"])
        except (KeyError, InvalidOperation):
            fail(f"{path.name}:{line}: invalid price/spec value")
        if min(vcpu, ram, storage) <= 0:
            fail(f"{path.name}:{line}: non-positive specification")
        expected = {
            "usd_per_gb_ram": price / ram,
            "usd_per_vcpu": price / vcpu,
            "usd_per_gb_storage": price / storage,
        }
        for column, value in expected.items():
            try:
                actual = Decimal(row[column])
            except (KeyError, InvalidOperation):
                fail(f"{path.name}:{line}: invalid {column}")
            comparable = rounded_like(value, actual)
            if actual != comparable:
                fail(f"{path.name}:{line}: {column} is {actual}; expected {comparable} at the CSV's published precision")
        checked += 1
    print(f"OK arithmetic: {checked} VPS plan rows")


def main():
    check_manifest()
    check_unit_prices()
    print("All local dataset checks passed. No provider pages were fetched.")


if __name__ == "__main__":
    main()
