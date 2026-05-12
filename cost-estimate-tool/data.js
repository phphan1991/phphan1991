// Master resource catalog extracted from the Seepage Wier Basin estimate (Item 51505)
// Categories: labor, material, constr (Constr Matl/Exp - off-job equipment), equip, subcontract
// burdenedRate is the effective MH rate (base + labor burdens) used to fill the Perm Labor column
// markup is applied to the unit cost for permanent materials (e.g., @109.13% supplier markup)

const RESOURCES = [
  // ===== Construction Materials / Expendables (Constr Matl/Exp column) =====
  { code: '5TRED40',      desc: '(HR) Ten Wheeler (7 CY, 1', unit: 'HR', unitCost: 150.000, category: 'constr' },
  { code: '5AGST35',      desc: '(S10) Haul Pea Gravel',     unit: 'TN', unitCost:  16.000, category: 'constr' },

  // ===== Equipment (Equip Ment column) =====
  { code: '801-1000114',  desc: '4MAN - 3/4 TN PICKUP T',    unit: 'HR', unitCost:  40.510, category: 'equip' },
  { code: '801-1000115',  desc: 'OP 4MAN - 3/4 TN TRK T',    unit: 'HR', unitCost:  40.510, category: 'equip' },
  { code: '801-1000116',  desc: 'G/C - 3/4 TN TRK TT-06',    unit: 'HR', unitCost:  40.510, category: 'equip' },
  { code: '802-0137600',  desc: 'CAT 330/345 HOE RAM A',     unit: 'HR', unitCost: 104.750, category: 'equip' },
  { code: '805-3000500',  desc: '16" JUMPING JACK',          unit: 'HR', unitCost:  16.280, category: 'equip' },
  { code: '807-0100050',  desc: '1 TON FLATBED PICKUP',      unit: 'HR', unitCost:  52.440, category: 'equip' },
  { code: '8AIRCP016-02', desc: '250 CFM AIR COMPRESS',      unit: 'HR', unitCost:  26.180, category: 'equip' },
  { code: '8AIRTO60',     desc: '> 60 LB AIR TOOLS',         unit: 'HR', unitCost:   1.840, category: 'equip' },
  { code: '8COMHG250',    desc: 'COMPACTORS, HAND G',        unit: 'HR', unitCost:  12.790, category: 'equip' },
  { code: '8ELGEN008-01', desc: 'ELECTRIC GENERATOR',        unit: 'HR', unitCost:  11.760, category: 'equip' },
  { code: '8HCECL0351F',  desc: 'CAT 336 F EXCAVATOR',       unit: 'HR', unitCost: 235.690, category: 'equip' },
  { code: '8LDRRT0100',   desc: 'JD 210K Loader w/Skip',     unit: 'HR', unitCost:  73.980, category: 'equip' },

  // ===== Labor (Perm Labor column) — burdened rate derived from source report =====
  { code: 'LABR_G3', desc: 'Laborer, General',        unit: 'MH', unitCost: 38.900, burdenedRate:  70.042, category: 'labor' },
  { code: 'OPER_4M', desc: 'Operator, Foreman',       unit: 'MH', unitCost: 76.180, burdenedRate: 114.417, category: 'labor' },
  { code: 'OPER_G3', desc: 'Operator, Group 3',       unit: 'MH', unitCost: 63.950, burdenedRate:  98.641, category: 'labor' },
  { code: 'OPER_G4', desc: 'Operator, Group 4',       unit: 'MH', unitCost: 62.570, burdenedRate:  97.250, category: 'labor' },
  { code: 'OPER_GC', desc: 'Operator, Grade Checker', unit: 'MH', unitCost: 62.570, burdenedRate:  97.250, category: 'labor' },

  // ===== Permanent Materials (Perm Material column) — markup 1.0913 already applied =====
  { code: '2AGBAS20',  desc: 'Class 2 Agg Ba@109.13%',  unit: 'TN', unitCost:    22.000, markup: 1.0913, category: 'material' },
  { code: '2AGBAS30',  desc: 'Class 3 Agg Ba@109.13%',  unit: 'TN', unitCost:    18.000, markup: 1.0913, category: 'material' },
  { code: '2COCRM45',  desc: '4000 psi Concr@109.13%',  unit: 'CY', unitCost:   161.270, markup: 1.0913, category: 'material' },
  { code: '2CORMX07',  desc: '7 Sack Concret@109.13%',  unit: 'CY', unitCost:   220.000, markup: 1.0913, category: 'material' },
  { code: '2DRPVC08',  desc: '8" PVC@109.13%',          unit: 'LF', unitCost:    37.691, markup: 1.0913, category: 'material' },
  { code: '2DRPVC081', desc: '8x8x5 Tee@109.13%',       unit: 'EA', unitCost:   250.000, markup: 1.0913, category: 'material' },
  { code: '2DRPVC082', desc: '8" End Cap@109.13%',      unit: 'EA', unitCost:   100.000, markup: 1.0913, category: 'material' },
  { code: '2DRPVC083', desc: '8" Elbos@109.13%',        unit: 'EA', unitCost:   100.000, markup: 1.0913, category: 'material' },
  { code: '2MIMTL16',  desc: 'Stainless Stee@109.13%',  unit: 'EA', unitCost:  3300.000, markup: 1.0913, category: 'material' },
  { code: '2UPWQV30',  desc: 'Water Quality @109.13%',  unit: 'EA', unitCost: 14194.000, markup: 1.0913, category: 'material' },
  { code: '2UPWQV31',  desc: 'Stainless Stee@109.13%',  unit: 'LS', unitCost: -2731.000, markup: 1.0913, category: 'material' },
  { code: '3ENDD20',   desc: 'Roll Off Dumps@109.13%',  unit: 'EA', unitCost:  2000.000, markup: 1.0913, category: 'material' },
  { code: '5OHDB15',   desc: 'Off Haul AC/PCC Rubble',  unit: 'LD', unitCost:   500.000, markup: 1.0000, category: 'material' },

  // ===== Subcontractor (Sub-Contract column) =====
  { code: '0QC_CONCRETE', desc: 'Concrete Quality Technicia', unit: 'HR', unitCost: 122.000, category: 'subcontract' },
  { code: '0QC_SOILS',    desc: 'Soils Technician',           unit: 'HR', unitCost: 117.000, category: 'subcontract' },
];

// Crew presets — corresponds to the "On-the-Fly / SWPP Crew / etc." line above each activity
const CREWS = [
  { code: 'XXX',    name: 'On-the-Fly' },
  { code: 'FA0005', name: 'SWPP Crew' },
];

// Unit-of-measure options for the bid item / activity quantities
const UNITS = ['LS', 'EA', 'LF', 'CY', 'TN', 'SF', 'LD', 'HR', 'MH'];

// Sample bid item & activities — mirrors the source PDF so users see a working example
const DEMO_ITEM = {
  bidItem: '51505',
  description: 'Seepage Wier Basin',
  unit: 'LS',
  takeoffQuan: 1.000,
  engrQuan: 1.000,
  schedule: '1',
  landItem: '100',
  estimatorInitials: 'JWE',
};

const DEMO_ACTIVITIES = [
  {
    code: '005-4100', desc: 'Demo Pad for Pipe and Conduit',
    quan: 1.00, unit: 'LS', hrsShft: 8.00, cal: '001', wc: '5222',
    crewCode: 'XXX', crewCH: 12.00, prod: 1.5000, prodS: 'S', labPcs: 5.00, eqpPcs: 6.00,
    notes: '',
    resources: [
      { code: '5TRED40',      pcs: 1.00, qty:  8.00 },
      { code: '801-1000115',  pcs: 1.00, qty: 12.00 },
      { code: '802-0137600',  pcs: 1.00, qty: 12.00 },
      { code: '8AIRCP016-02', pcs: 1.00, qty: 12.00 },
      { code: '8AIRTO60',     pcs: 1.00, qty: 12.00 },
      { code: '8HCECL0351F',  pcs: 1.00, qty: 12.00 },
      { code: '8LDRRT0100',   pcs: 1.00, qty: 12.00 },
      { code: 'LABR_G3',      pcs: 2.00, qty: 24.00 },
      { code: 'OPER_4M',      pcs: 1.00, qty: 12.00 },
      { code: 'OPER_G4',      pcs: 2.00, qty: 24.00 },
    ],
  },
  {
    code: '005-4103', desc: 'Excavate for Additional Conduit',
    quan: 120.00, unit: 'LF', hrsShft: 8.00, cal: '001', wc: '5222',
    crewCode: 'XXX', crewCH: 16.00, prod: 2.0000, prodS: 'S', labPcs: 6.00, eqpPcs: 3.00,
    notes: '',
    resources: [
      { code: '5TRED40',     pcs: 1.00, qty:  8.00 },
      { code: '801-1000115', pcs: 1.00, qty: 16.00 },
      { code: '8HCECL0351F', pcs: 1.00, qty: 16.00 },
      { code: '8LDRRT0100',  pcs: 1.00, qty: 16.00 },
      { code: 'LABR_G3',     pcs: 2.00, qty: 32.00 },
      { code: 'OPER_4M',     pcs: 1.00, qty: 16.00 },
      { code: 'OPER_G3',     pcs: 2.00, qty: 32.00 },
      { code: 'OPER_GC',     pcs: 1.00, qty: 16.00 },
    ],
  },
  {
    code: '005-4105', desc: 'Install Additional Piping',
    quan: 50.00, unit: 'LF', hrsShft: 8.00, cal: '001', wc: '5222',
    crewCode: 'XXX', crewCH: 8.00, prod: 1.0000, prodS: 'S', labPcs: 6.00, eqpPcs: 4.00,
    notes: '',
    resources: [
      { code: '801-1000115', pcs: 1.00, qty:  8.00 },
      { code: '801-1000116', pcs: 1.00, qty:  8.00 },
      { code: '8COMHG250',   pcs: 1.00, qty:  8.00 },
      { code: '8LDRRT0100',  pcs: 1.00, qty:  8.00 },
      { code: 'LABR_G3',     pcs: 3.00, qty: 24.00 },
      { code: 'OPER_4M',     pcs: 1.00, qty:  8.00 },
      { code: 'OPER_G4',     pcs: 1.00, qty:  8.00 },
      { code: 'OPER_GC',     pcs: 1.00, qty:  8.00 },
    ],
  },
  {
    code: '005-4106', desc: 'Backfill Electric Trench',
    quan: 120.00, unit: 'LF', hrsShft: 8.00, cal: '001', wc: '5222',
    crewCode: 'XXX', crewCH: 16.00, prod: 2.0000, prodS: 'S', labPcs: 6.00, eqpPcs: 3.50,
    notes: 'Backfill Electrical Trench w/ Red Concrete & CL3',
    resources: [
      { code: '801-1000114',  pcs: 1.00, qty: 16.00 },
      { code: '801-1000116',  pcs: 1.00, qty: 16.00 },
      { code: '805-3000500',  pcs: 0.50, qty:  8.00 },
      { code: '8ELGEN008-01', pcs: 0.50, qty:  8.00 },
      { code: '8LDRRT0100',   pcs: 0.50, qty:  8.00 },
      { code: 'LABR_G3',      pcs: 1.00, qty: 16.00 },
      { code: 'OPER_4M',      pcs: 1.00, qty: 16.00 },
      { code: 'OPER_G3',      pcs: 4.00, qty: 64.00 },
    ],
  },
  {
    code: '005-4170', desc: 'Furnish Backfill for Weir & Trenches',
    quan: 182.00, unit: 'TN', hrsShft: 8.00, cal: '001', wc: '5222',
    crewCode: '', crewCH: 0, prod: 0, prodS: '', labPcs: 0, eqpPcs: 0,
    notes: '',
    resources: [
      { code: '2AGBAS20', pcs: 1.00, qty: 182.00 },
      { code: '2AGBAS30', pcs: 1.00, qty: 182.00 },
      { code: '2CORMX07', pcs: 1.00, qty:  45.00 },
    ],
  },
  {
    code: '005-4198', desc: 'Quality Control',
    quan: 1.00, unit: 'LS', hrsShft: 8.00, cal: '001', wc: '5222',
    crewCode: 'XXX', crewCH: 16.00, prod: 2.0000, prodS: 'S', labPcs: 0, eqpPcs: 0,
    notes: '',
    resources: [
      { code: '0QC_CONCRETE', pcs: 2.00, qty: 32.00 },
      { code: '0QC_SOILS',    pcs: 1.00, qty: 16.00 },
    ],
  },
];
