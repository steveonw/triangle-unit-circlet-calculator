"""V4.2 display regression. Run: python test_v42_display.py V4_1.html V4_2.html
Requires Node.js and SymPy. The independent AST interpreter accepts the printed
math (including Unicode powers and rational denominators) without Atlas's parser.
"""
import ast,json,random,re,subprocess,sys
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
rng=random.Random(20261126)
old,new=map(Path,sys.argv[1:3])
exprs=[]
for u,v in [('sin','cos'),('cos','sin')]:
 for sign in ['+','-']:
  for k in range(1,9):
   for m in [0,k,max(0,k-1),min(8,k+1)]:
    for p in ['1',f'(2+{u}+{v})']:
     exprs.append(f'({p})*(1{sign}{u})^{k}/({v}^{2*m})')
for _ in range(400):
 u,v=rng.choice([('sin','cos'),('cos','sin')]);a,b,m,n=[rng.randrange(0,6) for i in range(4)]
 exprs.append(f'({rng.choice([-3,-1,1,2,5])})*(1-{u})^{a}*(1+{u})^{b}*(2+{u}-{v})/({u}^{m}*{v}^{n})')
exprs+=['sin+cos','sin-cos','(sin+cos)/2','(1+sin)^2','(1-cos)^3/sin^6','(1-sin)^4/cos^8','(1+sin)^3*cos','(sin^2+cos^2)^2','(1-sin)*(1+sin)','1/sec','(sin+cos)^3','sin^2-tan^2','(1-sin)^2+(1-sin)*cos','(1+cos)^3/2']
exprs=list(dict.fromkeys(exprs))
angles=[0,45,89.999999,90,180,223.7,270,360]
def run(path):
 s=path.read_text();s=s[s.index('const TA=(()=>{'):];s=s[:s.index('\n})();')+6]
 s+='''\nconst fs=require('fs'),data=JSON.parse(fs.readFileSync(0,'utf8'));console.log(JSON.stringify(data.exprs.map(e=>{try{const r=TA.compile(e),q=r.q;return {text:r.text,canonical:r.canonicalText||null,mask:r.mask,sig:TA.sig(q),values:data.angles.map(d=>TA.value(r,d)),sing:[0,90,180,270].map(d=>TA.singularity(r,d))}}catch(e){return {error:e.message}}})));'''
 return json.loads(subprocess.run(['node','-e',s],input=json.dumps(dict(exprs=exprs,angles=angles)),capture_output=True,text=True,check=True).stdout)
oldr,newr=run(old),run(new)
trans=str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹','0123456789')
def tree(src):
 src=re.sub('[⁰¹²³⁴⁵⁶⁷⁸⁹]+',lambda m:'**'+m[0].translate(trans),src)
 return ast.parse(src.replace('−','-').replace('·','*').replace('^','**'),mode='eval').body
def evaluate(node,s,c):
 if isinstance(node,ast.Constant) and isinstance(node.value,int):return F(node.value)
 if isinstance(node,ast.Name):
  if node.id=='sin':return s
  if node.id=='cos':return c
  if node.id=='tan':return s/c
  if node.id=='cot':return c/s
  if node.id=='sec':return 1/c
  if node.id=='csc':return 1/s
 if isinstance(node,ast.UnaryOp):
  x=evaluate(node.operand,s,c);return -x if isinstance(node.op,ast.USub) else x
 if isinstance(node,ast.BinOp):
  a,b=evaluate(node.left,s,c),evaluate(node.right,s,c)
  if isinstance(node.op,ast.Add):return a+b
  if isinstance(node.op,ast.Sub):return a-b
  if isinstance(node.op,ast.Mult):return a*b
  if isinstance(node.op,ast.Div):return a/b
  if isinstance(node.op,ast.Pow):return a**int(b)
 raise ValueError(ast.dump(node))
points=[(F(0),F(1)),(F(1),F(0)),(F(0),F(-1)),(F(-1),F(0))]+[(F(2*t,1+t*t),F(1-t*t,1+t*t)) for t in [F(1,2),F(-2,3),F(2),F(-3),F(1,17),F(16,17),F(-11,19)]]
t=sp.symbols('t');s=2*t/(1+t*t);c=(1-t*t)/(1+t*t)
checked=reject=factored=values=domains=identities=0
for e,a,b in zip(exprs,oldr,newr):
 if 'error' in a:
  assert a==b,(e,a,b);reject+=1;continue
 assert 'error' not in b,(e,b)
 for k in ['mask','sig','values','sing']:assert a[k]==b[k],(e,k,a[k],b[k])
 checked+=1
 if b['canonical']:factored+=1
 T,U=tree(e),tree(b['text'])
 for i,(sv,cv) in enumerate(points):
  try:x=evaluate(T,sv,cv)
  except ZeroDivisionError:continue
  y=evaluate(U,sv,cv)
  assert x==y,(e,b['text'],sv,cv,x,y)
  values+=1
  if i<4:domains+=1
 if b['canonical']:
  # Independent exact proof in rational function field, not sampled arithmetic.
  assert sp.cancel(evaluate(T,s,c)-evaluate(U,s,c))==0,(e,b['text'])
  identities+=1
expected={'(1-cos)^3/sin^6':'1 / (1 + cos)³','(1-sin)^4/cos^8':'1 / (1 + sin)⁴'}
for e,x in expected.items():assert newr[exprs.index(e)]['text']==x
print(f'Generated {len(exprs)} unique cases; accepted {checked}; unchanged bounded rejections {reject}')
print(f'New factored displays: {factored}; exact SymPy rational identities: {identities}')
print(f'Exact display value comparisons: {values}; allowed cardinal comparisons: {domains}')
print('V4.1/V4.2 canonical signature, domain masks, numerical values and singularities identical on all accepted cases.')
print('All display checks PASS')
