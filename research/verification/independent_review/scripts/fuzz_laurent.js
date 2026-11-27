'use strict';
// Independent fuzz test, first written for V4.1 (products, quotients, sums and
// integer powers; divisors were mostly monomials in V4.1).
// Usage: node fuzz_laurent.js <app.html> [--n 40000] [--seed 20261126] [--out DIR]
// Compares the app's TA engine with the separate reference evaluator in common.js:
//   * at 0/90/180/270 degrees: defined-or-undefined must agree, and values must agree;
//   * at four random generic angles (at least 1 degree from an axis): values must agree.
const fs = require('fs');
const path = require('path');
const { loadEngine, refEval, makeRng, distinctExpressions, CARDINALS, FUNCS, sha256, parseArgs } = require('./common');

const args = parseArgs(process.argv.slice(2));
const html = args._[0];
if (!html) { console.error('usage: node fuzz_laurent.js <app.html> [--n N] [--seed S] [--out DIR]'); process.exit(2); }
const N = Number(args.n || 40000), SEED = Number(args.seed || 20261126);
const { TA, engineSha256, fileSha256 } = loadEngine(html);

// Expression generator (same grammar as the original review run; see README for the RNG correction).
// Only distinct expressions are tested; `drawsNeeded` records how many draws that took.
const g = makeRng(SEED);
function factor(d) { const r = g.rnd(); if (r < 0.6) { let f = g.pick(FUNCS); if (g.rnd() < 0.5) f += '^' + g.pick(['-3', '-2', '-1', '0', '2', '3']); return f; } if (r < 0.75) return String(1 + Math.floor(g.rnd() * 3)); if (d < 2) return '(' + sum(d + 1) + ')' + (g.rnd() < 0.3 ? '^' + g.pick(['2', '3', '-1', '0']) : ''); return g.pick(FUNCS); }
function prod(d) { const n = 1 + Math.floor(g.rnd() * 3); let out = factor(d); for (let k = 1; k < n; k++) out += g.pick([' * ', ' / ', ' ']) + factor(d); return out; }
function sum(d) { const n = 1 + Math.floor(g.rnd() * (d ? 2 : 3)); let out = prod(d); for (let k = 1; k < n; k++) out += g.pick([' + ', ' - ']) + prod(d); return out; }
const { list: exprs, attempts: drawsNeeded } = distinctExpressions(() => sum(0), N);

// Test angles come from a separate stream, so every app version sees the same expressions and angles.
const a = makeRng(SEED + 1);
const S = { app: path.basename(html), fileSha256, engineSha256, seed: SEED, angleSeed: SEED + 1, expressions: N, distinctExpressions: new Set(exprs).size, drawsNeeded, rng: 'mulberry32', expressionListSha256: sha256(exprs.join('\n')),
  accepted: 0, acceptedLaurent: 0, acceptedGeneral: 0, rejected: 0, rejectedByMessage: {},
  cardinalChecks: 0, cardinalValueChecks: 0, genericChecks: 0, maskValueDisagreements: 0,
  maxScaledError: 0, maxScaledErrorCase: null, failures: [] };
const rejected = [];
for (const e of exprs) {
  const angles = Array.from({ length: 4 }, () => Math.round((1 + a.rnd() * 358) * 100) / 100);
  let r;
  try { r = TA.compile(e); } catch (err) { S.rejected++; S.rejectedByMessage[err.message] = (S.rejectedByMessage[err.message] || 0) + 1; rejected.push(err.message + '\t' + e); continue; }
  S.accepted++; if (r.general) S.acceptedGeneral++; else S.acceptedLaurent++;
  for (const [deg, s, c] of CARDINALS) {
    const lit = refEval(e, s, c), v = TA.value(r, deg);
    let appUndefined = Number.isNaN(v);
    if (!r.general) { // V4.1-style results: the two-bit mask is the documented domain; check it agrees with value()
      const maskUndefined = Boolean((r.mask & 1) && s === 0 || (r.mask & 2) && c === 0);
      if (maskUndefined !== appUndefined) S.maskValueDisagreements++;
      appUndefined = maskUndefined;
    }
    S.cardinalChecks++;
    if (Number.isNaN(lit) !== appUndefined) { S.failures.push({ kind: 'cardinal-domain', e, deg, reference: lit, app: v }); continue; }
    if (!appUndefined) { S.cardinalValueChecks++; if (!(Math.abs(v - lit) <= 1e-9 * Math.max(1, Math.abs(lit)))) S.failures.push({ kind: 'cardinal-value', e, deg, reference: lit, app: v }); }
  }
  for (const deg of angles) {
    if (Math.abs(deg % 90) < 1 || Math.abs(deg % 90) > 89) continue;
    const x = deg * Math.PI / 180, lit = refEval(e, Math.sin(x), Math.cos(x));
    if (!Number.isFinite(lit) || Math.abs(lit) >= 1e6) continue;
    const v = TA.value(r, deg), rel = Math.abs(v - lit) / Math.max(1, Math.abs(lit));
    S.genericChecks++;
    if (rel > S.maxScaledError || Number.isNaN(rel)) { if (!Number.isNaN(rel)) { S.maxScaledError = rel; S.maxScaledErrorCase = { e, deg, app: v, reference: lit }; } }
    if (!(rel < 1e-6)) S.failures.push({ kind: 'generic-value', e, deg, reference: lit, app: v });
  }
}
S.failureCount = S.failures.length; S.failures = S.failures.slice(0, 50);
if (args.out) { fs.mkdirSync(args.out, { recursive: true }); fs.writeFileSync(path.join(args.out, 'laurent_summary.json'), JSON.stringify(S, null, 1) + '\n'); fs.writeFileSync(path.join(args.out, 'laurent_rejected.txt'), rejected.join('\n') + (rejected.length ? '\n' : '')); }
console.log(JSON.stringify({ ...S, failures: S.failures.length ? S.failures : [] }, null, 1));
process.exit(S.failureCount ? 1 : 0);
