'use strict';
// Shared helpers for the independent review harnesses.
// The reference evaluator below is written separately from the app's TA engine.
// It mirrors the documented grammar (left-to-right * and /, implicit
// multiplication, one ^ per atom, unary +/-) and applies the literal
// definitions of the six functions with ordinary floating-point arithmetic.
const fs = require('fs');
const crypto = require('crypto');

// Load the inline TA module from a Trig Atlas HTML file without a browser.
// The module starts at "const TA=(()=>{" and ends at the first "\n})();".
function loadEngine(htmlPath) {
  const src = fs.readFileSync(htmlPath, 'utf8');
  const start = src.indexOf('const TA=(()=>{');
  if (start < 0) throw new Error('TA module not found in ' + htmlPath);
  const end = src.indexOf('\n})();', start);
  if (end < 0) throw new Error('End of TA module not found in ' + htmlPath);
  const block = src.slice(start, end + 6);
  const TA = new Function(block + '\nreturn TA;')();
  return { TA, engineSha256: sha256(block), fileSha256: sha256(fs.readFileSync(htmlPath)) };
}

function sha256(data) { return crypto.createHash('sha256').update(data).digest('hex'); }

// Reference evaluator. Returns NaN when the expression as written is undefined
// (any division by an exact zero, or a zero base with a negative power).
// With track=true it instead returns the smallest |divisor| seen, which is used
// to confirm or search for excluded angles away from the axes.
function refEval(expr, s, c, track) {
  let t = expr.toLowerCase(), tok = [], i = 0, m;
  while (i < t.length) {
    if (!t.slice(i).trim()) break;
    m = /^\s*(sin|cos|tan|cot|sec|csc|\d+|[()+*\/^-])/.exec(t.slice(i));
    if (!m) throw new Error('reference tokenizer: ' + expr);
    tok.push(m[1]); i += m[0].length;
  }
  let j = 0, minDiv = Infinity;
  const peek = () => tok[j], take = () => tok[j++], U = NaN;
  const div = (a, b) => {
    if (!Number.isNaN(b)) minDiv = Math.min(minDiv, Math.abs(b));
    return (Number.isNaN(a) || Number.isNaN(b) || b === 0) ? U : a / b;
  };
  const fn = { sin: () => s, cos: () => c, tan: () => div(s, c), cot: () => div(c, s), sec: () => div(1, c), csc: () => div(1, s) };
  function atom() { const x = take(); if (x === '(') { const v = sum(); take(); return v; } if (fn[x]) return fn[x](); return Number(x); }
  function power() {
    const x = atom();
    if (peek() === '^') {
      take(); let sg = 1;
      if (peek() === '-' || peek() === '+') sg = take() === '-' ? -1 : 1;
      const n = sg * Number(take());
      if (Number.isNaN(x)) return U;
      if (n < 0) { minDiv = Math.min(minDiv, Math.abs(x)); return x === 0 ? U : x ** n; }
      return x ** n; // 0^0 = 1 for a defined base, as documented by the app
    }
    return x;
  }
  function unary() { if (peek() === '+') { take(); return unary(); } if (peek() === '-') { take(); return -unary(); } return power(); }
  function prod() {
    let x = unary();
    while (peek() === '*' || peek() === '/' || peek() === '(' || fn[peek()] || /^\d+$/.test(peek() || '')) {
      const q = peek();
      if (q === '*' || q === '/') { take(); const y = unary(); x = q === '/' ? div(x, y) : (Number.isNaN(x) || Number.isNaN(y) ? U : x * y); }
      else { const y = power(); x = (Number.isNaN(x) || Number.isNaN(y)) ? U : x * y; }
    }
    return x;
  }
  function sum() {
    let x = prod();
    while (peek() === '+' || peek() === '-') { const q = take(), y = prod(); x = (Number.isNaN(x) || Number.isNaN(y)) ? U : (q === '+' ? x + y : x - y); }
    return x;
  }
  const v = sum();
  return track ? minDiv : v;
}

// mulberry32: a 32-bit generator using exact integer arithmetic (Math.imul, >>>).
// Seeds are passed explicitly so runs are reproducible.
// NOTE: the first draft of these harnesses used `(state*1103515245+12345)%2**31` on JS numbers.
// That product exceeds 2**53, loses precision, and fell into a cycle of 10,466 draws, so
// "40,000 expressions" contained only a few hundred distinct ones. Do not reintroduce it.
function makeRng(seed) {
  let state = seed >>> 0;
  const rnd = () => {
    state = (state + 0x6D2B79F5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  return { rnd, pick: a => a[Math.floor(rnd() * a.length)] };
}

// Draw expressions until `n` distinct ones are collected (bounded number of attempts).
function distinctExpressions(gen, n, maxAttempts = n * 20) {
  const seen = new Set(); let attempts = 0;
  while (seen.size < n && attempts < maxAttempts) { seen.add(gen()); attempts++; }
  if (seen.size < n) throw new Error(`only ${seen.size} distinct expressions after ${attempts} draws`);
  return { list: [...seen], attempts };
}

const CARDINALS = [[0, 0, 1], [90, 1, 0], [180, 0, -1], [270, -1, 0]];
const FUNCS = ['sin', 'cos', 'tan', 'cot', 'sec', 'csc'];

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) { const k = a.slice(2); out[k] = argv[i + 1]; i++; } else out._.push(a);
  }
  return out;
}

module.exports = { loadEngine, refEval, makeRng, distinctExpressions, CARDINALS, FUNCS, sha256, parseArgs };
