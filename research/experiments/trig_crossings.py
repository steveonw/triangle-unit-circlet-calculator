"""Seeded checks of the octahedron crossing construction (NumPy)."""
import itertools as it
import numpy as np
N=100_000
rng=np.random.default_rng(20261126)
V=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],float)
names=['cos','sec','sin','csc','tan','cot']
exp=np.array([[0,1],[0,-1],[1,0],[-1,0],[1,-1],[-1,1]])
E=[(i,j) for i,j in it.combinations(range(6),2) if i//2!=j//2]
D=[(e,f) for e,f in it.combinations(E,2) if not set(e)&set(f)]
S=[(e,f) for e,f in D if np.linalg.norm(np.cross(V[e[1]]-V[e[0]],V[f[1]]-V[f[0]]))>1e-10]
print('Edges, disjoint edge pairs, skew edge pairs:',len(E),len(D),len(S))
n=rng.normal(size=(N,3)); n/=np.linalg.norm(n,axis=1)[:,None]
def orient(i,j,k):return n@np.cross(V[j]-V[i],V[k]-V[i])
count=np.zeros(N,int); all_inverse=True
cross={}
for (i,j),(k,l) in S:
    flags=(orient(i,j,k)*orient(i,j,l)<0)&(orient(k,l,i)*orient(k,l,j)<0)
    count+=flags
    cross[(tuple(sorted((i,j))),tuple(sorted((k,l))))]=flags
    rem=sorted(set(range(6))-{i,j,k,l}); assert tuple(rem) in E
    m1=(V[i]+V[j])/2;m2=(V[k]+V[l])/2;m3=V[rem].mean(axis=0)
    d=m1-m2;d/=np.linalg.norm(d);B=np.eye(3)-np.outer(d,d)
    p=B@m1; m=B@m3
    assert np.allclose(p,B@m2) and np.allclose(m,-2*p) and np.linalg.norm(p)>1e-12
    assert np.array_equal(exp[[i,j,k,l]].sum(axis=0),-exp[rem].sum(axis=0))
for (e,f),flags in cross.items():
    opposite=tuple(sorted((tuple(sorted(i^1 for i in e)),tuple(sorted(i^1 for i in f)))))
    assert np.array_equal(flags,cross[opposite])
print('Midpoint alignment and symbolic complement:',len(S),'of',len(S))
print('Crossings per random view:',dict(zip(*np.unique(count,return_counts=True))))
absolute=np.abs(n); dominant=(2*absolute.max(axis=1)>absolute.sum(axis=1))
print('Dominant coordinate predicts crossing count:',int(np.count_nonzero(count==np.where(dominant,2,6))), 'of', N)
# Independent direct numerical evaluations for the crossing identity.
t=rng.uniform(-np.pi,np.pi,N);t=t[(np.abs(np.sin(t))>.01)&(np.abs(np.cos(t))>.01)];s,c=np.sin(t),np.cos(t)
f=np.stack((c,1/c,s,1/s,s/c,c/s),axis=-1)
err=0.
for e,g in S:
    rem=sorted(set(range(6))-set(e)-set(g))
    u=f[:,list(e)+list(g)].prod(axis=1);v=1/f[:,rem].prod(axis=1)
    err=max(err,np.max(np.abs(u-v)/np.maximum(1,np.abs(v))))
print('Direct numeric comparisons:',len(t)*len(S),'max scaled error',err)
