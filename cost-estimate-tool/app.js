/* ===========================================================================
 * Cost Estimate Tool — HeavyBid-style UI
 * Reads RESOURCES, CREWS, UNITS, DEMO_ITEM, DEMO_ACTIVITIES from data.js
 * ========================================================================= */

const state = {
  activities: [],
};

let nextActivityId = 1;
let nextResourceId = 1;
const newActivityId = () => 'a' + (nextActivityId++);
const newResourceId = () => 'r' + (nextResourceId++);

const RESOURCE_BY_CODE = Object.fromEntries(RESOURCES.map(r => [r.code, r]));

/* ---------- Formatting helpers ---------- */
const fmtMoney = (n, decimals = 0) => {
  if (n === 0 || n == null || isNaN(n)) return decimals ? '0.00' : '0';
  const sign = n < 0 ? '-' : '';
  const abs = Math.abs(n);
  return sign + abs.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
};
const fmtMoneyCell = n => (n ? fmtMoney(Math.round(n)) : '');
const fmtNum = (n, d = 2) => Number(n || 0).toFixed(d);

/* ---------- Compute one resource line ---------- */
function computeLine(resourceLine) {
  const meta = RESOURCE_BY_CODE[resourceLine.code];
  const out = {
    code: resourceLine.code,
    desc: '',
    unit: '',
    unitCost: 0,
    pcs: Number(resourceLine.pcs) || 0,
    qty: Number(resourceLine.qty) || 0,
    labor: 0, material: 0, constr: 0, equip: 0, subcontract: 0, total: 0,
    category: '',
  };
  if (!meta) return out;
  out.desc = meta.desc;
  out.unit = meta.unit;
  out.unitCost = meta.unitCost;
  out.category = meta.category;

  const qty = out.qty;

  switch (meta.category) {
    case 'labor': {
      const rate = meta.burdenedRate ?? meta.unitCost;
      out.labor = qty * rate;
      break;
    }
    case 'material': {
      const markup = meta.markup ?? 1;
      out.material = qty * meta.unitCost * markup;
      break;
    }
    case 'constr': {
      out.constr = qty * meta.unitCost;
      break;
    }
    case 'equip': {
      out.equip = qty * meta.unitCost;
      break;
    }
    case 'subcontract': {
      out.subcontract = qty * meta.unitCost;
      break;
    }
  }
  out.total = out.labor + out.material + out.constr + out.equip + out.subcontract;
  return out;
}

function computeActivity(activity) {
  const totals = { labor: 0, material: 0, constr: 0, equip: 0, subcontract: 0, total: 0, mh: 0 };
  const lines = activity.resources.map(r => {
    const c = computeLine(r);
    totals.labor       += c.labor;
    totals.material    += c.material;
    totals.constr      += c.constr;
    totals.equip       += c.equip;
    totals.subcontract += c.subcontract;
    totals.total       += c.total;
    if (c.unit === 'MH') totals.mh += c.qty;
    return c;
  });
  return { lines, totals };
}

function computeReport() {
  const totals = { labor: 0, material: 0, constr: 0, equip: 0, subcontract: 0, total: 0, mh: 0 };
  for (const a of state.activities) {
    const { totals: t } = computeActivity(a);
    totals.labor += t.labor;
    totals.material += t.material;
    totals.constr += t.constr;
    totals.equip += t.equip;
    totals.subcontract += t.subcontract;
    totals.total += t.total;
    totals.mh += t.mh;
  }
  return totals;
}

/* ---------- Rendering ---------- */
const $ = sel => document.querySelector(sel);
const $$ = sel => Array.from(document.querySelectorAll(sel));
const el = (tag, attrs = {}, children = []) => {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') node.className = v;
    else if (k === 'html') node.innerHTML = v;
    else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
    else if (v === false || v == null) continue;
    else node.setAttribute(k, v);
  }
  for (const c of [].concat(children)) {
    if (c == null) continue;
    node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
  }
  return node;
};

function resourceOptionsHTML(selectedCode) {
  const groups = {
    constr:      'Constr Matl/Exp',
    equip:       'Equipment',
    labor:       'Labor',
    material:    'Permanent Materials',
    subcontract: 'Subcontractor',
  };
  let html = '<option value="">— select resource —</option>';
  for (const [cat, label] of Object.entries(groups)) {
    html += `<optgroup label="${label}">`;
    for (const r of RESOURCES.filter(x => x.category === cat)) {
      const sel = r.code === selectedCode ? ' selected' : '';
      html += `<option value="${r.code}"${sel}>${r.code} — ${r.desc}</option>`;
    }
    html += '</optgroup>';
  }
  return html;
}

function crewOptionsHTML(selectedCode) {
  let html = '<option value="">—</option>';
  for (const c of CREWS) {
    const sel = c.code === selectedCode ? ' selected' : '';
    html += `<option value="${c.code}"${sel}>${c.code} — ${c.name}</option>`;
  }
  return html;
}

function unitOptionsHTML(selectedUnit) {
  let html = '';
  for (const u of UNITS) {
    const sel = u === selectedUnit ? ' selected' : '';
    html += `<option value="${u}"${sel}>${u}</option>`;
  }
  return html;
}

function renderActivity(activity) {
  const { lines, totals } = computeActivity(activity);
  const aid = activity.id;
  const p = (suffix) => `act-${aid}/${suffix}`;

  // ---- Activity banner ----
  const banner = el('div', { class: 'activity-banner' });
  banner.innerHTML = `
    <div class="code"><input class="inline-input" value="${activity.code}" data-field="code" data-path="${p('code')}" /></div>
    <div class="desc"><input class="inline-input" value="${activity.desc}" data-field="desc" data-path="${p('desc')}" /></div>
    <div class="quan-label">Quan:</div>
    <div class="quan"><input class="inline-input" value="${fmtNum(activity.quan)}" data-field="quan" data-path="${p('quan')}" style="text-align:right" />
                     <select data-field="unit" data-path="${p('unit')}" class="inline-input" style="width:46px">${unitOptionsHTML(activity.unit)}</select></div>
    <div class="meta1">Hrs/Shft: <input class="inline-input" value="${fmtNum(activity.hrsShft)}" data-field="hrsShft" data-path="${p('hrsShft')}" style="width:38px;text-align:right" />
                     &nbsp; Cal: <input class="inline-input" value="${activity.cal}" data-field="cal" data-path="${p('cal')}" style="width:30px;text-align:right" /></div>
    <div class="meta2">WC: <input class="inline-input" value="${activity.wc}" data-field="wc" data-path="${p('wc')}" style="width:40px;text-align:right" /></div>
    <div class="actions"><button title="Delete activity" data-del-activity>×</button></div>
  `;

  // wire activity-field updates
  banner.querySelectorAll('[data-field]').forEach(input => {
    input.addEventListener('input', () => {
      const f = input.dataset.field;
      let v = input.value;
      if (['quan', 'hrsShft'].includes(f)) v = Number(v) || 0;
      activity[f] = v;
      rerender();
    });
  });
  banner.querySelector('[data-del-activity]').addEventListener('click', () => {
    state.activities = state.activities.filter(a => a !== activity);
    renderAll();
  });

  // ---- Optional crew header line ----
  let crewLine = null;
  if (activity.crewCode || activity.crewCH || activity.labPcs || activity.eqpPcs) {
    crewLine = el('div', { class: 'crew-line' });
    crewLine.innerHTML = `
      <div class="label"><select class="inline-input" data-field="crewCode" data-path="${p('crewCode')}">${crewOptionsHTML(activity.crewCode)}</select></div>
      <div class="name">${(CREWS.find(c => c.code === activity.crewCode) || {}).name || ''}</div>
      <div class="ch"><input class="inline-input" value="${fmtNum(activity.crewCH)}" data-field="crewCH" data-path="${p('crewCH')}" style="width:48px;text-align:right" /> CH</div>
      <div class="prod">Prod: <input class="inline-input" value="${fmtNum(activity.prod, 4)}" data-field="prod" data-path="${p('prod')}" style="width:60px;text-align:right" />
        <input class="inline-input" value="${activity.prodS || ''}" data-field="prodS" data-path="${p('prodS')}" style="width:30px;text-align:center" /></div>
      <div class="pcs">Lab Pcs: <input class="inline-input" value="${fmtNum(activity.labPcs)}" data-field="labPcs" data-path="${p('labPcs')}" style="width:46px;text-align:right" />
                      &nbsp; Eqp Pcs: <input class="inline-input" value="${fmtNum(activity.eqpPcs)}" data-field="eqpPcs" data-path="${p('eqpPcs')}" style="width:46px;text-align:right" /></div>
    `;
    crewLine.querySelectorAll('[data-field]').forEach(input => {
      input.addEventListener('input', () => {
        const f = input.dataset.field;
        let v = input.value;
        if (['crewCH','prod','labPcs','eqpPcs'].includes(f)) v = Number(v) || 0;
        activity[f] = v;
        rerender();
      });
    });
  }

  // ---- Optional notes line (e.g., "Backfill Electrical Trench w/ Red Concrete & CL3") ----
  let notesLine = null;
  if (activity.notes && activity.notes.length) {
    notesLine = el('div', { class: 'crew-line', style: 'font-style:italic;color:#444' });
    notesLine.innerHTML = `<div style="grid-column:1 / span 5"><input class="inline-input" value="${activity.notes}" data-field="notes" data-path="${p('notes')}" style="width:100%" /></div>`;
    notesLine.querySelector('input').addEventListener('input', e => {
      activity.notes = e.target.value;
    });
  }

  // ---- Resource lines ----
  const resourceRows = activity.resources.map((res, idx) => {
    const c = lines[idx];
    const row = el('div', { class: 'resource-line' });
    const rp = (f) => p(`res-${idx}/${f}`);
    row.innerHTML = `
      <div class="code"><select data-rfield="code" data-path="${rp('code')}">${resourceOptionsHTML(res.code)}</select></div>
      <div class="desc"><input class="txt" readonly value="${c.desc || ''}" /></div>
      <div class="pcs"><input class="num" type="number" step="0.01" value="${fmtNum(res.pcs)}" data-rfield="pcs" data-path="${rp('pcs')}" /></div>
      <div class="qty"><input class="num" type="number" step="0.01" value="${fmtNum(res.qty)}" data-rfield="qty" data-path="${rp('qty')}" /></div>
      <div class="unit"><input class="txt" readonly value="${c.unit || ''}" /></div>
      <div class="uc"><input class="num" readonly value="${c.unitCost ? fmtNum(c.unitCost, 3) : ''}" /></div>
      <div class="lab">${fmtMoneyCell(c.labor)}</div>
      <div class="mat">${fmtMoneyCell(c.material)}</div>
      <div class="ce">${fmtMoneyCell(c.constr)}</div>
      <div class="eq">${fmtMoneyCell(c.equip)}</div>
      <div class="sub">${fmtMoneyCell(c.subcontract)}</div>
      <div class="tot">${fmtMoneyCell(c.total)}</div>
      <div class="del"><button title="Delete resource">×</button></div>
    `;
    row.querySelectorAll('[data-rfield]').forEach(input => {
      input.addEventListener('input', () => {
        const f = input.dataset.rfield;
        let v = input.value;
        if (f === 'pcs' || f === 'qty') v = Number(v) || 0;
        res[f] = v;
        rerender();
      });
    });
    row.querySelector('.del button').addEventListener('click', () => {
      activity.resources.splice(idx, 1);
      renderAll();
    });
    return row;
  });

  // ---- Add-resource row ----
  const addRow = el('div', { class: 'add-resource-row' });
  addRow.innerHTML = `<button>+ Add Resource Line</button>`;
  addRow.querySelector('button').addEventListener('click', () => {
    activity.resources.push({ code: '', pcs: 1.00, qty: 0 });
    renderAll();
  });

  // ---- Activity totals line ----
  const tot = el('div', { class: 'activity-total-line' });
  const grandStr = '$' + fmtMoney(totals.total, 2);
  const unitCalc = activity.quan > 0 ? (totals.total / activity.quan) : 0;
  tot.innerHTML = `
    <div class="grand">${grandStr}</div>
    <div class="mh">${fmtNum(totals.mh)} MH ${activity.quan > 0 ? '· ' + fmtNum(totals.mh/activity.quan, 4) + ' MH/' + activity.unit : ''}</div>
    <div class="uc">${activity.quan > 0 ? '$' + fmtNum(unitCalc, 2) + '/' + activity.unit : ''}</div>
    <div class="lab">${fmtMoneyCell(totals.labor)}</div>
    <div class="mat">${fmtMoneyCell(totals.material)}</div>
    <div class="ce">${fmtMoneyCell(totals.constr)}</div>
    <div class="eq">${fmtMoneyCell(totals.equip)}</div>
    <div class="sub">${fmtMoneyCell(totals.subcontract)}</div>
    <div class="tot">${fmtMoneyCell(totals.total)}</div>
  `;

  const wrap = el('section', { class: 'activity', 'data-aid': activity.id });
  wrap.appendChild(banner);
  if (crewLine) wrap.appendChild(crewLine);
  if (notesLine) wrap.appendChild(notesLine);
  resourceRows.forEach(r => wrap.appendChild(r));
  wrap.appendChild(addRow);
  wrap.appendChild(tot);
  return wrap;
}

function renderActivities() {
  const host = $('#activities');
  host.innerHTML = '';
  for (const a of state.activities) host.appendChild(renderActivity(a));
}

function renderReportTotals() {
  const totals = computeReport();
  $('#rtTitle').textContent = '$' + fmtMoney(totals.total, 2) + '   *** Report Totals ***   ' + fmtNum(totals.mh) + ' MH';
  $('#rtLab').textContent = fmtMoneyCell(totals.labor);
  $('#rtMat').textContent = fmtMoneyCell(totals.material);
  $('#rtCE').textContent  = fmtMoneyCell(totals.constr);
  $('#rtEq').textContent  = fmtMoneyCell(totals.equip);
  $('#rtSub').textContent = fmtMoneyCell(totals.subcontract);
  $('#rtTot').textContent = fmtMoneyCell(totals.total);
}

function renderAll() {
  renderActivities();
  renderReportTotals();
}

/* Preserve focus & cursor position across full re-renders so typing feels smooth */
function withFocusPreserved(fn) {
  const a = document.activeElement;
  const path = a && a.dataset ? a.dataset.path : null;
  let selStart = null, selEnd = null;
  if (path && a.setSelectionRange) {
    try { selStart = a.selectionStart; selEnd = a.selectionEnd; } catch (_) {}
  }
  fn();
  if (!path) return;
  const next = document.querySelector('[data-path="' + (window.CSS && CSS.escape ? CSS.escape(path) : path) + '"]');
  if (!next) return;
  next.focus();
  if (selStart != null && next.setSelectionRange) {
    try { next.setSelectionRange(selStart, selEnd); } catch (_) {}
  }
}
function rerender() { withFocusPreserved(renderAll); }

/* ---------- Activity / resource creation ---------- */
function blankActivity() {
  return {
    id: newActivityId(),
    code: '005-0000',
    desc: 'New Activity',
    quan: 1.00,
    unit: 'LS',
    hrsShft: 8.00,
    cal: '001',
    wc: '5222',
    crewCode: 'XXX',
    crewCH: 8.00,
    prod: 1.0000,
    prodS: 'S',
    labPcs: 0,
    eqpPcs: 0,
    notes: '',
    resources: [],
  };
}

/* ---------- Demo loader ---------- */
function loadDemo() {
  // Header
  $('#bItem').value        = DEMO_ITEM.bidItem;
  $('#bDesc').value        = DEMO_ITEM.description;
  $('#bUnit').value        = DEMO_ITEM.unit;
  $('#bTakeoffQuan').value = fmtNum(DEMO_ITEM.takeoffQuan, 3);
  $('#bEngrQuan').value    = fmtNum(DEMO_ITEM.engrQuan, 3);
  $('#bSchedule').value    = DEMO_ITEM.schedule;
  $('#bLandItem').value    = DEMO_ITEM.landItem;
  $('#bInitials').value    = DEMO_ITEM.estimatorInitials;
  $('#hItem').value        = DEMO_ITEM.bidItem;

  state.activities = DEMO_ACTIVITIES.map(a => ({
    ...a,
    id: newActivityId(),
    resources: a.resources.map(r => ({ ...r })),
  }));
  renderAll();
}

/* ---------- Toolbar wiring ---------- */
$('#btnLoadDemo').addEventListener('click', loadDemo);
$('#btnAddActivity').addEventListener('click', () => {
  state.activities.push(blankActivity());
  renderAll();
});
$('#btnPrint').addEventListener('click', () => window.print());
$('#btnClear').addEventListener('click', () => {
  if (!confirm('Clear all activities?')) return;
  state.activities = [];
  renderAll();
});
$('#btnExport').addEventListener('click', () => {
  const payload = {
    header: {
      company:   $('#hCompany').value,
      job:       $('#hJob').value,
      project:   $('#hProject').value,
      estimator: $('#hEstimator').value,
      date:      $('#hDate').value,
      time:      $('#hTime').value,
      page:      $('#hPage').value,
      bidItem:   $('#bItem').value,
      desc:      $('#bDesc').value,
      unit:      $('#bUnit').value,
      takeoffQuan: $('#bTakeoffQuan').value,
      engrQuan:    $('#bEngrQuan').value,
      schedule:    $('#bSchedule').value,
      landItem:    $('#bLandItem').value,
      initials:    $('#bInitials').value,
    },
    activities: state.activities,
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = (payload.header.bidItem || 'estimate') + '-estimate.json';
  a.click();
  URL.revokeObjectURL(url);
});
$('#btnImport').addEventListener('click', () => $('#fileImport').click());
$('#fileImport').addEventListener('change', async e => {
  const file = e.target.files[0];
  if (!file) return;
  const text = await file.text();
  try {
    const data = JSON.parse(text);
    if (data.header) {
      const h = data.header;
      const set = (id, v) => { if (v !== undefined) $(id).value = v; };
      set('#hCompany', h.company); set('#hJob', h.job); set('#hProject', h.project);
      set('#hEstimator', h.estimator); set('#hDate', h.date); set('#hTime', h.time); set('#hPage', h.page);
      set('#bItem', h.bidItem); set('#hItem', h.bidItem);
      set('#bDesc', h.desc); set('#bUnit', h.unit);
      set('#bTakeoffQuan', h.takeoffQuan); set('#bEngrQuan', h.engrQuan);
      set('#bSchedule', h.schedule); set('#bLandItem', h.landItem); set('#bInitials', h.initials);
    }
    if (Array.isArray(data.activities)) {
      state.activities = data.activities.map(a => ({ ...a, id: newActivityId() }));
    }
    renderAll();
  } catch (err) {
    alert('Could not import: ' + err.message);
  }
  e.target.value = '';
});

// Keep bid item field in sync with the centered header
$('#bItem').addEventListener('input', e => { $('#hItem').value = e.target.value; });
$('#hItem').addEventListener('input', e => { $('#bItem').value = e.target.value; });

/* ---------- Initial render: load demo so users see the example ---------- */
loadDemo();
