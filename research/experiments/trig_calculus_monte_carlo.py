"""Reproducible Monte Carlo tests of cyclic three-circle geometry. NumPy only."""
import numpy as np
from numpy.polynomial.legendre import leggauss

N=100_000
rng=np.random.default_rng(20261126)
pi=np.pi
I=np.eye(3)
S=np.array([[0.,0.,1.],[1.,0.,0.],[0.,1.,0.]]) # columns: P,Q,R

def m(t):
    return np.cos(t)[...,None,None]*I+np.sin(t)[...,None,None]*S

def f(t):
    s,c=np.sin(t),np.cos(t)
    return np.stack((s,c,s/c,c/s,1/c,1/s),axis=-1)

def prim(t):
    s,c=np.sin(t),np.cos(t)
    return np.stack((-c,s,-np.log(abs(c)),np.log(abs(s)),np.log(abs((1+s)/c)),np.log(abs(s/(1+c)))),axis=-1)

def d2geom(t):
    # Reconstruct sine and cosine from geometric centroid and its velocity.
    H=m(t).sum(axis=(-1,-2))/3/np.sqrt(3)
    K=m(t+pi/2).sum(axis=(-1,-2))/3/np.sqrt(3)
    s,c=np.sqrt(3)/2*(H-K),np.sqrt(3)/2*(H+K)
    return np.stack((-s,-c,2*s/c**3,2*c/s**3,(1+s*s)/c**3,(1+c*c)/s**3),axis=-1)

def scaled(a,b): return abs(a-b)/np.maximum(1,abs(b))
def report(label,e): print(label,'max',float(np.max(e)),'p99',float(np.quantile(e,.99)),'rms',float(np.sqrt(np.mean(e*e))))

t=rng.uniform(0,2*pi,N)
M=m(t); V=m(t+pi/2); A=m(t+pi); J=m(t+3*pi/2)
report('acceleration is inversion',abs(A+M))
report('integral cycle velocity+primitive',abs(J+V))
# Random endpoint integrals: independent Gaussian quadrature on unrestricted vector waves.
a,b=rng.uniform(-2*pi,2*pi,(2,N))
xx,ww=leggauss(32)
q=np.zeros_like(M)
for z,w in zip(xx,ww): q+=w*m((a+b)/2+(b-a)/2*z)
q*=((b-a)/2)[:,None,None]
report('vector integral vs quadrature',abs(q-(m(a+pi/2)-m(b+pi/2))))
# All six scalar functions. Stay inside a single pole-free quadrant; no principal values.
k=rng.integers(0,4,N)
t=k*pi/2+rng.uniform(.02,pi/2-.02,N)
h=np.minimum(.001,.02*np.minimum(t-k*pi/2,(k+1)*pi/2-t))
# Five-point second derivative from standard trig function evaluations.
d2=(-f(t+2*h)+16*f(t+h)-30*f(t)+16*f(t-h)-f(t-2*h))/(12*h[:,None]**2)
e=scaled(d2geom(t),d2)
print('second derivatives each max scaled',e.max(axis=0));report('second derivatives',e)
a=k*pi/2+rng.uniform(.02,pi/2-.02,N);b=k*pi/2+rng.uniform(.02,pi/2-.02,N)
xx,ww=leggauss(64)
q=np.zeros((N,6))
for z,w in zip(xx,ww):q+=w*f((a+b)/2+(b-a)/2*z)
q*=((b-a)/2)[:,None]
e=scaled(prim(b)-prim(a),q)
print('integrals each max scaled',e.max(axis=0));report('six scalar integrals',e)
# Random viewing directions. Orthographic projection expressed as a 3D rank-2 matrix.
t=rng.uniform(0,2*pi,N)
n=rng.normal(size=(N,3));n/=np.linalg.norm(n,axis=1)[:,None]
B=I-n[:,:,None]*n[:,None,:]
U=B;W=B@S
Y=B@m(t)
dot=lambda a,b:np.sum(a*b,axis=(-1,-2))
g=dot(U,W)
condition=np.sqrt((2+abs(g))/(2-abs(g)))
def recover(Y):
    a=dot(U,Y);b=dot(W,Y)
    return (2*a-g*b)/(4-g*g),(2*b-g*a)/(4-g*g)
c,s=recover(Y)
report('screen reconstruction cos/sin',np.maximum(abs(c-np.cos(t)),abs(s-np.sin(t))))
print('projection condition number min max',condition.min(),condition.max())
# Noise per coordinate on screen, projected from 3D isotropic independent noise.
for sigma in [.001,.005,.01,.02]:
    y=Y+sigma*(B@rng.normal(size=Y.shape));c,s=recover(y)
    err=np.angle(np.exp(1j*(np.arctan2(s,c)-t)))*180/pi
    print('noise',sigma,'angle RMS deg',np.sqrt(np.mean(err*err)),'p95 abs',np.quantile(abs(err),.95))
# Every screen coordinate is harmonic: projection and differentiation commute.
report('screen acceleration inversion',abs(B@m(t+pi)+Y))
# Triangle side/area oscillation and integral geometry from position and velocity centroid.
L2=np.sum((m(t)[:,:,0]-m(t)[:,:,1])**2,axis=1)
Lv2=np.sum((m(t+pi/2)[:,:,0]-m(t+pi/2)[:,:,1])**2,axis=1)
report('triangle size complement',abs(L2+Lv2-4))
