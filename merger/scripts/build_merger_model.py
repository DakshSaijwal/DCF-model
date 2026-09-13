"""
build_merger_model.py
----------------------
Hypothetical merger model: Havells India acquires IFB Industries Limited.

Unlike the LBO model in this repo, this is a PLAUSIBLE real-world deal shape.
Havells is debt-free and cash-rich; its Lloyd segment (air conditioners,
refrigerators, washing machines) has been losing share and posted a segment
loss in FY26. IFB Industries is a real, smaller (~INR 5,600 Cr revenue) listed
home-appliance manufacturer (washing machines, microwaves, dishwashers) that
would meaningfully broaden Havells' white-goods scale. The illustrative deal
terms below are NOT based on any actual announced transaction, advisory
mandate, or non-public information -- they are built entirely from each
company's own public FY26 results, to demonstrate merger-model mechanics.

Run:  python scripts/build_merger_model.py
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
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

TOPBORDER = Border(top=Side(style="thin"))
TOPDOUBLE = Border(top=Side(style="thin"), bottom=Side(style="double"))

NUM = '#,##0;(#,##0);"-"'
PCT = '0.0%'
MULT = '0.00x'
RS = '#,##0.00'


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


def widths(ws, a=52, rest=15):
    ws.column_dimensions["A"].width = a
    for col in ["B", "C", "D", "E", "F"]:
        ws.column_dimensions[col].width = rest


wb = Workbook()

# =============================================================== COVER =====
ws = wb.active
ws.title = "Cover"
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = 84

put(ws, "A1", "HAVELLS INDIA LIMITED", TITLE)
put(ws, "A2", "Hypothetical Acquisition of IFB Industries Limited: Merger Model & Accretion/Dilution Analysis", SUB)

put(ws, "A4", "WHY THIS DEAL, AND WHY IT IS DIFFERENT FROM THE LBO MODEL", TITLE)
note = ("The LBO model elsewhere in this repository models Havells as a hypothetical ACQUISITION TARGET, "
        "and states plainly that this is unrealistic given the company's promoter control and scale. This "
        "model does the opposite: it models Havells as the ACQUIRER of a real, smaller, publicly listed "
        "company. This is a plausible real-world deal shape. Havells is debt-free with a large cash pile, "
        "and its Lloyd segment (air conditioners, refrigerators, washing machines) posted a segment loss "
        "in FY26 on falling revenue. IFB Industries is a real home-appliance manufacturer (washing "
        "machines, microwaves, dishwashers) roughly a fourteenth of Havells' size by market value -- a "
        "genuine bolt-on scale. The deal TERMS used here (premium, financing mix, synergies) are entirely "
        "illustrative and are not based on any actual announced transaction, advisory mandate, or "
        "non-public information about either company.")
put(ws, "A5", note, BLACK)
ws["A5"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A5:B5")
ws.row_dimensions[5].height = 105

rows = [
    ("Acquirer", "Havells India Limited (NSE: HAVELLS) -- standalone FY26A financials, consistent with the companion DCF and LBO models in this repo."),
    ("Target", "IFB Industries Limited (NSE: IFBIND) -- consolidated FY26A financials (home appliances + engineering segments)."),
    ("Deal structure", "Illustrative acquisition of 100% of IFB's outstanding equity at a control premium to its current market price."),
    ("Consideration", "Base case: 100% cash, funded by a mix of Havells' own balance sheet cash and newly raised acquisition debt -- the company's first-ever borrowing beyond lease liabilities."),
    ("Analysis horizon", "Year 1 pro forma (illustrative, as if the combination had been in place for the full FY26 year)."),
    ("Units", "INR crore unless stated otherwise"),
    ("Colour convention", "BLUE = hardcoded input (mostly reported figures)   |   BLACK = formula on this sheet   |   GREEN = link from another sheet   |   YELLOW FILL = assumption requiring justification"),
    ("Disclaimer", "Educational exercise. Not investment research, not a deal recommendation, not investment advice, and not based on any actual or rumoured transaction."),
]
r = 13
for k, v in rows:
    put(ws, f"A{r}", k, BOLD)
    put(ws, f"B{r}", v, BLACK)
    ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 44 if len(v) > 90 else 16
    r += 2

# =========================================================== ASSUMPTIONS ===
aw = wb.create_sheet("Assumptions")
widths(aw, a=54)
put(aw, "A1", "STANDALONE FINANCIALS AND DEAL ASSUMPTIONS", TITLE)
put(aw, "A2", "Every yellow cell is an input you own and must justify. Blue cells are reported figures.", SUB)

rows = [
    (4, "HAVELLS (ACQUIRER) -- FY26A STANDALONE, CLEAN", None, None, None),
    (5, "Clean operating EBIT (ex fair-value gain, ex exceptional item)", 1784, NUM,
        "EBITDA 2,213 less D&A 429, consistent with the companion DCF model's treatment of the Goldi Solar fair-value gain."),
    (6, "Other income, net", 204, NUM, "Reported FY26A other income."),
    (7, "Existing finance cost (lease interest)", 37, NUM, "Reported FY26A finance cost; Havells carries no borrowings today."),
    (8, "Effective tax rate", 0.252, PCT, "Statutory rate under the concessional regime, same as the companion models."),
    (9, "Diluted shares outstanding (crore)", 62.70, NUM, "Same as the companion DCF and LBO models."),
    (10, "Current share price (INR)", 1190.00, RS, "Same valuation date as the companion models."),
    (12, "IFB INDUSTRIES (TARGET) -- FY26A CONSOLIDATED, AS REPORTED", None, None, None),
    (13, "Reported profit before tax", 192.45, NUM, "FY26A consolidated PBT, as reported."),
    (14, "Reported net profit", 143.56, NUM, "FY26A consolidated net profit, as reported."),
    (15, "Effective tax rate (reported)", "=1-B14/B13", PCT, None),
    (16, "Estimated net finance cost (verify against annual report)", 20, NUM,
        "Not separately disclosed in the results summary used to build this model. Placeholder: confirm against "
        "IFB's FY26 annual report finance-cost note before presenting this model."),
    (17, "Adjusted EBIT (PBT + estimated finance cost)", "=B13+B16", NUM, None),
    (18, "Diluted shares outstanding (crore)", 4.05, NUM, "Derived as reported net profit / reported EPS (Rs 35.43)."),
    (19, "Current share price (INR)", 1300.00, RS, "Implied from FY26A market capitalisation (~INR 5,268 Cr) / diluted shares."),
    (21, "DEAL TERMS", None, None, None),
    (22, "Control premium over IFB's current share price", 0.25, PCT, "Illustrative; typical control premiums in Indian strategic M&A run 20-40%."),
    (23, "Offer price per IFB share (INR)", "=B19*(1+B22)", RS, None),
    (24, "Cash consideration (% of deal)", 1.00, PCT, "Base case: all-cash. Vary this on the Sensitivity tab to test a stock-funded alternative."),
    (25, "Cash drawn from Havells' existing balance sheet", 1500, NUM,
        "Deliberately less than Havells' full FY26A cash balance (INR 2,351 Cr) -- unlike the LBO model, this deal retains a cash buffer."),
    (26, "New acquisition debt: interest rate (all-in)", 0.095, PCT,
        "Priced better than the LBO model's 10.5% -- an investment-grade strategic acquirer borrowing on its own strong balance sheet commands a better rate than a leveraged sponsor deal."),
    (27, "Foregone interest rate on cash used to fund the deal", 0.065, PCT, "Illustrative short-term liquid-fund / FD yield opportunity cost."),
    (28, "Transaction fees (% of equity purchase price)", 0.015, PCT, "Advisory, legal and financing fees."),
    (30, "PURCHASE PRICE ALLOCATION (SIMPLIFIED)", None, None, None),
    (31, "% of equity purchase price allocated to amortisable intangibles", 0.15, PCT,
        "Simplification: the remainder is allocated to non-amortising goodwill. A full PPA would also step up "
        "inventory and fixed assets; this model does not."),
    (32, "Intangible amortisation period (years)", 10, NUM, "Illustrative useful life for acquired brand/customer relationships."),
    (33, "Incremental D&A tax-deductible?", "No", None,
        "Assumption: this is a share purchase, so the acquirer does not receive a stepped-up tax basis in India -- "
        "the incremental book D&A from the step-up is therefore NOT tax-deductible. This is a real technical "
        "nuance between share deals and asset deals worth knowing for an M&A interview."),
    (35, "SYNERGIES", None, None, None),
    (36, "Run-rate annual pre-tax cost synergies", 100, NUM,
        "Illustrative: combined distribution network and manufacturing/procurement scale across the two "
        "companies' white-goods lines. Not based on any actual synergy study."),
    (37, "Year 1 realisation (% of run-rate)", 0.50, PCT, "Standard first-year phase-in assumption; full run-rate typically takes 18-24 months."),
]
for r, name, v, fmt, note in rows:
    if v is None:
        label(aw, r, name, bold=True)
        aw.cell(row=r, column=1).fill = GREYFILL
        continue
    is_formula = isinstance(v, str) and v.startswith("=")
    is_input = isinstance(v, (int, float)) or (isinstance(v, str) and not is_formula)
    label(aw, r, name, indent=1)
    put(aw, f"B{r}", v, BLUE if (is_input and not is_formula) else BOLD, fmt,
        fill=YELLOW if (is_input and not is_formula) else None,
        border=TOPBORDER if is_formula else None)
    if note:
        put(aw, f"D{r}", note, SUB)
        aw[f"D{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        aw.row_dimensions[r].height = 44 if len(note) > 140 else (30 if len(note) > 70 else 16)
        aw.column_dimensions["D"].width = 68

A = "Assumptions"

# ========================================================= SOURCES & USES ==
sw = wb.create_sheet("Sources & Uses")
widths(sw, a=48)
put(sw, "A1", "SOURCES & USES", TITLE)
put(sw, "A2", "The two columns must tie out exactly. INR crore.", SUB)

put(sw, "A4", "USES", BOLD, fill=GREYFILL)
put(sw, "A5", "IFB diluted shares (crore)", BLACK)
put(sw, "B5", f"={A}!$B$18", GREEN, NUM)
put(sw, "A6", "x Offer price per share (INR)", BLACK)
put(sw, "B6", f"={A}!$B$23", GREEN, RS)
put(sw, "A7", "Equity purchase price", BOLD)
put(sw, "B7", "=B5*B6", BOLD, NUM, border=TOPBORDER)
put(sw, "A8", "Transaction fees", BLACK)
put(sw, "B8", f"=B7*{A}!$B$28", BLACK, NUM)
put(sw, "A9", "TOTAL USES", BOLD)
put(sw, "B9", "=B7+B8", BOLD, NUM, border=TOPDOUBLE)

put(sw, "A12", "SOURCES", BOLD, fill=GREYFILL)
put(sw, "A13", "Cash consideration (% of deal)", BLACK)
put(sw, "B13", f"={A}!$B$24", GREEN, PCT)
put(sw, "A14", "Total cash portion of the deal", BLACK)
put(sw, "B14", "=B9*B13", BLACK, NUM)
put(sw, "A15", "  of which: from Havells' existing balance sheet", BLACK)
put(sw, "B15", f"=MIN({A}!$B$25,B14)", BLACK, NUM)
put(sw, "A16", "  of which: new acquisition term loan (plug)", BOLD)
put(sw, "B16", "=B14-B15", BOLD, NUM, border=TOPBORDER)
put(sw, "A17", "Stock portion of the deal (new Havells shares issued)", BLACK)
put(sw, "B17", "=B9*(1-B13)", BLACK, NUM)
put(sw, "A18", "  new Havells shares issued (crore)", BLACK)
put(sw, "B18", f"=B17/{A}!$B$10", BLACK, NUM)
put(sw, "A19", "TOTAL SOURCES", BOLD)
put(sw, "B19", "=B15+B16+B17", BOLD, NUM, border=TOPDOUBLE)

put(sw, "A21", "CHECK (Sources - Uses, must be zero)", BOLD)
put(sw, "B21", "=B19-B9", BOLD, NUM, border=TOPDOUBLE)

put(sw, "A24", "Implied acquisition leverage (new debt / Havells FY26A EBITDA of 2,213)", BOLD)
put(sw, "B24", "=B16/2213", BLACK, MULT)
put(sw, "A25", "Implied premium check: offer price vs. current IFB price", BOLD)
put(sw, "B25", f"=B6/{A}!$B$19-1", BLACK, PCT)

# ================================================= PURCHASE PRICE ALLOCATION
pw = wb.create_sheet("Purchase Price Allocation")
widths(pw, a=50)
put(pw, "A1", "PURCHASE PRICE ALLOCATION (SIMPLIFIED)", TITLE)
put(pw, "A2", "A full PPA also steps up inventory and fixed assets and recognises deferred tax on the step-up; "
              "this model simplifies to a single amortisable intangible plus goodwill, which is enough to "
              "demonstrate the accretion/dilution mechanics without over-building a first merger model.", SUB)

put(pw, "A4", "Equity purchase price", BLACK)
put(pw, "B4", "='Sources & Uses'!$B$7", GREEN, NUM)
put(pw, "A5", "x % allocated to amortisable intangibles", BLACK)
put(pw, "B5", f"={A}!$B$31", GREEN, PCT)
put(pw, "A6", "Amortisable intangible asset", BOLD)
put(pw, "B6", "=B4*B5", BOLD, NUM, border=TOPBORDER)
put(pw, "A7", "Goodwill (residual, non-amortising)", BOLD)
put(pw, "B7", "=B4-B6", BOLD, NUM, border=TOPBORDER)
put(pw, "A9", "Amortisation period (years)", BLACK)
put(pw, "B9", f"={A}!$B$32", GREEN, NUM)
put(pw, "A10", "Incremental annual D&A from the step-up", BOLD)
put(pw, "B10", "=B6/B9", BOLD, NUM, border=TOPBORDER)
put(pw, "A11", "Tax-deductible?", BLACK)
put(pw, "B11", f"={A}!$B$33", GREEN)
put(pw, "A12", "NOTE", BOLD)
put(pw, "A13", "This is a share purchase, so Havells does not receive a stepped-up tax basis in the target's "
               "assets under Indian tax law. The incremental book D&A above reduces reported (book) profit but "
               "creates no cash tax benefit -- this model applies tax at the standard rate to book pre-tax "
               "profit throughout, which is the standard simplification in a first accretion/dilution model; a "
               "more complete model would track book-tax differences and deferred tax separately.", SUB)
pw["A13"].alignment = Alignment(wrap_text=True, vertical="top")
pw.merge_cells("A13:D13")
pw.row_dimensions[13].height = 75

# ===================================================== PRO FORMA INCOME ====
iw = wb.create_sheet("Pro Forma Income Statement")
widths(iw, a=52)
put(iw, "A1", "PRO FORMA INCOME STATEMENT -- YEAR 1 (ILLUSTRATIVE)", TITLE)
put(iw, "A2", "As if the two companies had been combined for the full FY26 year. INR crore.", SUB)

rows = [
    (4, "Havells clean operating EBIT", f"={A}!$B$5"),
    (5, "IFB adjusted EBIT", f"={A}!$B$17"),
    (6, "Combined operating EBIT", "=B4+B5"),
    (8, "Add: Havells other income", f"={A}!$B$6"),
    (9, "Less: Havells existing finance cost (lease interest)", f"=-{A}!$B$7"),
    (10, "Less: IFB existing finance cost (assumed retained)", f"=-{A}!$B$16"),
    (12, "Add: run-rate synergies realised in Year 1", "='Sensitivity'!$B$4"),
    (13, "Less: incremental D&A from intangible step-up", "=-'Purchase Price Allocation'!$B$10"),
    (14, "Less: interest on new acquisition debt", "=-'Sources & Uses'!$B$16*Assumptions!$B$26"),
    (15, "Less: foregone interest income on cash used to fund the deal", "=-'Sources & Uses'!$B$15*Assumptions!$B$27"),
    (17, "PRO FORMA PROFIT BEFORE TAX", "=SUM(B6,B8:B10,B12:B15)"),
    (18, "Less: tax at group effective rate", f"=-B17*{A}!$B$8"),
    (19, "PRO FORMA NET INCOME", "=B17+B18"),
    (21, "Pro forma diluted shares (Havells existing + new shares issued)", f"={A}!$B$9+'Sources & Uses'!$B$18"),
    (22, "PRO FORMA EPS (INR)", "=B19/B21"),
]
for r, name, f in rows:
    bold = r in (6, 17, 19, 22)
    label(iw, r, name, bold=bold)
    put(iw, f"B{r}", f, BOLD if bold else BLACK, NUM if r != 22 else RS,
        border=TOPBORDER if bold else None)

# ======================================================= ACCRETION/DILUTION
dw = wb.create_sheet("Accretion-Dilution")
widths(dw, a=52)
put(dw, "A1", "ACCRETION / DILUTION SUMMARY", TITLE)
put(dw, "A2", "Year 1, illustrative. This is the single number an M&A banker is asked for first.", SUB)

put(dw, "A4", "Havells standalone EPS (INR)", BOLD)
put(dw, "B4", f"=({A}!$B$5+{A}!$B$6-{A}!$B$7)*(1-{A}!$B$8)/{A}!$B$9", BOLD, RS, border=TOPBORDER)
put(dw, "A5", "Pro forma combined EPS (INR)", BOLD)
put(dw, "B5", "='Pro Forma Income Statement'!$B$22", BOLD, RS, border=TOPBORDER)
put(dw, "A6", "Accretion / (Dilution)", BOLD)
put(dw, "B6", "=B5/B4-1", BOLD, PCT, border=TOPDOUBLE)

put(dw, "A9", "READING THIS RESULT", BOLD)
put(dw, "A10", "A negative number means the deal is DILUTIVE: combined Year 1 EPS is lower than Havells would "
               "have earned standing alone, even though no value is destroyed strategically. That happens "
               "whenever the after-tax cost of the consideration and financing exceeds the after-tax earnings "
               "the target contributes -- which is common for a rich-multiple acquisition (IFB trades near "
               "36x trailing earnings) funded partly with debt priced above the target's own earnings yield. "
               "A dilutive deal is not automatically a bad deal: strategic rationale (here, fixing Lloyd's "
               "competitive scale in white goods) can justify near-term dilution if the acquirer believes "
               "synergies or growth will close the gap over time. See the Sensitivity tab for what it would "
               "take to break even.", SUB)
dw["A10"].alignment = Alignment(wrap_text=True, vertical="top")
dw.merge_cells("A10:E10")
dw.row_dimensions[10].height = 105

# ============================================================ SENSITIVITY ==
vw = wb.create_sheet("Sensitivity")
widths(vw, a=40, rest=13)
put(vw, "A1", "SENSITIVITY & BREAKEVEN SYNERGIES", TITLE)
put(vw, "A2", "Row B4 drives the Year 1 synergy figure used on the Pro Forma Income Statement tab -- "
              "change it directly, or read it off the grid below.", SUB)

put(vw, "A4", "Year 1 realised synergies (feeds Pro Forma tab)", BOLD)
put(vw, "B4", f"={A}!$B$36*{A}!$B$37", BOLD, NUM, border=TOPBORDER)

put(vw, "A7", "GRID: CASH % OF DEAL (columns) x SYNERGY REALISATION (rows) -- Year 1 accretion/(dilution)", BOLD)
cash_grid = [0.0, 0.25, 0.50, 0.75, 1.00]
syn_grid = [0.0, 0.25, 0.50, 0.75, 1.00]

put(vw, "B9", "Synergy % \\ Cash %", BOLD, fill=GREYFILL, align="center")
for j, c in enumerate(cash_grid):
    col = get_column_letter(3 + j)
    put(vw, f"{col}9", f"{c:.0%}", BOLD, align="center", fill=GREYFILL)

for i, s in enumerate(syn_grid):
    r = 10 + i
    put(vw, f"B{r}", f"{s:.0%}", BOLD, fill=GREYFILL)
    for j, c in enumerate(cash_grid):
        col = get_column_letter(3 + j)
        cash_amt = f"('Sources & Uses'!$B$9*{c})"
        cash_from_bs = f"MIN({A}!$B$25,{cash_amt})"
        new_debt = f"({cash_amt}-{cash_from_bs})"
        stock_amt = f"('Sources & Uses'!$B$9*(1-{c}))"
        new_shares = f"({stock_amt}/{A}!$B$10)"
        synergies = f"({A}!$B$36*{s})"
        pbt = (f"({A}!$B$5+{A}!$B$17+{A}!$B$6-{A}!$B$7-{A}!$B$16"
               f"+{synergies}-'Purchase Price Allocation'!$B$10"
               f"-{new_debt}*{A}!$B$26-{cash_from_bs}*{A}!$B$27)")
        ni = f"({pbt}*(1-{A}!$B$8))"
        shares = f"({A}!$B$9+{new_shares})"
        eps = f"({ni}/{shares})"
        base_eps = "'Accretion-Dilution'!$B$4"
        put(vw, f"{col}{r}", f"=IFERROR({eps}/{base_eps}-1,NA())", BLACK, PCT, align="center")

put(vw, "A17", "BREAKEVEN SYNERGIES (closed-form)", BOLD)
put(vw, "A18", "Run-rate pre-tax synergies needed to make the base-case deal (100% cash, as structured on "
               "Sources & Uses) exactly EPS-neutral in Year 1:", SUB)
vw["A18"].alignment = Alignment(wrap_text=True)
vw.merge_cells("A18:F18")
vw.row_dimensions[18].height = 30

put(vw, "A20", "Required pro forma PBT for EPS neutrality", BLACK)
put(vw, "B20", f"='Accretion-Dilution'!$B$4*{A}!$B$9/(1-{A}!$B$8)", BLACK, NUM)
put(vw, "A21", "Pro forma PBT at zero Year 1 synergies", BLACK)
put(vw, "B21", (f"={A}!$B$5+{A}!$B$17+{A}!$B$6-{A}!$B$7-{A}!$B$16"
                f"-'Purchase Price Allocation'!$B$10"
                f"-'Sources & Uses'!$B$16*{A}!$B$26-'Sources & Uses'!$B$15*{A}!$B$27"), BLACK, NUM)
put(vw, "A22", "Gap to close (= required Year 1 synergy contribution)", BOLD)
put(vw, "B22", "=B20-B21", BOLD, NUM, border=TOPBORDER)
put(vw, "A23", "Implied required RUN-RATE synergies (Year 1 gap / realisation %)", BOLD)
put(vw, "B23", f"=B22/{A}!$B$37", BOLD, NUM, border=TOPDOUBLE)
put(vw, "A24", "vs. the illustrative run-rate synergy assumption actually used", BLACK)
put(vw, "B24", f"={A}!$B$36", GREEN, NUM)

# --------------------------------------------------------------- save ------
out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "Havells_Merger_Model.xlsx"))
os.makedirs(os.path.dirname(out), exist_ok=True)
wb.save(out)
print("Written:", out)
