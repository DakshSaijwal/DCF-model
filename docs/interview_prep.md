# Interview Prep

If you cannot answer these from memory, you cannot claim this project. Practise them out loud.

## The mechanical ones

**"Depreciation increases by ₹100. Walk me through all three statements."**
Income statement: EBIT falls 100; at a 25% tax rate net profit falls 75.
Cash flow: start from net profit down 75, add back the 100 of non-cash D&A, so cash rises 25.
Balance sheet: cash up 25, PP&E down 100, so assets fall 75; retained earnings fall 75. Balances.

**"Why FCFF and not FCFE?"**
FCFF values the whole operating business before financing, so it is independent of capital
structure and is discounted at WACC. FCFE is post-debt and discounted at cost of equity. For
Havells, which has no borrowings, the two converge; say so, it shows you understand why the
choice matters rather than reciting it.

**"Why mid-year discounting?"**
Cash arrives through the year, not in a lump on 31 March. Discounting at t = 0.5, 1.5, 2.5 rather
than 1, 2, 3 avoids systematically undervaluing every cash flow.

**"Where does circularity come from and how do you handle it?"**
Interest depends on average debt, which depends on cash, which depends on net profit, which
depends on interest. Enable iterative calculation and build a circuit-breaker switch that zeroes
the interest formula so you can clear a broken model. Havells has no borrowings so the loop is
inert here, but the model is built with the switch anyway.

## The ones specific to this model

**"What is the biggest weakness of your valuation?"**
Terminal value is roughly three-quarters of enterprise value, so the answer is dominated by
assumptions beyond the forecast horizon. Say the number, do not hide it.

**"Your DCF says the stock is worth far less than it trades at. Are you saying the market is wrong?"**
No, I am saying that at the current price the market is assuming X% growth and Y% terminal margin,
and here is my view on whether that is achievable. Lead with the reverse DCF, not with a verdict.

**"Why did you exclude the ₹283 crore gain?"**
It is an unrealised fair value mark-up on a minority stake in Goldi Solar, a company Havells does
not operate. It is not operating income and it is not cash. Including it would inflate FCFF in
every forecast year. The stake is instead carried into the equity bridge at its ₹883 crore book
value, so it is counted once, in the right place.

**"Havells has no debt. Doesn't that make your WACC just cost of equity?"**
Essentially yes, the debt weight is under half a percent, all of it Ind AS 116 lease liabilities.
I did not invent a capital structure to make the formula look more interesting. I did run a
sensitivity at a hypothetical 20% target debt weight, which lowers WACC by roughly X% and raises
value per share by Y%.

**"Lighting contribution margin printed 37.2% in Q4. Why did you use 31%?"**
Management guided that the long-term average is 30–32%; the quarter was flattered by year-end
releases. Using the flattering quarter would have been the easy choice and the wrong one.

**"What did you find that wasn't in the headline numbers?"**
<< Your answer. The debtor-days collapse from 21 to 13 is a good candidate if you investigated it.
So is the correlation between Lloyd and ECD as weather-levered categories. Have something. >>

## The one that decides it

**"Walk me through your model."**
Ninety seconds. Business → segment revenue drivers → margin structure → what the model links →
valuation method → answer → the single assumption it hinges on. Practise it until it is boring.
