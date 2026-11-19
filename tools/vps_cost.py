#!/usr/bin/env python3
"""vps_cost -- query the open VPS pricing tables in this repository.

Pure standard library. Reads the CSV files under data/ and answers the three
questions people actually ask before signing a VPS contract:

  1. which published plan is the cheapest per GB of RAM
  2. what a term of 12 / 24 / 36 months costs at that rate
  3. what the renewal price is, and how far the renewal gap moves

Every figure printed here comes from the CSVs. Figures the tool derives itself
are labelled "derived"; figures the vendor never published are printed as
"not published" rather than filled in.

Examples:
    python tools/vps_cost.py                       # all plans, best RAM value first
    python tools/vps_cost.py --budget 10           # plans at or under $10/month
    python tools/vps_cost.py --provider OVHcloud    # one provider only
    python tools/vps_cost.py --terms               # term totals where published
    python tools/vps_cost.py --renewal             # first term vs renewal
    python tools/vps_cost.py --budget 10 --csv     # machine-readable output
"""

import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data', 'open')


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        sys.exit('missing data file: %s' % path)
    with open(path, newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def num(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def table(rows, headers, aligns=None):
    if not rows:
        return '  (no rows)'
    aligns = aligns or ['l'] * len(headers)
    widths = []
    for i, head in enumerate(headers):
        width = len(head)
        for row in rows:
            width = max(width, len(str(row[i])))
        widths.append(width)
    out = ['  ' + '  '.join(h.ljust(widths[i]) for i, h in enumerate(headers)),
           '  ' + '  '.join('-' * widths[i] for i in range(len(headers)))]
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            text = str(cell)
            cells.append(text.ljust(widths[i]) if aligns[i] == 'l' else text.rjust(widths[i]))
        out.append('  ' + '  '.join(cells))
    return '\n'.join(out)


def cmd_plans(args):
    plans = load('vps-plan-pricing.csv')
    if args.provider:
        wanted = args.provider.lower()
        plans = [p for p in plans if wanted in p['provider'].lower()]
    if args.budget is not None:
        plans = [p for p in plans
                 if num(p['price_usd_per_month']) is not None
                 and num(p['price_usd_per_month']) <= args.budget]
    plans.sort(key=lambda p: num(p['usd_per_gb_ram']) if num(p['usd_per_gb_ram']) is not None
               else float('inf'))

    # The source tables group plans into tier classes, and one plan can sit in two
    # of them (OVHcloud VPS-1 is 2 vCPU / 4 GB, so it is listed against both the
    # 1 GB class and the 4 GB class). Keep one row per plan and say so.
    seen = {}
    collapsed = []
    for p in plans:
        key = (p['provider'], p['plan'])
        if key in seen:
            collapsed.append((p['provider'], p['plan']))
            continue
        seen[key] = p
    plans = list(seen.values())

    rows = []
    for p in plans:
        rate = num(p['price_usd_per_month'])
        annual = '%.2f' % (rate * 12) if rate is not None else 'not published'
        rows.append([
            p['provider'],
            p['plan'],
            p['vcpu'],
            p['ram_gb'],
            p['price_usd_per_month'],
            p['usd_per_gb_ram'],
            p['usd_per_gb_storage'],
            annual,
            p['source_urls'],
        ])
    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(['provider', 'plan', 'vcpu', 'ram_gb', 'price_usd_per_month',
                         'usd_per_gb_ram', 'usd_per_gb_storage',
                         'twelve_month_straight_line_derived', 'source_urls'])
        writer.writerows(rows)
        return
    print('Published plans, cheapest RAM first'
          + (' (budget <= $%s)' % args.budget if args.budget is not None else ''))
    print(table(rows,
                ['provider', 'plan', 'vCPU', 'RAM GB', '$/mo', '$/GB RAM', '$/GB storage',
                 '12mo derived', 'source'],
                ['l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l']))
    print('\n  12mo derived = monthly rate x 12, arithmetic on the published rate only.')
    print('  Source column is the vendor page the row was read from.')
    if collapsed:
        pairs = sorted(set(collapsed))
        print('  %d row(s) collapsed: %s appear in more than one tier class in the'
              ' source tables, with identical prices.'
              % (len(collapsed), ', '.join('%s %s' % pair for pair in pairs)))


def cmd_terms(args):
    rows_in = load('contract-term-total-cost.csv')
    rows = []
    for r in rows_in:
        rows.append([r['provider'], r['plan'], r['displayed_starting_rate_usd_per_month'],
                     r['cost_1_month_usd'], r['cost_12_months_usd'],
                     r['cost_24_months_usd'], r['cost_36_months_usd'], r['source_urls']])
    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(['provider', 'plan', 'rate_usd_per_month', 'cost_1_month_usd',
                         'cost_12_months_usd', 'cost_24_months_usd', 'cost_36_months_usd',
                         'source_urls'])
        writer.writerows(rows)
        return
    print('Published term totals (USD)')
    print(table(rows,
                ['provider', 'plan', '$/mo', '1 mo', '12 mo', '24 mo', '36 mo', 'source'],
                ['l', 'l', 'r', 'r', 'r', 'r', 'r', 'l']))


def cmd_renewal(args):
    rows_in = load('renewal-price-comparison.csv')
    rows = []
    for r in rows_in:
        first = r['first_term_price']
        renewal = r['renewal_price']
        rows.append([r['provider'], first[:52], renewal[:52], r['renewal_to_first_ratio'][:34],
                     r['checked_on'], r['official_pricing_page']])
    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(['provider', 'first_term_price', 'renewal_price',
                         'renewal_to_first_ratio', 'checked_on', 'official_pricing_page'])
        writer.writerows(rows)
        return
    print('First term vs renewal')
    print(table(rows,
                ['provider', 'first term', 'renewal', 'renewal / first', 'checked',
                 'official pricing page'],
                ['l', 'l', 'l', 'l', 'l', 'l']))
    print('\n  "not published" and "Cannot calculate" are the vendor\'s own answer, not a gap here.')


def cmd_payment_methods(args):
    rows_in = load('provider-payment-methods.csv')
    rows = []
    for r in rows_in:
        rows.append([r['field'], r['provider'], r['as_printed_on_provider_page'][:64]])
    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(['field', 'provider', 'as_printed_on_provider_page', 'source_urls'])
        writer.writerows([[r['field'], r['provider'], r['as_printed_on_provider_page'],
                           r['source_urls']] for r in rows_in])
        return
    print('Payment methods as printed on each provider page')
    print(table(rows, ['field', 'provider', 'as printed'], ['l', 'l', 'l']))
    print('\n  "Not printed" means the provider page did not publish it. '
          '"Read blocked" means the page returned an error and was not read.')


def cmd_backups(args):
    rows_in = load('backup-tier-terms.csv')
    rows = []
    for r in rows_in:
        rows.append([r['provider_and_tier'][:34], r['trigger'][:22],
                     r['retention_as_printed'][:26], r['price_as_printed'][:30]])
    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(['provider_and_tier', 'trigger', 'retention_as_printed',
                         'price_as_printed', 'what_the_copy_does_not_include', 'source_urls'])
        writer.writerows([[r['provider_and_tier'], r['trigger'], r['retention_as_printed'],
                           r['price_as_printed'], r['what_the_copy_does_not_include'],
                           r['source_urls']] for r in rows_in])
        return
    print('Backup tiers, terms as printed')
    print(table(rows, ['provider / tier', 'trigger', 'retention', 'price'], ['l', 'l', 'l', 'l']))


def cmd_overage(args):
    rows_in = load('bandwidth-overage-units.csv')
    rows = []
    for r in rows_in:
        rows.append([r['provider'], r['method_as_printed'][:34], r['number_as_printed'][:34]])
    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(['provider', 'method_as_printed', 'number_as_printed', 'unit', 'source_urls'])
        writer.writerows([[r['provider'], r['method_as_printed'], r['number_as_printed'],
                           r['unit'], r['source_urls']] for r in rows_in])
        return
    print('What happens past the traffic allowance')
    print(table(rows, ['provider', 'method as printed', 'number as printed'], ['l', 'l', 'l']))


def main():
    ap = argparse.ArgumentParser(
        description='Query published VPS pricing tables.',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--budget', type=float, metavar='USD',
                    help='only plans at or under this monthly price')
    ap.add_argument('--provider', metavar='NAME', help='filter by provider name')
    ap.add_argument('--terms', action='store_true', help='show published term totals')
    ap.add_argument('--renewal', action='store_true', help='show first term vs renewal')
    ap.add_argument('--payments', action='store_true',
                    help='show payment methods as printed on provider pages')
    ap.add_argument('--backups', action='store_true', help='show backup tier terms')
    ap.add_argument('--overage', action='store_true',
                    help='show how each provider meters traffic past the allowance')
    ap.add_argument('--csv', action='store_true', help='CSV output instead of a table')
    args = ap.parse_args()

    if args.terms:
        cmd_terms(args)
    elif args.renewal:
        cmd_renewal(args)
    elif args.payments:
        cmd_payment_methods(args)
    elif args.backups:
        cmd_backups(args)
    elif args.overage:
        cmd_overage(args)
    else:
        cmd_plans(args)


if __name__ == '__main__':
    main()
