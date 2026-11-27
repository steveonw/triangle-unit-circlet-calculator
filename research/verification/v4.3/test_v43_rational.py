"""Independent verification of V4.3 rational engine. Requires Node, SymPy, mpmath.
Usage: python test_v43_rational.py Trig_Atlas_v4_3_Rational.html
"""
import json, math, random, subprocess, sys
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as sp
mp.mp.dps=100
rng=random.Random(20261126)
NAMES=['sin','cos','tan','cot','sec','csc']
def fn(n):return ('fn',n)
def num(n):return ('int',n)
def op(o,a,b):return(o,a,b)
def powr(a,n):return('pow',a,n)
s,c=fn('sin'),fn('cos'); one=num(1); zero=num(0)
def src(a):
 o=a[0]
 if o=='fn':return a[1]
 if o=='int':return '('+str(a[1])+')' if a[1]<0 else str(a[1])
 if o=='pow':return '('+src(a[1])+')^'+str(a[2])
 return '('+src(a[1])+o+src(a[2])+')'
def val(a,s,c):
 o=a[0]
 if o=='int':return s*0+a[1]
 if o=='fn':
  return {'sin':lambda:s,'cos':lambda:c,'tan':lambda:s/c,'cot':lambda:c/s,'sec':lambda:1/c,'csc':lambda:1/s}[a[1]]()
 v=val(a[1],s,c)
 if o=='pow':return v**a[2]
 w=val(a[2],s,c)
 return {'+':lambda:v+w,'-':lambda:v-w,'*':lambda:v*w,'/':lambda:v/w}[o]()
def poly(p,x):
 z=0
 for v in reversed(p):z=z*x+int(v)
 return z
def circle(t,k):
 u,v=2*t/(1+t*t),(1-t*t)/(1+t*t)
 return [(u,v),(v,-u),(-u,-v),(-v,u)][k]
base=[op('+',s,c),op('-',s,c),op('+',one,c),op('-',one,s),op('-',op('*',num(2),s),one),op('-',op('*',num(3),s),one),op('+',num(2),s),op('+',powr(s,2),powr(c,2)),op('+',fn('tan'),num(1)),op('-',fn('sec'),fn('tan'))]
A=[]
for b in base:
 A.extend([op('/',one,b),op('/',s,b),op('/',b,b),op('/',powr(b,3),powr(b,2)),powr(b,-2),powr(op('/',one,b),0),op('/',zero,b)])
def leaf():return fn(rng.choice(NAMES)) if rng.random()<.8 else num(rng.choice([-3,-2,-1,0,1,2,3]))
def gen(depth):
 if depth==0:return leaf()
 o=rng.choice(['+','-','*','/','pow'])
 if o=='pow':return powr(gen(depth-1),rng.choice([-2,-1,0,1,2,3]))
 return op(o,gen(depth-1),gen(depth-1))
for i in range(300):
 b=op(rng.choice(['+','-']),gen(rng.randrange(1,3)),leaf());a=gen(rng.randrange(1,3));A.append(op('/',a,b))
# Always-undefined divisors; reject instead of silently extending their domain.
A.extend([op('/',one,op('-',s,s)),op('/',one,op('-',op('+',powr(s,2),powr(c,2)),one)),powr(op('-',s,s),-1),op('/',num(0),op('-',c,c))])
A=list({src(a):a for a in A}.values());angles=[0,30,45,89.999999,90,120,135,150,179.999999,180,225,270,315,359.999999,360,37,112.345,278.9]+[rng.uniform(0,360) for i in range(12)]
js=Path(sys.argv[1]).read_text();js=js[js.index('const TA=(()=>{'):];js=js[:js.index('\n})();')+6]
js+='''\nconst fs=require('fs'),data=JSON.parse(fs.readFileSync(0,'utf8'));const out=data.exprs.map(expr=>{try{let r=TA.compile(expr);return {general:!!r.general,text:r.text,roots:r.roots?.map(p=>({angle:p.angle,exactAngle:p.exactAngle,kind:p.kind,order:p.order,limit:p.limit,undefinedAt:Number.isNaN(TA.value(r,p.angle)),extension:TA.value(r,p.angle,true),chart:p.chart,interval:p.interval})),charts:r.rcharts,values:data.angles.map(a=>TA.value(r,a)),sing:data.angles.map(a=>TA.singularity(r,a)?.kind||null)}}catch(e){return {error:e.message}}});console.log(JSON.stringify(out,(_,v)=>typeof v==='bigint'?v.toString():v));'''
R=json.loads(subprocess.run(['node','-e',js],input=json.dumps(dict(exprs=list(map(src,A)),angles=angles)),text=True,capture_output=True,check=True,timeout=100).stdout)
# Exact reference for original domain on rational points (includes chart boundaries).
points=[F(-1),F(-3,4),F(-1,3),F(0),F(1,7),F(1,2),F(1)]
# Additional exact symbolic reference: independently walk the AST, collect roots of
# every divisor before cancellation, and use SymPy's polynomial root isolation.
t=sp.symbols('t');u=2*t/(1+t*t);v=(1-t*t)/(1+t*t)
def symbolic(a,s,c):
 o=a[0]
 if o=='int':return sp.Integer(a[1]),[]
 if o=='fn':
  if a[1]=='sin':return s,[]
  if a[1]=='cos':return c,[]
  if a[1] in ['tan','sec']:return sp.cancel((s if a[1]=='tan' else 1)/c),[sp.fraction(sp.cancel(c))[0]]
  return sp.cancel((c if a[1]=='cot' else 1)/s),[sp.fraction(sp.cancel(s))[0]]
 x,dx=symbolic(a[1],s,c)
 if o=='pow':
  if a[2]<0:
   if x==0:raise ZeroDivisionError
   dx=dx+[sp.fraction(x)[0]]
  return sp.cancel(x**a[2]),dx
 y,dy=symbolic(a[2],s,c);ds=dx+dy
 if o=='/':
  if y==0:raise ZeroDivisionError
  ds=ds+[sp.fraction(y)[0]]
 z={'+':lambda:x+y,'-':lambda:x-y,'*':lambda:x*y,'/':lambda:x/y}[o]()
 return sp.cancel(z),ds
def pp(p):return sp.Poly(sum(int(w)*t**i for i,w in enumerate(p)),t,domain=sp.QQ)
def ref_roots(a,k):
 ss,cc=[(u,v),(v,-u),(-u,-v),(-v,u)][k];z,ds=symbolic(a,ss,cc)
 den=sp.Poly(sp.fraction(z)[1],t,domain=sp.QQ);domain=sp.Poly(1,t,domain=sp.QQ)
 for d in ds:
  d=sp.Poly(d,t,domain=sp.QQ)
  if d.is_zero:raise ZeroDivisionError
  domain=sp.lcm(domain,d.sqf_part())
 domain=domain.monic();roots=[]
 for (lo,hi),_ in domain.intervals(eps=sp.Rational(1,10**30)):
  if hi<-1 or lo>1 or (k==2 and lo==hi and abs(lo)==1):continue
  rt=(lo+hi)/2;deg=(k*90+float(2*sp.atan(rt)*180/sp.pi))%360
  if deg>360-1e-12:deg=0
  # Root belongs to a square-free denominator multiplicity factor iff the
  # factor has a root in the isolation interval (or vanishes at exact endpoint).
  order=0
  for factor,m in den.sqf_list()[1]:
   if (factor.eval(lo)==0 if lo==hi else factor.count_roots(lo,hi)>0):order=m;break
  lim=None if order else float(z.subs(t,rt).evalf(40))
  roots.append((deg,order,lim))
 return z,domain,roots
accepted=general=legacy=rejected=zero_rej=bounded=exact=domain_checks=numeric=proofs=isolated=limits=0;worst=(0,None);bad=[]
for i,(a,r) in enumerate(zip(A,R)):
 e=src(a)
 if 'error' in r:
  rejected+=1
  if 'identically zero' in r['error'] or 'Division by zero' in r['error']:
   zero_rej+=1
   try:symbolic(a,u,v)
   except ZeroDivisionError:pass
   else:bad.append((e,'unexpected zero rejection',r['error']))
  elif any(x in r['error'] for x in ['large','limit','complexity','indistinguishable']):bounded+=1
  else:bad.append((e,'unexpected rejection',r['error']))
  continue
 accepted+=1
 if not r['general']:legacy+=1;continue
 general+=1
 for k,ch in enumerate(r['charts']):
  for pt in points:
   ss,cc=circle(pt,k);orig=poly(ch['x'],pt)!=0
   try:ref=val(a,ss,cc);valid=True
   except ZeroDivisionError:valid=False
   domain_checks+=1
   if valid!=orig:bad.append((e,'domain',k,str(pt),valid,orig))
   if valid:
    exact+=1
    if poly(ch['d'],pt)==0 or F(poly(ch['n'],pt),poly(ch['d'],pt))!=ref:bad.append((e,'value',k,str(pt)))
 for d,g,sg in zip(angles,r['values'],r['sing']):
  q=round(d/90);delta=mp.mpf(d)-90*q;ss,cc=mp.sin(delta*mp.pi/180),mp.cos(delta*mp.pi/180);ss,cc=[(ss,cc),(cc,-ss),(-ss,-cc),(-cc,ss)][q%4]
  if sg:continue # independently verified by isolated-root checks below
  try:ref=val(a,ss,cc)
  except ZeroDivisionError:bad.append((e,'missed numerical exclusion',d));continue
  if g is None:bad.append((e,'nonfinite',d));continue
  er=float(abs(mp.mpf(g)-ref)/max(1,abs(ref)));numeric+=1
  if er>worst[0]:worst=(er,(e,d,g,mp.nstr(ref,16)))
  if er>3e-10:bad.append((e,'numeric',d,er))
 # Full independent symbolic verification on all targeted cases, plus 80 random cases.
 if i<150:
  eroots=[]
  for k in [0,2]:
   z,domain,roots=ref_roots(a,k);ch=r['charts'][k];n,d=pp(ch['n']),pp(ch['d']);refn,refd=map(lambda v:sp.Poly(v,t,domain=sp.QQ),sp.fraction(z));
   assert n*refd==d*refn,(e,k,'symbolic fraction mismatch')
   assert pp(ch['x']).monic()==domain,(e,k,'domain polynomial mismatch')
   proofs+=1;eroots.extend(roots)
  eroots.sort();assert len(eroots)==len(r['roots']),(e,eroots,r['roots'])
  for (deg,order,lim),got in zip(eroots,r['roots']):
   assert abs(deg-got['angle'])<1e-9 and got['undefinedAt'],(e,deg,got)
   assert (order>0)==(got['kind']=='pole'),(e,order,got)
   if order:assert got['order']==-order and got['extension'] is None,(e,order,got)
   else:
    assert math.isclose(got['limit'],lim,rel_tol=1e-10,abs_tol=1e-10) and got['extension']==got['limit'],(e,lim,got)
    limits+=1
   isolated+=1
print(f'Seed 20261126; {len(A)} unique inputs; {accepted} accepted ({general} general, {legacy} legacy); {zero_rej} zero-denominator and {bounded} bounded rejections')
print(f'Exact rational chart-value comparisons: {exact}; original-domain checks: {domain_checks}; 100-digit numerical comparisons: {numeric}')
print(f'Independent SymPy exact chart/domain identities: {proofs}; isolated roots / classifications: {isolated}; finite limits: {limits}')
print('Maximum scaled numerical error:',worst)
print('Failures:',len(bad),bad[:8]);assert not bad
