# -*- coding: utf-8 -*-
import os, json
from gen_core import *

# ================================================================ html blocks
def block(heading, viz, bullets, was, extra="", wide=False):
    b = "".join("<li>%s</li>" % x for x in bullets)
    lst = '<ul class="bl">%s</ul>' % b if bullets else ""
    core = (viz or "") + lst
    fx = '<p class="fx"><span>Was</span> %s</p>' % was if was else ""
    return '<section class="bk"><h3 class="bh">%s</h3>%s%s%s</section>' % (heading, core, extra, fx)

def formula(s):
    return '<p class="fm">%s</p>' % s

def grid23():
    cells = [("Lab chamber design fee", "Dedicated commissioner", "Lab cable, per m"),
             ("Site set-up, mobilisation", "Site supervision, welfare", "Consumables, waste")]
    o = ['<div class="g23"><div class="gh"></div><div class="gh">FIXED</div>'
         '<div class="gh">TIME-RELATED</div><div class="gh">VARIABLE</div>']
    for i, rowname in enumerate(("DIRECT", "INDIRECT")):
        o.append('<div class="gr">%s</div>' % rowname)
        for c in cells[i]:
            o.append('<div class="gc">%s</div>' % c)
    o.append("</div>")
    return "".join(o)

def col(num, title, blocks):
    head = ('<div class="ph"><span class="pn">%s</span><span class="pt">%s</span></div>' % (num, title)) if num else ""
    return '<div class="col">%s%s</div>' % (head, "".join(blocks))

# ================================================================ phase content
import content

def phase1(): return content.P1(block, col, formula)
def phase2(): return content.P2(block, col, formula)
def phase3(): return content.P3(block, col, formula)
def phase4(): return content.P4(block, col, formula)
def phase5(): return content.P5(block, col, formula)

def ecls():
    rows = [("5", "0\u20132%", "concept screening"),
            ("4", "1\u201315%", "study or feasibility"),
            ("3", "10\u201340%", "budget authorisation"),
            ("2", "30\u201375%", "control, or bid and tender"),
            ("1", "65\u2013100%", "check estimate, bid and tender")]
    o = ['<div class="ecl"><div class="eh">CLASS</div><div class="eh">% DEFINED</div>'
         '<div class="eh">TYPICAL PURPOSE</div>']
    for c, d, p in rows:
        o.append('<div class="ec">%s</div><div>%s</div><div>%s</div>' % (c, d, p))
    o.append('</div><p class="enote">AACE 17R-97. Accuracy ranges widen sharply toward Class 5 '
             '\u2014 take them from the standard.</p>')
    return "".join(o)

def col_loop():
    steps = ["Cut off and accrue &mdash; every measure to the same day",
             "Update the estimate at completion",
             "Bridge the movement from last month&rsquo;s EAC",
             "Issue it, with the trend behind the movement",
             "Act on the variance: raise a change, or draw contingency",
             "Capture the as-built cost and normalise it",
             "Return it to the benchmark set Phase 5 draws on"]
    li = "".join('<li><span class="sn">%d</span>%s</li>' % (i+1, t) for i, t in enumerate(steps))
    return col("", "Closing the loop", [
        block("The monthly cycle", None, [], "",
              extra='<ol class="cyc">%s</ol>' % li +
                    formula("this cycle <b>is</b> CHECK and ACT in the Phase 1 project-control map")),
        block("Where each phase sits", None, [
            "<b>1</b> sets the loop, and says when influence is still worth spending.",
            "<b>2</b> fixes the words, so two people reading one number mean the same thing.",
            "<b>3</b> is the loop running: measure, forecast, explain the movement.",
            "<b>4</b> draws the boundaries, so nothing is counted twice or missed.",
            "<b>5</b> applies Phase 1&rsquo;s curve where influence is highest.",
        ], ""),
        block("How this issue was checked", None, [
            "Every element of the previous version was transcribed and reviewed, one reviewer per panel.",
            "Each finding was then attacked twice, independently: on technical accuracy, and on industry practice. A finding was dropped when both attacks succeeded.",
            "<b>%d</b> raised, <b>%d</b> dropped, <b>%d</b> carried. Sheet 3 lists them all." % (RAISED, DROPPED, CARRIED),
        ], ""),
        block("Estimate class, at a glance", None, [
            "Phase 1 says influence is highest where the estimate is weakest. This is that scale.",
        ], "", extra=ecls() + formula("state the class on every estimate you issue")),
        block("Basis and limits", None, [
            "Every figure here is illustrative, chosen so that the arithmetic ties. None of it is project data.",
            "Replace the worked examples with your own. The definitions, relationships and order of operations are what these sheets are for.",
        ], ""),
    ])

from fixes_data import RAISED, DROPPED, CARRIED, CRIT, FIXES, STOOD

PHASE_TITLES = {"1": "Lifecycle foundations", "2": "The language of cost",
                "3": "Measures, variance, forecast", "4": "Fit-out boundaries",
                "5": "Lab and infrastructure scenarios"}

def sheet_fixes():
    out = []
    for phase, items in FIXES:
        out.append('<div class="fxg"><div class="fxh"><span class="pn">%s</span>'
                   '<span class="pt">%s</span></div>' % (phase, PHASE_TITLES[phase]))
        for was, now, crit in items:
            out.append('<div class="fr%s"><p class="was">%s</p><p class="now">%s</p></div>'
                       % (" crit" if crit else "", was, now))
        out.append('</div>')
    out.append('<div class="fxg"><div class="fxh"><span class="pn">&mdash;</span>'
               '<span class="pt">Challenged, and left as it was</span></div>')
    for a, b in STOOD:
        out.append('<div class="fr stood"><p class="was">%s</p><p class="now">%s</p></div>' % (a, b))
    out.append('</div>')
    return "".join(out)

# ================================================================ css
CSS = """
*{box-sizing:border-box}
body{margin:0;background:%(paper)s;color:%(ink)s;
 font-family:'IBM Plex Sans',ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.sheet{width:%(W)dpx;height:%(H)dpx;background:%(paper)s;padding:28px 40px 24px;
 display:flex;flex-direction:column;overflow:hidden}
.mast{display:flex;align-items:flex-end;gap:26px;border-bottom:2.5px solid %(ink)s;padding-bottom:9px}
.mast h1{margin:0;font-family:'Archivo',sans-serif;font-weight:700;font-size:34px;
 line-height:.96;letter-spacing:-.018em;flex:none}
.mast .sub{font-size:13px;color:%(muted)s;line-height:1.32;max-width:250px;padding-bottom:2px}
.mast .sub b{color:%(ink)s}
.mast .note{margin-left:auto;text-align:right;font-size:12px;line-height:1.4;
 color:%(muted)s;max-width:560px;padding-bottom:2px}
.mast .note b{color:%(blue)s}
.basis{display:flex;gap:20px;font-size:12px;color:%(muted)s;border-bottom:1px solid %(rule)s;
 padding:4px 0 5px;margin-bottom:10px}
.basis b{color:%(ink)s;font-weight:600}
.cols{display:flex;gap:20px;flex:1;min-height:0}
.col{flex:1 1 0;min-width:0;padding-right:19px;border-right:1px solid %(rule)s;
 display:flex;flex-direction:column}
.col:last-child{border-right:0;padding-right:0}
.ph{display:flex;align-items:center;gap:8px;border-bottom:2px solid %(ink)s;
 padding-bottom:4px;margin-bottom:8px}
.pn{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;
 background:%(blue)s;color:#fff;font-family:'Archivo',sans-serif;font-weight:700;font-size:13px;flex:none}
.pt{font-family:'Archivo',sans-serif;font-weight:700;font-size:15px;letter-spacing:-.01em;line-height:1.08}
.bk{margin-bottom:5px}
.bk:last-child{margin-bottom:0}
.bh{margin:0 0 5px;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
 color:%(blue)s;border-bottom:1px solid %(ink)s;padding-bottom:3px;line-height:1.25}
.row{display:flex;gap:14px;align-items:flex-start}
.viz{width:275px}
.row .bl{flex:1 1 0;min-width:0;margin-top:-2px}
.bl{margin:0;padding:0;list-style:none}
.bl li{font-size:12px;line-height:1.32;margin-bottom:1px;padding-left:9px;position:relative;text-wrap:pretty}
.bl li:last-child{margin-bottom:0}
.bl li:before{content:"";position:absolute;left:0;top:7px;width:4px;height:1.5px;background:%(blue)s}
.fm{margin:6px 0 0;font-family:'IBM Plex Mono',monospace;font-size:12px;line-height:1.45;
 border-top:1px solid %(rule)s;border-bottom:1px solid %(rule)s;padding:4px 0;letter-spacing:-.012em}
.fm b{color:%(blue)s}
.fx{margin:5px 0 0;font-size:12px;line-height:1.32;color:%(muted)s;text-wrap:pretty}
.fx span{font-weight:700;color:%(blue)s;text-transform:uppercase;letter-spacing:.05em}
.g23{display:grid;grid-template-columns:68px 1fr 1fr 1fr;border:1px solid %(ink)s;margin-bottom:7px}
.g23>div{padding:3px 6px;font-size:12px;line-height:1.22;border-right:1px solid %(rule)s;
 border-bottom:1px solid %(rule)s}
.g23>div:nth-child(4n){border-right:0}
.g23>div:nth-last-child(-n+4){border-bottom:0}
.g23 .gh,.g23 .gr{font-weight:700;color:%(blue)s;text-transform:uppercase;letter-spacing:.02em}
.ecl{display:grid;grid-template-columns:48px 100px 1fr;border-top:1px solid %(ink)s;
 border-bottom:1px solid %(ink)s;margin-bottom:5px}
.ecl>div{padding:3px 10px 3px 0;font-size:12px;line-height:1.2;border-bottom:1px solid %(rule)s}
.ecl>div:nth-last-child(-n+3){border-bottom:0}
.ecl .eh{font-weight:700;color:%(blue)s;text-transform:uppercase;letter-spacing:.02em}
.ecl .ec{font-weight:700;color:%(blue)s}
.enote{margin:0 0 2px;font-size:12px;line-height:1.3;color:%(muted)s}
.cyc{margin:0;padding:0;list-style:none;counter-reset:c}
.cyc li{font-size:12px;line-height:1.3;padding:4px 0 4px 26px;position:relative;
 border-bottom:1px solid %(rule)s}
.cyc li:last-child{border-bottom:0}
.sn{position:absolute;left:0;top:4px;width:17px;height:17px;background:%(blue4)s;color:%(blue)s;
 font-weight:700;font-size:12px;display:inline-flex;align-items:center;justify-content:center}
.foot{display:flex;gap:14px;align-items:baseline;border-top:2px solid %(ink)s;margin-top:10px;
 padding-top:6px;font-size:12px;line-height:1.35}
.foot b{font-family:'Archivo',sans-serif;font-weight:700;text-transform:uppercase;
 letter-spacing:.05em;color:%(blue)s;flex:none}
.foot p{margin:0;color:%(muted)s}
.foot p i{color:%(ink)s;font-style:normal;font-weight:600}
.fxcols{column-count:5;column-gap:22px;flex:1;min-height:0}
.fxg{margin-bottom:12px}
.fxh{break-after:avoid}
.fxh{display:flex;align-items:center;gap:8px;border-bottom:2px solid %(ink)s;
 padding-bottom:4px;margin-bottom:8px}
.fr{break-inside:avoid;margin-bottom:7px;padding-left:9px;border-left:2px solid %(rule)s}
.fr.crit{border-left-color:%(blue)s}
.fr.stood{border-left-style:dotted}
.was{margin:0;font-size:12px;line-height:1.3;color:%(muted)s;text-wrap:pretty}
.now{margin:2px 0 0;font-size:12px;line-height:1.3;color:%(ink)s;text-wrap:pretty}
.now:before{content:"\\2192\\00a0";color:%(blue)s;font-weight:700}
.stat{display:flex;border:1px solid %(ink)s;margin-bottom:12px}
.stat div{flex:1;padding:6px 12px;border-right:1px solid %(rule)s}
.stat div:last-child{border-right:0}
.stat b{display:block;font-family:'Archivo',sans-serif;font-size:22px;font-weight:700;line-height:1;color:%(blue)s}
.stat span{font-size:12px;color:%(muted)s;line-height:1.25;display:block;margin-top:3px}
""" % dict(paper=PAPER, ink=INK, blue=BLUE, blue4=BLUE4, muted=MUTED, rule=RULE, W=W, H=H)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@600;700&family=IBM+Plex+Mono:wght@500;600&'
         'family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">')

BASIS = ('<div class="basis"><span><b>Basis for every figure on these sheets</b> &mdash; illustrative, '
         'not project data</span><span><b>US$</b>, Q3 2026 price level</span>'
         '<span><b>Real</b> (constant) dollars unless marked nominal</span>'
         '<span><b>US national average</b> location</span>'
         '<span>Phase 3 measures at <b>one cut-off date</b></span></div>')

def mast(h1, sub, note):
    return ('<div class="mast"><h1>%s</h1><div class="sub">%s</div>'
            '<div class="note">%s</div></div>' % (h1, sub, note))

FOOT1 = ('<div class="foot"><b>Read across</b><p>The framework sets the loop, the vocabulary makes one number '
         'mean one thing, and the measures run the loop each month. <i>Sheet 2</i> takes the same discipline to '
         'the fit-out boundary and to lab and infrastructure sizing. <i>Sheet 3</i> lists every correction made '
         'to the previous version of this roadmap, and every challenge the original survived.</p></div>')

FOOT2 = ('<div class="foot"><b>Read back</b><p>Both panels here are Phase 1&rsquo;s curve applied where influence '
         'is still cheap to use: the boundary is set before the packages go out, and the sizing decision is made '
         'before the capital is committed. <i>Sheet 3</i> lists every correction made to the previous version.</p></div>')

NOTE1 = ('This replaces an earlier version that carried <b>%d confirmed errors</b>, %d of them critical: a '
         'four-step control loop with two ACTs and no PLAN, a project stage printed twice, a chart that '
         'contradicted its own caption, a funnel that made the forecast the smallest number on the panel, and a '
         'bridge carrying no values at all.' % (CARRIED, CRIT))
NOTE2 = ('The two panels the earlier version got most wrong: a cost classification resting on what a cost was '
         '<i>built for</i> rather than what it can be <i>traced to</i>, an exclusion note hung on the wrong side '
         'of a benchmark, a capacity formula whose operator was addition, and a conditional answer printed as a rule.')
NOTE3 = ('Every element of the previous version was transcribed and reviewed, one reviewer per panel. Each '
         'finding was then attacked twice and independently &mdash; once on technical accuracy, once on industry '
         'practice &mdash; and dropped when both attacks succeeded. Blue rules mark the changes that alter what a '
         'reader would <b>do</b>.')

def page1():
    return ('<div class="sheet">%s%s<div class="cols">%s%s%s</div>%s</div>'
            % (mast("Mastering<br>Cost Management",
                    "A visual roadmap for technical real estate.<br><b>Corrected issue &mdash; sheet 1 of 3.</b>", NOTE1),
               BASIS, phase1(), phase2(), phase3(), FOOT1))

def page2():
    return ('<div class="sheet">%s%s<div class="cols">%s%s%s</div>%s</div>'
            % (mast("Boundaries<br>and scenarios",
                    "Cost management applied to technical real estate.<br><b>Corrected issue &mdash; sheet 2 of 3.</b>", NOTE2),
               BASIS, phase4(), phase5(), col_loop(), FOOT2))

def page3():
    stat = ('<div class="stat">'
            '<div><b>%d</b><span>errors raised across the five panels</span></div>'
            '<div><b>%d</b><span>dropped &mdash; the original was defensible</span></div>'
            '<div><b>%d</b><span>carried into the corrected sheets</span></div>'
            '<div><b>%d</b><span>of those critical: wrong, not merely loose</span></div>'
            '<div><b>%d</b><span>garbled labels restored to readable terms</span></div>'
            '</div>' % (RAISED, DROPPED, CARRIED, CRIT, 14))
    return ('<div class="sheet">%s%s<div class="fxcols">%s</div></div>'
            % (mast("What changed,<br>and why",
                    "Corrections to the cost management roadmap.<br><b>Sheet 3 of 3.</b>", NOTE3),
               stat, sheet_fixes()))

# ================================================================ output
OUT = os.path.dirname(os.path.abspath(__file__))
BOARDS = [("Main.dc.html", "Roadmap: foundations, language, control", page1),
          ("Scenarios.dc.html", "Roadmap: boundaries and scenarios", page2),
          ("Corrections.dc.html", "What changed, and why", page3)]

def dc(body, w_, h_):
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n<style>\n%s</style>\n</helmet>\n'
            '<div style="width:%dpx;height:%dpx">%s</div>\n</x-dc>\n'
            '<script data-dc-script data-props=\'{"$preview":{"width":%d,"height":%d}}\'>\n'
            'class Component extends DCLogic {\n  renderVals() { return {}; }\n}\n</script>\n</body>\n</html>\n'
            % (FONTS, CSS, w_, h_, body, w_, h_))

def standalone(title, bodies):
    secs = "".join('<div class="page">%s</div>' % b for b in bodies)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n%s\n<style>\n%s\n'
            'body{background:#EDF0F3;padding:24px;display:flex;flex-direction:column;align-items:center;gap:24px}\n'
            '.page{box-shadow:0 1px 4px rgba(0,0,0,.2)}\n'
            '@media print{body{background:#fff;padding:0;gap:0}.page{box-shadow:none;page-break-after:always}\n'
            '@page{size:%dpx %dpx;margin:0}}\n'
            '</style>\n</head>\n<body>\n%s</body>\n</html>\n' % (title, FONTS, CSS, W, H, secs))

def main():
    pages = []
    for fname, title, fn in BOARDS:
        b = fn()
        pages.append(b)
        with open(os.path.join(OUT, "project", fname), "w") as f:
            f.write(dc(b, W, H))
    idx = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-09-17T19:30:00Z"},
           "title": "Cost Management Roadmap", "launch": {"view": "canvas"}, "pages": [],
           "boards": {fname: {"x": i*(W+80), "y": 0, "w": W, "h": H, "title": title,
                              "print": "fixed", "paper": "letter"}
                      for i, (fname, title, _) in enumerate(BOARDS)},
           "order": [f for f, _, _ in BOARDS],
           "notes": {"t1": {"x": 0, "y": -250,
                            "text": "Mastering Cost Management — corrected issue",
                            "kind": "title1", "maxW": 3*W + 160}},
           "designSystems": []}
    with open(os.path.join(OUT, "project", "canvas.json"), "w") as f:
        json.dump(idx, f, indent=1)
    with open(os.path.join(OUT, "cost-management-roadmap.html"), "w") as f:
        f.write(standalone("Mastering Cost Management — corrected roadmap", pages))
    print("written", len(pages), "sheets")

main()
