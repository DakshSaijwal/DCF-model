# Havells India: Hypothetical LBO Model

A leveraged buyout model built on top of the [3-statement DCF model](../model/Havells_3Statement_DCF_Model.xlsx) in this repository. Single senior term loan, India-adjusted leverage, explicit hypothetical framing.

> **Read this before anything else in this folder.**

## Havells is not a realistic LBO target, and the model says so

A leveraged buyout is an acquisition funded mostly by debt rather than the buyer's own cash, with the target's own future cash flow paying that debt down. Three real facts make Havells a poor fit for one:

1. **Promoter control.** QRG Investments and Holdings, the founding Gupta family's holding company, owns roughly 59% of Havells. Taking the company private would mean the family selling control of a business it has run since 1984.
2. **Size.** Havells' market capitalisation is around ₹70,000 crore (~$8 billion). A buyout at this scale would be one of the largest ever attempted in India.
3. **India's debt market.** Bank-dominated and structurally more conservative than the US syndicated loan or high-yield market that supports 4–6x EBITDA leverage today. This model anchors to roughly 2.75x total leverage instead, an India-adjusted, conservative assumption.

This model is built anyway, deliberately, as a **hypothetical exercise in LBO mechanics on a clean, well-disclosed dataset**, not a deal thesis. The `Assumptions` tab prices the entry at 12x EV/EBITDA, well below Havells' actual public trading multiple (~33x), specifically so the mechanics produce a sane, interpretable base case. The `Sensitivity` tab then shows what happens as the entry multiple rises toward that real trading multiple, and the answer is that returns go sharply negative. **That collapse is the actual finding of this exercise**: it's the mechanical reason a real buyout at Havells' traded price wouldn't clear an acceptable return, which is a more useful and more honest takeaway than either ignoring the question or pretending the deal is realistic.

Say all of this out loud before anyone reads the numbers. It is the single highest-value sentence in the whole project.

## What's in the workbook

| Tab | Contents |
|---|---|
| `Cover` | Scope and the read-this-first warning above |
| `Assumptions` | Entry/exit multiples, leverage, debt pricing, fees, every yellow cell justified |
| `Sources & Uses` | The two-column table that must tie to zero |
| `Operating Model` | Revenue, EBITDA, D&A, capex, working capital, carried over from the companion DCF model's base case, FY27E–FY31E |
| `Debt Schedule` | Single senior term loan: mandatory amortisation + 100% cash sweep, with the same circuit-breaker pattern as the DCF model for the interest circularity |
| `Returns Analysis` | Exit equity value, MOIC, IRR, and a returns bridge decomposing IRR into EBITDA growth, multiple change, and deleveraging |
| `Sensitivity` | Entry × exit multiple grid, the table that shows the return collapse described above |

## Two honest limitations baked into the model, not hidden from it

**No cash buffer at close.** The model assumes Havells' entire FY26A cash pile (₹2,351 Cr) is swept to help fund its own acquisition. That leaves zero cushion entering FY27E, and Havells' near-term capex (elevated for capacity expansion, carried over from the DCF forecast) makes free cash flow negative in the first year before mandatory amortisation. The model does not include a revolving credit facility to plug that gap, a real deal would need one, or a smaller debt quantum, or a retained minimum cash balance. This is disclosed on the `Debt Schedule` and `Sources & Uses` tabs rather than smoothed over.

**Single tranche only.** No mezzanine or subordinated debt. Simpler to build and defend, and arguably realistic at this leverage level anyway, but a genuine simplification versus a real deal's capital stack.

## Verification

```bash
python scripts/build_lbo_model.py
python /path/to/xlsx-skill/scripts/recalc.py model/Havells_LBO_Model.xlsx
```

Two checks must both read zero: `Sources & Uses!B24` (sources minus uses) and `Returns Analysis!B28` (the returns bridge must reconcile to the actual exit equity value).

Base case result at these assumptions: **2.07x MOIC, 15.6% IRR** over a 5-year hold, at a 12x entry/exit multiple and 2.75x leverage.

## Before you present this

- [ ] Replace the illustrative debt pricing (10.5%) with an actual benchmark, an Indian large-cap secured lending rate or a comparable rated NCD.
- [ ] Decide, and state, whether you'd rather demonstrate the mechanics on a more realistic (non-promoter-controlled, smaller) target instead of Havells. Either is defensible; know which you chose and why.
- [ ] Practice the "walk me through your returns bridge" answer, see the parent repo's `docs/interview_prep.md` for the equivalent DCF version; the same discipline applies here.
