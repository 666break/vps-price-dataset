# Data dictionary

One section per dataset. Every value is transcribed from the cited public page; nothing is estimated. Where a source did not publish a figure the cell says so. Published alongside the human-readable tables at https://serverbudget.com/compare and the other ServerBudget pages listed below.

All files are in `data/open/`. `manifest.json` records row counts, byte sizes and md5 for each CSV.

## vps-plan-pricing.csv (9 rows)

- **Columns:** `provider`, `plan`, `tier_group`, `tier_reference_spec`, `vcpu`, `ram_gb`, `storage_gb`, `price_usd_per_month`, `usd_per_gb_ram`, `usd_per_vcpu`, `usd_per_gb_storage`, `source_urls`
- **Units:** `vcpu` = vCPU cores; `ram_gb` = GiB RAM; `storage_gb` = GB storage; `price_usd_per_month` = USD/month; `usd_per_gb_ram` = USD per GiB RAM; `usd_per_vcpu` = USD per vCPU; `usd_per_gb_storage` = USD per GB storage; `source_urls` = official provider pricing URL.
- **Source:** https://serverbudget.com/vps-price-compare.html ; each row keeps the provider's own URL (DigitalOcean, OVHcloud, ScalaHosting).
- **Method:** Three published tiers per provider. Per-unit figures are arithmetic from the published monthly price and the published spec, rounded to the precision stored; they are not benchmarks. Introductory-vs-renewal billing wording is kept verbatim in `plan`.

## vps-addon-costs.csv (15 rows)

- **Columns:** `provider`, `feature`, `published_cost_or_terms`, `source_urls`
- **Units:** `published_cost_or_terms` is the source wording (USD/month, a percentage, or an explicit "no separate price" statement); `source_urls` = official provider pricing URL.
- **Source:** https://serverbudget.com/vps-price-compare.html ; provider URLs per row.
- **Method:** Backup, snapshots, dedicated IPv4, bandwidth overage and billing term as printed on each provider's page. Where no separate price is listed, the cell says so rather than assuming zero.

## vps-price-vs-renewal.csv (3 rows)

- **Columns:** `provider`, `plan`, `price_now_usd_per_month`, `renewal_price`, `renewal_gap`, `billing_terms`, `source_urls`
- **Units:** `price_now_usd_per_month` = USD/month; `renewal_price` = source wording (USD/month where published); `renewal_gap` = multiple (x) or `cannot compute`.
- **Source:** https://serverbudget.com/vps-price-compare.html ; provider URLs per row.
- **Method:** Headline price beside renewal price. If the official page publishes no renewal price the cell reads `none published on the official page` and the gap is `cannot compute` — no value is inferred.

## renewal-price-comparison.csv (10 rows)

- **Columns:** `provider`, `plan_and_configuration`, `first_term_price`, `renewal_price`, `renewal_to_first_ratio`, `add_on_fees_with_published_numbers`, `official_pricing_page`, `checked_on`
- **Units:** prices are the source's own wording; `renewal_to_first_ratio` = multiple (x) with the arithmetic shown; `checked_on` = review date (YYYY-MM-DD); `official_pricing_page` = official URL.
- **Source:** https://serverbudget.com/vps-renewal-price.html ; official provider URLs per row.
- **Method:** First-term vs renewal terms as stated on provider pages. A struck-through price is not treated as a renewal price unless the page labels it as one. Add-on amounts are included only where the page published a number. Sensitive wording is preserved verbatim.

## coupon-offers.csv (133 rows)

- **Columns:** `provider`, `offer`, `how_to_get_and_conditions`, `official_source_url`, `review_date`
- **Units:** `review_date` = date the page was read (YYYY-MM-DD); amounts and percentages are the source's own wording; `official_source_url` = official provider page.
- **Source:** the per-provider coupon/promo pages listed on https://serverbudget.com/ (a2hosting, bluehost, chemicloud, cloudways, contabo, domain, dreamhost, fastcomet, godaddy, greengeeks, hetzner, hostgator, hostinger, hostpapa, hostwinds, inmotionhosting, interserver, knownhost, liquidweb, namecheap, ovhcloud, porkbun, scalahosting, siteground, vultr).
- **Method:** Offers and conditions transcribed from official pages with a source URL and review date. Where no code is published the row says so; where a term could not be confirmed the row says `Unconfirmed`. No code was tested and no result is claimed.

## datacenter-region-pricing.csv (6 rows)

- **Columns:** `city`, `entry_tier_usd`, `2_vcpu_tier_usd`, `4_vcpu_tier_usd`, `8_vcpu_tier_usd`, `panel_addon_usd`, `source_urls`
- **Units:** all price columns = USD per month; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/vps-datacenter-region-price.html ; each row's official URL (https://vps.us/kvm-vps/).
- **Method:** Published price by datacenter city across the entry, 2-, 4- and 8-vCPU tiers, plus the published panel add-on. No regional adjustment is applied.

## contract-term-total-cost.csv (4 rows)

- **Columns:** `provider`, `plan`, `displayed_starting_rate_usd_per_month`, `cost_1_month_usd`, `cost_12_months_usd`, `cost_24_months_usd`, `cost_36_months_usd`, `source_urls`
- **Units:** all cost columns = USD total for that term; `displayed_starting_rate_usd_per_month` = USD/month; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/cheap-vps-contract-length-total-cost.html ; official URL per row (https://www.ovhcloud.com/en/vps/).
- **Method:** Term totals are the provider's published monthly rate multiplied by the number of months in the term; the arithmetic is shown by the columns and no discount is invented.

## entry-tier-pricing.csv (4 rows)

- **Columns:** `memory`, `vcpu`, `transfer`, `ssd`, `hourly_usd`, `monthly_usd`, `source_urls`
- **Units:** `memory` = GiB/MiB RAM; `vcpu` = vCPU cores; `transfer` = GiB/month; `ssd` = GB; `hourly_usd` = USD/hour; `monthly_usd` = USD/month; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/cheap-vps-entry-price.html ; official URL per row (https://www.digitalocean.com/pricing/droplets).
- **Method:** Entry tier specs with the published hourly rate beside the published monthly cap, as stated on the official page.

## Notes

- A blank or explicitly unavailable value means the cited source did not publish it; it is not zero.
- These are snapshots, not a live feed. Follow the source URLs and verify current terms before purchasing.
- Reuse licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) with attribution.
