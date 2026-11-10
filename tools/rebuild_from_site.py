#!/usr/bin/env python3
"""Rebuild data/vps-plans.csv from the public ServerBudget homepage.

Reads the JSON-LD ItemList embedded in the homepage and writes one CSV row
per published price. Standard library only; no API key, no login.

Usage:
    python tools/rebuild_from_site.py
    python tools/rebuild_from_site.py --source https://serverbudget.com/ --out data/vps-plans.csv
"""

import argparse
import csv
import datetime
import json
import re
import sys
import urllib.request

DEFAULT_SOURCE = "https://serverbudget.com/"
DEFAULT_OUT = "data/vps-plans.csv"
UA = "vps-price-dataset-rebuild/1.0 (public JSON-LD reader)"

FIELDS = [
    "position",
    "provider",
    "plan_label",
    "monthly_usd",
    "type",
    "source_url",
    "site_read_date",
    "rebuilt_at_utc",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def find_itemlist(html):
    pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    for match in re.finditer(pattern, html, re.S):
        try:
            obj = json.loads(match.group(1))
        except (ValueError, TypeError):
            continue
        if isinstance(obj, dict) and obj.get("@type") == "ItemList":
            return obj.get("itemListElement", [])
    raise RuntimeError("no JSON-LD ItemList found on the source page")


def parse_row(item, site_read_date, rebuilt_at):
    name = item.get("name", "").strip()
    url = item.get("url", "").strip()
    prices = re.findall(r"\$([0-9]+(?:\.[0-9]+)?)", name)
    if not prices:
        raise RuntimeError("no price in ItemList name: " + name)
    provider = name.split(" - ")[0].strip()
    kind = "add-on" if "add-on" in provider.lower() else "plan"
    return {
        "position": item.get("position", ""),
        "provider": provider,
        "plan_label": name,
        "monthly_usd": prices[-1],
        "type": kind,
        "source_url": url,
        "site_read_date": site_read_date,
        "rebuilt_at_utc": rebuilt_at,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    html = fetch(args.source)
    items = find_itemlist(html)
    if not items:
        raise RuntimeError("ItemList is empty")

    date_match = re.search(r"Newest read\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", html)
    site_read_date = date_match.group(1) if date_match else ""
    rebuilt_at = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    rows = [parse_row(i, site_read_date, rebuilt_at) for i in items]
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print("wrote %d rows to %s" % (len(rows), args.out))
    if not site_read_date:
        print("warning: source page had no 'Newest read' date", file=sys.stderr)


if __name__ == "__main__":
    main()
