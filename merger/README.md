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

## Before you present this

- [ ] Verify IFB's actual net finance cost and diluted share count against its FY26 annual report.
- [ ] Decide whether a lower control premium, a different financing mix, or a longer analysis horizon (Year 2-3, once synergies are more fully realised) changes the story enough to be worth presenting alongside the Year 1 result.
- [ ] Practice explaining why a strategically sound deal can still be EPS-dilutive in Year 1; that distinction is exactly what gets tested in an interview.
