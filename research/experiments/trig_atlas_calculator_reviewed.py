#!/usr/bin/env python3
"""Trig Atlas: exact simplifier for products, quotients and integer powers
of the six trig functions at one common angle. No external dependencies.
Use: python trig_atlas_calculator.py 'sin sec cot' --angle 37
     python trig_atlas_calculator.py 'sin^2 / cos' --angle 45
     python trig_atlas_calculator.py --benchmark
"""
import argparse
import math
import random
import re
import statistics
import time
from dataclasses import dataclass

# Each vertex is (exponent of sin, exponent of cos).
# Opposite octahedron vertices have negated coordinates in this algebraic map.
VERTICES = {'sin': (1,0), 'csc': (-1,0), 'cos': (0,1),
            'sec': (0,-1), 'tan': (1,-1), 'cot': (-1,1)}
# Bits for domain constraints: sin != 0, cos != 0.
POLES = {'sin':0, 'cos':0, 'tan':2, 'sec':2, 'cot':1, 'csc':1}
ZEROS = {'sin':1, 'cos':2, 'tan':1, 'cot':2, 'sec':0, 'csc':0}
NAMES = {v:k for k,v in VERTICES.items()}
NAMES[(0,0)] = '1'

@dataclass(frozen=True)
class Formula:
    a: int
    b: int
    domain: int
    def text(self):
        if (self.a,self.b) in NAMES:
            return NAMES[(self.a,self.b)]
        for n,(a,b) in VERTICES.items():
            for k in range(2,max(abs(self.a),abs(self.b))+1):
                if (a*k,b*k)==(self.a,self.b): return f'{n}^{k}'
        if (self.a,self.b)==(1,1): return 'sin*cos (= sin(2x)/2)'
        if (self.a,self.b)==(1,-2): return "sec*tan (= sec')"
        if (self.a,self.b)==(-2,1): return "csc*cot (= -csc')"
        def term(n,k): return n if k==1 else f'{n}^{k}'
        top='*'.join(term(n,k) for n,k in [('sin',self.a),('cos',self.b)] if k>0) or '1'
        bottom='*'.join(term(n,-k) for n,k in [('sin',self.a),('cos',self.b)] if k<0)
        return top if not bottom else f'{top}/({bottom})'
    def restrictions(self):
        return ', '.join(n+'(x) != 0' for n,i in [('sin',1),('cos',2)] if self.domain&i) or 'none'
    def value(self,deg):
        if not math.isfinite(deg): raise ValueError('Angle must be finite')
        # Exact zeros at representable multiples of 90 degrees.
        d=math.remainder(deg,360)
        if d in (0,90,-90,180,-180):
            s,c={0:(0.,1.),90:(1.,0.),-90:(-1.,0.),180:(0.,-1.),-180:(0.,-1.)}[d]
        else:
            r=math.radians(d); s,c=math.sin(r),math.cos(r)
        if self.domain&1 and s==0 or self.domain&2 and c==0:
            raise ValueError('Original expression is undefined at this angle')
        return s**self.a*c**self.b

def parse(expression):
    # Flat product/quotient grammar, left-to-right; parentheses not supported.
    pat=r'\s*(?:(sin|cos|tan|sec|csc|cot)(?:\s*\^\s*([+-]?\d+))?|([*/]))'
    a=b=domain=0; pos=0; op=1; need=True; seen=False; factors=[]
    while pos<len(expression):
        if not expression[pos:].strip(): break
        m=re.match(pat,expression[pos:])
        if not m: raise ValueError('Use trig names, integer powers, * or / (no parentheses)')
        name,exp,symbol=m.groups(); pos+=m.end()
        if symbol:
            if need: raise ValueError('Unexpected operator')
            op=-1 if symbol=='/' else 1; need=True; continue
        if not need: op=1  # implicit multiplication
        raw_exp=int(exp or '1'); k=op*raw_exp; x,y=VERTICES[name]
        if abs(k)>1000: raise ValueError('Exponent too large')
        a+=k*x; b+=k*y; domain|=POLES[name]
        if raw_exp<0 or (op<0 and raw_exp>0): domain|=ZEROS[name]
        factors.append((name,k)); need=False; seen=True
    if need or not seen: raise ValueError('Incomplete expression')
    return Formula(a,b,domain), factors

WORKLOAD=['sin sec','sin sec cot','sin cos tan','cos cot sin sec',
          'sin tan csc sec','csc sec cot','cos tan sec cot',
          'sec csc sin cos','tan cot sec sec','sin sin cos cos',
          'sin^4 csc^3 sec cos','tan^3 cot^2 sec cos']

# Compile equivalent numeric expressions once, outside the timed loops.
# Reference uses standard math.sin/cos/tan calls; cached version shares sin/cos.
DIRECT={'sin':'sin(x)','cos':'cos(x)','tan':'tan(x)','sec':'(1/cos(x))','csc':'(1/sin(x))','cot':'(1/tan(x))'}
CACHED={'sin':'s','cos':'c','tan':'(s/c)','sec':'(1/c)','csc':'(1/s)','cot':'(c/s)'}

def product_code(factors, mapping):
    return '*'.join(mapping[n] if k==1 else f'({mapping[n]})**({k})' for n,k in factors) or '1.0'

def compiled(expr,mode):
    f,factors=parse(expr)
    gl={'sin':math.sin,'cos':math.cos,'tan':math.tan}
    if mode=='direct': return eval('lambda x: '+product_code(factors,DIRECT),gl)
    if mode=='cached':
        exec('def calculate(x):\n    s=sin(x); c=cos(x)\n    return '+product_code(factors,CACHED),gl)
        return gl['calculate']
    a,b=f.a,f.b
    def power(base,k):
        if k==0:return None
        if k==1:return base
        if k==-1:return '(1/'+base+')'
        return f'{base}**({k})'
    # Only evaluate needed trig functions; common sine/cosine use reused locally.
    body='*'.join(t for t in [power('sin(x)',a),power('cos(x)',b)] if t is not None) or '1.0'
    # Use native tangent when the simplified result is exactly tangent or cotangent.
    if (a,b)==(1,-1):body='tan(x)'
    if (a,b)==(-1,1):body='1/tan(x)'
    return eval('lambda x: '+body,gl)

def benchmark(n=240000, repeats=7):
    rng=random.Random(20261126)
    # Same random angles for all three paths. Keep away from poles for timing;
    # separately test exact undefined points through the public calculator.
    angles=[]
    while len(angles)<n:
        x=rng.uniform(-math.pi,math.pi)
        if min(abs(math.sin(x)),abs(math.cos(x)))>.01: angles.append(x)
    funcs={m:[compiled(e,m) for e in WORKLOAD] for m in ['direct','cached','atlas']}
    cases=[(i%len(WORKLOAD),x) for i,x in enumerate(angles)]
    def run(m):
        ff=funcs[m]; total=0.
        for i,x in cases: total+=ff[i](x)
        return total
    times={m:[] for m in funcs}
    for m in funcs: run(m)
    for _ in range(repeats):
        order=list(funcs); rng.shuffle(order)
        for m in order:
            t=time.perf_counter();run(m);times[m].append(time.perf_counter()-t)
    err=max(abs(funcs['direct'][i](x)-funcs['atlas'][i](x))/max(1.,abs(funcs['direct'][i](x))) for i,x in cases)
    # Domain checks at singularities and cancellation: never assign a value to a hole.
    checks=[('sin csc',0,False),('sin sec cot',90,False),('cos sec',90,False),('tan cot',0,False),('sin cos',90,True),('cos cot',90,True),('sin sec',0,True),('sin / sin',180,False),('sec^-1',90,False),('sin^0',0,True),('cos / sin^-1',0,False),('sin / cos^-1',90,False),('cos / sin^0',0,True)]
    passed=0
    for expr,angle,valid in checks:
        try:parse(expr)[0].value(angle);actual=True
        except ValueError:actual=False
        assert actual==valid,(expr,angle,actual,valid)
        passed+=1
    med={m:statistics.median(t) for m,t in times.items()}
    print(f'{n:,} evaluations, {len(WORKLOAD)} expressions, {repeats} timed repetitions; seed 20261126')
    for m in funcs:print(f'{m}: median {med[m]*1000:.3f} ms; range {min(times[m])*1000:.3f}-{max(times[m])*1000:.3f} ms')
    print(f'Speedup vs direct: {med["direct"]/med["atlas"]:.3f}x; vs cached: {med["cached"]/med["atlas"]:.3f}x')
    print(f'Max scaled error: {err:.3g}; domain checks: {passed}/{len(checks)}')
    for e in WORKLOAD:print(e,'->',parse(e)[0].text())

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('expression',nargs='?');p.add_argument('--angle',type=float,help='degrees');p.add_argument('--benchmark',action='store_true');args=p.parse_args()
    if args.benchmark:benchmark()
    elif args.expression:
        try:
            f,_=parse(args.expression);print('Simplified:',f.text());print('Original domain:',f.restrictions())
            if args.angle is not None:print('Value:',f.value(args.angle))
        except (ValueError,OverflowError) as e:p.error(str(e))
    else:p.print_help()
