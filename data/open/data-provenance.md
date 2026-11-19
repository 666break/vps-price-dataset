# Data provenance

Where each CSV in `data/` came from, and how the numbers were read.

## Rules the extraction followed

1. **Every figure comes from a vendor's own page.** No price is estimated, no
   monthly rate is converted to an hourly rate, no two currencies are averaged.
2. **A missing figure stays missing.** When a vendor's page does not publish a
   renewal price or an add-on amount, the cell says `not published` or
   `Cannot calculate`. Those cells are kept rather than dropped, because the
   absence is itself a finding.
3. **Footnote markers are resolved to URLs.** The source pages mark each figure
   with a marker such as `[S1]` and list those markers in their own source
   section. The extraction resolves every marker to the URL recorded there, so
   each row keeps a working pointer to the page it was read from.
4. **The read date travels with the number.** `review_date` on the coupon sheet
   and `checked_on` on the renewal sheet are the dates a human read the vendor
   page. They are not publication dates.

## File by file

| File | Source page | Read on |
|---|---|---|
| `vps-plan-pricing.csv` | `serverbudget.com/vps-price-compare` | 2026-11-10 |
| `vps-addon-costs.csv` | `serverbudget.com/vps-price-compare` | 2026-11-10 |
| `vps-price-vs-renewal.csv` | `serverbudget.com/vps-price-compare` | 2026-11-10 |
| `renewal-price-comparison.csv` | `serverbudget.com/vps-renewal-price` | 2026-11-08 |
| `coupon-offers.csv` | 26 provider pages, e.g. `serverbudget.com/vultr-coupon-code` | 2026-09-25, 2026-10-13, 2026-10-26, 2026-10-27 |
| `datacenter-region-pricing.csv` | `serverbudget.com/vps-datacenter-region-price` | 2026-11-11 |
| `contract-term-total-cost.csv` | `serverbudget.com/cheap-vps-contract-length-total-cost` | 2026-11-14 |
| `entry-tier-pricing.csv` | `serverbudget.com/cheap-vps-entry-price` | 2026-11-12 |
| `provider-payment-methods.csv` | `serverbudget.com/vps-payment-methods` | 2026-11-19 |
| `backup-tier-terms.csv` | `serverbudget.com/vps-backup-tier-comparison` | 2026-11-18 |
| `included-transfer-allowances.csv` | `serverbudget.com/included-transfer-by-tier` | 2026-11-18 |
| `storage-extension-costs.csv` | `serverbudget.com/vps-storage-extension-cost` | 2026-11-18 |
| `bandwidth-overage-units.csv` | `serverbudget.com/vps-overage-throttle-vs-metered` | 2026-11-19 |
| `managed-db-metering-objects.csv` | `serverbudget.com/managed-database-engine-prices` | 2026-11-18 |

The per-row `source_urls` column holds the vendor URL the row itself points at,
which is the more precise pointer of the two.

## Notes on specific columns

- **`tier_group` and `tier_reference_spec`** come from the three published tier
  tables on the price comparison page. The same plan can appear in more than one
  tier class: OVHcloud VPS-1 is a 2 vCPU / 4 GB machine, so it is listed against
  both the 1 GB class and the 4 GB class at the same price. The rows are kept as
  published; `tools/vps_cost.py` collapses them and says how many it collapsed.
- **`published_cost_or_terms`** is one text column rather than a number plus a
  note, because several providers express an add-on as a percentage of the plan
  price plus a per-GB rate, and splitting that into one number would be a guess.
- **`renewal_to_first_ratio`** carries the vendor's own arithmetic where the
  vendor published one, and `Cannot calculate` where it did not.
- **`cost_12_months_usd` and the other term columns** are the straight-line
  totals published on the contract-length page, which states them for OVHcloud
  VPS-1 to VPS-4.
- **Datacenter region pricing** is tier pricing read from the plan page the
  source page records as `[S1]`; all six cities carry the same four tier prices
  and the same control-panel add-on.

## Reproducing the extraction

The extraction runs from the site source, not from these CSVs. The generator and
the per-file checksums it produced are kept alongside the site source.
