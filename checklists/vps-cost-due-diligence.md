# VPS Cost Due-Diligence Checklist

A reusable list of questions to ask before comparing two VPS quotes. Each item
names the cost that is usually missing from a headline "from $X/mo" price and
links to the page where that specific item was checked against published
provider terms. Work through it with your own provider's pricing page open.

- [ ] **What is the renewal price, not just the first-term price?**
  A 12-month-upfront rate can be an introductory rate. Note the term, the
  upfront total, and the monthly rate it becomes at renewal.
  Checked on: [promo renewal cost](https://serverbudget.com/cheap-vps-promo-renewal-cost), [renewal price](https://serverbudget.com/vps-renewal-price).

- [ ] **Is the billing term a commitment?**
  Per-second billing with no annual commitment and 12 months paid upfront are
  not comparable monthly figures. Record the term next to the price.
  Checked on: [price per GB comparison](https://serverbudget.com/vps-price-compare).

- [ ] **What does backup actually cost?**
  Some providers include a daily backup, some charge a flat monthly fee, and
  some charge a percentage of the instance price or a per-GiB usage rate.
  Checked on: [snapshot billing](https://serverbudget.com/vps-price-snapshot-billing), [price per GB comparison](https://serverbudget.com/vps-price-compare).

- [ ] **Are snapshots billed per GB per month?**
  A $0.40/mo flat fee and $0.06/GB/mo behave very differently once you keep
  several snapshots. Compute your expected retained size.
  Checked on: [snapshot billing](https://serverbudget.com/vps-price-snapshot-billing).

- [ ] **Is there a bandwidth allowance, and what is the overage rate?**
  "Unmetered", "unlimited included", and a fixed outbound allowance with no
  published overage price are three different risk profiles.
  Checked on: [bandwidth overage](https://serverbudget.com/vps-price-bandwidth-overage).

- [ ] **How much is an extra IPv4 address?**
  Additional IPs are usually a separate line item and are rarely in the plan
  headline. Check the per-address monthly price and any setup fee.
  Checked on: [extra IPv4 pricing](https://serverbudget.com/vps-price-extra-ipv4).

- [ ] **Is tax included in the displayed price?**
  Sales tax / VAT depends on billing address and is often added at checkout.
  Record whether the quoted figure is tax-inclusive.
  Checked on: [sales tax](https://serverbudget.com/vps-price-sales-tax).

- [ ] **Are you still billed while the instance is stopped?**
  Stopping a VM may or may not stop charges for reserved CPU, RAM, disk or IP.
  Checked on: [stopped-instance billing](https://serverbudget.com/vps-price-stopped-instance).

- [ ] **Which currency is the price in, and who eats the FX spread?**
  A price displayed in a currency different from your card's billing currency
  can move with the exchange rate and card fees.
  Checked on: [currency and FX](https://serverbudget.com/vps-price-currency-and-fx).

- [ ] **List every non-server line item on the invoice.**
  Control panel licences, backups, snapshots, IPs, OS licences and premium
  support are commonly separate. Put each on its own line with its published
  unit price before comparing totals.
  Checked on: [hidden fees line-item checklist](https://serverbudget.com/cheap-vps-hidden-fees).

- [ ] **Normalise by a published spec, not by the plan name.**
  Divide the monthly price by published RAM, vCPU and storage. If a provider
  publishes no spec, exclude it from that comparison rather than guessing.
  Worked example: [price per GB](https://serverbudget.com/vps-price-compare).

## How to use this with the dataset in this repository

1. Fill in the checklist for each candidate provider.
2. Add the resulting line items to a copy of `data/hidden-costs.csv`.
3. Rank comparable plans with `python tools/price_per_unit.py --sort usd_per_gb_ram`.
4. Recompute the 12-month total using the renewal row, not the introductory row.
