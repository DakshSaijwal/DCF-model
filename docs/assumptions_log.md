# Assumptions Log

Every yellow cell in the model gets a row here. An assumption without a source is a guess, and a
guess you cannot defend is worse than no model at all.

**How to fill this in.** For each driver: what you set it to, where the evidence came from
(transcript, filing, industry data), and what would have to happen for you to be wrong. Two
sentences each is enough. Delete the `<< >>` prompts as you go.

---

## 1. Revenue growth by segment

### Cables: 39% of FY26 revenue, grew 20.8%

| | |
|---|---|
| FY27E–FY31E | << your numbers >> |
| Evidence | << Q4 FY26 call: power cables strong on transmission capex, data centres, real estate; domestic wires saw slight degrowth on channel inventory normalisation and a stronger base >> |
| Note on pricing | Cables are priced on copper/aluminium pass-through, so revenue moves with metal prices even at flat volume. Split your assumption into volume growth and realisation growth and say which you are assuming. |
| What breaks it | << e.g. infrastructure capex cycle turns; copper collapses; competitive intensity from Polycab/KEI compresses realisation >> |

### Lloyd Consumer: 18% of revenue, fell 22.9%, segment result −₹203 cr

| | |
|---|---|
| FY27E–FY31E | << your numbers >> |
| Evidence | << Management attributed weakness to a milder start to summer and a strong prior-year base. Decide whether you believe that is cyclical or structural. >> |
| What breaks it | << two consecutive weak summers; Voltas/Blue Star share gains; inability to restore contribution margin from 8.4% >> |

### Electrical Consumer Durables: 17%, fell 3.4%
### Switchgears: 11.5%, grew 7.9%, contribution margin 36.9%
### Others (solar): 7.7%, grew 25.2%
### Lighting & Fixtures: 7.4%, flat

<< repeat the table for each >>

**Correlation warning.** ECD (fans, coolers) and Lloyd (air conditioners) are both weather-levered.
A bull case that assumes both recover independently is double-counting one good summer. State
explicitly that you have accounted for this.

---

## 2. Contribution margins

| Segment | FY25A | FY26A | Your forecast | Justification |
|---|---|---|---|---|
| Switchgears | 37.9% | 36.9% | | << FY26 dip attributed to a lag in passing through cost increases, expected to normalise >> |
| Cables | 14.1% | 16.9% | | << FY26 margin was supported by a rising commodity price trend, is that repeatable? >> |
| Lighting & Fixtures | 32.6% | 32.3% | | **Management guided long-term contribution margin of 30–32%.** Q4 printed 37.2% on year-end releases. Use the guided range, not the flattering quarter. |
| ECD | 23.8% | 23.0% | | |
| Others | 17.0% | 16.2% | | << structurally lower than group average; growth here dilutes blended margin >> |
| Lloyd | 13.5% | 8.4% | | << recovery path and timing >> |

---

## 3. Cost and cash flow drivers

| Driver | FY26A | Your forecast | Justification |
|---|---|---|---|
| A&SP (% of revenue) | 2.7% | | |
| Other SG&A (% of revenue) | 9.2% | | |
| Effective tax rate | 23.4% | | The FY26 reported rate is flattered by the untaxed fair value gain. Use the statutory rate. |
| Capex (% of revenue) | 6.6% | | FY26 capex of ₹1,484 cr (vs ₹753 cr in FY25) was elevated for capacity addition in cables and refrigerators. Is that a one-off? |
| D&A (% of revenue) | 1.9% | | Should rise with a lag behind the capex bulge. |
| Inventory days | 71 | | |
| Debtor days | 13 | | **Investigate this.** Debtor days fell from 21 to 13 and receivables dropped from ₹1,254 cr to ₹782 cr while revenue grew. Read the FY26 annual report notes for channel financing or receivable factoring. If receivables are being sold, working capital is flattered. |
| Creditor days | 47 | | |
| Dividend payout | 36.8% | | ₹627 cr paid in both FY25 and FY26. |

---

## 4. Discount rate

| Input | Value | Source | Date pulled |
|---|---|---|---|
| Risk-free rate | 7.02% | India 10-year G-Sec yield, indiamacroindicators.co.in | 11-Sep-2026 |
| Beta | 0.90 | Equentis published stock-screener estimate ("volatility broadly in line with the market") | 11-Sep-2026 |
| Cross-check beta | Not yet run | `scripts/beta_regression.py` was not run against a live downloaded price series for this pass. The 0.90 figure above is a third-party estimate, not a self-run regression. **Genuine gap: run this before presenting the model in an interview setting**, and report the R² alongside the point estimate. |
| Equity risk premium | 7.31% | Damodaran country equity risk premium table, July 2026 update. This is the total India ERP (4.17% mature-market ERP + India country risk premium), reported via secondary coverage of the workbook, not the primary Stern spreadsheet directly. Verify against pages.stern.nyu.edu/~adamodar before final submission. | 11-Sep-2026 |
| Cost of equity | 13.60% | = 7.02% + 0.90 × 7.31% | derived |
| Debt weight | ~0.4% | Lease liabilities only; no borrowings | |
| **WACC** | **13.57%** | Effectively equal to cost of equity given the near-zero debt weight | derived |

**On the debt-free structure:** Havells carries no borrowings, so WACC is almost exactly cost of equity (13.57% vs. 13.60% cost of equity; the tiny gap is the lease-liability weight). I did not fabricate a target capital structure to make this section look more sophisticated. As a sensitivity worth running: at a hypothetical 20% target debt weight and an 8% pre-tax cost of debt, WACC would fall to roughly 12.0-12.3%, which, given how close the base case already sits to the terminal-growth ceiling found in Section 6, would materially increase intrinsic value. That sensitivity is a legitimate thing to show in an interview precisely because it demonstrates the valuation's fragility to the discount-rate assumption, not because it closes the gap to the market price.

---

## 5. Terminal value

| Input | Value | Justification |
|---|---|---|
| Terminal growth (g) | 5.0% (shipped assumption) | Nominal India proxy: ~4% real GDP + inflation, held below WACC (13.57%) and below the long-run nominal GDP growth ceiling. |
| Terminal capex % | 3.5% (fades down from 5.0% in Y1) | Set to converge toward, not below, terminal D&A (2.3% of revenue and rising) by the final forecast year, a company cannot shrink its asset base forever while growing. Worth double-checking the exact crossover year explicitly before presenting. |
| TV as % of EV | **75.7%** | This is above 75%. Stated openly here and in the investment memo: the overwhelming majority of this valuation rests on assumptions about the world 5+ years out, not on the explicit forecast. This is the single most important caveat on the whole model. |
| Exit multiple cross-check | Not yet built | **Genuine gap.** A comps tab (Polycab, KEI, Crompton Greaves Consumer, V-Guard, Voltas, Blue Star) computing implied terminal EV/EBITDA against where peers actually trade today has not been built for this pass. This is the highest-value next addition to this model. |

---

## 6. Reverse DCF

| | |
|---|---|
| Market price on valuation date | Rs 1,117 (11-Sep-2026, sourced from bajajbroking.in intraday quote: Rs 70,036 Cr market cap / 62.7 Cr shares) |
| Implied terminal growth rate (holding WACC and the 5-year explicit forecast fixed) | **~12.1%**, solved numerically by bisection on Assumptions!B39 until DCF!B34 matched the market price |
| Is that achievable? | **No.** India's long-run nominal GDP growth is reasonably estimated at 9-11%. A 12.1% perpetual growth rate means Havells would need to outgrow the entire Indian economy, forever: mathematically impossible to sustain indefinitely, and not a marginal violation of the "g must be below long-run GDP growth" rule stated above, but a clear one. Worth noting too: at g = 12.1% against a WACC of 13.57%, the (WACC − g) spread is only 1.4 percentage points, meaning the Gordon growth formula is operating in a highly unstable region of its own domain: a 50 bps move in either input would swing the output by a large multiple. My conclusion, written up fully in the investment memo, is that the market is very unlikely to be pricing Havells off a disciplined 5-year-explicit-plus-perpetuity DCF at all; something else (a longer assumed high-growth runway, scarcity/index-weight premium, or M&A optionality) is more likely doing the work. |
