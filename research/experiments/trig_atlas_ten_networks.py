"""Ten-unit Trig Atlas experiments. Python 3 + NumPy. Seeded and reproducible.
Nodes expose sin/cos; links use explicitly specified operations, not physical contact.
"""
import numpy as np

N=10
rng=np.random.default_rng(20261126)

def edges(name):
    if name=='Chain': return [(i,i+1) for i in range(N-1)]
    if name=='Tree': return [((i-1)//2,i) for i in range(1,N)]
    if name=='Star': return [(0,i) for i in range(1,N)]
    if name=='Ring': return [(i,(i+1)%N) for i in range(N)]
    if name=='Grid': return [(i,i+1) for i in range(N-1) if i%5!=4]+[(i,i+5) for i in range(5)]

names=['Chain','Tree','Star','Ring','Grid']

def graph(name):
    A=np.zeros((N,N))
    for i,j in edges(name): A[i,j]=A[j,i]=1
    return A,np.diag(A.sum(axis=1))-A

# Angle composition, identical random inputs for both reductions.
angles=rng.uniform(-np.pi,np.pi,(100000,N))
z=np.cos(angles)+1j*np.sin(angles)
ref=np.exp(1j*angles.sum(axis=1))
serial=z[:,0].copy()
for j in range(1,N): serial*=z[:,j]
w=z.copy()
while w.shape[1]>1:
    pairs=w.shape[1]//2
    p=w[:,:2*pairs:2]*w[:,1:2*pairs:2]
    w=np.column_stack((p,w[:,-1])) if w.shape[1]%2 else p
print('Angle composition: trials, max complex error, RMS error')
for name,val in [('Serial',serial),('Balanced reduction',w[:,0])]:
    err=np.abs(val-ref)
    print(name,len(err),err.max(),np.sqrt(np.mean(err**2)))

# Parallel Fourier synthesis: ten odd harmonics; numerical RMS against square wave.
t=(np.arange(200000)+.5)*2*np.pi/200000
sq=np.where(t<np.pi,1.,-1.)
print('\nFourier: active units, RMS error, maximum overshoot')
for k in [1,3,5,10]:
    odd=np.arange(1,2*k,2)
    y=(4/np.pi)*(np.sin(t[:,None]*odd)/odd).sum(axis=1)
    print(k,np.sqrt(np.mean((y-sq)**2)),y.max()-1)

# Ring with equally spaced phases: harmonic cancellation. Test random global phases.
phase=rng.uniform(-np.pi,np.pi,100000)[:,None]+2*np.pi*np.arange(N)[None,:]/N
print('\nPhase ring: harmonic, max absolute error from expected complex sum')
for k in [1,2,3,4,5,6,7,8,9,10,11,20]:
    y=np.exp(1j*k*phase).sum(axis=1)
    ref_ring=N*np.exp(1j*k*phase[:,0]) if k%N==0 else 0
    print(k,np.max(np.abs(y-ref_ring)))
print('Ring sum sin^2 range:',(np.sin(phase)**2).sum(1).min(),(np.sin(phase)**2).sum(1).max())

# Same rule for every graph: linear diffusion of unwrapped phase offsets.
# dx/dt = -L x, coupling 1 per edge, mean conserved.
initial=rng.normal(0,.2,(10000,N)); initial-=initial.mean(axis=1,keepdims=True)
initial_norm=np.linalg.norm(initial,axis=1)
print('\nDiffusion: graph, edges, gap, median remaining disagreement at t=5, slowest-mode time to 5%')
for name in names:
    A,L=graph(name)
    eig,V=np.linalg.eigh(L)
    q=initial@V
    y=(q*np.exp(-5*eig))@V.T
    rem=np.linalg.norm(y,axis=1)/initial_norm
    print(name,len(edges(name)),eig[1],np.median(rem),np.log(20)/eig[1],np.max(np.abs(y.mean(axis=1))))

# Nonlinear oscillator feedback: dtheta_i/dt = sum_j sin(theta_j-theta_i).
# Test the same nearly evenly spaced starting phases on each graph.
# Complex mean amplitude R=1 indicates complete phase agreement, R=0 cancellation.
phase0=2*np.pi*np.arange(N)[None,:]/N+rng.normal(0,.05,(256,N))
def evolve(A,theta,t_end=80,dt=.05):
    # Equivalent to sum_j Aij sin(theta_j-theta_i), efficient matrix form.
    def f(x):
        s,c=np.sin(x),np.cos(x)
        return (s@A)*c-(c@A)*s
    x=theta.copy()
    for _ in range(round(t_end/dt)):
        k1=f(x); k2=f(x+dt*k1/2); k3=f(x+dt*k2/2); k4=f(x+dt*k3)
        x+=dt*(k1+2*k2+2*k3+k4)/6
    return x,f(x)
print('\nNonlinear feedback: graph, median R, trials R>0.99, max residual angular velocity')
for name in names:
    A,_=graph(name)
    x,v=evolve(A,phase0)
    R=np.abs(np.exp(1j*x).mean(axis=1))
    print(name,np.median(R),np.count_nonzero(R>.99),np.max(np.abs(v)))
    if name=='Ring':
        step=np.angle(np.exp(1j*(np.roll(x,-1,axis=1)-x)))
        print('Ring winding counts:',np.unique(np.rint(step.sum(1)/(2*np.pi)),return_counts=True),'median step (deg)',np.median(step)*180/np.pi)

# Axis-aligned unit octahedra are translated L1 balls of radius 1.
# They do not overlap iff all pairwise L1 center distances are >=2;
# a distance of 2 along one coordinate axis gives exactly one shared vertex.
centers={
    'Chain': [(2*i,0,0) for i in range(10)],
    'Grid': [(2*(i%5),2*(i//5),0) for i in range(10)],
    'Ring': [(0,0,0),(2,0,0),(4,0,0),(6,0,0),(6,2,0),(6,4,0),(4,4,0),(2,4,0),(0,4,0),(0,2,0)],
}
print('\nPhysical vertex-contact layouts: name, contact count, minimum L1 distance, degree sequence')
for name,pts in centers.items():
    C=np.array(pts)
    d=np.abs(C[:,None,:]-C[None,:,:]).sum(-1)
    contact=(d==2)
    assert np.all(d[np.triu_indices(N,1)]>=2)
    assert set(map(tuple,np.argwhere(np.triu(contact,1))))==set(tuple(sorted(e)) for e in edges(name))
    print(name,int(contact.sum()/2),d[np.triu_indices(N,1)].min(),contact.sum(1).tolist())
