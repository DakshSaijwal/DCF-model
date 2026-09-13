"""
build_model.py
--------------
Generates the Havells India 3-statement + DCF model workbook.

Everything in the output workbook is a live formula. Nothing is a
Python-computed constant except (a) reported historical figures and
(b) forecast assumptions, both of which are colour-coded.

Colour convention (standard sell-side):
    BLUE   text  = hardcoded input / assumption you may change
    BLACK  text  = formula computed on the same sheet
    GREEN  text  = link pulled from another sheet
    YELLOW fill  = assumption you MUST justify in docs/assumptions_log.md

Historical source:
    Havells India Ltd, Information Update on Financial Results,
    Q4 & FY ended 31 March 2026, filed with NSE/BSE 22 April 2026.
    Standalone basis. All figures in INR crore.

Run:  python scripts/build_model.py
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

# ---------------------------------------------------------------- styling ---
BLUE = Font(name="Arial", size=10, color="0000FF")
BLACK = Font(name="Arial", size=10, color="000000")
GREEN = Font(name="Arial", size=10, color="008000")
BOLD = Font(name="Arial", size=10, bold=True)
TITLE = Font(name="Arial", size=13, bold=True)
SUB = Font(name="Arial", size=10, italic=True, color="595959")
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")

YELLOW = PatternFill("solid", fgColor="FFFF00")
NAVY = PatternFill("solid", fgColor="1F3864")
GREYFILL = PatternFill("solid", fgColor="F2F2F2")

TOPBORDER = Border(top=Side(style="thin"))
TOPDOUBLE = Border(top=Side(style="thin"), bottom=Side(style="double"))

NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%'
MULT = '0.0x'
RS = '#,##0.00'

# Column map: B..H
YEARS = ["FY25A", "FY26A", "FY27E", "FY28E", "FY29E", "FY30E", "FY31E"]
COLS = ["B", "C", "D", "E", "F", "G", "H"]
FC = COLS[2:]          # forecast columns D..H
FIRST_FC, LAST_FC = "D", "H"


def put(ws, cell, value, font=BLACK, fmt=None, fill=None, border=None, align=None):
    c = ws[cell]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if border:
        c.border = border
    if align:
        c.alignment = Alignment(horizontal=align)
    return c


def label(ws, row, text, bold=False, indent=0):
    c = ws.cell(row=row, column=1)
    c.value = text
    c.font = BOLD if bold else BLACK
    if indent:
        c.alignment = Alignment(indent=indent)


def year_header(ws, row, note=None):
    """Write the FY25A..FY31E header band."""
    put(ws, f"A{row}", note or "INR crore", HDR, fill=NAVY)
    for col, yr in zip(COLS, YEARS):
        put(ws, f"{col}{row}", yr, HDR, fill=NAVY, align="center")


def widths(ws, a=52, rest=13):
    ws.column_dimensions["A"].width = a
    for col in COLS + ["I", "J", "K", "L", "M"]:
        ws.column_dimensions[col].width = rest


wb = Workbook()

# =============================================================== COVER =====
ws = wb.active
ws.title = "Cover"
ws.column_dimensions["A"].width = 34
ws.column_dimensions["B"].width = 78

put(ws, "A1", "HAVELLS INDIA LIMITED", TITLE)
put(ws, "A2", "Three-Statement Operating Model & Discounted Cash Flow Valuation", SUB)

rows = [
    ("Ticker", "NSE: HAVELLS  |  BSE: 517354"),
    ("Sector", "Electrical equipment / Fast-moving electrical goods (FMEG)"),
    ("Reporting basis", "STANDALONE (subsidiaries immaterial: standalone is ~99.7% of consolidated revenue)"),
    ("Units", "INR crore unless stated otherwise"),
    ("Fiscal year end", "31 March"),
    ("Historical period", "FY2025A - FY2026A"),
    ("Forecast period", "FY2027E - FY2031E (5 years)"),
    ("", ""),
    ("Prepared by", "<< YOUR NAME >>"),
    ("Date", "<< DATE >>"),
    ("", ""),
    ("Primary source", "Havells India Ltd, Information Update on Financial Results for Q4 and FY ended 31 Mar 2026, filed with NSE/BSE 22 April 2026"),
    ("Secondary sources", "Annual Reports FY22-FY26; quarterly earnings call transcripts; RBI (G-Sec yield); NYU Stern / Damodaran (equity risk premium, unlevered betas)"),
    ("", ""),
    ("Colour convention", "BLUE = hardcoded input   |   BLACK = formula on this sheet   |   GREEN = link from another sheet   |   YELLOW FILL = assumption requiring written justification"),
    ("", ""),
    ("Disclaimer", "This model was built as an educational exercise. It is not investment research and is not a recommendation to buy or sell any security. All forward-looking figures are the author's own estimates."),
]
r = 4
for k, v in rows:
    if k:
        put(ws, f"A{r}", k, BOLD)
        put(ws, f"B{r}", v, BLACK)
        ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 30 if len(v) > 90 else 15
    r += 1

put(ws, "A24", "HOW TO USE", TITLE)
steps = [
    "1.  Open the 'Assumptions' tab. Every yellow cell is an input you own. Change one and the entire model recalculates.",
    "2.  'Check' on the Balance Sheet tab must read zero in every column. If it does not, the model is broken - do not use the output.",
    "3.  Fill the yellow inputs on 'WACC' with figures you pulled yourself, on a date you record.",
    "4.  Read the DCF output alongside 'Sensitivity' - a single point estimate is not a valuation.",
    "5.  Record the reasoning behind every input in docs/assumptions_log.md. That document, not this file, is what you will be questioned on.",
]
for i, s in enumerate(steps):
    put(ws, f"A{25+i}", s, BLACK)

# ========================================================= ASSUMPTIONS =====
aw = wb.create_sheet("Assumptions")
widths(aw)
put(aw, "A1", "ASSUMPTIONS", TITLE)
put(aw, "A2", "Yellow cells are inputs. Justify each one in docs/assumptions_log.md before presenting this model.", SUB)

year_header(aw, 4)

SEGMENTS = ["Switchgears", "Cables", "Lighting & Fixtures",
            "Electrical Consumer Durables", "Others (incl. solar)", "Lloyd Consumer"]

# --- revenue growth
put(aw, "A6", "REVENUE GROWTH (YoY %)", BOLD, fill=GREYFILL)
GROWTH_R0 = 7
growth_defaults = {
    "Switchgears": [0.09, 0.09, 0.09, 0.08, 0.08],
    "Cables": [0.14, 0.13, 0.12, 0.11, 0.10],
    "Lighting & Fixtures": [0.03, 0.04, 0.04, 0.04, 0.04],
    "Electrical Consumer Durables": [0.08, 0.09, 0.09, 0.08, 0.08],
    "Others (incl. solar)": [0.22, 0.20, 0.18, 0.15, 0.12],
    "Lloyd Consumer": [0.12, 0.14, 0.12, 0.10, 0.09],
}
for i, seg in enumerate(SEGMENTS):
    r = GROWTH_R0 + i
    label(aw, r, seg, indent=1)
    # historical growth computed from the IS
    put(aw, f"C{r}", f"=IF(IS!C{9+i}=0,0,IS!D{9+i}/IS!C{9+i}-1)", BLACK, PCT)
    for col, v in zip(FC, growth_defaults[seg]):
        put(aw, f"{col}{r}", v, BLUE, PCT, fill=YELLOW)
GROWTH_ROWS = {seg: GROWTH_R0 + i for i, seg in enumerate(SEGMENTS)}

# --- contribution margin
CM_R0 = GROWTH_R0 + 8
put(aw, f"A{CM_R0-1}", "CONTRIBUTION MARGIN (% of segment revenue)", BOLD, fill=GREYFILL)
put(aw, f"A{CM_R0-2}", "Havells definition: Net Revenue less material cost, manufacturing variables, direct selling variables and depreciation.", SUB)
cm_hist = {  # FY25A, FY26A actuals
    "Switchgears": (0.379, 0.369), "Cables": (0.141, 0.169),
    "Lighting & Fixtures": (0.326, 0.323), "Electrical Consumer Durables": (0.238, 0.230),
    "Others (incl. solar)": (0.170, 0.162), "Lloyd Consumer": (0.135, 0.084),
}
cm_fc = {
    "Switchgears": [0.372, 0.375, 0.375, 0.375, 0.375],
    "Cables": [0.165, 0.163, 0.162, 0.160, 0.160],
    "Lighting & Fixtures": [0.310, 0.310, 0.310, 0.310, 0.310],
    "Electrical Consumer Durables": [0.233, 0.235, 0.235, 0.235, 0.235],
    "Others (incl. solar)": [0.165, 0.168, 0.170, 0.170, 0.170],
    "Lloyd Consumer": [0.100, 0.115, 0.125, 0.130, 0.130],
}
for i, seg in enumerate(SEGMENTS):
    r = CM_R0 + i
    label(aw, r, seg, indent=1)
    put(aw, f"B{r}", cm_hist[seg][0], BLUE, PCT)
    put(aw, f"C{r}", cm_hist[seg][1], BLUE, PCT)
    for col, v in zip(FC, cm_fc[seg]):
        put(aw, f"{col}{r}", v, BLUE, PCT, fill=YELLOW)
CM_ROWS = {seg: CM_R0 + i for i, seg in enumerate(SEGMENTS)}

# --- cost & other drivers
OP_R0 = CM_R0 + 8
put(aw, f"A{OP_R0-1}", "OPERATING & CASH FLOW DRIVERS", BOLD, fill=GREYFILL)
drivers = [
    ("Advertising & sales promotion (% of net revenue)", 0.029, 0.027, [0.028]*5, PCT),
    ("Other SG&A (% of net revenue)", 0.091, 0.092, [0.090]*5, PCT),
    ("Other income, net (INR cr)", 259, 204, [220, 240, 260, 280, 300], NUM),
    ("Effective tax rate", 0.259, 0.234, [0.252]*5, PCT),
    ("Capital expenditure (% of net revenue)", 0.035, 0.066, [0.050, 0.045, 0.040, 0.038, 0.035], PCT),
    ("Depreciation & amortisation (% of net revenue)", 0.018, 0.019, [0.020, 0.021, 0.022, 0.022, 0.023], PCT),
    ("Inventory days (on net revenue)", 67, 71, [71]*5, NUM),
    ("Debtor days (on net revenue)", 21, 13, [15]*5, NUM),
    ("Creditor days (on net revenue)", 51, 47, [47]*5, NUM),
    ("Dividend payout (% of net profit)", 0.421, 0.368, [0.370]*5, PCT),
    ("Lease liability interest rate", 0.08, 0.08, [0.08]*5, PCT),
    ("Lease payments (INR cr)", 90, 90, [95, 100, 105, 110, 115], NUM),
]
for i, (name, h1, h2, fc, fmt) in enumerate(drivers):
    r = OP_R0 + i
    label(aw, r, name, indent=1)
    put(aw, f"B{r}", h1, BLUE, fmt)
    put(aw, f"C{r}", h2, BLUE, fmt)
    for col, v in zip(FC, fc):
        put(aw, f"{col}{r}", v, BLUE, fmt, fill=YELLOW)
DR = {name: OP_R0 + i for i, (name, *_rest) in enumerate(drivers)}

# --- valuation statics
VS_R0 = OP_R0 + len(drivers) + 2
put(aw, f"A{VS_R0-1}", "VALUATION STATICS", BOLD, fill=GREYFILL)
statics = [
    ("Diluted shares outstanding (crore)", 62.70, NUM1,
     "Equity share capital INR 63cr at INR 1 face value. VERIFY against latest shareholding pattern."),
    ("Current market price (INR / share)", 1190.00, RS, "Update to the price on your valuation date."),
    ("Terminal growth rate (g)", 0.05, PCT, "Must be below WACC and below long-run nominal GDP growth."),
    ("Non-core investments carried to equity bridge (INR cr)", 883.00, NUM,
     "Goldi Solar stake: INR 600cr cost + INR 283cr unrealised fair value gain. Excluded from operating EBIT."),
    ("Mid-year discounting convention (1 = on, 0 = off)", 1, NUM, "Cash arrives through the year, not on 31 March."),
]
for i, (name, v, fmt, note) in enumerate(statics):
    r = VS_R0 + i
    label(aw, r, name, indent=1)
    put(aw, f"B{r}", v, BLUE, fmt, fill=YELLOW)
    put(aw, f"D{r}", note, SUB)
ST = {name: VS_R0 + i for i, (name, *_r) in enumerate(statics)}

A = "Assumptions"


def a(name_row, col):
    return f"{A}!${col}${name_row}"


# ============================================================ HISTORICALS ==
hw = wb.create_sheet("Historicals")
widths(hw, a=52, rest=15)
put(hw, "A1", "REPORTED HISTORICALS", TITLE)
put(hw, "A2", "As reported. Do not link forecasts to this tab - it exists as an audit trail so a reader can tie the model back to the filing.", SUB)
put(hw, "A3", "Source: Havells India Ltd, Information Update on Financial Results, Q4 & FY ended 31 Mar 2026, filed with NSE/BSE 22 Apr 2026. Standalone. INR crore.", SUB)

hist_block = [
    ("PROFIT & LOSS", None, None),
    ("Net revenue", 21746, 22466),
    ("Contribution", 4343, 4458),
    ("Add: depreciation / amortisation", 399, 429),
    ("Less: advertising & sales promotion", 622, 602),
    ("Less: other SG&A", 1970, 2072),
    ("EBITDA", 2149, 2213),
    ("Depreciation / amortisation", 399, 429),
    ("Other income, net", 259, 204),
    ("Fair value gain on financial asset (unrealised)", 0, 283),
    ("Exceptional items", 0, -45),
    ("Profit before tax", 2009, 2226),
    ("Tax", 520, 520),
    ("Net profit", 1489, 1705),
    ("", None, None),
    ("SEGMENT REVENUE", None, None),
    ("Switchgears", 2395, 2585),
    ("Cables", 7184, 8677),
    ("Lighting & Fixtures", 1653, 1655),
    ("Electrical Consumer Durables", 4011, 3874),
    ("Others", 1379, 1727),
    ("Lloyd Consumer", 5123, 3948),
    ("", None, None),
    ("BALANCE SHEET", None, None),
    ("Property, plant & equipment and intangibles", 4745, 5761),
    ("Investments", 74, 956),
    ("Other non-current assets", 158, 247),
    ("Inventories", 4007, 4398),
    ("Trade receivables", 1254, 782),
    ("Cash, equivalents and other bank balances", 3353, 2351),
    ("Other financial assets", 6, 9),
    ("Other current assets", 179, 221),
    ("Total assets", 13775, 14724),
    ("Equity share capital", 63, 63),
    ("Other equity", 8268, 9414),
    ("Lease liabilities - non-current", 241, 188),
    ("Deferred tax liabilities, net", 375, 435),
    ("Other non-current liabilities", 67, 62),
    ("Lease liabilities - current", 78, 77),
    ("Trade payables", 3040, 2903),
    ("Other financial liabilities", 865, 868),
    ("Other current liabilities", 778, 715),
    ("Total equity and liabilities", 13775, 14724),
    ("", None, None),
    ("CASH FLOW", None, None),
    ("Operating net cash flow", 1543, 1557),
    ("Capital expenditure", -753, -1484),
    ("Dividends paid", -627, -627),
]
year_header(hw, 5)
r = 6
for name, v25, v26 in hist_block:
    if v25 is None:
        label(hw, r, name, bold=True)
        if name:
            hw.cell(row=r, column=1).fill = GREYFILL
    else:
        label(hw, r, name, indent=1)
        put(hw, f"B{r}", v25, BLUE, NUM)
        put(hw, f"C{r}", v26, BLUE, NUM)
    r += 1

# ======================================================= INCOME STATEMENT ==
iw = wb.create_sheet("IS")
widths(iw)
put(iw, "A1", "INCOME STATEMENT", TITLE)
put(iw, "A2", "INR crore. Format mirrors the company's own investor-update P&L so figures tie directly to the filing.", SUB)
put(iw, "A3", "Note: the FY26 unrealised fair value gain on the Goldi Solar stake (INR 283cr) and the INR 45cr exceptional item are deliberately EXCLUDED. Neither is operating income.", SUB)
year_header(iw, 5)

# rows
IS_SEG0 = 9
put(iw, "A7", "REVENUE", BOLD, fill=GREYFILL)
seg_hist = {"Switchgears": (2395, 2585), "Cables": (7184, 8677),
            "Lighting & Fixtures": (1653, 1655), "Electrical Consumer Durables": (4011, 3874),
            "Others (incl. solar)": (1379, 1727), "Lloyd Consumer": (5123, 3948)}
for i, seg in enumerate(SEGMENTS):
    r = IS_SEG0 + i
    label(iw, r, seg, indent=1)
    put(iw, f"B{r}", seg_hist[seg][0], BLUE, NUM)
    put(iw, f"C{r}", seg_hist[seg][1], BLUE, NUM)
    for j, col in enumerate(FC):
        prev = COLS[COLS.index(col) - 1]
        put(iw, f"{col}{r}", f"={prev}{r}*(1+{A}!{col}${GROWTH_ROWS[seg]})", BLACK, NUM)
IS_REV = IS_SEG0 + 6
label(iw, IS_REV, "Net revenue", bold=True)
for col in COLS:
    put(iw, f"{col}{IS_REV}", f"=SUM({col}{IS_SEG0}:{col}{IS_SEG0+5})", BOLD, NUM, border=TOPBORDER)

IS_CON0 = IS_REV + 3
put(iw, f"A{IS_CON0-1}", "CONTRIBUTION", BOLD, fill=GREYFILL)
for i, seg in enumerate(SEGMENTS):
    r = IS_CON0 + i
    label(iw, r, seg, indent=1)
    for col in COLS:
        put(iw, f"{col}{r}", f"={col}{IS_SEG0+i}*{A}!{col}${CM_ROWS[seg]}", BLACK, NUM)
IS_CON = IS_CON0 + 6
label(iw, IS_CON, "Total contribution", bold=True)
for col in COLS:
    put(iw, f"{col}{IS_CON}", f"=SUM({col}{IS_CON0}:{col}{IS_CON0+5})", BOLD, NUM, border=TOPBORDER)
IS_CONPCT = IS_CON + 1
label(iw, IS_CONPCT, "   as % of net revenue")
for col in COLS:
    put(iw, f"{col}{IS_CONPCT}", f"={col}{IS_CON}/{col}{IS_REV}", SUB, PCT)

R = IS_CONPCT + 2
IS_DA_ADD = R
label(R := R, None) if False else None
label(iw, IS_DA_ADD, "Add: depreciation & amortisation", indent=1)
IS_ASP = IS_DA_ADD + 1
IS_SGA = IS_DA_ADD + 2
IS_EBITDA = IS_DA_ADD + 3
IS_EBITDAM = IS_DA_ADD + 4
IS_DA = IS_DA_ADD + 6
IS_EBIT = IS_DA_ADD + 7
IS_EBITM = IS_DA_ADD + 8
IS_OI = IS_DA_ADD + 10
IS_FIN = IS_DA_ADD + 11
IS_PBT = IS_DA_ADD + 12
IS_TAX = IS_DA_ADD + 13
IS_NP = IS_DA_ADD + 14
IS_NPM = IS_DA_ADD + 15
IS_DIV = IS_DA_ADD + 17
IS_RET = IS_DA_ADD + 18

label(iw, IS_ASP, "Less: advertising & sales promotion", indent=1)
label(iw, IS_SGA, "Less: other SG&A", indent=1)
label(iw, IS_EBITDA, "EBITDA", bold=True)
label(iw, IS_EBITDAM, "   EBITDA margin")
label(iw, IS_DA, "Less: depreciation & amortisation", indent=1)
label(iw, IS_EBIT, "EBIT (clean, operating)", bold=True)
label(iw, IS_EBITM, "   EBIT margin")
label(iw, IS_OI, "Add: other income, net", indent=1)
label(iw, IS_FIN, "Less: finance cost (lease interest)", indent=1)
label(iw, IS_PBT, "Profit before tax", bold=True)
label(iw, IS_TAX, "Less: tax", indent=1)
label(iw, IS_NP, "NET PROFIT", bold=True)
label(iw, IS_NPM, "   net margin")
label(iw, IS_DIV, "Memo: dividends declared", indent=1)
label(iw, IS_RET, "Memo: retained earnings for the year", indent=1)

SCH = "Schedules"
for col in COLS:
    put(iw, f"{col}{IS_DA_ADD}", f"=Schedules!{col}$8", GREEN, NUM)
    put(iw, f"{col}{IS_ASP}", f"=-{col}{IS_REV}*{A}!{col}${DR['Advertising & sales promotion (% of net revenue)']}", BLACK, NUM)
    put(iw, f"{col}{IS_SGA}", f"=-{col}{IS_REV}*{A}!{col}${DR['Other SG&A (% of net revenue)']}", BLACK, NUM)
    put(iw, f"{col}{IS_EBITDA}", f"={col}{IS_CON}+{col}{IS_DA_ADD}+{col}{IS_ASP}+{col}{IS_SGA}", BOLD, NUM, border=TOPBORDER)
    put(iw, f"{col}{IS_EBITDAM}", f"={col}{IS_EBITDA}/{col}{IS_REV}", SUB, PCT)
    put(iw, f"{col}{IS_DA}", f"=-{SCH}!{col}$8", GREEN, NUM)
    put(iw, f"{col}{IS_EBIT}", f"={col}{IS_EBITDA}+{col}{IS_DA}", BOLD, NUM, border=TOPBORDER)
    put(iw, f"{col}{IS_EBITM}", f"={col}{IS_EBIT}/{col}{IS_REV}", SUB, PCT)
    put(iw, f"{col}{IS_OI}", f"={A}!{col}${DR['Other income, net (INR cr)']}", GREEN, NUM)
    put(iw, f"{col}{IS_FIN}", f"=-{SCH}!{col}$29", GREEN, NUM)
    put(iw, f"{col}{IS_PBT}", f"={col}{IS_EBIT}+{col}{IS_OI}+{col}{IS_FIN}", BOLD, NUM, border=TOPBORDER)
    put(iw, f"{col}{IS_TAX}", f"=-{col}{IS_PBT}*{A}!{col}${DR['Effective tax rate']}", BLACK, NUM)
    put(iw, f"{col}{IS_NP}", f"={col}{IS_PBT}+{col}{IS_TAX}", BOLD, NUM, border=TOPDOUBLE)
    put(iw, f"{col}{IS_NPM}", f"={col}{IS_NP}/{col}{IS_REV}", SUB, PCT)
    put(iw, f"{col}{IS_DIV}", f"=-{col}{IS_NP}*{A}!{col}${DR['Dividend payout (% of net profit)']}", BLACK, NUM)
    put(iw, f"{col}{IS_RET}", f"={col}{IS_NP}+{col}{IS_DIV}", BLACK, NUM)

# ============================================================= SCHEDULES ===
sw = wb.create_sheet("Schedules")
widths(sw)
put(sw, "A1", "SUPPORTING SCHEDULES", TITLE)
put(sw, "A2", "Fixed assets, working capital and lease liabilities. Every balance-sheet movement originates here.", SUB)
year_header(sw, 4)

put(sw, "A6", "FIXED ASSET (PP&E AND INTANGIBLES) SCHEDULE", BOLD, fill=GREYFILL)
label(sw, 7, "Opening net block", indent=1)
label(sw, 8, "Less: depreciation & amortisation", indent=1)
label(sw, 9, "Add: capital expenditure", indent=1)
label(sw, 10, "Other movements (disposals, reclassification)", indent=1)
label(sw, 11, "Closing net block", bold=True)
put(sw, "B8", 399, BLUE, NUM)
put(sw, "C7", 4745, BLUE, NUM)
put(sw, "C8", 429, BLUE, NUM)
put(sw, "C9", 1484, BLUE, NUM)
put(sw, "C10", -39, BLUE, NUM)
put(sw, "C11", "=C7-C8+C9+C10", BOLD, NUM, border=TOPBORDER)
put(sw, "D10", "FY26 plug: the reported closing block of INR 5,761cr does not tie to opening less depreciation plus capex. "
              "Disposals and reclassifications explain the gap. Trace it in the FY26 annual report PP&E note and replace this plug.", SUB)
for col in FC:
    prev = COLS[COLS.index(col) - 1]
    put(sw, f"{col}7", f"={prev}11", BLACK, NUM)
    put(sw, f"{col}8", f"=IS!{col}${IS_REV}*{A}!{col}${DR['Depreciation & amortisation (% of net revenue)']}", BLACK, NUM)
    put(sw, f"{col}9", f"=IS!{col}${IS_REV}*{A}!{col}${DR['Capital expenditure (% of net revenue)']}", BLACK, NUM)
    put(sw, f"{col}10", 0, BLUE, NUM)
    put(sw, f"{col}11", f"={col}7-{col}8+{col}9+{col}10", BOLD, NUM, border=TOPBORDER)

put(sw, "A13", "WORKING CAPITAL SCHEDULE", BOLD, fill=GREYFILL)
wc_rows = [
    (14, "Inventories", "Inventory days (on net revenue)"),
    (15, "Trade receivables", "Debtor days (on net revenue)"),
    (16, "Trade payables", "Creditor days (on net revenue)"),
]
wc_actuals = {14: (4007, 4398), 15: (1254, 782), 16: (3040, 2903)}
for r, name, drv in wc_rows:
    label(sw, r, name, indent=1)
    put(sw, f"B{r}", wc_actuals[r][0], BLUE, NUM)
    put(sw, f"C{r}", wc_actuals[r][1], BLUE, NUM)
    for col in FC:
        put(sw, f"{col}{r}", f"=IS!{col}${IS_REV}*{A}!{col}${DR[drv]}/365", BLACK, NUM)
put(sw, "D13", "Historical columns are the reported balances, so the FY27 movement ties exactly to the FY26 balance sheet. "
              "Forecast columns are driven by the days assumptions.", SUB)
label(sw, 17, "Net working capital", bold=True)
label(sw, 18, "Increase / (decrease) in net working capital", indent=1)
label(sw, 19, "   NWC days on net revenue")
for col in COLS:
    put(sw, f"{col}17", f"={col}14+{col}15-{col}16", BOLD, NUM, border=TOPBORDER)
    put(sw, f"{col}19", f"={col}17/IS!{col}${IS_REV}*365", SUB, NUM)
for col in COLS[1:]:
    prev = COLS[COLS.index(col) - 1]
    put(sw, f"{col}18", f"={col}17-{prev}17", BLACK, NUM)

put(sw, "A22", "LEASE LIABILITY SCHEDULE", BOLD, fill=GREYFILL)
put(sw, "A23", "Havells carries no borrowings. The only debt-like liability on the balance sheet is Ind AS 116 lease liabilities.", SUB)
label(sw, 25, "Opening lease liability", indent=1)
label(sw, 26, "Add: interest accretion (to income statement)", indent=1)
label(sw, 27, "Less: lease payments (cash)", indent=1)
label(sw, 28, "Closing lease liability", bold=True)
label(sw, 29, "Memo: finance cost to income statement", indent=1)
put(sw, "A24", "SIMPLIFYING ASSUMPTION: principal is held flat, i.e. new leases recognised each year are assumed to offset amortisation of existing ones. "
              "Cash lease payments therefore equal interest accretion. At INR 265cr against a market capitalisation near INR 75,000cr this is immaterial, "
              "but state it in your memo rather than letting a reader discover it.", SUB)
put(sw, "C25", 319, BLUE, NUM)
put(sw, "C26", 37, BLUE, NUM)
put(sw, "C27", 91, BLUE, NUM)
put(sw, "C28", 265, BLUE, NUM)
put(sw, "C29", "=C26", BLACK, NUM)
for col in FC:
    prev = COLS[COLS.index(col) - 1]
    put(sw, f"{col}25", f"={prev}28", BLACK, NUM)
    put(sw, f"{col}26", f"={col}25*{A}!{col}${DR['Lease liability interest rate']}", BLACK, NUM)
    put(sw, f"{col}27", f"={col}26", BLACK, NUM)
    put(sw, f"{col}28", f"={col}25+{col}26-{col}27", BOLD, NUM, border=TOPBORDER)
    put(sw, f"{col}29", f"={col}26", BLACK, NUM)
label(sw, 30, "   split: non-current (70%)", indent=1)
label(sw, 31, "   split: current (30%)", indent=1)
for col in FC:
    put(sw, f"{col}30", f"={col}28*0.7", BLACK, NUM)
    put(sw, f"{col}31", f"={col}28*0.3", BLACK, NUM)
put(sw, "C30", 188, BLUE, NUM)
put(sw, "C31", 77, BLUE, NUM)

# ========================================================== CASH FLOW ======
cw = wb.create_sheet("CFS")
widths(cw)
put(cw, "A1", "CASH FLOW STATEMENT", TITLE)
put(cw, "A2", "Indirect method. Forecast years only - the historical cash flow is on the Historicals tab.", SUB)
year_header(cw, 4)

cf = {
    6: ("OPERATING ACTIVITIES", None),
    7: ("Net profit", f"=IS!{{c}}${IS_NP}"),
    8: ("Add back: depreciation & amortisation", "=Schedules!{c}$8"),
    9: ("Less: increase in net working capital", "=-Schedules!{c}$18"),
    10: ("Cash flow from operations", "=SUM({c}7:{c}9)"),
    12: ("INVESTING ACTIVITIES", None),
    13: ("Capital expenditure", "=-Schedules!{c}$9"),
    14: ("Other movements in fixed assets", "=-Schedules!{c}$10"),
    15: ("Cash flow from investing", "=SUM({c}13:{c}14)"),
    17: ("FINANCING ACTIVITIES", None),
    18: ("Dividends paid", f"=IS!{{c}}${IS_DIV}"),
    19: ("Cash flow from financing", "={c}18"),
    21: ("Net increase / (decrease) in cash", "={c}10+{c}15+{c}19"),
    22: ("Opening cash and bank balances", None),
    23: ("Closing cash and bank balances", "={c}21+{c}22"),
}
for r, (name, f) in cf.items():
    if f is None and name.isupper():
        label(cw, r, name, bold=True)
        cw.cell(row=r, column=1).fill = GREYFILL
        continue
    bold = r in (10, 15, 19, 21, 23)
    label(cw, r, name, bold=bold)
    if f:
        for col in FC:
            put(cw, f"{col}{r}", f.replace("{c}", col), BOLD if bold else BLACK, NUM,
                border=TOPBORDER if bold else None)
put(cw, "C23", 2351, BLUE, NUM)
for col in FC:
    prev = COLS[COLS.index(col) - 1]
    put(cw, f"{col}22", f"={prev}23", BLACK, NUM)

# ========================================================= BALANCE SHEET ===
bw = wb.create_sheet("BS")
widths(bw)
put(bw, "A1", "BALANCE SHEET", TITLE)
put(bw, "A2", "The 'Check' row must read zero in every column. A non-zero check means the model is broken.", SUB)
year_header(bw, 4)

BS_ROWS = [
    (6, "ASSETS", None, None, None),
    (7, "Property, plant & equipment and intangibles", 4745, 5761, "=Schedules!{c}$11"),
    (8, "Investments", 74, 956, "=C8"),
    (9, "Other non-current assets", 158, 247, "=C9"),
    (10, "Inventories", 4007, 4398, "=Schedules!{c}$14"),
    (11, "Trade receivables", 1254, 782, "=Schedules!{c}$15"),
    (12, "Cash, equivalents and other bank balances", 3353, 2351, "=CFS!{c}$23"),
    (13, "Other financial assets", 6, 9, "=C13"),
    (14, "Other current assets", 179, 221, "=C14"),
    (15, "TOTAL ASSETS", None, None, "=SUM({c}7:{c}14)"),
    (17, "EQUITY AND LIABILITIES", None, None, None),
    (18, "Equity share capital", 63, 63, "=C18"),
    (19, "Other equity", 8268, 9414, None),
    (20, "Lease liabilities - non-current", 241, 188, "=Schedules!{c}$30"),
    (21, "Deferred tax liabilities, net", 375, 435, "=C21"),
    (22, "Other non-current liabilities", 67, 62, "=C22"),
    (23, "Lease liabilities - current", 78, 77, "=Schedules!{c}$31"),
    (24, "Trade payables", 3040, 2903, "=Schedules!{c}$16"),
    (25, "Other financial liabilities", 865, 868, "=C25"),
    (26, "Other current liabilities", 778, 715, "=C26"),
    (27, "TOTAL EQUITY AND LIABILITIES", None, None, "=SUM({c}18:{c}26)"),
]
for r, name, v25, v26, f in BS_ROWS:
    if f is None and v25 is None:
        label(bw, r, name, bold=True)
        bw.cell(row=r, column=1).fill = GREYFILL
        continue
    bold = name.isupper()
    label(bw, r, name, bold=bold, indent=0 if bold else 1)
    if v25 is not None:
        put(bw, f"B{r}", v25, BLUE, NUM)
        put(bw, f"C{r}", v26, BLUE, NUM)
    if f:
        for col in FC:
            fnt = GREEN if "!" in f else BLACK
            put(bw, f"{col}{r}", f.replace("{c}", col), BOLD if bold else fnt, NUM,
                border=TOPBORDER if bold else None)
# totals for historical columns
for col in ("B", "C"):
    put(bw, f"{col}15", f"=SUM({col}7:{col}14)", BOLD, NUM, border=TOPBORDER)
    put(bw, f"{col}27", f"=SUM({col}18:{col}26)", BOLD, NUM, border=TOPBORDER)
# retained earnings roll-forward
for col in FC:
    prev = COLS[COLS.index(col) - 1]
    put(bw, f"{col}19", f"={prev}19+IS!{col}${IS_RET}", BLACK, NUM)

put(bw, "A31", "The FY25A column reads 1 rather than 0. This is the company's own rounding in the abridged balance sheet it filed, not a model error - the reported totals do not sum exactly. Every forecast column reads zero.", SUB)
label(bw, 29, "CHECK (must be zero)", bold=True)
for col in COLS:
    put(bw, f"{col}29", f"={col}15-{col}27", BOLD, NUM, border=TOPDOUBLE)

# ================================================================= WACC ====
ww = wb.create_sheet("WACC")
ww.column_dimensions["A"].width = 52
ww.column_dimensions["B"].width = 14
ww.column_dimensions["C"].width = 72
put(ww, "A1", "WEIGHTED AVERAGE COST OF CAPITAL", TITLE)
put(ww, "A2", "Havells carries no borrowings. WACC is therefore close to pure cost of equity. Replace every yellow cell with a figure you pulled yourself, and record the date.", SUB)

wacc_rows = [
    (4, "COST OF EQUITY (CAPM)", None, None, None),
    (5, "Risk-free rate (10-year India G-Sec yield)", 0.068, PCT, "SOURCE: RBI / CCIL. Record the date you pulled this."),
    (6, "Levered beta", 0.90, NUM1, "Run scripts/beta_regression.py on 5y weekly returns vs NIFTY 500. Cross-check against Damodaran's unlevered beta for Electrical Equipment, relevered."),
    (7, "Equity risk premium (India)", 0.065, PCT, "SOURCE: Damodaran country risk premium table. Cite the vintage."),
    (8, "Cost of equity  =  Rf + beta x ERP", "=B5+B6*B7", PCT, None),
    (10, "COST OF DEBT", None, None, None),
    (11, "Pre-tax cost of debt", 0.080, PCT, "Implied lease discount rate. Havells has no borrowings, so this is a notional figure."),
    (12, "Marginal tax rate", 0.252, PCT, "Indian statutory rate under the concessional regime."),
    (13, "After-tax cost of debt", "=B11*(1-B12)", PCT, None),
    (15, "CAPITAL STRUCTURE", None, None, None),
    (16, "Market value of equity (INR cr)", f"={A}!B{ST['Diluted shares outstanding (crore)']}*{A}!B{ST['Current market price (INR / share)']}", NUM, "Shares x price, both from Assumptions."),
    (17, "Debt: lease liabilities (INR cr)", "=Schedules!C28", NUM, "The only debt-like item on the balance sheet."),
    (18, "Total capital (INR cr)", "=B16+B17", NUM, None),
    (19, "Weight of equity", "=B16/B18", PCT, None),
    (20, "Weight of debt", "=B17/B18", PCT, None),
    (22, "WACC", "=B19*B8+B20*B13", PCT, "With a debt weight this small, WACC is effectively cost of equity. Say so explicitly in your memo rather than fabricating leverage."),
]
for r, name, v, fmt, note in wacc_rows:
    if v is None:
        label(ww, r, name, bold=True)
        ww.cell(row=r, column=1).fill = GREYFILL
        continue
    label(ww, r, name, bold=(r in (8, 13, 22)), indent=0 if r in (8, 13, 22) else 1)
    is_input = isinstance(v, (int, float))
    put(ww, f"B{r}", v, BLUE if is_input else BOLD, fmt,
        fill=YELLOW if is_input else None, border=TOPBORDER if r in (8, 13, 22) else None)
    if note:
        put(ww, f"C{r}", note, SUB)
        ww[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ww.row_dimensions[r].height = 28

# ================================================================== DCF ====
dw = wb.create_sheet("DCF")
widths(dw)
put(dw, "A1", "DISCOUNTED CASH FLOW - FREE CASH FLOW TO FIRM", TITLE)
put(dw, "A2", "FCFF = EBIT x (1 - tax rate) + D&A - capex - increase in net working capital.", SUB)
put(dw, "A3", "EBIT here is CLEAN OPERATING EBIT: it excludes other income, the Goldi Solar fair value gain and exceptional items. Those are handled in the equity bridge instead.", SUB)

put(dw, "A5", "INR crore", HDR, fill=NAVY)
for col, yr in zip(FC, YEARS[2:]):
    put(dw, f"{col}5", yr, HDR, fill=NAVY, align="center")

D_EBIT, D_TAXR, D_NOPAT = 7, 8, 9
D_DA, D_CAPEX, D_NWC, D_FCFF = 11, 12, 13, 15
D_T, D_DF, D_PV = 17, 18, 19
for r, name in [(D_EBIT, "EBIT (clean, operating)"), (D_TAXR, "Effective tax rate"),
                (D_NOPAT, "NOPAT = EBIT x (1 - t)"), (D_DA, "Add: depreciation & amortisation"),
                (D_CAPEX, "Less: capital expenditure"), (D_NWC, "Less: increase in net working capital"),
                (D_FCFF, "FREE CASH FLOW TO FIRM"), (D_T, "Discount period (mid-year convention)"),
                (D_DF, "Discount factor"), (D_PV, "Present value of FCFF")]:
    label(dw, r, name, bold=r in (D_NOPAT, D_FCFF))
for i, col in enumerate(FC):
    put(dw, f"{col}{D_EBIT}", f"=IS!{col}${IS_EBIT}", GREEN, NUM)
    put(dw, f"{col}{D_TAXR}", f"={A}!{col}${DR['Effective tax rate']}", GREEN, PCT)
    put(dw, f"{col}{D_NOPAT}", f"={col}{D_EBIT}*(1-{col}{D_TAXR})", BOLD, NUM, border=TOPBORDER)
    put(dw, f"{col}{D_DA}", f"=Schedules!{col}$8", GREEN, NUM)
    put(dw, f"{col}{D_CAPEX}", f"=-Schedules!{col}$9", GREEN, NUM)
    put(dw, f"{col}{D_NWC}", f"=-Schedules!{col}$18", GREEN, NUM)
    put(dw, f"{col}{D_FCFF}", f"={col}{D_NOPAT}+{col}{D_DA}+{col}{D_CAPEX}+{col}{D_NWC}", BOLD, NUM, border=TOPDOUBLE)
    put(dw, f"{col}{D_T}", f"={i+1}-{A}!$B${ST['Mid-year discounting convention (1 = on, 0 = off)']}*0.5", BLACK, NUM1)
    put(dw, f"{col}{D_DF}", f"=1/(1+WACC!$B$22)^{col}{D_T}", BLACK, '0.000')
    put(dw, f"{col}{D_PV}", f"={col}{D_FCFF}*{col}{D_DF}", BLACK, NUM)

V0 = 22
val_rows = [
    (V0, "VALUATION BRIDGE", None, None, None),
    (V0+1, "Sum of PV of explicit forecast FCFF", f"=SUM(D{D_PV}:H{D_PV})", NUM, None),
    (V0+2, "Terminal value (Gordon growth)", f"=H{D_FCFF}*(1+{A}!$B${ST['Terminal growth rate (g)']})/(WACC!$B$22-{A}!$B${ST['Terminal growth rate (g)']})", NUM, "TV = final-year FCFF x (1+g) / (WACC - g)"),
    (V0+3, "PV of terminal value", f"=B{V0+2}*H{D_DF}", NUM, None),
    (V0+4, "ENTERPRISE VALUE", f"=B{V0+1}+B{V0+3}", NUM, None),
    (V0+5, "   terminal value as % of enterprise value", f"=B{V0+3}/B{V0+4}", PCT, "If this is above 75%, say so openly in your memo. It is the standard criticism of any DCF."),
    (V0+7, "Add: cash, equivalents and bank balances", "=BS!C12", NUM, "FY26 closing balance."),
    (V0+8, "Less: lease liabilities (debt-like)", "=-Schedules!C28", NUM, None),
    (V0+9, "Add: non-core investments", f"={A}!$B${ST['Non-core investments carried to equity bridge (INR cr)']}", NUM, "Goldi Solar stake at carrying value, since its earnings were excluded from EBIT."),
    (V0+10, "EQUITY VALUE", f"=B{V0+4}+B{V0+7}+B{V0+8}+B{V0+9}", NUM, None),
    (V0+11, "Diluted shares outstanding (crore)", f"={A}!$B${ST['Diluted shares outstanding (crore)']}", NUM1, None),
    (V0+12, "INTRINSIC VALUE PER SHARE (INR)", f"=B{V0+10}/B{V0+11}", RS, None),
    (V0+13, "Current market price (INR)", f"={A}!$B${ST['Current market price (INR / share)']}", RS, None),
    (V0+14, "Implied upside / (downside)", f"=B{V0+12}/B{V0+13}-1", PCT, "If this is wildly positive, re-examine your assumptions before you conclude the market is wrong."),
]
for r, name, f, fmt, note in val_rows:
    if f is None:
        label(dw, r, name, bold=True)
        dw.cell(row=r, column=1).fill = GREYFILL
        continue
    bold = name.isupper()
    label(dw, r, name, bold=bold, indent=0 if bold else 1)
    put(dw, f"B{r}", f, BOLD if bold else BLACK, fmt, border=TOPBORDER if bold else None)
    if note:
        put(dw, f"D{r}", note, SUB)

DCF_VPS = V0 + 12

# ========================================================== SENSITIVITY ====
vw = wb.create_sheet("Sensitivity")
widths(vw, a=34, rest=13)
put(vw, "A1", "SENSITIVITY ANALYSIS", TITLE)
put(vw, "A2", "Intrinsic value per share (INR). Each cell fully re-discounts the explicit forecast and rebuilds terminal value at the stated WACC and g.", SUB)
put(vw, "A4", "WACC (columns) vs terminal growth g (rows)", BOLD)

wacc_grid = [-0.02, -0.01, 0.0, 0.01, 0.02]
g_grid = [-0.01, -0.005, 0.0, 0.005, 0.01]

put(vw, "B6", "g  \\  WACC", BOLD, align="center", fill=GREYFILL)
for j, dwacc in enumerate(wacc_grid):
    col = get_column_letter(3 + j)
    put(vw, f"{col}6", f"=WACC!$B$22+{dwacc}", BOLD, PCT, align="center", fill=GREYFILL)
for i, dg in enumerate(g_grid):
    r = 7 + i
    put(vw, f"B{r}", f"={A}!$B${ST['Terminal growth rate (g)']}+{dg}", BOLD, PCT, fill=GREYFILL)
    for j, dwacc in enumerate(wacc_grid):
        col = get_column_letter(3 + j)
        w = f"(WACC!$B$22+{dwacc})"
        g = f"({A}!$B${ST['Terminal growth rate (g)']}+{dg})"
        pv_explicit = f"SUMPRODUCT(DCF!$D${D_FCFF}:$H${D_FCFF},(1+{w})^-DCF!$D${D_T}:$H${D_T})"
        tv = f"DCF!$H${D_FCFF}*(1+{g})/({w}-{g})"
        pv_tv = f"{tv}*(1+{w})^-DCF!$H${D_T}"
        eq = (f"({pv_explicit}+{pv_tv}+BS!$C$12-Schedules!$C$28"
              f"+{A}!$B${ST['Non-core investments carried to equity bridge (INR cr)']})")
        f = f"=IF({w}<={g},NA(),{eq}/{A}!$B${ST['Diluted shares outstanding (crore)']})"
        put(vw, f"{col}{r}", f, BLACK, RS, align="center")

put(vw, "B14", "Current market price", BOLD)
put(vw, "C14", f"={A}!$B${ST['Current market price (INR / share)']}", BLUE, RS)
put(vw, "B15", "Base case intrinsic value", BOLD)
put(vw, "C15", f"=DCF!$B${DCF_VPS}", GREEN, RS)

put(vw, "A18", "REVERSE DCF", TITLE)
put(vw, "A19", "Hold WACC and g fixed, then use Excel's Goal Seek (Data > What-If Analysis > Goal Seek) to solve for the segment growth or contribution margin", SUB)
put(vw, "A20", "assumptions that make DCF!B" + str(DCF_VPS) + " equal the current market price. Then write one paragraph on whether those implied assumptions are achievable.", SUB)
put(vw, "A21", "This is the most defensible thing in the whole model. A DCF that disagrees with the market is only interesting once you can say WHAT the market is assuming.", SUB)

# --------------------------------------------------------------- save ------
out = os.path.join(os.path.dirname(__file__), "..", "model",
                   "Havells_3Statement_DCF_Model.xlsx")
out = os.path.abspath(out)
os.makedirs(os.path.dirname(out), exist_ok=True)
wb.save(out)
print("Written:", out)
