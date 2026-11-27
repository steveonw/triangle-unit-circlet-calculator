'use strict';
// V4.3.1 display check: the typeset general-path answer must mean exactly what the user typed.
// Usage: node display_roundtrip.js <app.html> [--n 3000] [--seed 20261128] [--out DIR]
// For every accepted general-path expression whose engine text is the raw input, the page's
// answerText() output is fed back into TA.compile. Required: no ASCII * ^ - left in the display,
// identical excluded angles and kinds, and bit-identical values at eight test angles.
const fs = require('fs');
const path = require('path');
const { loadEngine, makeRng, distinctExpressions, FUNCS, sha256, parseArgs } = require('./common');
const args = parseArgs(process.argv.slice(2));
const html = args._[0];
const N = Number(args.n || 3000), SEED = Number(args.seed || 20261128);
const { TA, fileSha256, engineSha256 } = loadEngine(html);
const src = fs.readFileSync(html, 'utf8');
const a = src.indexOf('function prettyExpression'), b = src.indexOf('function answerText');
if (a < 0 || b < 0) { console.error('No answer formatter in ' + html + ' (expected for versions before V4.3.1)'); process.exit(2); }
const { answerText } = new Function(src.slice(a, src.indexOf('\n', b)) + ';return {answerText};')();

const g = makeRng(SEED);
function factor(d) { const r = g.rnd(); if (r < 0.55) { let f = g.pick(FUNCS); if (g.rnd() < 0.4) f += '^' + g.pick(['-2', '-1', '0', '2', '3']); return f; } if (r < 0.7) return String(1 + Math.floor(g.rnd() * 3)); if (d < 2) return '(' + sum(d + 1) + ')' + (g.rnd() < 0.35 ? '^' + g.pick(['2', '-1', '-2', '0']) : ''); return g.pick(FUNCS); }
function prod(d) { const n = 1 + Math.floor(g.rnd() * 3); let out = factor(d); for (let k = 1; k < n; k++) out += g.pick([' * ', ' / ', ' / ', ' ', '']) + factor(d); return out; }
function sum(d) { const n = 1 + Math.floor(g.rnd() * (d ? 2 : 3)); let out = (g.rnd() < 0.1 ? '-' : '') + prod(d); for (let k = 1; k < n; k++) out += g.pick([' + ', ' - ', '-', '+']) + prod(d); return out; }
const HAND = ['1/(2*sin-1)', 'sin/(1+cos)', '-sin/(1+cos)^2', '(sin^2-cos^2+2)/(sin-cos)', '2 sin cos/(1-tan^2)', '(sin+cos)(sin-cos)/(1+sin)', '-(1-cos)^3/(2+sin)^-2', '1/-sin', 'sin²/(1−cos+2)', '(3*sin-sin*3-3)/(2*sin^2+2*cos^2)'];
const { list, attempts } = distinctExpressions(() => sum(0), N);
const exprs = [...HAND, ...list];
const ANG = [0, 13.7, 45, 90, 121.3, 180, 247.9, 333.3];
const S = { app: path.basename(html), fileSha256, engineSha256, seed: SEED, rng: 'mulberry32', randomExpressions: N, drawsNeeded: attempts, handPicked: HAND.length, expressionListSha256: sha256(exprs.join('\n')),
  generalAccepted: 0, typesetRaw: 0, typesetOther: 0, roundTripChecks: 0, failures: [], examples: [] };
for (const e of exprs) {
  let r; try { r = TA.compile(e); } catch { continue; }
  if (!r.general) continue;
  S.generalAccepted++;
  const shown = answerText(r);
  if (r.text !== String(r.source).trim()) { S.typesetOther++; continue; }
  S.typesetRaw++;
  if (S.examples.length < 12) S.examples.push([e, shown]);
  const bad = m => S.failures.push({ e, shown, problem: m });
  if (/[*^-]/.test(shown)) { bad('ASCII operator left in display'); continue; }
  let q; try { q = TA.compile(shown); } catch (err) { bad('display does not re-parse: ' + err.message); continue; }
  const sig = x => JSON.stringify(x.roots.map(p => [p.angle, p.kind, p.order]));
  if (sig(q) !== sig(r)) { bad('different exclusions after re-parse'); continue; }
  for (const d of ANG) { const v1 = TA.value(r, d), v2 = TA.value(q, d); S.roundTripChecks++; if (!(Object.is(v1, v2) || (Number.isNaN(v1) && Number.isNaN(v2)))) bad(`value differs at ${d}°: ${v1} vs ${v2}`); }
}
S.failureCount = S.failures.length; S.failures = S.failures.slice(0, 50);
if (args.out) { fs.mkdirSync(args.out, { recursive: true }); fs.writeFileSync(path.join(args.out, 'display_roundtrip.json'), JSON.stringify(S, null, 1) + '\n'); }
console.log(JSON.stringify(S, null, 1));
process.exit(S.failureCount ? 1 : 0);
