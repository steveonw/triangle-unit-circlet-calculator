'use strict';
// Hand-written hole/pole cases with mathematically derived expectations.
// Usage: node singularity_cases.js <app.html> [--out DIR]
// "general" cases need V4.3+ (non-monomial divisors); older versions are expected to reject them.
const fs = require('fs');
const path = require('path');
const { loadEngine, parseArgs } = require('./common');
const args = parseArgs(process.argv.slice(2));
const html = args._[0];
const { TA, fileSha256, engineSha256 } = loadEngine(html);
const R2 = Math.SQRT2;
// exclusions: angle -> ['hole', limit] or ['pole', order]. Angles not listed must be defined.
const CASES = [
  ['sin sec cot', { 0: ['hole', 1], 90: ['hole', 1], 180: ['hole', 1], 270: ['hole', 1] }],
  ['sin^2 + cos^2', {}],
  ['sec^2 - tan^2', { 90: ['hole', 1], 270: ['hole', 1] }],
  ['cos / sin^-1', { 0: ['hole', 0], 180: ['hole', 0] }],
  ['1/tan', { 0: ['pole', 1], 90: ['hole', 0], 180: ['pole', 1], 270: ['hole', 0] }],
  ['(1-cos)/sin^2', { 0: ['hole', 0.5], 180: ['pole', 2] }],
  ['(1-sin)^4/cos^8', { 90: ['hole', 1 / 16], 270: ['pole', 8] }],
  ['tan * cos', { 90: ['hole', 1], 270: ['hole', -1] }],
  ['sin^2 * csc^3', { 0: ['pole', 1], 180: ['pole', 1] }],
  ['cot * sin', { 0: ['hole', 1], 180: ['hole', -1] }],
  ['tan^0', { 90: ['hole', 1], 270: ['hole', 1] }],
  ['sin^0', {}],
  ['(1 - cos)^3 / sin^6', { 0: ['hole', 1 / 8], 180: ['pole', 6] }],
  ['csc - cot', { 0: ['hole', 0], 180: ['pole', 1] }],
  ['1/(sin^2+cos^2)', {}, 'general'],
  ['sin/(1+cos)', { 180: ['pole', 1] }, 'general'],
  ['(sin-cos)/(sin-cos)', { 45: ['hole', 1], 225: ['hole', 1] }, 'general'],
  ['1/(2*sin-1)', { 30: ['pole', 1], 150: ['pole', 1] }, 'general'],
  ['(1+cos)/(1-cos)', { 0: ['pole', 2] }, 'general'],
  ['1/(sin+cos)^2', { 135: ['pole', 2], 315: ['pole', 2] }, 'general'],
  ['(sin^2-cos^2)/(sin-cos)', { 45: ['hole', R2], 225: ['hole', -R2] }, 'general'],
];
function exclusions(r) {
  if (r.general) return r.roots.map(p => ({ angle: p.angle, kind: p.kind, order: Math.abs(p.order || 0), limit: p.limit }));
  const out = [];
  for (const d of [0, 90, 180, 270]) { const s = TA.singularity(r, d); if (s) out.push({ angle: d, kind: s.kind, order: Math.abs(s.order), limit: s.limit }); }
  return out;
}
const rows = [], failures = [];
for (const [e, exp, need] of CASES) {
  let r;
  try { r = TA.compile(e); } catch (err) { rows.push({ e, status: need === 'general' ? 'rejected (needs V4.3+)' : 'REJECTED', message: err.message }); if (need !== 'general') failures.push(e + ': rejected'); continue; }
  const got = exclusions(r), problems = [];
  const keys = Object.keys(exp).map(Number);
  for (const k of keys) {
    const x = got.find(p => Math.abs(p.angle - k) < 1e-9);
    if (!x) { problems.push(`${k}°: not excluded`); continue; }
    const [kind, v] = exp[k];
    if (x.kind !== kind) problems.push(`${k}°: ${x.kind}, expected ${kind}`);
    else if (kind === 'hole' && !(Math.abs(x.limit - v) < 1e-12)) problems.push(`${k}°: limit ${x.limit}, expected ${v}`);
    else if (kind === 'pole' && x.order !== v) problems.push(`${k}°: order ${x.order}, expected ${v}`);
  }
  for (const x of got) if (!keys.some(k => Math.abs(x.angle - k) < 1e-9)) problems.push(`${x.angle}°: unexpected exclusion`);
  if (problems.length) failures.push(e + ': ' + problems.join('; '));
  rows.push({ e, status: problems.length ? 'FAIL' : 'pass', path: r.general ? 'general' : 'laurent', display: r.text,
    exclusions: got.map(p => `${+p.angle.toFixed(6)}° ${p.kind}${p.kind === 'hole' ? ' limit ' + p.limit : ' order ' + p.order}`) });
}
const report = { app: path.basename(html), fileSha256, engineSha256, cases: rows.length, failures, rows };
if (args.out) { fs.mkdirSync(args.out, { recursive: true }); fs.writeFileSync(path.join(args.out, 'singularity_cases.json'), JSON.stringify(report, null, 1) + '\n'); }
for (const r of rows) console.log(`${r.status.padEnd(24)} ${r.e.padEnd(26)} ${r.display ? '→ ' + r.display : r.message}  ${r.exclusions ? r.exclusions.join(' | ') : ''}`);
console.log(`${rows.length} cases, ${failures.length} failures`);
process.exit(failures.length ? 1 : 0);
