(() => {
  'use strict';

  const exprEl = document.getElementById('exprLine');
  const resultEl = document.getElementById('resultLine');
  const statShift = document.getElementById('statShift');
  const statMode = document.getElementById('statMode');

  const state = {
    expr: '',          // raw expression with display tokens
    lastAns: 0,
    angleMode: 'DEG',  // DEG | RAD
    shift: false,
    alpha: false,
    hyp: false,
    sdMode: 'D',       // D = decimal, F = fraction-ish (toggle visual)
    justEvaluated: false,
  };

  // Mapping of display tokens (what user sees in expression) → JS code.
  // Done in two passes so implicit multiplication runs against the
  // user-level token soup, not the post-substitution Math.* identifiers
  // (otherwise "log10(" would get "0(" rewritten to "0*(", and trig
  // substitutions like "sin(" would re-match inside "Math.sin(" forever).
  function normalizeForEval(expr) {
    let s = expr;

    // Pass 1 — operators and constants only (token shape preserved)
    s = s.replace(/×10\^\(/g, '#TENPOW#');
    s = s.replace(/×/g, '*');
    s = s.replace(/÷/g, '/');
    s = s.replace(/−/g, '-');
    s = s.replace(/π/g, '#PI#');
    s = s.replace(/(?<![a-zA-Z#])e(?![a-zA-Z(#])/g, '#E#');
    s = s.replace(/Ans/g, '#ANS#');

    // Powers (note: ⁻¹ is handled AFTER func-token detection so that
    // "sin⁻¹(" is still intact when we look for inverse trig tokens)
    s = s.replace(/²/g, '**2');
    s = s.replace(/³/g, '**3');
    s = s.replace(/\^/g, '**');

    // Pass 2 — implicit multiplication using opaque function placeholders.
    // Replace each function-token "name(" with a unique sentinel "@F<i>@("
    // so "<digit><sentinel>(" can be detected as "needs *" without
    // mistakenly matching digits inside the future Math.* identifier.
    const funcTokens = [
      ['sin⁻¹(', 'asin', 'trig-inv'],
      ['cos⁻¹(', 'acos', 'trig-inv'],
      ['tan⁻¹(', 'atan', 'trig-inv'],
      ['sinh⁻¹(', 'asinh', 'hyp'],
      ['cosh⁻¹(', 'acosh', 'hyp'],
      ['tanh⁻¹(', 'atanh', 'hyp'],
      ['sinh(', 'sinh', 'hyp'],
      ['cosh(', 'cosh', 'hyp'],
      ['tanh(', 'tanh', 'hyp'],
      ['sin(', 'sin',  'trig'],
      ['cos(', 'cos',  'trig'],
      ['tan(', 'tan',  'trig'],
      ['log(', 'log10','plain'],
      ['ln(',  'log',  'plain'],
      ['√(',   'sqrt', 'plain'],
      ['∛(',   'cbrt', 'plain'],
    ];
    const placeholders = []; // [{sentinel, jsfn, kind}]
    funcTokens.forEach(([tok, jsfn, kind], i) => {
      if (s.includes(tok)) {
        const sentinel = `@F${i}@`;
        // Replace token "name(" with "<sentinel>("
        s = s.split(tok).join(sentinel + '(');
        placeholders.push({ sentinel, jsfn, kind });
      }
    });

    // Implicit multiplication on the placeholder-form string:
    //   digit/) followed by ( or by a sentinel or by #PI#/#E#/#ANS#/#TENPOW#
    s = s.replace(/(\d|\))(\s*)(\()/g, '$1*$3');
    s = s.replace(/(\d|\))(\s*)(@F\d+@)/g, '$1*$3');
    s = s.replace(/(\d|\))(\s*)(#PI#|#E#|#ANS#|#TENPOW#)/g, '$1*$3');
    // Also: constant followed by ( implies multiplication
    s = s.replace(/(#PI#|#E#|#ANS#)(\s*)(\()/g, '$1*$3');

    // Pass 3 — substitute placeholders with Math.* equivalents,
    // applying angle-mode wrapping for trig funcs by post-processing
    // the matching argument span.
    for (const { sentinel, jsfn, kind } of placeholders) {
      while (s.includes(sentinel + '(')) {
        const idx = s.indexOf(sentinel + '(');
        const openIdx = idx + sentinel.length;
        const closeIdx = findMatchingParen(s, openIdx);
        if (closeIdx === -1) break;
        const inner = s.slice(openIdx + 1, closeIdx);
        let replacement;
        if (kind === 'trig') {
          replacement = state.angleMode === 'DEG'
            ? `Math.${jsfn}((${inner})*Math.PI/180)`
            : `Math.${jsfn}(${inner})`;
        } else if (kind === 'trig-inv') {
          replacement = state.angleMode === 'DEG'
            ? `(Math.${jsfn}(${inner})*180/Math.PI)`
            : `Math.${jsfn}(${inner})`;
        } else {
          replacement = `Math.${jsfn}(${inner})`;
        }
        s = s.slice(0, idx) + replacement + s.slice(closeIdx + 1);
      }
    }

    // Pass 4 — final placeholder substitutions and remaining ⁻¹ → **(-1)
    s = s.replace(/⁻¹/g, '**(-1)');
    s = s.replace(/#PI#/g, '(Math.PI)');
    s = s.replace(/#E#/g, '(Math.E)');
    s = s.replace(/#ANS#/g, '(' + state.lastAns + ')');
    s = s.replace(/#TENPOW#/g, '*Math.pow(10,');

    return s;
  }

  function findMatchingParen(s, openIdx) {
    let depth = 0;
    for (let i = openIdx; i < s.length; i++) {
      if (s[i] === '(') depth++;
      else if (s[i] === ')') {
        depth--;
        if (depth === 0) return i;
      }
    }
    return -1;
  }

  function render() {
    exprEl.textContent = state.expr || '';
    statShift.textContent = state.angleMode === 'DEG' ? 'D'
      : state.angleMode === 'RAD' ? 'R' : 'G';
    if (state.shift) statShift.textContent = 'S ' + statShift.textContent;
    if (state.alpha) statShift.textContent = 'A ' + statShift.textContent;
    statMode.textContent = 'Math';
    // Auto-scroll expression to right
    exprEl.scrollLeft = exprEl.scrollWidth;
  }

  function setResult(value, isError=false) {
    resultEl.textContent = value;
    resultEl.classList.toggle('error', isError);
  }

  function append(token) {
    if (state.justEvaluated && /[0-9.πe(]/.test(token[0])) {
      state.expr = '';
    }
    state.justEvaluated = false;
    state.expr += token;
    render();
  }

  function backspace() {
    if (!state.expr) return;
    // Try to remove a multi-char token cleanly
    const multiTokens = ['sin⁻¹(', 'cos⁻¹(', 'tan⁻¹(', 'sinh(', 'cosh(', 'tanh(',
                          '×10^(', 'sin(', 'cos(', 'tan(', 'log(', 'ln(', '√(', '∛(', 'Ans'];
    for (const t of multiTokens) {
      if (state.expr.endsWith(t)) {
        state.expr = state.expr.slice(0, -t.length);
        render();
        return;
      }
    }
    state.expr = state.expr.slice(0, -1);
    render();
  }

  function clearAll() {
    state.expr = '';
    state.justEvaluated = false;
    setResult('');
    render();
  }

  function evaluate() {
    if (!state.expr.trim()) return;
    try {
      let normalized = normalizeForEval(state.expr);
      // Auto-close any unclosed parens
      const opens = (normalized.match(/\(/g) || []).length;
      const closes = (normalized.match(/\)/g) || []).length;
      normalized += ')'.repeat(Math.max(0, opens - closes));

      // Evaluate in a restricted scope
      // eslint-disable-next-line no-new-func
      const result = Function('"use strict"; return (' + normalized + ')')();

      if (typeof result !== 'number' || !isFinite(result)) {
        setResult('Math ERROR', true);
        return;
      }
      const formatted = formatNumber(result);
      setResult(formatted);
      state.lastAns = result;
      state.justEvaluated = true;
    } catch (e) {
      setResult('Syntax ERROR', true);
    }
  }

  function formatNumber(n) {
    if (state.sdMode === 'F') {
      const f = toFractionString(n);
      if (f) return f;
    }
    if (Math.abs(n) < 1e-10) return '0';
    const abs = Math.abs(n);
    if (abs >= 1e10 || (abs > 0 && abs < 1e-4)) {
      return n.toExponential(9).replace(/\.?0+e/, 'e');
    }
    // Up to 10 significant digits
    const str = parseFloat(n.toPrecision(10)).toString();
    return str;
  }

  function toFractionString(n) {
    if (!isFinite(n) || Number.isInteger(n)) return null;
    const sign = n < 0 ? -1 : 1;
    n = Math.abs(n);
    const whole = Math.floor(n);
    let frac = n - whole;
    if (frac < 1e-10) return null;
    // Stern–Brocot for best rational up to denominator 10000
    let lo_n = 0, lo_d = 1, hi_n = 1, hi_d = 1;
    let best_n = 1, best_d = 1, best_err = Infinity;
    for (let i = 0; i < 100; i++) {
      const m_n = lo_n + hi_n;
      const m_d = lo_d + hi_d;
      if (m_d > 10000) break;
      const v = m_n / m_d;
      const err = Math.abs(v - frac);
      if (err < best_err) { best_err = err; best_n = m_n; best_d = m_d; }
      if (err < 1e-10) break;
      if (v < frac) { lo_n = m_n; lo_d = m_d; }
      else { hi_n = m_n; hi_d = m_d; }
    }
    if (best_err > 1e-6) return null;
    const num = sign * (whole * best_d + best_n);
    return whole === 0
      ? `${sign === -1 ? '-' : ''}${best_n}/${best_d}`
      : `${sign === -1 ? '-' : ''}${whole}⌐${best_n}/${best_d}`;
  }

  // ---------- Key handler ----------
  function handleKey(key) {
    // Modifier keys
    if (key === 'SHIFT') { state.shift = !state.shift; state.alpha = false; updateShiftLabels(); render(); return; }
    if (key === 'ALPHA') { state.alpha = !state.alpha; state.shift = false; render(); return; }
    if (key === 'MODE') { state.angleMode = state.angleMode === 'DEG' ? 'RAD' : 'DEG'; render(); return; }
    if (key === 'ON') { clearAll(); state.lastAns = 0; return; }
    if (key === 'AC') {
      if (state.shift) { /* OFF */ clearAll(); state.shift = false; updateShiftLabels(); return; }
      clearAll(); return;
    }
    if (key === 'DEL') {
      if (state.shift) { /* INS — not implemented */ state.shift = false; updateShiftLabels(); return; }
      backspace(); return;
    }
    if (key === 'EQ') { evaluate(); state.shift = state.alpha = false; updateShiftLabels(); render(); return; }

    // Digits
    if (/^[0-9]$/.test(key)) {
      if (state.shift && key === '0') { /* Rnd */ append('Math.round('); state.shift = false; updateShiftLabels(); return; }
      append(key); state.shift = state.alpha = false; updateShiftLabels(); return;
    }
    if (key === 'DOT') {
      if (state.shift) { append('Math.random()'); state.shift = false; updateShiftLabels(); return; }
      append('.'); return;
    }

    // Operators
    const opMap = { PLUS: '+', MINUS: '−', MUL: '×', DIV: '÷' };
    if (opMap[key]) { append(opMap[key]); return; }

    if (key === 'NEG') { append('(-'); return; }
    if (key === 'LPAREN') { append('('); return; }
    if (key === 'RPAREN') { append(')'); return; }

    // Functions
    if (key === 'SIN') { append(state.shift ? 'sin⁻¹(' : 'sin('); state.shift = false; updateShiftLabels(); return; }
    if (key === 'COS') { append(state.shift ? 'cos⁻¹(' : 'cos('); state.shift = false; updateShiftLabels(); return; }
    if (key === 'TAN') { append(state.shift ? 'tan⁻¹(' : 'tan('); state.shift = false; updateShiftLabels(); return; }
    if (key === 'LOG') { append(state.shift ? '10^(' : 'log('); state.shift = false; updateShiftLabels(); return; }
    if (key === 'LN')  { append(state.shift ? 'e^(' : 'ln('); state.shift = false; updateShiftLabels(); return; }
    if (key === 'SQRT') { append(state.shift ? '%' : '√('); state.shift = false; updateShiftLabels(); return; }
    if (key === 'SQUARE') { append(state.shift ? '∛(' : '²'); state.shift = false; updateShiftLabels(); return; }
    if (key === 'POW') { append('^('); return; }
    if (key === 'INV') { append('⁻¹'); return; }
    if (key === 'EXP') {
      if (state.shift) { append('π'); state.shift = false; updateShiftLabels(); return; }
      append('×10^('); return;
    }
    if (key === 'ANS') {
      if (state.shift) { state.angleMode = state.angleMode === 'DEG' ? 'RAD' : 'DEG'; state.shift = false; updateShiftLabels(); render(); return; }
      append('Ans'); return;
    }
    if (key === 'SD') { state.sdMode = state.sdMode === 'D' ? 'F' : 'D'; if (state.lastAns) setResult(formatNumber(state.lastAns)); return; }
    if (key === 'HYP') { /* no-op visual */ state.hyp = !state.hyp; return; }
    if (key === 'FRAC') { append('/'); return; }
    if (key === 'LOGAB') { append('log('); return; }
    if (key === 'ENG') { /* no-op */ return; }
    if (key === 'RCL') { /* memory recall — not implemented */ return; }
    if (key === 'MPLUS') { /* memory add — not implemented */ return; }
    if (key === 'CALC') { evaluate(); return; }

    // Cursor keys — ignore for now
    if (['UP', 'DOWN', 'LEFT', 'RIGHT'].includes(key)) return;
  }

  function updateShiftLabels() {
    document.querySelectorAll('.shift-key').forEach(el => {
      el.classList.toggle('shift-active', state.shift);
    });
  }

  // ---------- Wire up button clicks ----------
  document.querySelectorAll('[data-key]').forEach(btn => {
    btn.addEventListener('click', () => handleKey(btn.dataset.key));
  });

  // ---------- Keyboard ----------
  document.addEventListener('keydown', (e) => {
    const k = e.key;
    if (/^[0-9]$/.test(k)) { handleKey(k); return; }
    const map = {
      '+': 'PLUS', '-': 'MINUS', '*': 'MUL', '/': 'DIV',
      '(': 'LPAREN', ')': 'RPAREN', '.': 'DOT',
      'Enter': 'EQ', '=': 'EQ',
      'Backspace': 'DEL', 'Escape': 'AC',
      's': 'SHIFT', 'S': 'SHIFT',
      'a': 'ALPHA', 'A': 'ALPHA',
      '^': 'POW',
    };
    if (map[k]) { e.preventDefault(); handleKey(map[k]); return; }
    if (k === 'p' || k === 'P') { append('π'); return; }
    if (k === 'r' || k === 'R') { append('√('); return; }
  });

  // Initial render
  render();
  setResult('0');
})();
