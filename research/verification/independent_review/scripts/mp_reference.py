"""High-precision port of the reference evaluator in common.js (same grammar), used to
adjudicate the largest app-vs-reference disagreement from a fuzz run.
Usage: python mp_reference.py <summary.json> [<app.html>]   or   python mp_reference.py --expr "<e>" --deg <d>
The angle is taken as its exact binary64 value. Prints the 60-digit value and, given a summary,
the relative error of the app and of the double-precision reference.
"""
import json, re, sys
import mpmath as mp
mp.mp.dps = 60

def evaluate(expr, deg):
    x = mp.mpf(deg) * mp.pi / 180
    s, c = mp.sin(x), mp.cos(x)
    tok = re.findall(r'sin|cos|tan|cot|sec|csc|\d+|[()+*/^-]', expr.lower())
    pos = [0]
    peek = lambda: tok[pos[0]] if pos[0] < len(tok) else None
    def take():
        t = tok[pos[0]]; pos[0] += 1; return t
    fn = {'sin': lambda: s, 'cos': lambda: c, 'tan': lambda: s / c, 'cot': lambda: c / s, 'sec': lambda: 1 / c, 'csc': lambda: 1 / s}
    def atom():
        t = take()
        if t == '(':
            v = total(); take(); return v
        return fn[t]() if t in fn else mp.mpf(int(t))
    def power():
        v = atom()
        if peek() == '^':
            take(); sg = 1
            if peek() in ('-', '+'): sg = -1 if take() == '-' else 1
            v = v ** (sg * int(take()))
        return v
    def unary():
        if peek() == '+': take(); return unary()
        if peek() == '-': take(); return -unary()
        return power()
    def prod():
        v = unary()
        while peek() is not None and (peek() in ('*', '/', '(') or peek() in fn or peek().isdigit()):
            q = peek()
            if q in ('*', '/'):
                take(); w = unary(); v = v / w if q == '/' else v * w
            else:
                v = v * power()
        return v
    def total():
        v = prod()
        while peek() in ('+', '-'):
            q = take(); w = prod(); v = v + w if q == '+' else v - w
        return v
    return total()

if __name__ == '__main__':
    if sys.argv[1] == '--expr':
        e, d = sys.argv[2], float(sys.argv[sys.argv.index('--deg') + 1])
        print(mp.nstr(evaluate(e, d), 30)); sys.exit(0)
    S = json.load(open(sys.argv[1]))
    case = S['maxScaledErrorCase']
    v = evaluate(case['e'], case['deg'])
    scale = max(1, abs(v))
    out = {'expression': case['e'], 'degrees': case['deg'], 'mp60': mp.nstr(v, 25),
           'app_scaled_error': float(abs(mp.mpf(case['app']) - v) / scale),
           'double_reference_scaled_error': float(abs(mp.mpf(case['reference']) - v) / scale)}
    print(json.dumps(out, indent=1))
