# -*- coding: utf-8 -*-
from gen_core import *

RAISED, DROPPED, CARRIED = 97, 9, 88
CRIT, MAJ, MIN = 20, 52, 16

FIXES = [
 ("1", [
  ("The PDCA ring read ACT &ndash; DO &ndash; ACT &ndash; DOO. PLAN and CHECK were missing.",
   "PLAN, DO, CHECK, ACT &mdash; each step once, clockwise, with ACT closing back into PLAN.", 1),
  ("Both circles carried the same heading, &ldquo;THE TCM FRAMEWORK&rdquo;.",
   "One heading. The two circles are the framework&rsquo;s two process maps, captioned separately.", 0),
  ("The project control circle had no cycle steps at all.",
   "Drawn as the same four-step loop, one level down.", 0),
  ("The two circles sat unconnected, reading as two independent systems.",
   "Linked: plans go in at DO, results come back at CHECK. Project control is recursive inside asset management.", 1),
  ("&ldquo;(Business-red)&rdquo;.",
   "&ldquo;(business / enterprise level)&rdquo;, paired with &ldquo;(project / technical level)&rdquo;.", 0),
  ("IDEATION &rsaquo; PLANNING &rsaquo; EXECUTION &rsaquo; EXECUTION &rsaquo; CLOSURE.",
   "Four stages, EXECUTION shown once.", 1),
  ("Four bars rising to CLOSURE, captioned &ldquo;cost influence greatest&rdquo; at planning.",
   "Two curves: influence falling 100&rarr;0, cumulative spend rising 0&rarr;100, crossing near %d%% of duration. The old chart said the opposite of its own caption." % round(CROSS_X), 1),
  ("&ldquo;The project delivery path&rdquo;, used as a heading twice.",
   "&ldquo;The project life cycle&rdquo;, used once. Delivery <i>method</i> is a separate decision.", 0),
  ("The asset life cycle drawn as a one-way run to termination.",
   "A return arc: operation and modification repeat many times before termination.", 0),
 ]),
 ("2", [
  ("Reproduction and replacement cost captioned as the decision &ldquo;whether to move existing equipment or buy new&rdquo;.",
   "They are valuation bases, not a decision. Keep-or-replace is a separate defender-and-challenger test on future cash flows.", 1),
  ("&ldquo;ECONOMIC COST TERMS&rdquo; printed twice, with the numbering restarted at 1.",
   "One heading, one list, numbered 1 to 7 without a restart.", 0),
  ("SUNK COST appeared twice, the second time verbatim.",
   "Listed once.", 0),
  ("&ldquo;INVESTINY CRIST (Esprect Processon)&rdquo;.",
   "Investment (first) cost &mdash; capital to acquire, install and commission, ready for use.", 0),
  ("Book cost defined as &ldquo;accounting value&rdquo;.",
   "A non-cash cost carried in the accounts. Book <i>value</i> is a different thing: first cost &minus; accumulated depreciation.", 1),
  ("Cash cost absent, so book cost stood alone.",
   "Added. Book cost is recorded now; the cash left earlier.", 0),
  ("&ldquo;Budgets define the term&rdquo;.",
   "&ldquo;Perspective defines the term&rdquo; &mdash; budgets do not decide which cost term applies.", 0),
  ("&ldquo;Parogone Benefit&rdquo; and &ldquo;Imwurenside Past Spend&rdquo;.",
   "&ldquo;The benefit of the best alternative given up&rdquo; and &ldquo;unrecoverable past outlay&rdquo;.", 0),
  ("Neither reproduction nor replacement was said to be priced at current costs.",
   "Both stated as priced at current costs, at the estimate date.", 0),
 ]),
 ("3", [
  ("A funnel placed FORECAST FINAL COST last and narrowest.",
   "The EAC is drawn as its own bar and is allowed to cross the budget line &mdash; which is the alarm, not a drawing error.", 1),
  ("Six items presented as one family of &ldquo;money measures&rdquo;.",
   "One baseline, four ledger states, one forecast. They are not the same kind of number.", 1),
  ("Incurred &rarr; invoiced &rarr; paid stated as a universal law.",
   "True for progress-billed work. Advances and milestone terms pay before cost is incurred.", 0),
  ("No cut-off date anywhere.",
   "Every measure reported at one stated cut-off date, accruals cut the same day.", 0),
  ("Budget, forecast and headroom drawn as three icons with no operator.",
   "Budget &minus; EAC = variance at completion. Worked: %s &minus; %s = %s." % (f1(BUDGET), f1(EAC), f1(VAC)), 1),
  ("Only the favourable case was drawn.",
   "Both signs. Positive is headroom; negative is a forecast overrun with a named action.", 0),
  ("Nothing warned that headroom must be taken against the forecast.",
   "Budget &minus; paid and budget &minus; committed are budget <i>remaining</i>, and ignore the cost to complete.", 0),
  ("The two build columns were drawn at different heights, captioned &ldquo;both must agree&rdquo;.",
   "Identical lengths, with the tie-out printed: %s = (%s &minus; %s) + %s + %s + %s." % (f1(ETC), f1(COMMITTED), f1(INCURRED), f1(UNCOMMITTED), f1(CHANGES), f1(RISK)), 1),
  ("The forecast bridge was a drawing of a suspension bridge.",
   "A waterfall: opening anchor, six signed movements that sum exactly, closing anchor. No balancing bar.", 1),
  ("&ldquo;SCHPE CHANRE&rdquo; and &ldquo;Duth must agree&rdquo;.",
   "&ldquo;Scope change&rdquo; and &ldquo;both must agree&rdquo;.", 0),
 ]),
 ("4", [
  ("Direct cost defined as a cost &ldquo;built for one objective&rdquo;.",
   "Traced to one cost object. Dedication is not the test &mdash; traceability is.", 1),
  ("Direct and indirect presented as fixed properties of a cost.",
   "The classification depends on which cost object is named. Supervision is indirect to the lab chamber, direct to the project.", 1),
  ("Indirect cost stopped at &ldquo;supports several objectives&rdquo;.",
   "Indirect is recovered by allocation on a declared driver: rate = pool &divide; driver quantity.", 0),
  ("Monthly crane hire labelled FIXED, with &ldquo;per month&rdquo; given as the definition of fixed.",
   "Three classes: fixed, time-related, variable. Only the time-related slice grows in a delay.", 1),
  ("&ldquo;Direct does not always mean variable&rdquo; &mdash; half the statement.",
   "Both directions, drawn as a 2 &times; 3 grid with every cell occupied.", 0),
  ("A two-way scope split: core and shell against tenant improvement.",
   "Three bands. The middle tier &mdash; landlord fit-out to lettable standard, UK Cat A / US warm shell &mdash; was missing.", 1),
  ("The interface note was unreadable.",
   "Set one demarcation point for every IT, AV and security system, carried on a signed scope matrix.", 0),
  ("The panel named one classification and carried three.",
   "The heading names all three: traceability, behaviour, scope.", 0),
 ]),
 ("5", [
  ("&ldquo;Excludes MEP, IT racks, specialised equipment&rdquo; was hung on the LAB side.",
   "Backwards. The exclusion belongs to the office benchmark; the lab rate is the number that includes them.", 1),
  ("A head-to-head with a figure on one side only.",
   "Both bars carry a total and a composition on one common zero-based scale, plus the delta between them.", 1),
  ("COST B = COST A &times; (Cap B <b>+</b> Cap A).",
   "COST B = COST A &times; (Cap B <b>&divide;</b> Cap A)<sup>n</sup>. The capacities divide.", 1),
  ("The exponent had dropped out, surviving as a stray quote mark. No value of n anywhere.",
   "n restored as an exponent. n &asymp; 0.6 for plants; range 0.5&ndash;0.9, rising toward 1.0 at large scale.", 1),
  ("An equals sign between a %d-unit plant and a %d-unit plant." % (CAP_A, CAP_B),
   "+%d%% capacity for +%d%% capital, and %d%% per ton per day. The two plants are not equal." % (round((CAP_RATIO-1)*100), round((COST_FACTOR-1)*100), round((UNIT_FACTOR-1)*100)), 1),
  ("&ldquo;90 ten-per-day thermsl plant&rdquo;, and the second label silently dropped &ldquo;thermal&rdquo;.",
   "Tons per day, thermal, on both labels. Same plant type both sides or the ratio means nothing.", 0),
  ("No validity limits on the rule.",
   "Valid roughly 0.5&times; to 2&times; the base capacity, same technology. Escalate and location-adjust first. Screening level only.", 0),
  ("Staged scored on lifecycle cost, ultimate on net present value.",
   "One metric for both: NPV of life-cycle cost, one discount rate, one horizon, one basis.", 1),
  ("&ldquo;Building ultimate capacity now is often cheaper&rdquo;, printed as the standing answer.",
   "Conditional. Ultimate wins only when escalation plus amortised remobilisation beats the discount rate and demand is firm. Crossover here: %.1f%% real." % (CROSSOVER*100), 1),
  ("No discount rate, horizon, escalation rate or demand assumption stated.",
   "All four printed with the chart, and flagged illustrative.", 0),
 ]),
]

STOOD = [
 ("The balance scale for price against cost.",
  "A level beam under a &ldquo;versus&rdquo; heading reads as &ldquo;compare these two&rdquo;, not as &ldquo;these are equal&rdquo;. Kept."),
 ("&ldquo;Cost influence is greatest at planning&rdquo;.",
  "Standard front-end-loading teaching. The error was the chart underneath it, not the statement. Kept."),
 ("&ldquo;Standardised metrics to prevent counting things twice&rdquo;.",
  "Double counting is exactly the failure common cost definitions exist to prevent. Kept."),
 ("&ldquo;Incremental cost: the future difference between alternatives&rdquo;.",
  "Usage is not uniform across the standard texts, and this reading is one of the accepted ones. Kept."),
 ("&ldquo;TI&rdquo; as the name of the occupier scope tier.",
  "In US practice TI names the work; the landlord&rsquo;s contribution is the TI <i>allowance</i>. Kept, with the UK term alongside."),
 ("&ldquo;Capacity factor&rdquo; as the name of the method.",
  "AACE RP 59R-10 calls it capacity factored estimating. Kept."),
 ("The building cutaway and the plant icons.",
  "Pointing devices, not claims. Kept, with the mechanism drawn over the top."),
]

def sheet_fixes():
    out = []
    for phase, items in FIXES:
        out.append('<div class="fxg"><div class="fxh"><span class="pn">%s</span>'
                   '<span class="pt">%s</span></div>' % (phase, {
                       "1": "Lifecycle foundations", "2": "The language of cost",
                       "3": "Measures, variance, forecast", "4": "Boundaries in technical fit-out",
                       "5": "Lab and infrastructure scenarios"}[phase]))
        for was, now, crit in items:
            out.append('<div class="fr%s"><p class="was">%s</p><p class="now">%s</p></div>'
                       % (" crit" if crit else "", was, now))
        out.append('</div>')
    out.append('<div class="fxg"><div class="fxh"><span class="pn">&mdash;</span>'
               '<span class="pt">Challenged and left as it was</span></div>')
    for a, b in STOOD:
        out.append('<div class="fr stood"><p class="was">%s</p><p class="now">%s</p></div>' % (a, b))
    out.append('</div>')
    return "".join(out)

