# Havells India: Hypothetical Acquisition of IFB Industries: Merger Model

A merger model and accretion/dilution analysis: Havells India (acquirer) buys IFB Industries Limited (target), built on top of the [3-statement DCF model](../model/Havells_3Statement_DCF_Model.xlsx) in this repository.

## Why this deal, and why it's different from the LBO model

The [LBO model](../lbo/README.md) elsewhere in this repo makes Havells the acquisition **target** and states plainly that this is unrealistic given the company's promoter control and scale. This model does the opposite: Havells is the **acquirer** of a real, smaller, publicly listed company. This is a genuinely plausible deal shape.

Havells is debt-free with a large cash pile, and its Lloyd segment (air conditioners, refrigerators, washing machines) posted a segment loss in FY26 on falling revenue: a real, disclosed competitive weakness. **IFB Industries** (NSE: IFBIND) is a real home-appliance manufacturer (washing machines, microwaves, dishwashers), roughly a fourteenth of Havells' size by market value, trading at a rich ~36x trailing P/E. A bolt-on acquisition to broaden white-goods scale is a standard strategic playbook move, not a hypothetical stretch.

**The deal terms used here are entirely illustrative.** Premium, financing mix, and synergies are constructed from each company's own public FY26 results, not from any actual announced transaction, advisory mandate, or non-public information about either company. Say this plainly before presenting the model.

## What's in the workbook

| Tab | Contents |
|---|---|
| `Cover` | Deal rationale and scope |
| `Assumptions` | Both companies' standalone FY26A financials, deal terms, purchase price allocation and synergy assumptions |
| `Sources & Uses` | The two-column table that must tie to zero |
| `Purchase Price Allocation` | Simplified: one amortisable intangible plus residual goodwill |
| `Pro Forma Income Statement` | Combined Year 1 income statement with all deal adjustments |
| `Accretion-Dilution` | The headline number: pro forma EPS vs. Havells' standalone EPS |
| `Sensitivity` | Cash % × synergy realisation grid, plus a closed-form breakeven synergy calculation |

## The finding

At the base-case assumptions (25% control premium, 100% cash funded by a mix of Havells' own cash and new acquisition debt, ₹100 Cr of illustrative run-rate synergies phased in at 50% in Year 1), the deal is **dilutive by roughly 23% to Havells' Year 1 EPS.**

That is not a modelling error: it is the mechanical result of paying a premium for a company trading at ~36x earnings, funded partly with new debt priced above the target's own earnings yield. The **breakeven synergy calculation** on the Sensitivity tab makes this concrete: making the deal EPS-neutral at these terms would require run-rate synergies of roughly ₹992 Cr: nearly five times IFB's own FY26 EBIT. That's not a realistic synergy number for a deal of this size, which is itself the honest conclusion: **at this price and this financing mix, the deal does not pay for itself on Year 1 earnings alone**, and would need to be justified on strategic grounds (fixing Lloyd's competitive scale) with a longer payback horizon in mind, not on near-term accretion.

The sensitivity grid also shows the classic cash-vs-stock tradeoff directly: heavier stock funding (less debt) is meaningfully less dilutive than an all-cash, debt-funded structure, because it avoids the interest cost drag even though it dilutes share count instead.

## Two honest simplifications

**IFB's finance cost is estimated, not sourced.** The public results summary used to build this model didn't break out IFB's net finance cost separately from PBT. The model uses a placeholder (₹20 Cr) flagged on the `Assumptions` tab; verify this against IFB's actual annual report before presenting the model.

**No deferred tax on the intangible step-up.** Because this is modelled as a share purchase, the incremental D&A from the purchase price allocation is not tax-deductible under Indian tax law: a real distinction between share and asset deals worth knowing for an interview. The model applies tax to book pre-tax profit throughout rather than tracking book-tax differences separately, which is the standard simplification in a first accretion/dilution build.

## Verification

```bash
python scripts/build_merger_model.py
python /path/to/xlsx-skill/scripts/recalc.py model/Havells_Merger_Model.xlsx
```

The check that must read zero: `Sources & Uses!B21`.

## Conclusion

All three items below are done.

- [x] **Verified IFB's net finance cost and diluted share count.** IFB Industries' FY26 Annual Report (its 50th) confirms the company is **net debt zero** with a CRISIL AA-/Positive credit rating. The model's original placeholder finance cost of Rs 20 Cr was directionally wrong for a net-cash company; it is now held at zero, sourced explicitly on the `Assumptions` tab. Note for transparency: this correction did not change the headline -22.9% result, because the old placeholder had been added into IFB's EBIT and then subtracted again as retained finance cost elsewhere in the model, so it canceled out algebraically. The number was accidentally right; the justification behind it wasn't, and that distinction matters if asked about it directly. Diluted share count (4.05 Cr) was independently confirmed against a second source (Yahoo Finance TTM diluted EPS of Rs 35.41 on Rs 144 Cr net income).

- [x] **Decided: financing mix matters more than time horizon.** At the base-case 100% cash financing, moving from Year 1 (50% synergy realisation) to a fully phased-in scenario (100% synergy) only improves the result from -22.9% to -20.3% dilutive, a marginal 2.6-point improvement. Waiting longer does not change the story enough to be worth presenting on its own. What does change the story is the **financing mix**: at 0% cash (an all-stock deal) combined with full synergy realisation, the deal turns marginally **accretive** (+0.9%). The right alternative scenario to present alongside the base case is therefore not "the same deal, later" but "the same deal, financed differently": see the full grid on the `Sensitivity` tab.

- [x] **Practiced the explanation.** A strategically sound deal can still be EPS-dilutive in Year 1 because accretion/dilution measures accounting earnings per share in the first year, not the strategic value of the combination. Here, IFB trades at roughly 36x trailing earnings, a rich multiple for a thin-margin appliance business, and financing most of that price with new debt costs more in Year 1 interest than IFB's own earnings contribute. That is a financing-and-price problem, not a "the deal is bad" problem: the same combination financed mostly in stock, with synergies further along, would not be meaningfully dilutive at all. The distinction to hold onto in an interview is between "this deal destroys value" (not shown here) and "this deal costs EPS in year one under this specific financing structure" (shown here); conflating the two is the mistake to avoid.
