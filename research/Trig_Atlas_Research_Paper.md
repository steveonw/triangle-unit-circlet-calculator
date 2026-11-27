# Trig Atlas: An Octahedral Visual Calculator for Trigonometry, Calculus, and Modular Mathematical Networks

**Exploratory research paper • 26 November 2026**  
Concept initiated by the original investigator; mathematical development and computational experiments assisted by AI. Prepared for independent technical review. Not peer reviewed.

## Abstract

This paper proposes Trig Atlas, a spatial mathematical interface based on labeling the six vertices of a regular octahedron with the six elementary trigonometric functions. Opposite vertices encode reciprocals; edges, triangular faces, and projected intersections encode products, identities, derivatives, and selected limits. Three orthogonal unit circles, synchronized in a cyclic orientation, generate a moving equilateral triangle and its derivative triangle. Their side lengths, centroid positions, and orthographic projections provide exact relationships for double-angle identities, harmonic motion, numerical reconstruction, and integration of sinusoidal coordinates. A complementary algebraic implementation represents each function by two integer exponents and domain constraints. In a reproducible Python benchmark of 240,000 precompiled evaluations, this representation was approximately 2.17 times faster than direct evaluation and 1.79 times faster than a baseline caching sine and cosine. Finally, ten-unit networks illustrate angle composition, Fourier synthesis, harmonic selection, and phase synchronization. The underlying mathematics is largely established; the proposed contribution is the unified three-dimensional representation and modular interface. The paper distinguishes exact results, computational observations, and hypotheses requiring independent validation.

**Keywords:** trigonometry; octahedron; visual symbolic calculator; reciprocal identities; orthographic projection; cyclic symmetry; analog computation; Fourier synthesis; coupled oscillators; mathematics education.

## 1. Motivation and scope

The investigation began with a simple question: could the six trigonometric functions be arranged on a six-vertex solid so that mathematical relationships become visible rather than memorized individually? A regular octahedron offers six vertices, twelve edges, eight triangular faces, and three mutually perpendicular interior diameters. Looking through a transparent model also exposes projected intersections of edges that do not meet in three-dimensional space. The original intuition was to use these features as a quick “eye calculator” for recognizing formulas. The investigation then added two, and subsequently three, unit circles, examined calculus, and connected multiple copies into networks.

Three layers should be distinguished. The **symbolic layer** uses labels and rules to simplify expressions; the **continuous geometric layer** uses moving points to generate numerical measurements; the **network layer** adds explicit operations between modules. The physical shape alone does not evaluate arbitrary functions or implement feedback. Each computational operation requires a mathematical rule, software, or a physical mechanism.

The goal is to test whether this unified representation offers educational, computational, or instrumentation advantages, rather than to claim a new trigonometric identity or a novel computing principle.

## 2. Related work and originality

The trigonometric identity hexagon is a close precedent. McCulley described circular and hyperbolic function mnemonics in 1957 [1]; Cook reproduces the diagrams and discusses their earlier provenance [2]. An instructional handout [3] explicitly presents unity triples, reciprocal diagonals, and adjacent products. Three mutually orthogonal great circles defining an inscribed octahedron are also standard geometry, as illustrated by a 2003 University of Washington laboratory exercise [4]. Basic unit-circle definitions and identities are standard textbook material [5]. Harmonic synthesis, complex rotation composition, and coupled phase-oscillator networks likewise have established mathematical foundations; twisted states on rings were studied by Wiley, Strogatz, and Girvan [6].

The six-function labeling is closely related to the hexagon: projecting the octahedron orthogonally along the normal of either unity face produces the familiar six-point arrangement. The present proposal emphasizes depth, all eight triangular faces, view-dependent crossings, synchronized moving points, and a common interface for calculus and linked networks. A targeted preliminary literature search identified precedents for these components, but did not establish whether this exact combined interface has previously been published. A systematic literature and patent search is required before any priority or novelty claim.

## 3. Static octahedral algebra

### 3.1 Coordinates, labels, and domain

Let $s=\sin\theta$, $c=\cos\theta$; angles are in radians for differentiation and integration. Use the unit octahedron $O=\{(x,y,z): |x|+|y|+|z|\leq1\}$. Its vertices are labeled as follows, matching the interactive prototype. The coordinate positions are symbolic labels, not the numerical values of the functions.

| Vertex position | Function | Exponent address $(a,b)$ | Undefined when |
|---|---|---|---|
| $(1,0,0)$ | cos | $(0,1)$ | Never |
| $(-1,0,0)$ | sec | $(0,-1)$ | $c=0$ |
| $(0,1,0)$ | sin | $(1,0)$ | Never |
| $(0,-1,0)$ | csc | $(-1,0)$ | $s=0$ |
| $(0,0,1)$ | tan | $(1,-1)$ | $c=0$ |
| $(0,0,-1)$ | cot | $(-1,1)$ | $s=0$ |

Every address represents the monomial $s^a c^b$. The common domain of all six functions is $D=\{\theta:s c\neq0\}$. Unless a broader original domain is explicitly preserved, the product identities below hold on $D$.

### 3.2 Three diameters and twelve edges

The interior diameters connect reciprocal pairs: $\sin\theta\csc\theta=1$, $\cos\theta\sec\theta=1$, and $\tan\theta\cot\theta=1$. Multiplication of two adjacent labels gives the following complete edge table (the common argument $\theta$ is omitted).

| Edge | Product | Additional connection |
|---|---|---|
| sin – sec | tan | Quotient identity |
| sin – cot | cos | Quotient identity |
| sec – cot | csc | Quotient identity |
| csc – cos | cot | Quotient identity |
| csc – tan | sec | Quotient identity |
| cos – tan | sin | Quotient identity |
| sin – cos | $\tfrac12\sin 2\theta$ | $\sin^2+\cos^2=1$ |
| tan – sec | $\sec'$ | $1+\tan^2=\sec^2$ |
| cot – csc | $-\csc'$ | $1+\cot^2=\csc^2$ |
| sin – tan | $\sec-\cos$ | $s^2/c$ |
| cos – cot | $\csc-\sin$ | $c^2/s$ |
| sec – csc | $\tan+\cot$ | $1/(sc)$ |

### 3.3 Eight faces and opposite-face symmetry

Each triangular face contains one function from each reciprocal pair. Consequently, antipodal face products are reciprocals. Two faces have product one, while the six remaining face products are squares of individual trigonometric functions.

| Face | Product | Opposite face | Product |
|---|---|---|---|
| sin, sec, cot | $1$ | csc, cos, tan | $1$ |
| sin, cos, tan | $\sin^2$ | csc, sec, cot | $\csc^2$ |
| sin, cos, cot | $\cos^2$ | csc, sec, tan | $\sec^2$ |
| sin, sec, tan | $\tan^2$ | csc, cos, cot | $\cot^2$ |

Proof: substitute the exponent addresses and add them. For example, the first face has sum $(1,0)+(0,-1)+(-1,1)=(0,0)$. The second face has sum $(1,0)+(0,1)+(1,-1)=(2,0)$. Reversing every vertex negates the sum. The two faces with products $\sec^2$ and $\csc^2$ encode $\tan'$ and $-\cot'$, respectively. The familiar Pythagorean identities require addition, not exponent addition alone.

### 3.4 The eye calculator and algebraic engine

A product, quotient, or integer power of same-angle functions can be normalized to $(a,b,\mathcal D)$: two integer exponents and the original domain constraints. Multiplication adds the addresses; division subtracts them; a power multiplies both by the exponent. Opposite addresses cancel. A zero address means the expression is 1 wherever the original expression is defined. The address space is two-dimensional even though its visual interface is three-dimensional. It is a lattice of Laurent monomials, not a new number system.

For example, $\sin\theta\sec\theta\cot\theta\cos\theta\tan\theta$ collapses to $\sin\theta$ on its original domain: the unity face removes three factors and the remaining edge reduces to sine. The visual operations correspond to exact, implementable algebra. The reduction does not make an originally undefined expression defined; $\sin\theta\csc\theta$ is still undefined at $\theta=n\pi$.

The representation also gives the derivative of a general monomial on $D$:

$$\frac{d}{d\theta}(s^a c^b)=s^a c^b(a\cot\theta-b\tan\theta).$$

This extends differentiation to products and powers, but the resulting sum needs a richer representation than one address. General additions, unrelated arguments, transcendental functions, and arbitrary symbolic integrations are outside the present calculator's grammar.

## 4. Looking through the octahedron: projected crossing rules

A transparent model lets two disjoint edges appear to cross as the observer changes view. There are 30 unordered disjoint edge pairs: six antipodal parallel pairs and 24 skew pairs. The latter can be projected to genuine interior screen intersections. A screen intersection is not a physical intersection.

Let the crossed edges contain four distinct labels $A,B,C,D$, with remaining labels $E,F$. Since the product of all six labels is 1 on $D$ (the domain),

$$ (AB)(CD)=\frac{1}{EF}. $$

Here the letters denote function values, not spatial coordinates. For any skew-edge pair the unused two vertices form a third edge. Example: $(\cos\theta\cot\theta)(\sin\theta\sec\theta)=\cos\theta$; the unused edge $\csc\theta\tan\theta=\sec\theta$ is reciprocal. Another crossing simplifies $\sin\theta\tan\theta\csc\theta\sec\theta$ to $\sec\theta\tan\theta=\sec'(\theta)$. Inversion through the center maps a crossing to one with reciprocal product. The rule arises from vertex selection, not from the numerical position of the crossing.

### 4.1 A precise midpoint alignment

Let $m_1,m_2$ be the midpoints of two skew edges, and $m_3$ the midpoint of the remaining edge. The sum of all six vertex coordinates is zero, so $m_1+m_2+m_3=0$. Let $B$ be orthogonal projection onto a plane perpendicular to $m_1-m_2$. Then $Bm_1=Bm_2=p$ and $Bm_3=-2p$. The crossing of the projected midpoints, origin, and remaining-edge midpoint are collinear, with distances $|p|:|Bm_3|=1:2$. This is exact in the specified view and was checked for all 24 skew pairs. Generic views need not cross at the midpoints.

### 4.2 Limits and singularities

For the first crossing example, as $\theta\to0^+$, the factor $\cos\theta\cot\theta$ tends to positive infinity and $\sin\theta\sec\theta$ tends to zero. Their product simplifies to $\cos\theta$, hence the limit is 1, while the original expression remains undefined at zero. The octahedron offers a visual cancellation cue for this particular $0\cdot\infty$ form. Looking along the cos–sec axis also exposes the sin/tan zero pair and csc/cot pole pair at $\theta=n\pi$; looking along the sin–csc axis exposes cos/cot zeros and sec/tan poles at $\theta=\pi/2+n\pi$. Arbitrary apparent intersections are not automatic proofs of identities or asymptotes.

### 4.3 Random-view experiment

A seeded simulation drew 100,000 unit viewing directions uniformly on the sphere by normalizing independent Gaussian coordinates. Strict projected segment-intersection tests counted only crossings of disjoint, nonparallel edges, excluding vertex contacts and degeneracies.

| Crossings per view | Count | Fraction |
|---|---:|---:|
| 2 | 65,097 | 65.097% |
| 6 | 34,903 | 34.903% |

Every tested view matched the following additional empirical criterion: two crossings if the largest absolute viewing-direction coordinate exceeds the sum of the other two, and six otherwise. A complete analytic classification, including degenerate orientations, remains an open proof exercise. Antipodal crossing flags matched for every sampled view. The symbolic complement rule and midpoint alignment were checked for all 24 pairs; 2,370,720 direct product comparisons away from poles gave maximum scaled error $6.34\times10^{-16}$.

## 5. Three synchronized unit circles and moving triangles

Three orthogonal unit circles pass through the six octahedral vertices. A particular cyclic synchronization gives moving points

$$P=(c,s,0),\quad Q=(0,c,s),\quad R=(s,0,c).$$

Each lies on its corresponding XY, YZ, or XZ circle. Cyclic permutation of coordinates is a 120-degree rotation about the direction $(1,1,1)$. Thus it sends $P$ to $Q$, $Q$ to $R$, and $R$ to $P$. The three points form an equilateral triangle for every $\theta$. This does not hold for arbitrary independent circle phases.

For each point $\|P\|=1$, and each pair has dot product $sc$. Therefore the common side length $L$, triangle area $A$, and signed centroid distance $h$ along the unit body diagonal satisfy

$$ L^2=2-2sc=2-\sin(2\theta),\qquad A=\frac{\sqrt3}{4}L^2. $$

$$ h=\frac{s+c}{\sqrt3},\qquad x+y+z=s+c. $$

The triangle lies in a plane parallel to a face of the octahedron. Its side ranges from 1 to $\sqrt3$. At $\theta=0,\pi/2,\pi,3\pi/2$, the moving points coincide with octahedral vertices; at $\theta=\pi/4$ and $5\pi/4$ the triangle is smallest; at $3\pi/4$ and $7\pi/4$ it is largest and its plane passes through the origin. The measurement $2-L^2$ gives $\sin(2\theta)$, but the side length alone cannot distinguish all angles.

### 5.1 Derivative triangle and invariants

The velocity points are $P'=(-s,c,0)$, $Q'=(0,-s,c)$, and $R'=(c,0,-s)$. They form a second equilateral triangle when treated as vectors from a common origin. Let $L_v$ be its side length and $h_v$ its signed centroid distance. Then

$$ L_v^2=2+\sin(2\theta),\qquad h_v=\frac{c-s}{\sqrt3}. $$

$$\boxed{L^2+L_v^2=4,\qquad A+A_v=\sqrt3,\qquad h^2+h_v^2=\frac23.}$$

The first two invariants are complementary size oscillations; the last gives a circle in the two-measurement space. Solving the centroid equations yields $s=\tfrac{\sqrt3}{2}(h-h_v)$ and $c=\tfrac{\sqrt3}{2}(h+h_v)$. Consequently all six functions can be reconstructed from these two signed measurements by the ordinary quotient and reciprocal definitions. This is a measurement scheme, not an independent way of generating trigonometry without a rotating angle input.

### 5.2 Calculus as rotation and endpoint difference

For any of the three position vectors $U$, differentiation with respect to angle gives a quarter-turn within its plane: $U'(\theta)=U(\theta+\pi/2)$. Thus $U''=-U$, $U'''=-U'$, and $U^{(4)}=U$. Inversion through the origin represents the second derivative, and an antiderivative of $U$ is $-U'$ plus a constant vector. The exact definite integral is

$$\int_a^b U(\theta)\,d\theta=U'(a)-U'(b).$$

This is a direct geometric illustration of the Fundamental Theorem of Calculus for sinusoidal coordinates. It also holds for the centroids and any fixed linear projection. If the angle is a time-dependent variable, time differentiation requires the chain rule; the simple quarter-turn is specifically a derivative with respect to the angle (or unit angular speed).

For completeness, the six scalar calculus formulas are:

| $f$ | $f'$ | $f''$ | Antiderivative (plus $C$) |
|---|---|---|---|
| $\sin$ | $\cos$ | $-\sin$ | $-\cos$ |
| $\cos$ | $-\sin$ | $-\cos$ | $\sin$ |
| $\tan$ | $\sec^2$ | $2\tan\sec^2$ | $-\ln\lvert\cos\rvert$ |
| $\cot$ | $-\csc^2$ | $2\cot\csc^2$ | $\ln\lvert\sin\rvert$ |
| $\sec$ | $\sec\tan$ | $\sec(1+2\tan^2)$ | $\ln\lvert\sec+\tan\rvert$ |
| $\csc$ | $-\csc\cot$ | $\csc(1+2\cot^2)$ | $\ln\lvert\csc-\cot\rvert$ |

The logarithmic antiderivatives are valid on individual pole-free intervals; crossing a pole is not an ordinary finite definite integral. Only the sinusoidal coordinates have the four-stage linear rotation cycle. The other functions require nonlinear operations.

## 6. Recovering angles from arbitrary calibrated views

An especially useful consequence of the three-circle system is redundant angle encoding. Define $S$ as the cyclic permutation matrix satisfying $S e_x=e_y$, $S e_y=e_z$, $S e_z=e_x$. The matrix whose columns are $P,Q,R$ is $M(\theta)=cI+sS$. Let $n$ be a unit viewing direction and $B=I-nn^T$ the orthographic projection onto the screen plane. Then the three labeled projected points form

$$Y=BM=cB+sBS.$$

Every individual screen coordinate is of the form $\alpha\cos\theta+\beta\sin\theta$. A single coordinate may lose information at some views. The three labeled points together do not: fit $c$ and $s$ using the Frobenius inner product. Put $g=\langle B,BS\rangle_F$, $u=\langle B,Y\rangle_F$, and $v=\langle BS,Y\rangle_F$. Because $\|B\|_F^2=\|BS\|_F^2=2$,

$$\begin{pmatrix}2&g\\g&2\end{pmatrix}\begin{pmatrix}c\\s\end{pmatrix}=\begin{pmatrix}u\\v\end{pmatrix}.$$

Since $g=-n^TSn$ and the symmetric part of $S$ has eigenvalues $1,-1/2,-1/2$, we have $-1\leq g\leq1/2$. The determinant $4-g^2$ is at least 3, so this system is invertible for every viewing direction. The least-squares design matrix has condition number at most $\sqrt3$. The explicit reconstruction is

$$c=\frac{2u-gv}{4-g^2},\qquad s=\frac{2v-gu}{4-g^2},\qquad \theta=\operatorname{atan2}(s,c)\pmod{2\pi}.$$

The theorem assumes labeled points, known center, scale, and screen orientation, orthographic projection, and ideal synchronized geometry. It does not apply unchanged to an uncalibrated perspective photograph, occluded markers, or unknown scale. It demonstrates that the redundancy of the three circles offers a well-conditioned measurement method under the stated assumptions.

## 7. Computational experiments and reproducibility

All numerical tests below are from Python code with fixed random seed 20261126. Experiments were rerun during preparation of this paper using Python 3.13.5 and NumPy 2.3.5 on a Linux environment. Maximum scaled error is $|\hat y-y|/\max(1,|y|)$ unless otherwise stated. The identities in Sections 3–6 follow analytically; simulation verifies implementations, illustrates frequencies, or evaluates performance under a specified model.

### 7.1 Geometry, derivatives, integrals, and angle readout

| Experiment | Number of trials or comparisons | Maximum error |
|---|---:|---:|
| Second derivative, six scalar functions vs five-point finite differences | 600,000 | $6.42\times10^{-7}$ scaled |
| Six definite integrals vs 64-point Gauss–Legendre quadrature | 600,000 | $3.12\times10^{-13}$ scaled |
| Vector integral vs 32-point quadrature | 100,000 angle intervals | $1.28\times10^{-14}$ absolute per component |
| Projected sine/cosine reconstruction | 100,000 random angles and views | $4.45\times10^{-16}$ absolute |
| Complementary squared triangle sides | 100,000 | $1.78\times10^{-15}$ absolute |

Scalar derivative and integral samples remained at least 0.02 radians inside a selected quadrant to avoid poles. These comparisons measure numerical implementation accuracy, not novelty or proof. A separate noise simulation added independent isotropic Gaussian coordinate errors projected onto the screen, with standard deviation relative to unit radius. Angle errors are wrapped to the interval $(-\pi,\pi]$.

| Screen coordinate noise (standard deviation) | RMS angle error | 95th percentile absolute error |
|---|---:|---:|
| 0.1% | 0.0418° | 0.0819° |
| 0.5% | 0.2083° | 0.4092° |
| 1% | 0.4161° | 0.8171° |
| 2% | 0.8341° | 1.6391° |

Near poles, the derived quotient/reciprocal functions can be much more sensitive than the reconstructed angle itself. These noise results describe a calibrated mathematical measurement model, not a tested physical instrument.

### 7.2 Symbolic calculation benchmark

A prototype parser compiles flat same-angle products, quotients, and integer powers to exponent addresses and preserves the original function-domain restrictions. A 12-expression workload included unity triples, products that reduce to sine, derivative products, and powers. Each method was evaluated 240,000 times at random angles with $|s|,|c|>0.01$, seven timed repetitions, with randomized ordering. The direct baseline evaluates each trig factor; the cached baseline evaluates sine and cosine once for each expression; the Atlas path evaluates only the simplified result. Parsing and compilation, domain-checking overhead in the timed inner loops, and rendering are excluded equally or are outside the benchmark.

| Method | Median execution time | Speedup relative to method |
|---|---:|---:|
| Direct standard-library functions | 47.161 ms | 2.17× |
| Cached sine and cosine | 38.910 ms | 1.79× |
| Atlas exponent simplification | 21.748 ms | 1.00× |

Maximum scaled numerical difference from direct evaluation was $6.66\times10^{-16}$. The reviewed parser passed 13 targeted singularity/domain checks. Review found and corrected a corner case: division by a negative power can remove a negative exponent from the normalized product but must retain the original zero restriction (e.g., $\cos\theta/\sin^{-1}\theta$ in this parser means division by a reciprocal power, not an inverse trigonometric function). The tested grammar does not include parentheses or general sums. The results show that pre-simplification can accelerate this deliberately simplifiable workload. They do not establish superiority over a mature computer algebra system, optimizing compiler, hand-simplified expressions, or single-value calculator operations. Timing varies by machine and workload. A human speed/accuracy study has not been conducted.

## 8. Linking ten Trig Atlas modules

Each module provides an angle and its function values, and links are explicitly assigned operations. Two kinds of connection are distinct: physical adjacency of solids and a computational graph of functions or oscillators. One can have a logical edge without physical contact. The ten-module experiment used five graph topologies: a path (chain), a balanced-style branching tree, a star (central hub), a ten-node ring, and a $2\times5$ grid. A parallel bank of ten outputs was additionally tested for Fourier synthesis.

### 8.1 Rotation composition and parallel reduction

Represent module $i$ by $z_i=\cos\theta_i+\mathrm{i}\sin\theta_i$. Multiplication composes angles, because $z_1z_2=\cos(\theta_1+\theta_2)+\mathrm{i}\sin(\theta_1+\theta_2)$. A chain evaluates $\prod_{i=1}^{10}z_i$ serially, requiring nine dependent multiplications. A balanced pairwise reduction also uses nine multiplications but has four dependent stages, allowing parallel execution. Across 100,000 random ten-angle sets, maximum complex error versus direct evaluation of $\exp(\mathrm{i}\sum_i\theta_i)$ was $4.72\times10^{-15}$ (serial) and $4.69\times10^{-15}$ (balanced). The ideal critical-path depth ratio is $9/4=2.25$; it is not a measured wall-clock speedup. This operation is standard complex multiplication and is a useful module-level connection rule.

### 8.2 Phase ring: harmonic selection

Let ten phases be $\theta_j=\phi+2\pi j/10$ for $j=0,\ldots,9$. The root-of-unity sum gives, for integer $k$,

$$\sum_{j=0}^9 e^{\mathrm{i}k\theta_j}=\begin{cases}10e^{\mathrm{i}k\phi},&10\mid k,\\0,&10\nmid k.\end{cases}$$

Thus equal-spaced phases cancel integer harmonics not divisible by ten, while multiples of ten reinforce. Also $\sum_j\sin^2\theta_j=\sum_j\cos^2\theta_j=5$. A test with 100,000 global starting phases and twelve harmonic indices gave maximum absolute complex-sum error below $7\times10^{-14}$. This illustrates an ideal harmonic selector, not a broadband filter with measured hardware performance.

### 8.3 Parallel wave synthesis

One unit per odd harmonic produces the truncated Fourier series of a square wave:

$$y_m(t)=\frac4\pi\sum_{j=0}^{m-1}\frac{\sin((2j+1)t)}{2j+1}.$$

| Active units $m$ | RMS error (target amplitude 1) |
|---:|---:|
| 1 | 0.43524 |
| 3 | 0.25874 |
| 5 | 0.20099 |
| 10 | 0.14229 |

Results used 200,000 equally spaced midpoint samples over one period. Ten units reduce RMS error by about 67% compared with one unit; overshoot near discontinuities persists (Gibbs phenomenon). The mathematics is established Fourier synthesis expressed through the proposed interface.

### 8.4 Graph topology and synchronization

For linear diffusion, use the same unit edge coupling on each undirected graph: $\dot x=-L_G x$, where $L_G$ is the graph Laplacian. The mean is conserved. For 10,000 common Gaussian random initial phase-offset vectors (mean removed), the following table gives the second-smallest Laplacian eigenvalue $\lambda_2$, a measure of the slowest decay mode, and median remaining disagreement $\|x(5)\|/\|x(0)\|$.

| Topology | Edges | $\lambda_2$ | Median remaining disagreement |
|---|---:|---:|---:|
| Chain | 9 | 0.0979 | 15.96% |
| Tree | 9 | 0.1772 | 12.61% |
| Star | 9 | 1.0000 | 0.65% |
| Ring | 10 | 0.3820 | 6.34% |
| Grid | 13 | 0.3820 | 3.48% |

The star converged fastest under the tested per-edge coupling and initial conditions; it also concentrates degree at one node. For nonlinear phase feedback, use the identical-frequency, rotating-frame Kuramoto-type rule

$$\dot\theta_i=\sum_{j\sim i}\sin(\theta_j-\theta_i).$$

For each topology, 256 identical initial conditions were drawn near the evenly spaced ring pattern, with independent Gaussian perturbations of standard deviation 0.05 rad. Integration used fourth-order Runge–Kutta, step 0.05, final time 80. All chain, tree, star, and grid trials reached order parameter $|N^{-1}\sum_j e^{\mathrm{i}\theta_j}|>0.99$. None of the ring trials did: all 256 retained winding number +1, with median neighbor difference 36 degrees. This is evidence of a local twisted state under the specified initial conditions, not the probability of its emergence from arbitrary random phases.

In an ideal ten-node nearest-neighbor ring, uniform winding states $q=0,\pm1,\pm2$ are locally stable modulo global rotation: their linearization is $-\cos(2\pi q/10)L_G$, with positive cosine for those values. This reproduces established coupled-oscillator behavior [6]. A phase-based memory is a potential application, but requires experimental write/read/reset operations, noise tolerance, and comparison to existing oscillator-memory designs. No memory hardware has been built.

### 8.5 Physical arrangement constraints

For identically oriented unit octahedra, non-overlap of interiors follows when every pair of centers has Manhattan ($L^1$) separation at least 2. Centers displaced by exactly 2 along one coordinate axis share a single vertex. The ten-unit chain, a rectangular perimeter ring, and a $2\times5$ grid can be arranged with 9, 10, and 13 such contacts, respectively. The nine-leaf star cannot be constructed with nine distinct one-to-one vertex ports on one six-vertex hub; external branching connectors are necessary. Adding rings, markers, actuators, or thickness requires further clearance and connection design. Physical contact alone does not implement angle multiplication or oscillator coupling.

## 9. Potential applications and development priorities

| Application | Proposed role | Evidence still needed |
|---|---|---|
| Mathematics education | Recall identities; visualize reciprocal pairs, limits, derivatives, integrals | Controlled learning, accuracy, and retention study against hexagon and unit-circle tools |
| Visual symbolic calculator | Select vertices and operations; show simplification and original domain | Usability testing, broader parser, comparison with existing CAS and hand simplification |
| Visual mathematical programming | Modular nodes with typed ports and explicit operators | Executable graph editor, type and domain checks, cycle handling |
| Signal and vibration laboratory | Fourier synthesis, phase rings, coupled oscillators | Benchmark against conventional DSP methods; noisy and nonideal inputs |
| Robotics and computer graphics | Illustrate chains of rotations and projection | Full rigid transformations, noncommutative 3D rotations, engineering benchmarks |
| Calibrated analog instrument | Three-circle angular readout and geometric demonstrations | Mechanical construction, calibration, tolerances, physical measurements |
| Phase-based memory | Investigate multiple locally stable winding states | Reliable writing, decoding, reset, noise and retention tests; existing-memory comparison |

The first two applications offer a practical route to testing the distinctive interface without demanding new hardware. The network editor could then combine symbolic, wave, and oscillator layers in a single visual laboratory. There is currently no evidence that octahedral hardware outperforms standard computers or that an AI reasons faster merely by using the shape.

## 10. Limitations, falsifiable questions, and independent review

The algebraic identities are exact on the appropriate domains; numerical observations are finite-sample implementation checks. The prototype's speed advantage is specific to precompiled simplifiable workloads. Neither human cognitive speed nor physical-device efficiency has been evaluated. Orthographic reconstruction assumes a calibrated camera, known origin and scale, and labeled visible points. Network behavior depends on selected link operators, coupling strengths, topology, and initial conditions. No general-purpose computation, novel physics, or exclusive mathematical priority is claimed. The combined representation is a design and research hypothesis, not yet a validated educational intervention.

The following questions are intended for independent AI, mathematics, education, and engineering reviewers:

1. Are the edge and face tables, crossing complement rule, midpoint 1:2 relation, and projection reconstruction derivations mathematically correct? Can the two-or-six crossing classification be proved exactly, and what happens at degenerate views?
2. What prior work uses a six-function octahedron, its off-axis projection crossings, or cyclic three-circle derivative triangles as an integrated calculator? Cite precise sources and distinguish a direct match from a related concept.
3. Does the integer-exponent representation offer any benefit beyond conventional symbolic simplification, and what benchmarks would fairly test it? Identify counterexamples and domain-handling defects.
4. Is the three-point reconstruction useful compared with a conventional calibrated sine/cosine encoder or other angular readouts? What assumptions are necessary for robustness?
5. Which proposed linked-module applications merit a prototype? Are there meaningful octahedron-specific operations that are not merely standard computations displayed on a solid?
6. How should an educational experiment compare the Atlas with a standard calculator, formula sheet, unit circle and trigonometric hexagon? Specify tasks, controls, accuracy, time, and delayed retention metrics.

A reviewer should challenge the claims, reproduce the experiments, and propose improvements rather than merely endorse the concept. A negative result on usefulness or originality would also be informative.

## 11. Conclusion

Trig Atlas unifies a six-function reciprocal labeling, product and face rules, apparent edge crossings, and three synchronized unit circles. The resulting equilateral position and derivative triangles encode double-angle and harmonic invariants. A calibrated three-point orthographic view recovers sine and cosine with a bounded condition number. A compact exponent-based calculator simplifies same-angle products, and ten-module simulations illustrate how explicit link rules change computational and dynamical behavior. These results support the mathematical coherence of the interface, not a claim of fundamentally new trigonometry or computing. The principal open question is whether this spatial organization produces measurable advantages in learning, symbolic interaction, or practical instrumentation.

## References

[1] McCulley, W. S. (1957). Notes on circular and hyperbolic functions. *Mathematics Magazine*, 31(1), 33–38. https://doi.org/10.2307/3029329. Bibliographic record and diagram provenance corroborated by [2].

[2] Cook, J. D. (2023). Mnemonic diagrams for trigonometric and hyperbolic functions. https://www.johndcook.com/blog/trig-mnemonic-diagrams/.

[3] JMAP. *Trigonometric Identity Hexagon*. Instructional handout. https://www.jmap.org/SupportFiles/JMAP_EXTRAS/Handouts/TrigIdentityHexagon.pdf.

[4] University of Washington, Mathematics 445 (Winter 2003). Lab 5: Octahedron and Cube in the Sphere. https://sites.math.washington.edu/~king/coursedir/m445w03/lab/lab05.html.

[5] OpenStax. *Algebra and Trigonometry 2e*, Section 7.4: The Other Trigonometric Functions. https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-4-the-other-trigonometric-functions.

[6] Wiley, D. A., Strogatz, S. H., & Girvan, M. (2006). The size of the sync basin. *Chaos*, 16(1), 015103. https://doi.org/10.1063/1.2165594.

## Appendix: reproducibility package

The accompanying package contains the standalone interactive calculus prototype, Python scripts and recorded outputs. Python 3 and NumPy are required for the geometry and network experiments; the symbolic calculator uses the Python standard library only. Run the following commands from the package directory:

```sh
python trig_crossings.py
python trig_calculus_monte_carlo.py
python trig_atlas_calculator_reviewed.py --benchmark
python trig_atlas_ten_networks.py
python trig_atlas_calculator_reviewed.py 'sin sec cot' --angle 37
```

The original calculator is retained for provenance and the reviewed version corrects the domain issue described in Section 7.2. Timing is expected to vary across machines; numerical counts and errors should be similar with the fixed seed and compatible floating-point libraries. The HTML prototype is an interactive illustration of the single-unit geometry and calculus; it is not a complete network editor. The network simulations are provided separately.
