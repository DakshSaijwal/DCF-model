"""
beta_regression.py
------------------
Estimates Havells' levered beta by regressing its weekly returns on the market's.

Beta measures how violently a stock moves relative to the market. A beta of 1.3 means
that historically, when the index moved 10%, this stock moved about 13%. It is the term
in CAPM that converts the market's risk premium into this company's cost of equity:

    Cost of equity = risk-free rate + beta x equity risk premium

The regression is:      r_stock,t  =  alpha  +  beta * r_market,t  +  e_t

where r are weekly percentage returns. Beta is the fitted slope. R-squared tells you how
much of the stock's movement the market explains, for a large-cap Indian industrial,
0.3 to 0.5 is typical. A low R-squared does not invalidate the beta, but it does mean the
estimate is noisy, and you should say so rather than quoting the slope to three decimals.

INPUT
-----
Two CSV files with columns  date,close, one for the stock, one for the index.
Download from NSE (Historical Data), Yahoo Finance, or your data provider, and save to
data/prices/. Weekly closes over five years is the standard window; five years of weekly
data gives ~260 observations, enough for a stable slope without reaching so far back that
the company's business mix has changed.

    python scripts/beta_regression.py \
        --stock  data/prices/havells_weekly.csv \
        --market data/prices/nifty500_weekly.csv

OUTPUT
------
Raw (levered) beta, alpha, R-squared, standard error of the slope, and a 95% confidence
interval. Record all of them in docs/assumptions_log.md, not just the point estimate.

CROSS-CHECK
-----------
A regression beta from a single stock is noisy. Professional practice is to cross-check it
against an industry beta: take Damodaran's unlevered ("asset") beta for Electrical
Equipment, then relever it to Havells' own capital structure using the Hamada equation

    beta_levered = beta_unlevered x [ 1 + (1 - tax rate) x (Debt / Equity) ]

Havells is effectively debt-free, so relevering barely moves the number, which is itself
worth one sentence in your memo. Report both estimates and explain any gap.
"""

import argparse
import sys

import numpy as np
import pandas as pd


def load_prices(path: str, label: str) -> pd.Series:
    df = pd.read_csv(path)
    cols = {c.lower().strip(): c for c in df.columns}
    date_col = next((cols[k] for k in ("date", "timestamp") if k in cols), None)
    close_col = next(
        (cols[k] for k in ("close", "adj close", "adj_close", "close price", "ltp") if k in cols),
        None,
    )
    if date_col is None or close_col is None:
        sys.exit(f"{label}: need a date column and a close column. Found: {list(df.columns)}")

    s = (
        df.assign(_d=pd.to_datetime(df[date_col], dayfirst=True, errors="coerce"))
        .dropna(subset=["_d"])
        .set_index("_d")[close_col]
    )
    s = pd.to_numeric(
        s.astype(str).str.replace(",", "", regex=False), errors="coerce"
    ).dropna().sort_index()
    if s.empty:
        sys.exit(f"{label}: no usable price data parsed from {path}")
    return s.rename(label)


def to_weekly_returns(prices: pd.Series) -> pd.Series:
    return prices.resample("W-FRI").last().pct_change().dropna()


def regress(y: np.ndarray, x: np.ndarray) -> dict:
    """Ordinary least squares of y on x with an intercept."""
    n = len(y)
    if n < 30:
        sys.exit(f"Only {n} overlapping observations. Use a longer price history.")

    X = np.column_stack([np.ones(n), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    alpha, beta = coef

    resid = y - X @ coef
    dof = n - 2
    sigma2 = resid @ resid / dof
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se_beta = float(np.sqrt(cov[1, 1]))

    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot

    return {
        "n": n,
        "alpha": float(alpha),
        "beta": float(beta),
        "se_beta": se_beta,
        "t_stat": float(beta) / se_beta if se_beta else float("nan"),
        "r_squared": r2,
        "ci_low": float(beta) - 1.96 * se_beta,
        "ci_high": float(beta) + 1.96 * se_beta,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Estimate beta by OLS on weekly returns.")
    p.add_argument("--stock", required=True, help="CSV of stock prices (date, close)")
    p.add_argument("--market", required=True, help="CSV of index prices (date, close)")
    p.add_argument("--tax-rate", type=float, default=0.252, help="Marginal tax rate for Hamada")
    p.add_argument("--debt", type=float, default=265.0, help="Debt, INR cr (Havells: lease liabilities)")
    p.add_argument("--equity", type=float, default=74613.0, help="Market cap, INR cr")
    args = p.parse_args()

    stock = to_weekly_returns(load_prices(args.stock, "stock"))
    market = to_weekly_returns(load_prices(args.market, "market"))
    joined = pd.concat([stock, market], axis=1, join="inner").dropna()

    res = regress(joined["stock"].to_numpy(), joined["market"].to_numpy())

    print("\nBETA REGRESSION, weekly returns, OLS")
    print("-" * 52)
    print(f"  Period                {joined.index.min():%d %b %Y} to {joined.index.max():%d %b %Y}")
    print(f"  Observations          {res['n']}")
    print(f"  Levered beta          {res['beta']:.3f}")
    print(f"  Std. error            {res['se_beta']:.3f}")
    print(f"  t-statistic           {res['t_stat']:.2f}")
    print(f"  95% CI                {res['ci_low']:.3f} to {res['ci_high']:.3f}")
    print(f"  R-squared             {res['r_squared']:.3f}")
    print(f"  Alpha (weekly)        {res['alpha']:.5f}")

    de = args.debt / args.equity
    unlevered = res["beta"] / (1 + (1 - args.tax_rate) * de)
    print("-" * 52)
    print(f"  D/E ratio             {de:.4f}")
    print(f"  Implied unlevered     {unlevered:.3f}")
    print("\n  Put the beta AND the R-squared in docs/assumptions_log.md.")
    print("  Cross-check against Damodaran's Electrical Equipment unlevered beta,")
    print("  relevered via Hamada, and explain any gap in your memo.\n")


if __name__ == "__main__":
    main()
