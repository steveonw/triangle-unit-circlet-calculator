"""Independent differential tests for the inline Trig Atlas V4.1 engine.
Requires Python 3, mpmath, sympy, and Node.js. No browser required.
Usage: python test_v41_math.py /path/to/Trig_Atlas_v4_1_Reliability.html
"""
import json, math, random, subprocess, sys
from fractions import Fraction
from pathlib import Path
import mpmath as mp
import sympy as sp
mp.mp.dps=180
rng=random.Random(20261126)
NAMES=['sin','cos','tan','cot','sec','csc']
def leaf(): return ('fn',rng.choice(NAMES)) if rng.random()<.8 else ('int',rng.randint(-7,7))
def monomial():
    a=('fn',rng.choice(NAMES));n=rng.randint(-3,3)
    return ('pow',a,n) if n!=1 else a
def gen(depth):
    if depth==0:return leaf()
    op=rng.choice(['+','-','*','/','pow'])
    if op=='pow':return ('pow',gen(depth-1),rng.randint(0,3))
    return (op,gen(depth-1),monomial() if op=='/' else gen(depth-1))
def src(a):
    op=a[0]
    if op=='fn':return a[1]
    if op=='int':return str(a[1]) if a[1]>=0 else '('+str(a[1])+')'
    if op=='pow':return '('+src(a[1])+')^'+str(a[2])
    return '('+src(a[1])+op+src(a[2])+')'
def val(a,s,c):
    op=a[0]
    if op=='int':return a[1]
    if op=='fn':
        n=a[1]
        if n=='sin':return s
        if n=='cos':return c
        if n=='tan':return s/c
        if n=='cot':return c/s
        if n=='sec':return 1/c
        return 1/s
    x=val(a[1],s,c)
    if op=='pow':return x**a[2]
    y=val(a[2],s,c)
    if op=='+':return x+y
    if op=='-':return x-y
    if op=='*':return x*y
    return x/y
A=[gen(rng.randint(1,4)) for _ in range(1000)]
# Identity-cancellation cases, including restrictions and nested signed powers.
s=('fn','sin');c=('fn','cos'); one=('int',1)
for k in range(1,9):
 for u,v in [(s,c),(c,s)]:
  for sign in ['+','-']:
   A.append(('/',('pow',(sign,one,u),k),('pow',v,2*k)))
for _ in range(200):
 x=gen(2);y=monomial();A.append(('-',('*',x,y),('*',y,x)))
angles=[0,90,180,270,360,.000001,89.999999,90.000001,179.999999,269.999999,270.000001,359.999999,89.99,37,45,135,223.7]
angles += [rng.uniform(-720,720) for _ in range(8)]
requests=[{'expr':src(a),'angles':angles} for a in A]
path=Path(sys.argv[1] if len(sys.argv)>1 else 'Trig_Atlas_v4_1_Reliability.html')
js=path.read_text(); js=js[js.index('const TA=(()=>{'):];js=js[:js.index('\n})();')+6]
js+='''\nconst fs=require('fs'); const input=JSON.parse(fs.readFileSync(0,'utf8'));const res=input.map(({expr,angles})=>{try{let r=TA.compile(expr),q=r.q;return {text:r.text,mask:r.mask,q:{p:[...q.p].map(([k,v])=>[k,v.toString()]),m:q.m,n:q.n,d:q.d.toString()},values:angles.map(d=>TA.value(r,d)),sing:[0,90,180,270].map(d=>TA.singularity(r,d))}}catch(e){return {error:e.message}}});console.log(JSON.stringify(res));'''
resp=json.loads(subprocess.run(['node','-e',js],input=json.dumps(requests),text=True,capture_output=True,check=True).stdout)
exact=card=comp=reject=0;worst=(0,None);bad=[]
rpoints=[(Fraction(3,5),Fraction(4,5)),(Fraction(-5,13),Fraction(12,13)),(Fraction(15,17),Fraction(-8,17)),(Fraction(-20,29),Fraction(-21,29))]
trig={d:(mp.sin(mp.mpf(d)*mp.pi/180),mp.cos(mp.mpf(d)*mp.pi/180)) for d in angles if d%90}
cardinal={0:(Fraction(0),Fraction(1)),90:(Fraction(1),Fraction(0)),180:(Fraction(0),Fraction(-1)),270:(Fraction(-1),Fraction(0)),360:(Fraction(0),Fraction(1))}
for a,r,req in zip(A,resp,requests):
 if 'error' in r:
  reject+=1
  if 'large' not in r['error'] and 'too long' not in r['error'] and 'integer powers' not in r['error']:bad.append((req['expr'],r['error']))
  continue
 q=r['q'];p=[(*map(int,k.split(',')),int(v)) for k,v in q['p']]
 for u,v in rpoints:
  got=sum(w*u**i*v**j for i,j,w in p)/(int(q['d'])*u**q['m']*v**(2*q['n'])) if p else Fraction(0)
  ref=val(a,u,v)
  exact+=1
  if got!=ref:bad.append(('EXACT',req['expr'],got,ref))
 for d,g in zip(angles,r['values']):
  if d in cardinal:
   try:
    ref=val(a,*cardinal[d]);ok=True
   except ZeroDivisionError:ok=False
   card+=1
   if ok != (g is not None):bad.append(('DOMAIN',req['expr'],d,g,ok))
   if ok and abs(float(ref)-g)>1e-10*max(1,abs(float(ref))):bad.append(('CARDINAL VALUE',req['expr'],d,g,float(ref)))
  else:
   ref=val(a,*trig[d]); comp+=1
   if g is None:bad.append(('NONFINITE',req['expr'],d));continue
   e=float(abs(mp.mpf(g)-ref)/max(1,abs(ref)))
   if e>worst[0]:worst=(e,(req['expr'],d,g,mp.nstr(ref,18)))
   if e>2e-10:bad.append(('NUMERIC',req['expr'],d,e))
print(f'Seed 20261126; generated {len(A)} expressions; accepted {len(A)-reject}; bounded rejections {reject}')
print(f'Exact rational comparisons: {exact}; domain/cardinal comparisons: {card}; 180-digit mpmath comparisons: {comp}')
print('Maximum scaled numeric error:',worst)
print('Failures:',len(bad),bad[:5])
assert not bad
# Independent SymPy rational-function limits: use local tangent-half-angle
# substitution directly in the literal AST, not the JavaScript polynomial transform.
t=sp.symbols('t');u=2*t/(1+t*t);v=(1-t*t)/(1+t*t)
count=0
for a,r in zip(A[-232:-200],resp[-232:-200]):
 if 'error' in r:continue
 for k,(S,C) in enumerate([(u,v),(v,-u),(-u,-v),(-v,u)]):
  sg=r['sing'][k]
  if sg is None:continue
  z=sp.cancel(val(a,S,C));num,den=map(lambda z:sp.Poly(z,t),sp.fraction(z));
  if num.is_zero:order=1;limit=0
  else:
   lo=lambda z:min(i[0] for i,v in z.terms() if v)
   i,j=lo(num),lo(den);order=i-j;limit=0 if order>0 else float(num.nth(i)/den.nth(j)) if order==0 else None
  assert (sg['kind']=='pole')==(order<0),(src(a),k,sg,order)
  if order<=0:assert sg['order']==order,(src(a),k,sg,order)
  if order>=0:assert math.isclose(sg['limit'],limit,rel_tol=1e-12,abs_tol=1e-12),(src(a),k,sg,limit)
  count+=1
print('SymPy independent pole/limit checks:',count,'passed')
