"""
build_lbo_model.py
-------------------
Havells India: hypothetical LBO model. Single senior term loan, India-adjusted
leverage. Built on top of the operating forecast from the companion 3-statement
DCF model (../../model/Havells_3Statement_DCF_Model.xlsx).

IMPORTANT: READ THIS BEFORE USING THE OUTPUT:
Havells is NOT a realistic LBO target. The promoter group (QRG Investments and
Holdings) holds ~59% of the company, and a take-private of a company this size
(~INR 70,000 Cr market cap) would be one of the largest buyouts ever attempted
in India. This model is an explicit hypothetical, built to demonstrate LBO
mechanics on a clean, well-disclosed dataset, not a deal thesis. Say this in
your memo before anyone reads the numbers.

Run:  python scripts/build_lbo_model.py
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import os

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
REDFILL = PatternFill("solid", fgColor="FFC7CE")

TOPBORDER = Border(top=Side(style="thin"))
TOPDOUBLE = Border(top=Side(style="thin"), bottom=Side(style="double"))

NUM = '#,##0;(#,##0);"-"'
PCT = '0.0%'
MULT = '0.00x'
RS = '#,##0.00'

YEARS = ["FY27E", "FY28E", "FY29E", "FY30E", "FY31E"]
COLS = ["B", "C", "D", "E", "F"]


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


def label(ws, row, text, bold=False, indent=0, col=1):
    c = ws.cell(row=row, column=col)
    c.value = text
    c.font = BOLD if bold else BLACK
    if indent:
        c.alignment = Alignment(indent=indent)


def year_header(ws, row, first_col="B"):
    put(ws, f"A{row}", "INR crore", HDR, fill=NAVY)
    start = COLS.index(first_col)
    for col, yr in zip(COLS[start:], YEARS):
        put(ws, f"{col}{row}", yr, HDR, fill=NAVY, align="center")


def widths(ws, a=50, rest=14):
    ws.column_dimensions["A"].width = a
    for col in ["B", "C", "D", "E", "F", "G", "H"]:
        ws.column_dimensions[col].width = rest


wb = Workbook()

# =============================================================== COVER =====
ws = wb.active
ws.title = "Cover"
ws.column_dimensions["A"].width = 34
ws.column_dimensions["B"].width = 82

put(ws, "A1", "HAVELLS INDIA LIMITED", TITLE)
put(ws, "A2", "Hypothetical Leveraged Buyout Model", SUB)

put(ws, "A4", "READ THIS FIRST", TITLE)
warn = ("Havells is NOT a realistic LBO target. The promoter group (QRG Investments and Holdings) "
        "holds approximately 59% of the company, and a take-private at this scale (~INR 70,000 Cr "
        "market cap) would be one of the largest buyouts ever attempted in India. India's bank-dominated "
        "debt market also would not support US-style leverage multiples. This model is an explicit "
        "hypothetical exercise in LBO mechanics on a clean, well-disclosed dataset: it is not a deal "
        "thesis and should never be presented as one. State this plainly in any memo or interview "
        "discussion of this model, before the numbers.")
put(ws, "A5", warn, BLACK)
ws["A5"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A5:B5")
ws.row_dimensions[5].height = 95

rows = [
    ("Companion model", "Operating forecast (revenue, EBITDA, D&A, capex, working capital) is carried over "
                          "from Havells_3Statement_DCF_Model.xlsx, base case, FY27E-FY31E."),
    ("Entry point", "Start of FY27E (i.e. transaction closes using FY26A actuals as the LTM reference)."),
    ("Debt structure", "Single senior secured term loan only, by design, no mezzanine tranche. Simpler and "
                        "cleaner for a first LBO build; a real deal at this leverage would likely be single-tranche anyway."),
    ("Leverage", "India-adjusted and conservative relative to US benchmarks (which run 4-6x EBITDA total in 2026): "
                 "this model anchors to roughly 2.5-3x total leverage, reflecting India's bank-dominated, lower-risk-tolerance debt market."),
    ("Units", "INR crore unless stated otherwise"),
    ("Colour convention", "BLUE = hardcoded input   |   BLACK = formula on this sheet   |   GREEN = link from another sheet   |   YELLOW FILL = assumption requiring justification"),
    ("Disclaimer", "Educational exercise. Not investment research, not a deal recommendation, not investment advice."),
]
r = 12
for k, v in rows:
    put(ws, f"A{r}", k, BOLD)
    put(ws, f"B{r}", v, BLACK)
    ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 44 if len(v) > 90 else 16
    r += 2

# =========================================================== ASSUMPTIONS ===
aw = wb.create_sheet("Assumptions")
widths(aw, a=48)
put(aw, "A1", "TRANSACTION ASSUMPTIONS", TITLE)
put(aw, "A2", "Every yellow cell is an input you own and must justify.", SUB)

rows = [
    (4, "ENTRY", None, None, None),
    (5, "Entry EBITDA, FY26A (LTM at close)", 2213, NUM, "Reported FY26A EBITDA. Source: Havells Information Update, Q4 FY26."),
    (6, "Illustrative entry EV/EBITDA multiple", 12.0, MULT, "Deliberately BELOW Havells' actual public trading multiple "
        "(~33x EV/EBITDA at a ~INR 1,190 share price); see memo cell below. A real buyer would need to pay near the "
        "trading multiple plus a control premium; at that price, no plausible debt-funded structure clears an "
        "acceptable IRR. Run the Sensitivity tab at higher entry multiples to see this directly."),
    (7, "  Memo: current public EV/EBITDA multiple (context only)", 32.8, MULT, "For contrast only; not used in any formula. "
        "Illustrates why Havells does not clear as a real LBO at its traded price."),
    (8, "Entry net cash (FY26A): cash & bank balances", 2351, NUM, "Havells' FY26A closing cash and other bank balances."),
    (9, "Entry net cash (FY26A): lease liabilities (debt-like)", -265, NUM, "The only debt-like item on Havells' balance sheet."),
    (10, "Entry net cash, total", "=B8+B9", NUM, None),
    (12, "FINANCING", None, None, None),
    (13, "Total leverage (x FY26A EBITDA)", 2.75, MULT, "India-adjusted and conservative vs. the 4-6x total typical in "
        "US buyouts today: this reflects a bank-dominated, lower-risk-tolerance Indian debt market."),
    (14, "Senior term loan interest rate (all-in)", 0.105, PCT, "Illustrative Indian large-cap secured lending rate. "
        "Cite an actual benchmark (SBI MCLR + spread, or a comparable rated NCD) before presenting this."),
    (15, "Mandatory amortisation (% of original principal, per year)", 0.05, PCT, "Standard term-loan amortisation schedule."),
    (16, "Cash sweep (% of excess free cash flow swept to debt paydown)", 1.00, PCT, "100% cash sweep is aggressive but "
        "standard base-case LBO practice; a covenant-lite deal might use less."),
    (17, "Transaction fees (% of entry EV)", 0.02, PCT, "Advisory, legal and financing fees: a standard planning assumption."),
    (18, "Target cash swept to fund the deal at close (% of entry cash)", 1.00, PCT, "Assumes the target's own cash pile "
        "is used to partially fund its own acquisition: standard practice for a cash-rich target, and especially "
        "relevant here given Havells carries INR 2,351 Cr of cash. NOTE: this leaves NO cash buffer post-close, "
        "which shows up as tight or negative free cash flow in the debt schedule's early years; see memo."),
    (20, "OPERATING & TAX (carried over from the 3-statement DCF model)", None, None, None),
    (21, "Effective tax rate", 0.252, PCT, "Same as the companion DCF model, statutory rate under the concessional regime."),
    (23, "EXIT", None, None, None),
    (24, "Hold period (years)", 5, NUM, "FY27E to FY31E, matching the DCF's forecast horizon."),
    (25, "Exit EV/EBITDA multiple", 12.0, MULT, "Base case: no multiple expansion assumed (same as entry). Test "
        "expansion/contraction on the Sensitivity tab."),
]
for r, name, v, fmt, note in rows:
    if v is None:
        label(aw, r, name, bold=True)
        aw.cell(row=r, column=1).fill = GREYFILL
        continue
    is_input = isinstance(v, (int, float))
    label(aw, r, name, indent=1)
    put(aw, f"B{r}", v, BLUE if is_input else BOLD, fmt, fill=YELLOW if is_input else None,
        border=TOPBORDER if not is_input else None)
    if note:
        put(aw, f"D{r}", note, SUB)
        aw[f"D{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        aw.row_dimensions[r].height = 44 if len(note) > 140 else (30 if len(note) > 70 else 16)
        aw.column_dimensions["D"].width = 70

A = "Assumptions"

# ========================================================= SOURCES & USES ==
sw = wb.create_sheet("Sources & Uses")
widths(sw, a=46)
put(sw, "A1", "SOURCES & USES", TITLE)
put(sw, "A2", "The two columns must tie out exactly. INR crore.", SUB)

put(sw, "A4", "ENTRY VALUATION", BOLD, fill=GREYFILL)
put(sw, "A5", "Entry EBITDA (FY26A)", BLACK)
put(sw, "B5", f"={A}!$B$5", GREEN, NUM)
put(sw, "A6", "x Entry EV/EBITDA multiple", BLACK)
put(sw, "B6", f"={A}!$B$6", GREEN, MULT)
put(sw, "A7", "Entry Enterprise Value", BOLD)
put(sw, "B7", "=B5*B6", BOLD, NUM, border=TOPBORDER)
put(sw, "A8", "Add: entry net cash (buyer pays for the cash pile too)", BLACK)
put(sw, "B8", f"={A}!$B$10", GREEN, NUM)
put(sw, "A9", "Equity Purchase Price", BOLD)
put(sw, "B9", "=B7+B8", BOLD, NUM, border=TOPBORDER)

put(sw, "A12", "USES", BOLD, fill=GREYFILL)
put(sw, "A13", "Purchase of equity", BLACK)
put(sw, "B13", "=B9", BLACK, NUM)
put(sw, "A14", "Transaction fees", BLACK)
put(sw, "B14", f"=B7*{A}!$B$17", BLACK, NUM)
put(sw, "A15", "TOTAL USES", BOLD)
put(sw, "B15", "=SUM(B13:B14)", BOLD, NUM, border=TOPDOUBLE)

put(sw, "A18", "SOURCES", BOLD, fill=GREYFILL)
put(sw, "A19", "New senior term loan", BLACK)
put(sw, "B19", f"={A}!$B$13*B5", BLACK, NUM)
put(sw, "A20", "Target's own cash, swept to fund the deal at close", BLACK)
put(sw, "B20", f"={A}!$B$8*{A}!$B$18", BLACK, NUM)
put(sw, "A21", "Sponsor equity (plug)", BOLD)
put(sw, "B21", "=B15-B19-B20", BOLD, NUM, border=TOPBORDER)
put(sw, "A22", "TOTAL SOURCES", BOLD)
put(sw, "B22", "=SUM(B19:B21)", BOLD, NUM, border=TOPDOUBLE)

put(sw, "A24", "CHECK (Sources - Uses, must be zero)", BOLD)
put(sw, "B24", "=B22-B15", BOLD, NUM, border=TOPDOUBLE)

put(sw, "A27", "Implied leverage at close", BOLD)
put(sw, "B27", "=B19/B5", BLACK, MULT)
put(sw, "A28", "Sponsor equity as % of total sources", BOLD)
put(sw, "B28", "=B21/B22", BLACK, PCT)
put(sw, "A30", "NOTE", BOLD)
put(sw, "A31", "This model funds the deal by sweeping 100% of Havells' own FY26A cash pile at close. That leaves zero "
               "cash buffer entering FY27E; a real deal would likely retain some minimum operating cash. Watch the "
               "Debt Schedule tab for tight or negative free cash flow in the early years as a direct consequence "
               "of this assumption; it is a genuine limitation, not a modelling error.", SUB)
sw["A31"].alignment = Alignment(wrap_text=True, vertical="top")
sw.merge_cells("A31:F31")
sw.row_dimensions[31].height = 60

# ============================================================= OPERATING ===
ow = wb.create_sheet("Operating Model")
widths(ow)
put(ow, "A1", "OPERATING MODEL (carried over from the 3-statement DCF model)", TITLE)
put(ow, "A2", "Base case FY27E-FY31E. Source: Havells_3Statement_DCF_Model.xlsx, IS and Schedules tabs.", SUB)
year_header(ow, 4)

op_data = {
    "Net revenue": [25127, 28151, 31310, 34439, 37595],
    "EBITDA": [2511, 2869, 3230, 3520, 3852],
    "Depreciation & amortisation": [503, 591, 689, 758, 865],
    "Capital expenditure": [1256, 1267, 1252, 1309, 1316],
    "Increase in net working capital": [407, 323, 338, 334, 337],
}
r = 6
OP_ROW = {}
for name, vals in op_data.items():
    label(ow, r, name, indent=1)
    for col, v in zip(COLS, vals):
        put(ow, f"{col}{r}", v, BLUE, NUM, fill=YELLOW)
    OP_ROW[name] = r
    r += 1
label(ow, 12, "EBIT = EBITDA - D&A", bold=True)
for col in COLS:
    put(ow, f"{col}12", f"={col}{OP_ROW['EBITDA']}-{col}{OP_ROW['Depreciation & amortisation']}", BOLD, NUM, border=TOPBORDER)
OP_EBIT = 12
label(ow, 13, "EBITDA margin")
for col in COLS:
    put(ow, f"{col}13", f"={col}{OP_ROW['EBITDA']}/{col}{OP_ROW['Net revenue']}", SUB, PCT)

# ========================================================= DEBT SCHEDULE ===
dw = wb.create_sheet("Debt Schedule")
widths(dw)
put(dw, "A1", "DEBT SCHEDULE: SINGLE SENIOR TERM LOAN", TITLE)
put(dw, "A2", "Mandatory amortisation of original principal, plus a 100% cash sweep of any free cash flow left over. "
              "Circularity (interest depends on the average balance, which depends on the sweep, which depends on "
              "free cash flow, which depends on interest) is handled with a circuit breaker, same as the DCF model.", SUB)
put(dw, "A3", "Enable File > Options > Formulas > Iterative Calculation before opening in Excel.", SUB)
year_header(dw, 5)

rows = [
    (7, "EBIT", f"='Operating Model'!{{c}}${OP_EBIT}"),
    (8, "Less: cash tax at operating tax rate", f"=-{{c}}7*{A}!$B$21"),
    (9, "NOPAT", "={c}7+{c}8"),
    (11, "Add: depreciation & amortisation", f"='Operating Model'!{{c}}${OP_ROW['Depreciation & amortisation']}"),
    (12, "Less: capital expenditure", f"=-'Operating Model'!{{c}}${OP_ROW['Capital expenditure']}"),
    (13, "Less: increase in net working capital", f"=-'Operating Model'!{{c}}${OP_ROW['Increase in net working capital']}"),
    (15, "Circuit breaker (0 = normal, 1 = break circularity)", None),
    (17, "Opening term loan balance", None),
    (18, "Interest expense (average balance x rate)", None),
    (19, "Cash available before mandatory amortisation", "={c}9+{c}11+{c}12+{c}13-{c}18"),
    (20, "Less: mandatory amortisation", None),
    (21, "Cash available for optional prepayment (sweep)", None),
    (22, "Optional prepayment (cash sweep)", None),
    (23, "Closing term loan balance", None),
    (25, "Excess cash after full debt paydown (accumulates)", None),
]
for r, name, f in rows:
    bold = r in (9, 19, 23, 25)
    label(dw, r, name, bold=bold)
    if f:
        for col in COLS:
            put(dw, f"{col}{r}", f.replace("{c}", col), BOLD if bold else BLACK, NUM, border=TOPBORDER if bold else None)

put(dw, "B15", 0, BLUE, NUM, fill=YELLOW)
for col in COLS[1:]:
    put(dw, f"{col}15", "=$B$15", BLACK, NUM)

for i, col in enumerate(COLS):
    prev = COLS[i - 1] if i > 0 else None
    if col == "B":
        put(dw, f"{col}17", "='Sources & Uses'!$B$19", GREEN, NUM)
    else:
        put(dw, f"{col}17", f"={prev}23", BLACK, NUM)
    put(dw, f"{col}18", f"=IF({col}$15=1,0,AVERAGE({col}17,{col}17-{col}20)*{A}!$B$14)", BLACK, NUM)
    put(dw, f"{col}20", f"=MIN({col}17,'Sources & Uses'!$B$19*{A}!$B$15)", BLACK, NUM)
    put(dw, f"{col}21", f"=MAX({col}19-{col}20,0)", BLACK, NUM)
    put(dw, f"{col}22", f"=MIN({col}21,{col}17-{col}20)*{A}!$B$16", BLACK, NUM)
    put(dw, f"{col}23", f"={col}17-{col}20-{col}22", BOLD, NUM, border=TOPBORDER)
    put(dw, f"{col}25", f"=MAX({col}19-{col}20-{col}22,0)"
                         + (f"+{prev}25" if prev else ""), BOLD, NUM, border=TOPBORDER)

put(dw, "A27", "NOTE ON EARLY-YEAR CASH FLOW", BOLD)
put(dw, "A28", "Because the target's entire cash pile was swept to fund the deal (Sources & Uses), there is no "
               "buffer entering FY27E. Havells' near-term capex is elevated (capacity additions carried over from "
               "the DCF forecast) relative to FY27E EBITDA, so 'cash available before mandatory amortisation' may "
               "be tight or negative in the first year or two. This model does not include a revolving credit "
               "facility to plug a shortfall: a genuine simplification, and a natural next extension.", SUB)
dw["A28"].alignment = Alignment(wrap_text=True, vertical="top")
dw.merge_cells("A28:F28")
dw.row_dimensions[28].height = 75

# ============================================================== RETURNS ====
rw = wb.create_sheet("Returns Analysis")
widths(rw, a=48)
put(rw, "A1", "RETURNS ANALYSIS", TITLE)
put(rw, "A2", "Clean end-of-period exit: no interim distributions assumed. INR crore.", SUB)

put(rw, "A4", "ENTRY", BOLD, fill=GREYFILL)
put(rw, "A5", "Sponsor equity invested", BLACK)
put(rw, "B5", "='Sources & Uses'!$B$21", GREEN, NUM)

put(rw, "A7", "EXIT (end of FY31E, after 5-year hold)", BOLD, fill=GREYFILL)
put(rw, "A8", "Exit-year EBITDA (FY31E)", BLACK)
put(rw, "B8", "='Operating Model'!$F$7", GREEN, NUM)
put(rw, "A9", "x Exit EV/EBITDA multiple", BLACK)
put(rw, "B9", f"={A}!$B$25", GREEN, MULT)
put(rw, "A10", "Exit Enterprise Value", BOLD)
put(rw, "B10", "=B8*B9", BOLD, NUM, border=TOPBORDER)
put(rw, "A11", "Less: closing term loan balance", BLACK)
put(rw, "B11", "=-'Debt Schedule'!$F$23", BLACK, NUM)
put(rw, "A12", "Add: accumulated excess cash", BLACK)
put(rw, "B12", "='Debt Schedule'!$F$25", GREEN, NUM)
put(rw, "A13", "Exit Equity Value", BOLD)
put(rw, "B13", "=B10+B11+B12", BOLD, NUM, border=TOPDOUBLE)

put(rw, "A16", "RETURNS", BOLD, fill=GREYFILL)
put(rw, "A17", "MOIC (exit equity / entry equity)", BOLD)
put(rw, "B17", "=B13/B5", BOLD, MULT, border=TOPBORDER)
put(rw, "A18", "Hold period (years)", BLACK)
put(rw, "B18", f"={A}!$B$24", GREEN, NUM)
put(rw, "A19", "IRR = MOIC^(1/years) - 1", BOLD)
put(rw, "B19", "=B17^(1/B18)-1", BOLD, PCT, border=TOPBORDER)

put(rw, "A22", "RETURNS BRIDGE (decomposing the IRR)", BOLD, fill=GREYFILL)
put(rw, "A23", "Entry equity value", BLACK)
put(rw, "B23", "=B5", BLACK, NUM)
put(rw, "A24", "+ EBITDA growth (at entry multiple)", BLACK)
put(rw, "B24", f"=(B8-'Operating Model'!$B$7)*{A}!$B$6", BLACK, NUM)
put(rw, "A25", "+ Multiple change (exit EBITDA x change in multiple)", BLACK)
put(rw, "B25", f"=B8*(B9-{A}!$B$6)", BLACK, NUM)
put(rw, "A26", "+ Deleveraging & cash generation", BLACK)
put(rw, "B26", "=B13-B23-B24-B25", BLACK, NUM)
put(rw, "A27", "Exit equity value (check, should equal B13)", BOLD)
put(rw, "B27", "=SUM(B23:B26)", BOLD, NUM, border=TOPBORDER)
put(rw, "A28", "Check (B27 - B13, must be zero)", BOLD)
put(rw, "B28", "=B27-B13", BOLD, NUM, border=TOPDOUBLE)

# ============================================================ SENSITIVITY ==
vw = wb.create_sheet("Sensitivity")
widths(vw, a=30, rest=12)
put(vw, "A1", "SENSITIVITY: ENTRY MULTIPLE x EXIT MULTIPLE", TITLE)
put(vw, "A2", "IRR at each combination. Note how quickly returns collapse as the entry multiple rises toward "
              "Havells' actual public trading multiple (~33x): this is the mechanical reason a real-world "
              "buyout at the traded price would not clear an acceptable return.", SUB)
vw["A2"].alignment = Alignment(wrap_text=True)
vw.merge_cells("A2:H2")
vw.row_dimensions[2].height = 30

entry_grid = [8, 10, 12, 15, 20, 25, 33]
exit_grid = [8, 10, 12, 15, 20]

put(vw, "B5", "Exit multiple \u2192 / Entry multiple \u2193", BOLD, fill=GREYFILL, align="center")
for j, ex in enumerate(exit_grid):
    col = chr(ord("C") + j)
    put(vw, f"{col}5", f"{ex}.0x", BOLD, align="center", fill=GREYFILL)
for i, en in enumerate(entry_grid):
    r = 6 + i
    put(vw, f"B{r}", f"{en}.0x", BOLD, fill=GREYFILL)
    for j, ex in enumerate(exit_grid):
        col = chr(ord("C") + j)
        entry_ev = f"('Sources & Uses'!$B$5*{en})"
        entry_equity = f"({entry_ev}+{A}!$B$10-'Sources & Uses'!$B$14-('Assumptions'!$B$13*'Sources & Uses'!$B$5)-('Assumptions'!$B$8*'Assumptions'!$B$18))"
        # Simplified: re-derive sponsor equity at this entry multiple directly
        fees = f"({entry_ev}*{A}!$B$17)"
        equity_price = f"({entry_ev}+{A}!$B$10)"
        total_uses = f"({equity_price}+{fees})"
        term_loan = f"({A}!$B$13*'Sources & Uses'!$B$5)"
        swept_cash = f"({A}!$B$8*{A}!$B$18)"
        sponsor_equity = f"({total_uses}-{term_loan}-{swept_cash})"
        exit_ev = f"('Operating Model'!$F$7*{ex})"
        exit_equity = f"({exit_ev}-'Debt Schedule'!$F$23+'Debt Schedule'!$F$25)"
        moic = f"({exit_equity}/{sponsor_equity})"
        irr = f"({moic}^(1/{A}!$B$24)-1)"
        put(vw, f"{col}{r}", f"=IFERROR({irr},NA())", BLACK, PCT, align="center")

put(vw, "A15", "Reading the grid", BOLD)
put(vw, "A16", "The diagonal (entry = exit, no multiple expansion or contraction) isolates the return from EBITDA "
               "growth and deleveraging alone. Columns to the right of the diagonal show upside from multiple "
               "expansion; columns to the left show what happens if you have to sell at a discount to what you paid.", SUB)
vw["A16"].alignment = Alignment(wrap_text=True)
vw.merge_cells("A16:H16")
vw.row_dimensions[16].height = 40

# --------------------------------------------------------------- save ------
out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "Havells_LBO_Model.xlsx"))
os.makedirs(os.path.dirname(out), exist_ok=True)
wb.save(out)
print("Written:", out)
