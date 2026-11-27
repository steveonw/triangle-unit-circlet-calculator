"""Compare the app's values near excluded angles with 50-digit mpmath.
Usage: python near_pole_mpmath.py <app.html> [--out DIR]
Requires Node.js (to run the app's inline TA engine) and mpmath.
The reference is evaluated at the exact binary64 value of the input angle, so the
comparison measures the app's evaluation, not the rounding of the typed decimal angle.
A naive double-precision evaluation is shown for contrast.
"""
import json, math, os, subprocess, sys
from pathlib import Path
import mpmath as mp

mp.mp.dps = 50
HERE = Path(__file__).resolve().parent
html = sys.argv[1]
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None

def f1(s, c): return (1 - s) ** 4 / c ** 8
def f2(s, c): return (1 - c) ** 3 / s ** 6
def f3(s, c): return (1 / c - 1) / (s / c)
CASES = [
    ('(1-sin)^4 / cos^8', f1, [89.99, 89.999, 89.999999, 270.0001]),
    ('(1 - cos)^3 / sin^6', f2, [0.001, 1e-6]),
    ('(sec - 1)/tan', f3, [1e-3, 1e-9]),
]
js = r"""
const {loadEngine}=require(process.argv[1]);const {TA}=loadEngine(process.argv[2]);
const cases=JSON.parse(process.argv[3]);console.log(JSON.stringify(cases.map(([e,d])=>TA.value(TA.compile(e),d))));
"""
pairs = [(e, d) for e, _, ds in CASES for d in ds]
app = json.loads(subprocess.check_output(['node', '-e', js, str(HERE / 'common.js'), html, json.dumps(pairs)], text=True))
rows, worst = [], 0.0
i = 0
for e, f, ds in CASES:
    for d in ds:
        x = mp.mpf(d) * mp.pi / 180  # mp.mpf(float) is the exact binary64 angle
        ref = f(mp.sin(x), mp.cos(x))
        r = math.radians(d)
        naive = f(math.sin(r), math.cos(r))
        rel = abs((mp.mpf(app[i]) - ref) / ref)
        worst = max(worst, float(rel))
        rows.append({'expression': e, 'degrees': d, 'app': app[i], 'mpmath50': mp.nstr(ref, 20), 'relative_error': float(rel), 'naive_double': naive})
        i += 1
for r in rows:
    print(f"{r['expression']:<22} {r['degrees']:<10} app {r['app']!r:<24} mpmath {r['mpmath50']:<26} rel {r['relative_error']:.2e}  naive {r['naive_double']!r}")
print(f'worst relative error {worst:.3e}')
if out:
    os.makedirs(out, exist_ok=True)
    Path(out, 'near_pole_mpmath.json').write_text(json.dumps({'app': Path(html).name, 'rows': rows, 'worst_relative_error': worst}, indent=1) + '\n')
sys.exit(0 if worst < 1e-10 else 1)
