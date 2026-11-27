'use strict';
// Independent fuzz test for V4.3+ general rational denominators.
// Usage: node fuzz_rational.js <app.html> [--n 3000] [--seed 20261127] [--out DIR]
// Checks, against the separate reference evaluator in common.js:
//   1. 0/90/180/270 degrees: defined-or-undefined and values agree;
//   2. six random generic angles: values agree (relative/absolute 1e-6, |value| <= 1e5);
//   3. every excluded angle the app reports away from the axes makes some divisor vanish (< 1e-9);
//   4. completeness scan: a 0.05-degree grid looks for divisor zeros the app did not report.
//      A suspected miss is refined by ternary search. If its smallest divisor is < 1e-9 it is
//      flagged, then classified: if the divisor shrinks steadily toward the nearest axis (where
//      the app already excludes the angle) it is recorded as a test artifact; otherwise it is a failure.
// Not meaningful for V4.1/V4.2, which reject non-monomial divisors.
const fs = require('fs');
const path = require('path');
const { loadEngine, refEval, makeRng, distinctExpressions, CARDINALS, FUNCS, sha256, parseArgs } = require('./common');

const args = parseArgs(process.argv.slice(2));
const html = args._[0];
if (!html) { console.error('usage: node fuzz_rational.js <app.html> [--n N] [--seed S] [--out DIR]'); process.exit(2); }
const N = Number(args.n || 3000), SEED = Number(args.seed || 20261127);
const { TA, engineSha256, fileSha256 } = loadEngine(html);

// Expression generator (same grammar as the original review run; see README for the RNG correction; more division and compound divisors).
// Only distinct expressions are tested; `drawsNeeded` records how many draws that took.
const g = makeRng(SEED);
function factor(d) { const r = g.rnd(); if (r < 0.55) { let f = g.pick(FUNCS); if (g.rnd() < 0.4) f += '^' + g.pick(['-2', '-1', '0', '2', '3']); return f; } if (r < 0.7) return String(1 + Math.floor(g.rnd() * 3)); if (d < 2) return '(' + sum(d + 1) + ')' + (g.rnd() < 0.35 ? '^' + g.pick(['2', '-1', '-2', '0']) : ''); return g.pick(FUNCS); }
function prod(d) { const n = 1 + Math.floor(g.rnd() * 3); let out = factor(d); for (let k = 1; k < n; k++) out += g.pick([' * ', ' / ', ' / ', ' ']) + factor(d); return out; }
function sum(d) { const n = 1 + Math.floor(g.rnd() * (d ? 2 : 3)); let out = prod(d); for (let k = 1; k < n; k++) out += g.pick([' + ', ' - ']) + prod(d); return out; }
const { list: exprs, attempts: drawsNeeded } = distinctExpressions(() => sum(0), N);
const a = makeRng(SEED + 1);

const nearAxis = (d, w) => Math.abs(((d + 45) % 90) - 45) < w;
const md = (e, deg) => refEval(e, Math.sin(deg * Math.PI / 180), Math.cos(deg * Math.PI / 180), true);
function classifyFlag(e, at, r) {
  // A divisor that vanishes to high order at an axis angle can stay below 1e-9 for a few degrees.
  // Such a flag is an artifact if (a) the smallest divisor keeps shrinking all the way to the
  // nearest axis angle and (b) the app already excludes that axis angle. A genuinely missed
  // exclusion would instead show a local minimum of the divisor away from the axis.
  const C = Math.round(at / 90) * 90, dist = at - C, axis = (C + 360) % 360;
  const fr = [1, 0.75, 0.5, 0.25, 0.1, 0.02], prof = fr.map(f => md(e, C + dist * f));
  const decays = prof.every((v, i) => i === 0 || v < prof[i - 1]);
  const axisExcluded = Number.isNaN(TA.value(r, axis));
  if (decays && axisExcluded) return { verdict: 'axis-artifact', nearestAxis: axis, profile: prof };
  const h = 0.01, localMin = md(e, at - h) > md(e, at) && md(e, at + h) > md(e, at);
  return { verdict: localMin ? 'possible-missed-exclusion' : 'unexplained', nearestAxis: axis, axisExcluded, profile: prof };
}

// Grid scan for divisor zeros the app did not report. Returns the first flag, or null.
function scanForMissedExclusion(e, r, roots) {
  for (let d = 0.025; d < 360; d += 0.05) {
    if (nearAxis(d, 0.2)) continue;
    if (md(e, d) < 2e-3 && !roots.some(q => Math.abs(q - d) < 0.3)) {
      let lo = d - 0.05, hi = d + 0.05;
      for (let k = 0; k < 80; k++) { const m1 = lo + (hi - lo) / 3, m2 = hi - (hi - lo) / 3; if (md(e, m1) < md(e, m2)) hi = m2; else lo = m1; }
      const at = (lo + hi) / 2;
      if (md(e, at) < 1e-9) return { at, ...classifyFlag(e, at, r) }; // one flag per expression keeps the scan bounded
    }
  }
  return null;
}

// Detector self-test: hide the app's real off-axis exclusions and confirm the scan finds them,
// then confirm it stays quiet when the real exclusions are supplied.
const SELF_TEST = ['1/(2*sin-1)', '1/(3*sin-1)', '(sin-cos)/(sin-cos)', '1/(sin+cos)^2'];
const detectorSelfTest = SELF_TEST.map(e => {
  const r = TA.compile(e), real = r.roots.map(p => p.angle);
  const hidden = scanForMissedExclusion(e, r, []), shown = scanForMissedExclusion(e, r, real);
  return { e, realExclusions: real, caughtWhenHidden: Boolean(hidden && hidden.verdict === 'possible-missed-exclusion'), quietWhenShown: shown === null };
});
if (!detectorSelfTest.every(t => t.caughtWhenHidden && t.quietWhenShown)) { console.error(JSON.stringify(detectorSelfTest, null, 1)); throw new Error('detector self-test failed'); }

const S = { app: path.basename(html), fileSha256, engineSha256, seed: SEED, angleSeed: SEED + 1, expressions: N, distinctExpressions: new Set(exprs).size, drawsNeeded, rng: 'mulberry32', expressionListSha256: sha256(exprs.join('\n')),
  accepted: 0, acceptedGeneral: 0, acceptedLaurent: 0, rejected: 0, rejectedByMessage: {},
  cardinalChecks: 0, cardinalValueChecks: 0, genericChecks: 0, maxScaledError: 0, maxScaledErrorCase: null,
  detectorSelfTest, offAxisExclusionsReported: 0, offAxisExclusionsConfirmed: 0, scanFlags: 0, scanFlagsAxisArtifacts: 0, failures: [] };
const rejected = [], flags = [];
for (const e of exprs) {
  const angles = Array.from({ length: 6 }, () => Math.round((0.5 + a.rnd() * 359) * 1000) / 1000);
  let r;
  try { r = TA.compile(e); } catch (err) { S.rejected++; S.rejectedByMessage[err.message] = (S.rejectedByMessage[err.message] || 0) + 1; rejected.push(err.message + '\t' + e); continue; }
  S.accepted++; if (r.general) S.acceptedGeneral++; else S.acceptedLaurent++;
  const roots = r.general ? r.roots.map(p => p.angle) : [];
  for (const [deg, s, c] of CARDINALS) {
    const lit = refEval(e, s, c), v = TA.value(r, deg); S.cardinalChecks++;
    if (Number.isNaN(lit) !== Number.isNaN(v)) S.failures.push({ kind: 'cardinal-domain', e, deg, reference: lit, app: v });
    else if (!Number.isNaN(lit)) { S.cardinalValueChecks++; if (!(Math.abs(v - lit) <= 1e-9 * Math.max(1, Math.abs(lit)))) S.failures.push({ kind: 'cardinal-value', e, deg, reference: lit, app: v }); }
  }
  for (const deg of angles) {
    if (roots.some(q => Math.abs(q - deg) < 0.05) || nearAxis(deg, 0.05)) continue;
    const x = deg * Math.PI / 180, lit = refEval(e, Math.sin(x), Math.cos(x));
    if (!Number.isFinite(lit) || Math.abs(lit) > 1e5) continue;
    const v = TA.value(r, deg), rel = Math.abs(v - lit) / Math.max(1, Math.abs(lit)); S.genericChecks++;
    if (rel > S.maxScaledError) { S.maxScaledError = rel; S.maxScaledErrorCase = { e, deg, app: v, reference: lit }; }
    if (!(rel < 1e-6)) S.failures.push({ kind: 'generic-value', e, deg, reference: lit, app: v });
  }
  if (!r.general) continue;
  for (const q of roots) {
    if (q % 90 === 0) continue;
    S.offAxisExclusionsReported++;
    const m = md(e, q);
    if (m < 1e-9) S.offAxisExclusionsConfirmed++; else S.failures.push({ kind: 'reported-exclusion-not-confirmed', e, angle: q, smallestDivisor: m });
  }
  const flag = scanForMissedExclusion(e, r, roots);
  if (flag) {
    S.scanFlags++; flags.push({ e, reportedExclusions: roots, ...flag });
    if (flag.verdict === 'axis-artifact') S.scanFlagsAxisArtifacts++; else S.failures.push({ kind: 'possible-missed-exclusion', e, ...flag });
  }
}
S.failureCount = S.failures.length; S.failures = S.failures.slice(0, 50);
if (args.out) {
  fs.mkdirSync(args.out, { recursive: true });
  fs.writeFileSync(path.join(args.out, 'rational_summary.json'), JSON.stringify(S, null, 1) + '\n');
  fs.writeFileSync(path.join(args.out, 'rational_rejected.txt'), rejected.join('\n') + (rejected.length ? '\n' : ''));
  fs.writeFileSync(path.join(args.out, 'rational_scan_flags.json'), JSON.stringify(flags, null, 1) + '\n');
}
console.log(JSON.stringify(S, null, 1));
process.exit(S.failureCount ? 1 : 0);
