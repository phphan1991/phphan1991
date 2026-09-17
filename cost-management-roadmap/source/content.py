# -*- coding: utf-8 -*-
"""Copy for the corrected roadmap. Graphic first, then a short stack of lines under it."""
from gen_core import *

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

def P1(block, col, formula):
    return col("1", "Lifecycle foundations", [
        block("One framework, two process maps", dia_pdca(), [
            "AACE&rsquo;s Total Cost Management framework: one framework, two maps.",
            "<b>1</b> strategic asset management, at business level. <b>2</b> project control, one level down.",
            "Each map is the same closed loop &mdash; PLAN, DO, CHECK, ACT, each step once.",
            "Project control runs <i>inside</i> asset management, not alongside it.",
        ], "a ring reading ACT&ndash;DO&ndash;ACT&ndash;DOO, and an empty second ring."),
        block("Two life cycles, nested", dia_lifecycles(), [
            "The asset is the outer container. Operation and modification repeat, many times.",
            "The project runs four stages, each shown once, inside the asset&rsquo;s life.",
            "Projects deliver the asset&rsquo;s creation and modification, and usually its end.",
            "&ldquo;Life cycle&rdquo;, not &ldquo;delivery path&rdquo; &mdash; delivery <i>method</i> is a separate decision.",
        ], "EXECUTION printed twice, and the two rows unrelated."),
        block("Influence falls as spend rises", chart_influence(), [
            "Influence on final cost runs 100 to 0; cumulative spend runs 0 to 100.",
            "They cross near " + str(round(CROSS_X)) + "% of duration. Influence is highest where the estimate is weakest.",
            "The same change costs about &times;10 more per stage deferred: $%s, then $%s." % (money(CHG_K10[0]), money(CHG_K10[3])),
            "That multiplier is a heuristic, not a law. It runs &times;3 to &times;10 &mdash; use your own data.",
        ], "bars rising to CLOSURE under a caption saying the opposite."),
    ])

def P2(block, col, formula):
    return col("2", "The language of cost", [
        block("Price, cost and value", dia_scale(), [
            "One amount, two names. Price is revenue to the seller; cost is what the buyer gives up.",
            "Value is neither: worth to a defined party at a defined date. An opinion, not an amount paid.",
            "The buyer&rsquo;s real cost is the installed cost, not the price.",
        ], "a two-term contrast, with value absent.",
           extra=formula("installed cost = %s + %s + %s + %s + %s = <b>%s</b> &nbsp;(%.2f&times; the price)"
                         % (money(P2_PRICE), money(P2_FRT), money(P2_TAX), money(P2_INST), money(P2_COMM), money(P2_TOTAL), P2_MULT))),
        block("Seven cost terms, numbered once", None, [
            "<b>1 Opportunity</b> &mdash; the benefit of the best alternative given up. Never in the accounts.",
            "<b>2 Sunk</b> &mdash; past outlay that cannot be recovered. Common to every option, so it cannot change the choice.",
            "<b>3 Book</b> &mdash; a non-cash cost carried in the accounts; depreciation is the standard case.",
            "<b>4 Cash</b> &mdash; an actual outlay. A book cost is recorded now; the cash left earlier.",
            "<b>5 Incremental</b> &mdash; the future difference between two options. Costs common to both drop out.",
            "<b>6 Investment (first)</b> &mdash; capital to acquire, install and commission, ready for use.",
            "<b>7 Life-cycle</b> &mdash; first cost plus operation, maintenance and disposal (ISO 15686-5).",
        ], "the heading and SUNK COST each printed twice."),
        block("Reproduction, replacement &mdash; and the decision they are not", dia_reprorep(), [
            "Both are valuation bases, not decisions. They price an asset you own, at today&rsquo;s costs.",
            "Cost approach: value = cost new &minus; depreciation + land.",
            "Keep or replace is a separate defender-and-challenger test, on future cash only: enter the asset at market value, never at book value or first cost.",
        ], "captioned as the move-or-buy decision. It is not.",
           extra=formula("defender $%s/yr vs challenger $%s/yr &nbsp;&middot;&nbsp; at book value it reads $%s, wrong by $%s a year"
                         % (money(DF_EUAC), money(CH_EUAC), money(DF_WRONG), money(DF_WRONG-DF_EUAC)))),
    ])

def P3(block, col, formula):
    return col("3", "Measures, variance, forecast", [
        block("One baseline, four states, one forecast", chart_states(), [
            "Four ledger balances at one cut-off date. Print the date; cut accruals the same day.",
            "Invoiced less paid (%s) is retention, terms and amounts withheld &mdash; not a saving. Only the EAC is compared with the budget." % f1(INVOICED-PAID),
        ], "a funnel that made the forecast the smallest figure."),
        block("Budget variance", None, [
            "Approved budget &minus; forecast final cost = variance at completion. Both signs, always.",
            "Positive is headroom. Negative is an overrun: raise a change or draw contingency now.",
            "Budget less paid, or less committed, is budget <i>remaining</i> &mdash; it ignores the %s still to come." % f1(ETC),
        ], "three icons, no operator, and only the good case.",
           extra=formula("%s &minus; %s = <b>%s</b> US$M &nbsp;&middot;&nbsp; %.1f%% of budget &nbsp;&middot;&nbsp; forecast overrun"
                         % (f1(BUDGET), f1(EAC), f1(VAC), VAC/BUDGET*100))),
        block("Two builds, one EAC", chart_builds(), [
            "Two views of one number &mdash; never add them. Any gap is unreconciled forecast.",
        ], "two columns of different heights, captioned &ldquo;both must agree&rdquo;.",
           extra=formula("%s + %s &nbsp;=&nbsp; %s + %s + %s + %s &nbsp;=&nbsp; <b>%s</b>"
                         % (f1(INCURRED), f1(ETC), f1(COMMITTED), f1(UNCOMMITTED), f1(CHANGES), f1(RISK), f1(EAC)))),
        block("The forecast bridge", chart_bridge(), [
            "1 scope +1.6 &middot; 2 quantity +0.9 &middot; 3 rates and escalation +0.5",
            "4 schedule +0.7 &middot; 5 risk &minus;1.2 &middot; 6 re-estimate &minus;0.2",
            "Anchored at both ends, summing exactly. No balancing bar, no residual, no rounding plug.",
        ], "a picture of a suspension bridge. No values, no signs."),
    ])

def P4(block, col, formula):
    return col("4", "Fit-out boundaries", [
        block("Traceability: direct or indirect", dia_traceability(), [
            "Direct is traced to one cost object. Indirect is pooled, then recovered by allocation.",
            "Nothing is direct or indirect by itself: supervision is indirect to the chamber and direct to the project. Declare the driver, and change it at your peril.",
        ], "&ldquo;built for one objective&rdquo;. Dedication is not the test.",
           extra=formula("rate = %s &divide; %s h = <b>$%.2f/h</b> &nbsp;&rarr;&nbsp; &times; %s h = $%s to the lab chamber"
                         % (money(POOL), money(DRIVER_H), RATE, money(LAB_H), money(LAB_ALLOC)))),
        block("Behaviour: three classes, not two", chart_behaviour(), [
            "Fixed does not move. Time-related runs per week. Variable runs per unit installed.",
            "Only the time-related slice grows in a delay: %d weeks &times; $%s = <b>$%s</b>." % (DELAY_WKS, money(TIMEREL_WK), money(DELAY_COST)),
        ], "monthly crane hire labelled fixed, by definition."),
        block("The two classifications are independent", grid23(), [
            "Every cell is occupied. Direct does not mean variable; indirect does not mean fixed.",
        ], "only half the statement. The converse holds too.", wide=True),
        block("Scope boundary: three bands", dia_bands(), [
            "Most gaps and double counts sit on the middle seam. The instrument is a signed scope matrix: supply, install, commission, own &mdash; per system, on one WBS.",
        ], "a two-way split &mdash; the middle tier was missing.", wide=True),
    ])

def P5(block, col, formula):
    return col("5", "Lab and infrastructure", [
        block("Benchmarks: the exclusion belongs to the office rate", chart_benchmark(), [
            "The office rate <i>excludes</i> lab HVAC and exhaust, lab power, racks and casework.",
            "The lab rate <i>includes</i> them, plus a shell premium for vibration and slab loading.",
            "$%d against $%d per gross sq ft here &mdash; %.1f&times;. Same city, same quarter, gross against gross." % (OFFICE_T, LAB_T, RATIO),
        ], "the exclusion note was hung on the lab side. Backwards."),
        block("Capacity factored estimating", chart_powerlaw(), [
            "The capacities <b>divide</b>, and n is an <b>exponent</b>. n &asymp; 0.6 for plants; range 0.5 to 0.9.",
            "+%d%% capital buys +%d%% capacity, so %d%% per ton per day." % (round((COST_FACTOR-1)*100), round((CAP_RATIO-1)*100), round((UNIT_FACTOR-1)*100)),
            "Valid 0.5&times; to 2&times; the base, same technology. Fixed-route networks use n &asymp; 0.2 to 0.3.",
            "Escalate and location-adjust first. Screening level only &mdash; confirm with quotes.",
        ], "capacities added, and the exponent had dropped out.",
           extra=formula("Cost B = Cost A &times; (Cap B &divide; Cap A)<sup>n</sup> &nbsp;&middot;&nbsp; (%d &divide; %d)<sup>0.6</sup> = <b>%.2f</b>"
                         % (CAP_B, CAP_A, COST_FACTOR))),
        block("Staged or ultimate: conditional, not a rule", chart_crossover(), [
            "One metric for both branches: NPV of life-cycle cost, one rate, one horizon, one basis.",
            "Ultimate wins when escalation plus amortised remobilisation beats the discount rate, <i>and</i> demand is firm.",
            "Staged wins when capital is dear, demand is uncertain, or the technology may change.",
        ], "printed as the standing answer, on two different metrics.",
           extra=formula("10-year horizon &middot; %d%% real escalation &middot; %d%% remobilisation &middot; curves cross at <b>%.1f%%</b> real"
                         % (ESC_R*100, REMOB*100, CROSSOVER*100))),
    ])
