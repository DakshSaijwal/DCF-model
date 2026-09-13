# LBO Interview Prep

## The mechanical ones

**"Walk me through Sources & Uses."**
Uses: the equity purchase price (entry EV plus net cash, since a buyer pays for the target's cash pile too) plus transaction fees. Sources: a senior term loan sized off a leverage multiple of EBITDA, the target's own cash swept in to help fund the deal, and sponsor equity as the plug that makes the two sides equal.

**"Why does the debt schedule need a circuit breaker?"**
Interest expense depends on the average debt balance; the average balance depends on how much gets swept; the sweep depends on free cash flow; free cash flow depends on interest expense. Circular. Same fix as any DCF debt schedule: enable iterative calculation and add a switch that zeroes the interest formula when you need to break the loop and debug.

**"Walk me through the returns bridge."**
Start at entry equity. Add EBITDA growth valued at the entry multiple, the value created just from the business growing, holding the multiple constant. Add the multiple change, exit EBITDA times the change in multiple, which could be zero, positive, or negative. Add deleveraging and cash generation, value created because debt got paid down and cash built up. The three should sum to exactly the exit equity value; if they don't, the model has an error somewhere upstream.

**"Why single-tranche and no revolver?"**
At this leverage level (2.75x, India-adjusted) a single senior facility is a defensible simplification. The absence of a revolver is a real limitation: it means the model can't fund a temporary cash shortfall, which shows up directly in FY27E as negative free cash flow before mandatory amortisation. Say this plainly rather than waiting to be asked.

## The one specific to this model

**"Would Havells actually get bought out like this?"**
No, and the model doesn't claim otherwise. The promoter family holds roughly 59% of the company, the deal size would be one of the largest buyouts ever attempted in India, and the debt market wouldn't support anywhere near US-style leverage. The model uses an illustrative entry multiple well below Havells' actual trading price specifically so the mechanics produce an interpretable result, and the sensitivity grid shows exactly what happens as you raise the entry multiple toward the real trading price: the IRR goes negative. That collapse is the actual finding here, not a flaw in the exercise.

**"What would make this a better model?"**
An actual sourced debt pricing benchmark instead of an illustrative rate; a revolver to handle the FY27E shortfall; and ideally, running the same exercise on a target where the "would this really happen" question doesn't need an entire caveat paragraph to answer.
