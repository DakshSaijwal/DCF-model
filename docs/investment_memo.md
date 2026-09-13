# Havells India Limited: Investment Memo

**Author:** Daksh Saijwal · **Date:** 11 September 2026 · **Price at valuation date:** Rs 1,117
**Intrinsic value (base case, 5% terminal growth):** Rs 258 · **Implied downside:** -77%

---

## 1. The business in five sentences

Havells is a leading Fast Moving Electrical Goods manufacturer and power distribution equipment maker, selling cables, switchgears, lighting, fans, appliances and air conditioners (the Lloyd brand) across India. It earns its money through a mix of a high-margin, brand-driven consumer business (switchgears, lighting) and a lower-margin, commodity-priced industrial business (cables). FY26 revenue was Rs 22,466 Cr on a 9.9% EBITDA margin, with cables now the largest segment after strong growth while Lloyd (air conditioners, refrigerators, washing machines) posted a segment loss on falling volumes. The company carries no borrowings and holds a large net cash position, which is unusual for an industrial manufacturer and central to how this model treats its discount rate. Management's own growth narrative rests on continuing to gain share in cables and stabilising Lloyd, both of which this model treats as base-case, not guaranteed, outcomes.

## 2. Thesis

1. **Havells is a well-run, structurally profitable business, but its current share price does not appear to be supported by a standard discounted cash flow at any defensible set of forecast assumptions.**
2. **The gap between intrinsic value and market price is large enough (roughly 75-80% at conservative but reasonable assumptions) that closing it requires either a terminal growth rate the model shows is mathematically unsustainable, or a belief that the market is pricing something other than discounted cash flow, for example, scarcity value, index-inclusion demand, or M&A optionality.**
3. **Lloyd's turnaround, not cables' continued strength, is the single assumption most likely to move this valuation meaningfully in either direction, because it is the segment currently furthest from its own historical margin and the one most exposed to a single bad or good summer.**

## 3. What has to be true

| Assumption | Base case | Why |
|---|---|---|
| Revenue CAGR FY27-FY31 | ~9-10%, fading from 10% to 7% | Cables normalises off a strong FY26; Lloyd partially recovers; ECD and switchgears grow near GDP-plus rates |
| Terminal EBITDA margin | ~11.5% | Up from FY26's 9.9%, assuming Lloyd's margin drag fades and switchgear pass-through normalises |
| WACC | 13.6% | CAPM cost of equity (Havells carries no debt): Rf 7.02% + beta 0.90 x India ERP 7.31%, all sourced 11-Sep-2026 (see Section 5) |
| Terminal growth | 5.0% | Nominal India growth proxy: roughly 4% real GDP plus inflation, held deliberately below WACC |

## 4. Valuation

The model values Havells on unlevered free cash flow (FCFF), a five-year explicit forecast (FY27-FY31) with a Gordon-growth terminal value and mid-year discounting. Enterprise value bridges to equity value by adding back Havells' large net cash position and its Goldi Solar investment at carrying value, since that stake's earnings are excluded from operating EBIT (it is an unrealised fair-value gain on a minority holding, not operating income).

At the base-case assumptions above, **intrinsic value is Rs 258 per share against a Rs 1,117 market price, a 77% gap.** Terminal value is 76% of enterprise value, meaning the overwhelming majority of this valuation rests on assumptions about the world a decade from now, not on the explicit five-year forecast. That concentration is disclosed, not hidden: it is the single most important caveat on this entire valuation, and it is also exactly why a reverse DCF is the more useful exercise here than defending a single point estimate.

**I have not adjusted terminal growth or terminal margin upward to close this gap**, because doing so without a specific, sourced reason to believe those higher figures are achievable is the most common failure mode in a student DCF, and it is visible immediately to anyone who checks the assumption against a GDP growth benchmark.

## 5. WACC: sourced and dated

| Input | Value | Source, pulled 11-Sep-2026 |
|---|---|---|
| Risk-free rate | 7.02% | India 10-year G-Sec yield, indiamacroindicators.co.in |
| Beta | 0.90 | Equentis stock-screener published beta estimate ("volatility broadly in line with the market") |
| Equity risk premium (India, total) | 7.31% | Damodaran country equity risk premium table, July 2026 update (4.17% mature-market ERP plus India country risk premium) |
| **Cost of equity = WACC** | **13.6%** | Havells carries no borrowings, so WACC is effectively pure cost of equity |

**A caveat on the beta figure:** this is a third-party published estimate, not a beta I derived myself from a downloaded price series via `scripts/beta_regression.py`. It is directionally consistent with what a self-run regression would likely show for a large-cap consumer/industrial name (the 0.85-1.10 range is typical), but before presenting this model in an interview setting I would run the actual regression and report the R-squared alongside the point estimate, since a sourced-but-unverified beta is a legitimate gap in this analysis and I want to be upfront about it rather than presenting it as more rigorous than it is.

## 6. The reverse DCF: what the market is actually assuming

Holding WACC (13.6%) and the five-year explicit forecast fixed, I solved numerically for the terminal growth rate that makes this model's output equal to the current Rs 1,117 market price. **The answer is approximately 12.1%, a perpetual growth rate, forever, not just for the next five or ten years.**

This is not achievable. India's long-run nominal GDP growth is reasonably estimated at 9-11% (roughly 6-7% real growth plus 3-4% inflation), and no individual company can outgrow the aggregate economy in perpetuity without eventually becoming a mathematically impossible share of it. A terminal growth assumption above the economy's own long-run growth rate is a textbook DCF error, and 12.1% is not a marginal violation of that rule; it is a growth rate this model would also flag as implausible if a forecast year showed it explicitly, let alone as a "forever" assumption.

There is also a second, related problem: at g = 12.1% against a WACC of 13.6%, the spread is only **1.4 percentage points**. The Gordon growth formula's denominator is (WACC − g), so a valuation built this close to that spread is acutely fragile, a 50 basis point move in either WACC or g, well within a year's normal market movement, would swing the implied value by a large multiple. **The market's own implied assumption is not just optimistic; it sits in the part of the formula's domain where small input changes produce enormous output changes**, which is itself a reason to be skeptical that investors are pricing Havells off a disciplined perpetuity-growth DCF at all.

**My conclusion:** the market is very likely not pricing Havells primarily on a standard FCFF DCF. More plausible explanations for the gap include a much longer assumed high-growth runway before any deceleration to a terminal rate (effectively, a 15-20 year explicit forecast compressed into a 5-year model would show a smaller implied terminal growth requirement), a scarcity or index-weight premium common among large-cap consumer names in India, or the market pricing in optionality, further M&A, new categories, or margin upside, that a base-case operating forecast does not capture. I am not asserting the stock is overvalued by 77%; I am asserting that the gap cannot be closed by a defensible terminal-growth assumption alone, and that whatever is closing it in the market's mind is not visible in this model's structure.

## 7. Risks

1. **Lloyd's recovery could outperform or underperform sharply based on a single summer's weather**, both ECD and Lloyd are correlated, weather-levered categories, so a bull or bear case that assumes both recover independently is double-counting the same underlying driver.
2. **Cables' recent strength is partly a commodity pass-through effect** (copper/aluminium prices), not pure volume growth, if metal prices fall, reported cable revenue growth could decelerate even with stable underlying demand.
3. **The beta used here is a third-party estimate, not self-verified**: if a self-run regression produces a materially different figure (particularly a higher beta, which is plausible given Havells' small-to-mid-cap-adjacent volatility relative to the Nifty), WACC and the entire intrinsic value output would need to be revised.

## 8. What I would want to know next

Whether sell-side consensus models for Havells use an explicit forecast period longer than five years (which would mechanically require a lower, more defensible implied terminal growth rate than the 12.1% found here); what specific assumption Havells' own management guidance implies for Lloyd's margin recovery timeline; and whether a self-run beta regression against the Nifty 500, using an actual five-year weekly price series, materially changes the 0.90 estimate used in this memo.

---

*Educational exercise. Not investment research and not a recommendation to buy or sell any security. All forward-looking figures are my own estimates.*
