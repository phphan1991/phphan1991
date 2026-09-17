# -*- coding: utf-8 -*-
"""Generates the corrected cost-management roadmap sheets.
Every printed number is computed here so the graphics and the copy cannot drift apart."""
import math, os, json

W, H = 1632, 1056
INK   = "#111417"
PAPER = "#ffffff"
BLUE  = "#0B4F9E"
BLUE2 = "#4E86BF"
BLUE3 = "#9FC2DF"
BLUE4 = "#DCE8F4"
RULE  = "#C3CCD4"
MUTED = "#49545E"

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ---------------------------------------------------------------- computed numbers
# Phase 1 - influence vs expenditure (straight segments between stated points, no smoothing)
INF = [(0,100),(15,95),(40,70),(92,15),(100,0)]
EXP = [(0,0),(15,2),(40,12),(92,97),(100,100)]
# crossing between x=40 and x=92
u = (70-12)/((97-12)+(70-15))
CROSS_X = 40 + u*52
CROSS_Y = 70 - u*55
# Phase 1 - cost of a late change
CHG_BASE = 5000
CHG_K10 = [CHG_BASE*10**n for n in range(4)]
CHG_K3  = [CHG_BASE*3**n for n in range(4)]
# Phase 2 - installed cost
P2_PRICE, P2_FRT, P2_INST, P2_COMM, P2_TAXR = 250000, 8000, 35000, 6000, 0.085
P2_TAX = P2_PRICE*P2_TAXR
P2_TOTAL = P2_PRICE+P2_FRT+P2_TAX+P2_INST+P2_COMM
P2_MULT = P2_TOTAL/P2_PRICE
# Phase 2 - book cost / defender-challenger
FIRST, SALV, LIFE = 500000, 50000, 10
DEP = (FIRST-SALV)/LIFE
BV4 = FIRST - 4*DEP
MKT = 120000
def ap(i, n): return i*(1+i)**n/((1+i)**n - 1)
I = 0.08
CH_EUAC = 450000*ap(I,10) + 30000
DF_EUAC = MKT*ap(I,5) + 70000
DF_WRONG = BV4*ap(I,5) + 70000
# Phase 3 - one baseline, four states, one forecast (US$M at a single cut-off)
BASELINE, APPROVED_CHG = 92.0, 8.0
BUDGET = BASELINE + APPROVED_CHG
COMMITTED, INCURRED, INVOICED, PAID = 84.0, 71.0, 66.0, 60.0
ETC = 32.5
EAC = INCURRED + ETC
VAC = BUDGET - EAC
UNCOMMITTED, CHANGES, RISK = 12.0, 4.5, 3.0
COMMIT_BUILD = COMMITTED + UNCOMMITTED + CHANGES + RISK
OPEN_EAC = 101.2
MOVES = [("Scope change", 1.6), ("Quantity and productivity", 0.9), ("Rate and escalation", 0.5),
         ("Schedule and prolongation", 0.7), ("Risk and contingency", -1.2), ("Re-estimate", -0.2)]
CLOSE_EAC = round(OPEN_EAC + sum(m[1] for m in MOVES), 1)
# Phase 4 - indirect allocation
POOL, DRIVER_H = 480000, 24000
RATE = POOL/DRIVER_H
LAB_H, LAB_DIRECT, OHP = 1850, 420000, 0.12
LAB_ALLOC = RATE*LAB_H
LAB_SUB = LAB_DIRECT + LAB_ALLOC
LAB_MARKUP = LAB_SUB*OHP
LAB_TOTAL = LAB_SUB + LAB_MARKUP
CRANE_WK, SUPV_WK = 3500, 4200
TIMEREL_WK = CRANE_WK + SUPV_WK
DELAY_WKS = 4
DELAY_COST = TIMEREL_WK*DELAY_WKS
# Phase 5 - benchmarks (illustrative)
OFFICE = [("Shell and core", 190), ("Office-grade MEP", 95), ("Office fit-out", 65)]
LAB = [("Shell and core", 190), ("Lab shell premium", 55), ("Lab HVAC and exhaust", 210),
       ("Power and electrical", 130), ("Process and IT racks", 85), ("Casework, fixed equipment", 110)]
OFFICE_T = sum(v for _, v in OFFICE)
LAB_T = sum(v for _, v in LAB)
DELTA = LAB_T - OFFICE_T
RATIO = LAB_T/OFFICE_T
# Phase 5 - capacity factored estimating
CAP_A, CAP_B, NEXP = 90, 138, 0.6
CAP_RATIO = CAP_B/CAP_A
COST_FACTOR = CAP_RATIO**NEXP
UNIT_FACTOR = COST_FACTOR/CAP_RATIO
# Phase 5 - staged vs ultimate (illustrative)
ULT = 100.0
STAGE1 = ULT*(0.5**NEXP)
P2_BASE, ESC_R, REMOB, YRS = 50.0, 0.02, 0.15, 10
STAGE2_FV = P2_BASE*(1+ESC_R)**YRS*(1+REMOB)
def staged_npv(r): return STAGE1 + STAGE2_FV/((1+r)**YRS)
CROSSOVER = ((STAGE2_FV/(ULT-STAGE1))**(1/YRS)) - 1

def f1(x): return ("%.1f" % x)
def money(x): return "{:,}".format(int(round(x)))

# ---------------------------------------------------------------- svg helpers
def txt(x, y, s, size=12, fill=INK, weight=500, anchor="start", mono=False, ls="0"):
    fam = "'IBM Plex Mono',monospace" if mono else "'IBM Plex Sans',sans-serif"
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" font-weight="%s" '
            'fill="%s" text-anchor="%s" letter-spacing="%s">%s</text>'
            % (x, y, fam, size, weight, fill, anchor, ls, esc(s)))

def line(x1, y1, x2, y2, stroke=RULE, w=1, dash=None, cap="butt"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="%s"/>'
            % (x1, y1, x2, y2, stroke, w, d, cap))

def rect(x, y, w_, h_, fill="none", stroke="none", sw=1, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x, y, max(w_, 0), max(h_, 0), fill, stroke, sw, d))

def poly(pts, stroke=BLUE, w=2, fill="none", dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    p = " ".join("%.1f,%.1f" % (a, b) for a, b in pts)
    return '<polyline points="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (p, fill, stroke, w, d)

def txtbg(x, y, s, size=12, fill=INK, weight=700, anchor="start", pad=3):
    w = len(s)*6.3 + pad*2
    x0 = x-pad if anchor == "start" else (x-w+pad if anchor == "end" else x-w/2)
    return (rect(x0, y-size+1.5, w, size+2, PAPER, "none")
            + txt(x, y, s, size, fill, weight, anchor))

def svg(w_, h_, body):
    return ('<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img" style="display:block">%s</svg>'
            % (w_, h_, w_, h_, body))

def arrow_defs():
    return ('<defs>'
            '<marker id="ab" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
            '<path d="M0,0 L8,4 L0,8 z" fill="%s"/></marker>'
            '<marker id="ak" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
            '<path d="M0,0 L8,4 L0,8 z" fill="%s"/></marker>'
            '</defs>' % (BLUE, INK))

# ================================================================ diagrams (drawn at 480px wide)
VW = 480

def dia_pdca():
    bw, bh, gx, gy = 90, 20, 26, 24
    s = [arrow_defs()]
    def loop(x0, y0, tag, caption):
        o = []
        pos = {"PLAN": (x0, y0), "DO": (x0+bw+gx, y0),
               "CHECK": (x0+bw+gx, y0+bh+gy), "ACT": (x0, y0+bh+gy)}
        for k, (x, y) in pos.items():
            o.append(rect(x, y, bw, bh, PAPER, INK, 1.2))
            o.append(txt(x+bw/2, y+bh-6, k, 12, INK, 600, "middle"))
        mx, my = x0+bw+gx/2, y0+bh+gy/2
        o.append(line(x0+bw+3, y0+bh/2, x0+bw+gx-5, y0+bh/2, BLUE, 1.5).replace("/>", ' marker-end="url(#ab)"/>'))
        o.append(line(x0+bw+gx+bw/2, y0+bh+3, x0+bw+gx+bw/2, y0+bh+gy-5, BLUE, 1.5).replace("/>", ' marker-end="url(#ab)"/>'))
        o.append(line(x0+bw+gx-3, y0+bh+gy+bh/2, x0+bw+5, y0+bh+gy+bh/2, BLUE, 1.5).replace("/>", ' marker-end="url(#ab)"/>'))
        o.append(line(x0+bw/2, y0+bh+gy-3, x0+bw/2, y0+bh+5, BLUE, 1.5).replace("/>", ' marker-end="url(#ab)"/>'))
        o.append('<circle cx="%.1f" cy="%.1f" r="8.5" fill="%s"/>' % (mx, my, BLUE))
        o.append(txt(mx, my+4, tag, 12, PAPER, 700, "middle"))
        o.append(txt(x0+(2*bw+gx)/2, y0+2*bh+gy+20, caption, 12, INK, 700, "middle"))
        return "".join(o)
    s.append(loop(0, 22, "1", "ASSET MANAGEMENT \u00b7 BUSINESS"))
    s.append(loop(274, 22, "2", "PROJECT CONTROL \u00b7 PROJECT"))
    s.append(line(208, 32, 272, 32, BLUE, 1.6).replace("/>", ' marker-end="url(#ab)"/>'))
    s.append(txt(240, 18, "plans go in", 12, BLUE, 600, "middle"))
    s.append(line(272, 76, 210, 76, BLUE, 1.6).replace("/>", ' marker-end="url(#ab)"/>'))
    s.append(txt(240, 94, "results back", 12, BLUE, 600, "middle"))
    return svg(VW, 112, "".join(s))

def dia_lifecycles():
    s = [arrow_defs()]
    ax = [66, 166, 262, 350, 452]
    s.append(txt(306, 10, "operation and modification repeat", 12, BLUE, 600, "middle"))
    s.append('<path d="M350,30 C 350,16 262,16 262,30" fill="none" stroke="%s" stroke-width="1.5" marker-end="url(#ab)"/>' % BLUE)
    s.append(line(30, 38, 470, 38, INK, 1.3))
    for x in ax:
        s.append('<circle cx="%.1f" cy="38" r="4" fill="%s"/>' % (x, BLUE))
    for t, x in zip(["IDEATION", "CREATION", "OPERATION", "MODIFICATION"], ax[:4]):
        s.append(txt(x, 52, t, 12, INK, 600, "middle"))
    s.append(txt(VW, 52, "TERMINATION", 12, INK, 600, "end"))
    s.append(txt(0, 66, "ASSET LIFE CYCLE", 12, BLUE, 700))
    for x in (166, 350):
        s.append(line(x, 58, x, 80, BLUE, 1.2, "3 3"))
    s.append(line(30, 88, 470, 88, INK, 1.3))
    px = [100, 220, 340, 440]
    for x in px:
        s.append('<circle cx="%.1f" cy="88" r="4" fill="%s"/>' % (x, BLUE))
    for t, x in zip(["IDEATION", "PLANNING", "EXECUTION", "CLOSURE"], px):
        s.append(txt(x, 102, t, 12, INK, 600, "middle"))
    s.append(txt(VW, 116, "PROJECT LIFE CYCLE, NESTED INSIDE IT", 12, BLUE, 700, "end"))
    return svg(VW, 122, "".join(s))

def chart_influence():
    x0, x1, y0, y1 = 34, 462, 12, 78
    def X(v): return x0 + v/100.0*(x1-x0)
    def Y(v): return y1 - v/100.0*(y1-y0)
    s = [arrow_defs()]
    for v in (0, 50, 100):
        s.append(line(x0, Y(v), x1, Y(v), "#E6EAEE", 1))
        s.append(txt(x0-5, Y(v)+4, str(v), 12, MUTED, 500, "end"))
    s.append(line(X(40), y0, X(40), y1, RULE, 1, "3 3"))
    s.append(poly([(X(a), Y(b)) for a, b in EXP], INK, 2.2))
    s.append(poly([(X(a), Y(b)) for a, b in INF], BLUE, 2.6))
    s.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s" stroke="%s" stroke-width="2"/>'
             % (X(CROSS_X), Y(CROSS_Y), PAPER, INK))
    s.append(txtbg(X(64), Y(34), "they cross at %d%%" % round(CROSS_X), 12, INK, 700))
    s.append(txtbg(X(3), Y(70), "ABILITY TO INFLUENCE", 12, BLUE, 700))
    s.append(txtbg(X(97), Y(70), "CUMULATIVE SPEND", 12, INK, 700, "end"))
    s.append(line(x0, y1, x1, y1, INK, 1.3))
    s.append(txt(x0, y1+15, "0", 12, MUTED, 500))
    s.append(txt((x0+x1)/2, y1+15, "% of project duration", 12, MUTED, 500, "middle"))
    s.append(txt(x1, y1+15, "100", 12, MUTED, 500, "end"))
    return svg(VW, y1+20, "".join(s))

def chart_states():
    lx, bx0, bx1 = 0, 78, 408
    top, rowh = 3, 14
    mx = 110.0
    def BX(v): return bx0 + v/mx*(bx1-bx0)
    s = []
    rows = [("COMMITTED", COMMITTED), ("INCURRED", INCURRED), ("INVOICED", INVOICED), ("PAID", PAID)]
    for i, (lab, v) in enumerate(rows):
        y = top + i*rowh
        s.append(txt(lx, y+10.5, lab, 12, INK, 600))
        s.append(rect(bx0, y+1, BX(v)-bx0, 10, BLUE2 if i else BLUE, "none"))
        s.append(txt(BX(v)+5, y+10, f1(v), 12, INK, 700))
    ey = top + 4*rowh + 8
    s.append(txt(lx, ey+10.5, "EAC", 12, INK, 700))
    s.append(rect(bx0, ey+1, BX(INCURRED)-bx0, 10, BLUE, "none"))
    s.append(rect(BX(INCURRED), ey+1, BX(EAC)-BX(INCURRED), 10, PAPER, BLUE, 1.2))
    s.append(txt((bx0+BX(INCURRED))/2, ey+10, f1(INCURRED), 12, PAPER, 700, "middle"))
    s.append(txt((BX(INCURRED)+BX(EAC))/2, ey+10, f1(ETC), 12, BLUE, 700, "middle"))
    s.append(txt(BX(EAC)+5, ey+10, f1(EAC), 12, INK, 700))
    s.append(line(BX(BUDGET), 0, BX(BUDGET), ey+14, INK, 1.5, "4 3"))
    s.append(txt(BX(BUDGET)+6, 10, "BUDGET %s" % f1(BUDGET), 12, INK, 700))
    s.append(txt(BX(BUDGET)+6, 24, "%s baseline" % f1(BASELINE), 12, MUTED, 500))
    s.append(txt(BX(BUDGET)+6, 37, "+ %s approved" % f1(APPROVED_CHG), 12, MUTED, 500))
    s.append(txt(0, ey+27, "US$M at one cut-off date. The EAC crossing the budget line is the alarm.", 12, MUTED, 500))
    return svg(VW, ey+31, "".join(s))

def chart_builds():
    full = float(VW)
    s = []
    def seg(vals, y, fills):
        o, x = [], 0.0
        for (lab, v), f in zip(vals, fills):
            w_ = v/EAC*full
            o.append(rect(x, y, w_, 21, f[0], f[1], 1))
            if w_ > 74:
                o.append(txt(x+w_/2, y+14.5, "%s %s" % (lab, f1(v)), 12, f[2], 700, "middle"))
            x += w_
        return "".join(o)
    s.append(txt(0, 10, "INCURRED BUILD", 12, INK, 700))
    s.append(txt(full, 10, "both stop at EAC %s" % f1(EAC), 12, INK, 700, "end"))
    s.append(seg([("Incurred", INCURRED), ("To complete", ETC)], 14,
                 [(BLUE, "none", PAPER), (PAPER, BLUE, BLUE)]))
    s.append(txt(0, 56, "COMMITMENT BUILD", 12, INK, 700))
    s.append(seg([("Committed", COMMITTED), ("Uncommitted", UNCOMMITTED), ("", CHANGES), ("", RISK)], 60,
                 [(BLUE, "none", PAPER), (BLUE2, "none", PAPER), (BLUE3, "none", INK), (PAPER, BLUE, BLUE)]))
    s.append(line(full-0.7, 8, full-0.7, 88, INK, 1.6))
    s.append(txt(0, 98, "committed %s \u00b7 uncommitted %s \u00b7 changes %s \u00b7 risk %s"
                 % (f1(COMMITTED), f1(UNCOMMITTED), f1(CHANGES), f1(RISK)), 12, MUTED, 500))
    return svg(VW, 102, "".join(s))

def chart_bridge():
    x0, slot, bw = 26, 56, 38
    ylo, yhi, ytop, ybot = 98.0, 106.0, 8, 68
    def Y(v): return ybot - (v-ylo)/(yhi-ylo)*(ybot-ytop)
    s = []
    s.append(line(x0-6, ybot, 474, ybot, INK, 1.3))
    for v in (98, 102, 106):
        s.append(txt(0, Y(v)+4, str(v), 12, MUTED, 500))
    run = OPEN_EAC
    s.append(rect(x0, Y(OPEN_EAC), bw, ybot-Y(OPEN_EAC), BLUE, "none"))
    s.append(txt(x0+bw/2, Y(OPEN_EAC)-5, f1(OPEN_EAC), 12, INK, 700, "middle"))
    names = ["scope", "quantity", "rates", "schedule", "risk", "re-est"]
    for i, (lab, v) in enumerate(MOVES):
        x = x0 + (i+1)*slot
        a, b = run, run+v
        top_, h_ = Y(max(a, b)), abs(Y(a)-Y(b))
        fill = (BLUE2, "none", 0) if v >= 0 else (PAPER, BLUE, 1.2)
        s.append(rect(x, top_, bw, max(h_, 1.6), fill[0], fill[1], fill[2]))
        s.append(txt(x+bw/2, top_-5, ("+" if v >= 0 else "−")+("%.1f" % abs(v)), 12, INK, 600, "middle"))
        s.append(txt(x+bw/2, ybot+14, names[i], 12, MUTED, 500, "middle"))
        s.append(line(x-(slot-bw), Y(a), x, Y(a), RULE, 1, "2 2"))
        run = b
    xf = x0 + 7*slot
    s.append(rect(xf, Y(CLOSE_EAC), bw, ybot-Y(CLOSE_EAC), BLUE, "none"))
    s.append(txt(xf+bw/2, Y(CLOSE_EAC)-5, f1(CLOSE_EAC), 12, INK, 700, "middle"))
    s.append(txt(x0, ybot+28, "opening EAC, 31 Jul", 12, MUTED, 500))
    s.append(txt(474, ybot+28, "closing EAC, 31 Aug", 12, MUTED, 500, "end"))
    return svg(VW, ybot+30, "".join(s))

def dia_scale():
    cx = 130
    s = []
    s.append(line(cx-90, 30, cx+90, 30, INK, 2.2))
    s.append('<path d="M%d,30 L%d,54 L%d,54 Z" fill="none" stroke="%s" stroke-width="1.6"/>' % (cx, cx-9, cx+9, INK))
    s.append(line(cx-16, 56, cx+16, 56, INK, 1.8))
    for px in (cx-90, cx+90):
        s.append(line(px, 30, px, 39, INK, 1.2))
        s.append('<path d="M%d,39 L%d,39 L%d,48 Z" fill="none" stroke="%s" stroke-width="1.4"/>'
                 % (px-17, px+17, px, INK))
    s.append(txt(cx-90, 21, "PRICE", 12, INK, 700, "middle"))
    s.append(txt(cx+90, 21, "COST", 12, INK, 700, "middle"))
    s.append(txt(cx-90, 62, "to the seller", 12, MUTED, 500, "middle"))
    s.append(txt(cx+90, 62, "to the buyer", 12, MUTED, 500, "middle"))
    s.append(txt(cx, 14, "one amount", 12, MUTED, 500, "middle"))
    s.append(rect(266, 6, 214, 58, PAPER, BLUE, 1.5))
    s.append(txt(276, 22, "VALUE", 12, BLUE, 700))
    s.append(txt(276, 38, "worth to a defined party at a", 12, INK, 500))
    s.append(txt(276, 52, "defined date — an opinion", 12, INK, 500))
    return svg(VW, 70, "".join(s))

def dia_reprorep():
    s = []
    s.append(rect(0, 0, VW, 18, BLUE, "none"))
    s.append(txt(VW/2, 13, "BOTH PRICED AT CURRENT COSTS, AT THE ESTIMATE DATE", 12, PAPER, 700, "middle"))
    s.append(line(VW/2, 24, VW/2, 72, RULE, 1))
    s.append(txt(0, 36, "REPRODUCTION COST NEW", 12, INK, 700))
    s.append(txt(VW/2+12, 36, "REPLACEMENT COST NEW", 12, INK, 700))
    s.append(txt(0, 51, "an exact duplicate — same", 12, MUTED, 500))
    s.append(txt(0, 65, "materials, design, workmanship", 12, MUTED, 500))
    s.append(txt(VW/2+12, 51, "equivalent utility — current", 12, MUTED, 500))
    s.append(txt(VW/2+12, 65, "materials and current standards", 12, MUTED, 500))
    return svg(VW, 72, "".join(s))

def dia_traceability():
    s = [arrow_defs()]
    s.append(rect(300, 4, 180, 30, PAPER, INK, 1.4))
    s.append(txt(390, 17, "COST OBJECT", 12, INK, 700, "middle"))
    s.append(txt(390, 29, "the lab chamber", 12, MUTED, 500, "middle"))
    for i, t in enumerate(["labour", "materials", "plant"]):
        y = 6 + i*12
        s.append(txt(0, y+4, t, 12, INK, 500))
        s.append(line(62, y+1, 294, 17, BLUE, 1.4).replace("/>", ' marker-end="url(#ab)"/>'))
    s.append(txt(120, 50, "TRACED = DIRECT", 12, BLUE, 700))
    s.append(line(0, 58, VW, 58, RULE, 1))
    s.append(rect(0, 66, 190, 32, BLUE4, BLUE, 1))
    s.append(txt(95, 80, "INDIRECT POOL", 12, BLUE, 700, "middle"))
    s.append(txt(95, 92, "supervision, insurance, prelims", 12, INK, 500, "middle"))
    for i in range(3):
        y = 66 + i*13
        s.append(rect(400, y, 80, 10, PAPER, INK, 1))
        s.append(line(196, 82, 396, y+5, BLUE, 1.3, "3 2").replace("/>", ' marker-end="url(#ab)"/>'))
    s.append(txt(300, 108, "three cost objects", 12, MUTED, 500, "middle"))
    s.append(txt(120, 108, "ALLOCATED = INDIRECT", 12, BLUE, 700, "middle"))
    return svg(VW, 110, "".join(s))

def chart_behaviour():
    x0, x1, y0, y1 = 34, 358, 10, 66
    def X(v): return x0 + v/20.0*(x1-x0)
    def Y(v): return y1 - v/160000.0*(y1-y0)
    s = []
    s.append(line(x0, y1, x1, y1, INK, 1.3))
    s.append(line(x0, y0, x0, y1, RULE, 1))
    s.append(rect(X(16), y0, X(20)-X(16), y1-y0, BLUE4, "none"))
    s.append(poly([(X(0), Y(60000)), (X(20), Y(60000))], INK, 1.8, dash="5 3"))
    s.append(poly([(X(0), Y(0)), (X(20), Y(TIMEREL_WK*20))], BLUE, 2.6))
    s.append(poly([(X(0), Y(96000)), (X(20), Y(96000))], BLUE2, 1.8, dash="2 3"))
    s.append(txt(x1+7, Y(TIMEREL_WK*20)+4, "TIME-RELATED", 12, BLUE, 700))
    s.append(txt(x1+7, Y(96000)+4, "VARIABLE", 12, BLUE2, 700))
    s.append(txt(x1+7, Y(60000)+4, "FIXED", 12, INK, 700))
    s.append(txt(0, Y(160000)+4, "160", 12, MUTED, 500))
    s.append(txt(0, Y(80000)+4, "$000", 12, MUTED, 500))
    s.append(txt(0, y1+4, "0", 12, MUTED, 500))
    s.append(txt(x0, y1+15, "0", 12, MUTED, 500))
    s.append(txt((x0+x1)/2, y1+15, "weeks on programme", 12, MUTED, 500, "middle"))
    s.append(txt(x1, y1+15, "20", 12, MUTED, 500, "end"))
    s.append(txt(X(18), y0+9, "delay", 12, BLUE, 700, "middle"))
    return svg(VW, y1+18, "".join(s))

def dia_bands():
    s = []
    bands = [("BASE BUILDING \u2014 shell and core, primary risers, base plant", PAPER, INK, INK, 1.3),
             ("LANDLORD FIT-OUT TO LETTABLE STANDARD \u2014 UK Cat A / US warm shell", BLUE4, BLUE, INK, 1),
             ("OCCUPIER FIT-OUT \u2014 UK Cat B / US tenant improvement, IT, AV, security", BLUE, "none", PAPER, 0)]
    for i, (lab, fill, stroke, fg, sw) in enumerate(bands):
        y = i*24
        s.append(rect(0, y, VW, 21, fill, stroke, sw))
        s.append(txt(9, y+14.5, lab, 12, fg, 700 if i == 2 else 600))
    for i in range(6):
        x = 52 + i*76
        s.append('<path d="M%d,40 L%d,47 L%d,54 L%d,47 Z" fill="%s" stroke="%s" stroke-width="1.4"/>'
                 % (x, x+7, x, x-7, PAPER, BLUE))
    return svg(VW, 70, "".join(s))

def chart_benchmark():
    bx0, bx1 = 0, 398
    mx = 800.0
    def BX(v): return bx0 + v/mx*(bx1-bx0)
    s = []
    tints = [BLUE, BLUE2, BLUE3, BLUE4, "#EFF4F9", PAPER]
    def bar(items, y, total, label):
        o, x = [], bx0
        for i, (nm, v) in enumerate(items):
            w_ = BX(v)-bx0
            o.append(rect(x, y, w_, 22, tints[i % len(tints)], INK, 0.8))
            if w_ > 30:
                o.append(txt(x+w_/2, y+15, str(v), 12, PAPER if i == 0 else INK, 700, "middle"))
            x += w_
        o.append(txt(x+6, y+15, "$%d" % total, 12, INK, 700))
        o.append(txt(0, y-5, label, 12, INK, 700))
        return "".join(o)
    s.append(bar(OFFICE, 14, OFFICE_T, "OFFICE BENCHMARK \u2014 shell, office MEP, office fit-out"))
    s.append(bar(LAB, 74, LAB_T, "LAB \u2014 the same shell, plus what the office rate leaves out"))
    s.append('<path d="M%.1f,50 L%.1f,42 L%.1f,42 L%.1f,50" fill="none" stroke="%s" stroke-width="1.4"/>'
             % (BX(OFFICE_T), BX(OFFICE_T), BX(LAB_T), BX(LAB_T), BLUE))
    s.append(txt(BX(LAB_T)+6, 47, "+$%d" % DELTA, 12, BLUE, 700))
    s.append(txt(0, 110, "US$ per gross sq ft, illustrative. The bracket is the lab scope the office rate excludes.",
                 12, MUTED, 500))
    return svg(VW, 114, "".join(s))

def chart_powerlaw():
    x0, x1, y0, y1 = 34, 372, 12, 72
    def X(v): return x0 + (v-0.5)/1.5*(x1-x0)
    def Y(v): return y1 - (v-0.5)/1.5*(y1-y0)
    s = []
    s.append(rect(X(0.5), y0, X(2.0)-X(0.5), y1-y0, PAPER, RULE, 1))
    hi = [(X(r/20.0), Y((r/20.0)**0.5)) for r in range(10, 41)]
    lo = [(X(r/20.0), Y((r/20.0)**0.9)) for r in range(40, 9, -1)]
    s.append('<polygon points="%s" fill="%s" stroke="none"/>'
             % (" ".join("%.1f,%.1f" % p for p in hi+lo), BLUE4))
    s.append(poly([(X(r/20.0), Y(r/20.0)) for r in range(10, 41)], INK, 1.1, dash="4 3"))
    s.append(poly([(X(r/20.0), Y((r/20.0)**0.6)) for r in range(10, 41)], BLUE, 2.6))
    s.append(line(X(CAP_RATIO), y1, X(CAP_RATIO), Y(COST_FACTOR), INK, 1, "2 2"))
    s.append(line(x0, Y(COST_FACTOR), X(CAP_RATIO), Y(COST_FACTOR), INK, 1, "2 2"))
    s.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (X(CAP_RATIO), Y(COST_FACTOR), INK))
    s.append(txt(x1+7, Y(2.0)+4, "n = 1.0", 12, MUTED, 600))
    s.append(txt(x1+7, Y(1.95**0.6)+4, "n = 0.6", 12, BLUE, 700))
    s.append(txt(x1+7, Y(1.95**0.6)+17, "band 0.5\u20130.9", 12, BLUE2, 600))
    s.append(txt(0, Y(COST_FACTOR)+4, "%.2f" % COST_FACTOR, 12, INK, 700))
    s.append(txt(X(CAP_RATIO), y1+15, "%.2f" % CAP_RATIO, 12, INK, 700, "middle"))
    s.append(txt(x0, y1+15, "0.5", 12, MUTED, 500, "middle"))
    s.append(txt(x1, y1+15, "2.0", 12, MUTED, 500, "end"))
    s.append(txt((x0+x1)/2, y1+27, "capacity ratio, Cap B \u00f7 Cap A", 12, MUTED, 500, "middle"))
    s.append(txt(0, y0-2, "cost factor", 12, MUTED, 500))
    return svg(VW, y1+31, "".join(s))

def chart_crossover():
    x0, x1, y0, y1 = 34, 404, 14, 72
    def X(v): return x0 + v/12.0*(x1-x0)
    def Y(v): return y1 - (v-80)/60.0*(y1-y0)
    s = []
    s.append(line(x0, y1, x1, y1, INK, 1.3))
    s.append(poly([(X(0), Y(ULT)), (X(12), Y(ULT))], INK, 2.2))
    s.append(poly([(X(r/2.0), Y(staged_npv(r/200.0))) for r in range(0, 25)], BLUE, 2.6))
    cx, cy = X(CROSSOVER*100), Y(ULT)
    s.append(line(cx, y0, cx, y1, INK, 1, "3 3"))
    s.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s" stroke="%s" stroke-width="2"/>' % (cx, cy, PAPER, INK))
    s.append(txt(cx+7, y0+8, "crossover %.1f%%" % (CROSSOVER*100), 12, INK, 700))
    s.append(txt(X(1.2), Y(124), "STAGED", 12, BLUE, 700))
    s.append(txt(x1+7, Y(ULT)+4, "ULTIMATE", 12, INK, 700))
    s.append(txt(0, Y(100)+4, "100", 12, MUTED, 500))
    s.append(txt(0, y1+4, "80", 12, MUTED, 500))
    s.append(txt(x0, y1+15, "0", 12, MUTED, 500, "middle"))
    s.append(txt((x0+x1)/2, y1+15, "real discount rate, %", 12, MUTED, 500, "middle"))
    s.append(txt(x1, y1+15, "12", 12, MUTED, 500, "end"))
    s.append(txt(cx-7, y1-3, "ultimate lower", 12, MUTED, 500, "end"))
    s.append(txt(cx+7, y1-3, "staged lower", 12, MUTED, 500))
    s.append(txt(0, y0-3, "NPV US$M", 12, MUTED, 500))
    return svg(VW, y1+20, "".join(s))

