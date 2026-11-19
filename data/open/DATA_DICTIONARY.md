# Data dictionary

One section per dataset. Every value is transcribed from the cited public page; nothing is estimated. Where a source did not publish a figure the cell says so. Published alongside the human-readable tables at https://serverbudget.com/compare and the other ServerBudget pages listed below.

All files are in `data/open/`. `manifest.json` records row counts, byte sizes and md5 for each CSV.

## vps-plan-pricing.csv (9 rows)

- **Columns:** `provider`, `plan`, `tier_group`, `tier_reference_spec`, `vcpu`, `ram_gb`, `storage_gb`, `price_usd_per_month`, `usd_per_gb_ram`, `usd_per_vcpu`, `usd_per_gb_storage`, `source_urls`
- **Units:** `vcpu` = vCPU cores; `ram_gb` = GiB RAM; `storage_gb` = GB storage; `price_usd_per_month` = USD/month; `usd_per_gb_ram` = USD per GiB RAM; `usd_per_vcpu` = USD per vCPU; `usd_per_gb_storage` = USD per GB storage; `source_urls` = official provider pricing URL.
- **Source:** https://serverbudget.com/vps-price-compare ; each row keeps the provider's own URL (DigitalOcean, OVHcloud, ScalaHosting).
- **Method:** Three published tiers per provider. Per-unit figures are arithmetic from the published monthly price and the published spec, rounded to the precision stored; they are not benchmarks. Introductory-vs-renewal billing wording is kept verbatim in `plan`.

## vps-addon-costs.csv (15 rows)

- **Columns:** `provider`, `feature`, `published_cost_or_terms`, `source_urls`
- **Units:** `published_cost_or_terms` is the source wording (USD/month, a percentage, or an explicit "no separate price" statement); `source_urls` = official provider pricing URL.
- **Source:** https://serverbudget.com/vps-price-compare ; provider URLs per row.
- **Method:** Backup, snapshots, dedicated IPv4, bandwidth overage and billing term as printed on each provider's page. Where no separate price is listed, the cell says so rather than assuming zero.

## vps-price-vs-renewal.csv (3 rows)

- **Columns:** `provider`, `plan`, `price_now_usd_per_month`, `renewal_price`, `renewal_gap`, `billing_terms`, `source_urls`
- **Units:** `price_now_usd_per_month` = USD/month; `renewal_price` = source wording (USD/month where published); `renewal_gap` = multiple (x) or `cannot compute`.
- **Source:** https://serverbudget.com/vps-price-compare ; provider URLs per row.
- **Method:** Headline price beside renewal price. If the official page publishes no renewal price the cell reads `none published on the official page` and the gap is `cannot compute` — no value is inferred.

## renewal-price-comparison.csv (10 rows)

- **Columns:** `provider`, `plan_and_configuration`, `first_term_price`, `renewal_price`, `renewal_to_first_ratio`, `add_on_fees_with_published_numbers`, `official_pricing_page`, `checked_on`
- **Units:** prices are the source's own wording; `renewal_to_first_ratio` = multiple (x) with the arithmetic shown; `checked_on` = review date (YYYY-MM-DD); `official_pricing_page` = official URL.
- **Source:** https://serverbudget.com/vps-renewal-price ; official provider URLs per row.
- **Method:** First-term vs renewal terms as stated on provider pages. A struck-through price is not treated as a renewal price unless the page labels it as one. Add-on amounts are included only where the page published a number. Sensitive wording is preserved verbatim.

## coupon-offers.csv (133 rows)

- **Columns:** `provider`, `offer`, `how_to_get_and_conditions`, `official_source_url`, `review_date`
- **Units:** `review_date` = date the page was read (YYYY-MM-DD); amounts and percentages are the source's own wording; `official_source_url` = official provider page.
- **Source:** the per-provider coupon/promo pages listed on https://serverbudget.com/ (a2hosting, bluehost, chemicloud, cloudways, contabo, domain, dreamhost, fastcomet, godaddy, greengeeks, hetzner, hostgator, hostinger, hostpapa, hostwinds, inmotionhosting, interserver, knownhost, liquidweb, namecheap, ovhcloud, porkbun, scalahosting, siteground, vultr).
- **Method:** Offers and conditions transcribed from official pages with a source URL and review date. Where no code is published the row says so; where a term could not be confirmed the row says `Unconfirmed`. No code was tested and no result is claimed.

## datacenter-region-pricing.csv (6 rows)

- **Columns:** `city`, `entry_tier_usd`, `2_vcpu_tier_usd`, `4_vcpu_tier_usd`, `8_vcpu_tier_usd`, `panel_addon_usd`, `source_urls`
- **Units:** all price columns = USD per month; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/vps-datacenter-region-price ; each row's official URL (https://vps.us/kvm-vps/).
- **Method:** Published price by datacenter city across the entry, 2-, 4- and 8-vCPU tiers, plus the published panel add-on. No regional adjustment is applied.

## contract-term-total-cost.csv (4 rows)

- **Columns:** `provider`, `plan`, `displayed_starting_rate_usd_per_month`, `cost_1_month_usd`, `cost_12_months_usd`, `cost_24_months_usd`, `cost_36_months_usd`, `source_urls`
- **Units:** all cost columns = USD total for that term; `displayed_starting_rate_usd_per_month` = USD/month; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/cheap-vps-contract-length-total-cost ; official URL per row (https://www.ovhcloud.com/en/vps/).
- **Method:** Term totals are the provider's published monthly rate multiplied by the number of months in the term; the arithmetic is shown by the columns and no discount is invented.

## entry-tier-pricing.csv (4 rows)

- **Columns:** `memory`, `vcpu`, `transfer`, `ssd`, `hourly_usd`, `monthly_usd`, `source_urls`
- **Units:** `memory` = GiB/MiB RAM; `vcpu` = vCPU cores; `transfer` = GiB/month; `ssd` = GB; `hourly_usd` = USD/hour; `monthly_usd` = USD/month; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/cheap-vps-entry-price ; official URL per row (https://www.digitalocean.com/pricing/droplets).
- **Method:** Entry tier specs with the published hourly rate beside the published monthly cap, as stated on the official page.

## provider-payment-methods.csv (48 rows)

- **Columns:** `field`, `provider`, `as_printed_on_provider_page`, `source_urls`
- **Units:** `field` = the payment attribute being checked (credit cards, PayPal, cryptocurrency, Alipay/UnionPay, billing currency, regional restriction); `as_printed_on_provider_page` = the source wording or an explicit status; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/vps-payment-methods ; official URL per row (Vultr FAQ, Hetzner cloud FAQ, Namecheap VPS pricing, DigitalOcean billing docs, OVHcloud payment-methods page, Hostinger VPS page).
- **Method:** One row per (attribute, provider). Two cell states are distinguished and must not be merged: **"Not printed on the ... page"** means the page was readable and did not list the value; **"Read blocked: ... returned HTTP 403/404"** or a Cloudflare challenge means the page was not readable and nothing about it is claimed. No payment method is inferred for a blocked page.

## backup-tier-terms.csv (7 rows)

- **Columns:** `provider_and_tier`, `trigger`, `retention_as_printed`, `price_as_printed`, `what_the_copy_does_not_include`, `source_urls`
- **Units:** `retention_as_printed` = the retention window in the provider's own words; `price_as_printed` = source wording (USD/month, a percentage of plan cost, "Included", or an explicit no-figure statement); `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/vps-backup-tier-comparison ; official URL per row (OVHcloud VPS options, DigitalOcean pricing, Hetzner cloud, Vultr pricing).
- **Method:** Published backup tiers with trigger, retention and price exactly as printed, plus the limit the accompanying copy does not state. Where no price is listed the cell says so rather than assuming zero.

## included-transfer-allowances.csv (3 rows)

- **Columns:** `provider`, `allowance_as_printed`, `how_the_allowance_is_attached`, `what_the_page_does_not_print`, `source_urls`
- **Units:** `allowance_as_printed` = the provider's own allowance wording (GiB or TB figures, or "unlimited" with the footnote); `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/included-transfer-by-tier ; official URL per row (DigitalOcean pricing, OVHcloud VPS, Hetzner cloud).
- **Method:** The traffic allowance as printed, the mechanism that attaches it to a plan, and the guarantee the page does not make. Providers that describe the allowance differently are not normalised into a single number.

## storage-extension-costs.csv (4 rows)

- **Columns:** `provider`, `what_the_addon_is_called`, `published_price_as_printed`, `billing_unit`, `size_range_as_printed`, `can_it_grow_or_shrink`, `snapshot_or_backup_on_the_addon`, `source_urls`
- **Units:** `published_price_as_printed` = source wording (USD/month, or an explicit "no figure printed" statement); `billing_unit` = the provider's own unit; `size_range_as_printed` = source wording; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/vps-storage-extension-cost ; official URL per row (Contabo, OVHcloud, DigitalOcean, Hetzner).
- **Method:** Disk add-on terms as printed, including whether the disk can grow or shrink and whether a snapshot or backup rides along. A provider that publishes no figure for the add-on keeps that empty; the row is not dropped.

## bandwidth-overage-units.csv (9 rows)

- **Columns:** `provider`, `method_as_printed`, `number_as_printed`, `unit`, `source_urls`
- **Units:** `method_as_printed` = the source wording for how the allowance and overage work; `number_as_printed` = the published figure; `unit` = the provider's own unit (GiB, TB, Mbps, 100 MB blocks) as printed; `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/vps-overage-throttle-vs-metered ; official URL per row (OVHcloud VPS, Hetzner billing FAQ, DigitalOcean pricing, DigitalOcean bandwidth docs).
- **Method:** Three things are kept apart and are not merged: the allowance as printed, what happens past it, and the rate if one is published. Throttling to a fixed Mbps and billing per GiB are different charges and appear as different rows. Where no per-GB or per-TB rate is printed the cell says so.

## managed-db-metering-objects.csv (3 rows)

- **Columns:** `provider`, `official_original_printed`, `metering_object`, `why_it_cannot_sit_in_the_same_column`, `source_urls`
- **Units:** `official_original_printed` = the provider's own pricing wording; `metering_object` = the unit the provider meters (node, broker, storage, and so on); `source_urls` = official provider URL.
- **Source:** https://serverbudget.com/managed-database-engine-prices ; official URL per row (OVHcloud managed database, DigitalOcean pricing, Hetzner cloud).
- **Method:** Each provider meters a different object, so the rows are not reduced to a single price column. The reason a provider's figure cannot sit in another's column is recorded on the row.

## Notes

- A blank or explicitly unavailable value means the cited source did not publish it; it is not zero.
- These are snapshots, not a live feed. Follow the source URLs and verify current terms before purchasing.
- Reuse licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) with attribution.
