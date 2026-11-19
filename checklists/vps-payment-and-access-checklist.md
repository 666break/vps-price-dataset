# VPS Payment and Access Checklist

A reusable list of the things to settle before you can actually pay a provider and
before traffic reaches the server. Written from what six providers publish (or do
not publish) on their own payment, backup and traffic pages — every item links to
the page where that item was checked.

## Paying for it

- [ ] **Which payment methods does the provider accept?**
  Card brand, PayPal, bank transfer and cryptocurrency are not interchangeable. A
  provider that lists none on the page you read may still accept them at checkout,
  and a provider that lists them may restrict one of them regionally.
  Checked on: [payment methods](https://serverbudget.com/vps-payment-methods).

- [ ] **Is the price billed in your currency or theirs?**
  One provider states it bills only in USD and does not convert to local currency
  to keep pricing stable; another lists prices in EUR excluding VAT. The currency
  you are charged in changes the final number for everyone outside that currency's
  zone.
  Checked on: [payment methods](https://serverbudget.com/vps-payment-methods), [currency and FX](https://serverbudget.com/vps-price-currency-and-fx).

- [ ] **If you pay with PayPal, does it need a backup funding source?**
  Some providers state that PayPal requires a credit card or bank account on file
  behind it. That re-introduces the card requirement you were trying to avoid.
  Checked on: [payment methods](https://serverbudget.com/vps-payment-methods).

- [ ] **Is there a regional restriction on any payment method?**
  One provider prints a regional restriction on a payment method. If you are
  outside that region, the method you planned to use is not available to you.
  Checked on: [payment methods](https://serverbudget.com/vps-payment-methods).

- [ ] **If you pay by cryptocurrency, which ones, and through which processor?**
  The list is provider-specific and is published as a processor's supported set,
  not as "we accept crypto". A crypto payment can also settle at a different
  exchange rate than the card price you compared.
  Checked on: [payment methods](https://serverbudget.com/vps-payment-methods).

## Getting the data back

- [ ] **What does the backup actually restore?**
  A backup that is described as protecting "all your information" is not the same
  as a stated retention window. One provider publishes a 24-hour window, another
  a rolling 7-day window, and one publishes no window at all.
  Checked on: [backup tiers](https://serverbudget.com/vps-backup-tier-comparison), [backup restore verification](https://serverbudget.com/vps-backup-restore-verification).

- [ ] **Is the backup automatic or manual, and what triggers it?**
  Automatic daily, automatic with a schedule, and manual snapshot are three
  different failure behaviours. A manual snapshot is one you have to remember.
  Checked on: [backup tiers](https://serverbudget.com/vps-backup-tier-comparison).

- [ ] **What is the traffic allowance, and what happens past it?**
  "Unlimited traffic" often carries a footnote. Past the allowance, one provider
  throttles to a fixed bandwidth with no price, another bills per GiB, and
  another bills in 100 MB blocks with round-up.
  Checked on: [traffic allowance by tier](https://serverbudget.com/included-transfer-by-tier), [overage metering](https://serverbudget.com/vps-overage-throttle-vs-metered).

- [ ] **Is the overage rate per GiB, per TB, or not published at all?**
  Two providers with the same headline price can have different overage units.
  A plan with no published overage rate is not the same as a plan with an
  expensive one.
  Checked on: [overage metering](https://serverbudget.com/vps-overage-throttle-vs-metered), [overage throttle vs billed](https://serverbudget.com/vps-overage-throttle-vs-billed).

- [ ] **Can you add disk later, and does it grow and shrink?**
  Some providers price the add-on, some do not publish a figure. Rules differ on
  whether the disk can grow, shrink, or be resized at all.
  Checked on: [storage extension cost](https://serverbudget.com/vps-storage-extension-cost).

## Getting in

- [ ] **Which email ports are open, and how do you check before you buy?**
  The port policy is published on the provider's documentation, but the
  reputation of the exact IP you will get is not knowable before signup.
  Checked on: [outbound identity](https://serverbudget.com/cheap-vps-outbound-identity).

- [ ] **Does the refund window apply to your plan?**
  Trial credits, monthly refunds and contract cancellation are different rights
  with different exclusions. One provider publishes a 14-day window with named
  exclusions.
  Checked on: [refund terms](https://serverbudget.com/vps-refund-terms-sla-fine-print), [refund rights](https://serverbudget.com/vps-trial-refund-compare).

## Notes on this list

- Every link above points to a page that records what was published on a
  provider's own site, on the date that page states.
- Where a provider page could not be read, the linked page says so and gives the
  HTTP status. Nothing on those pages is inferred.
- Prices and terms change. Re-check the provider's page before you sign.
