# AI handover — Trig Atlas

## Start here

Trig Atlas is a user-directed, AI-assisted exploratory mathematics project. The user's original idea was to arrange the six trig functions on an octahedron and use rotation, through-view crossings, and synchronized unit circles as an "eye calculator." Keep the geometry central: this is not simply a generic CAS with a 3D ornament.

**Latest working version:** [Trig_Atlas_v4_2_Readability.html](Trig_Atlas_v4_2_Readability.html). V4.2 is a display-only layer with verified factor extraction and original-domain preservation. See [V4.2 verification](research/verification/v4.2/README.md). **Preserved numerical regression baseline:** [Trig_Atlas_v4_1_Reliability.html](Trig_Atlas_v4_1_Reliability.html). Open directly in a modern browser; no external dependencies or network required. Git blob SHA: db7a7ac9518f772d7147aea4c95eb3084b1cfcf8. Preserve it as a reference when making changes. [HISTORY.md](HISTORY.md) explains prior versions. [Research paper](research/Trig_Atlas_Research_Paper.md) records the theory and experiments (November 26, 2026, exploratory and not peer reviewed).

## User-facing workspaces

- **Eye Calculator:** select vertices, edges, faces or projected crossings to construct a same-angle expression. Exact simplification, original domain, graph, hole/pole classification and numeric evaluation. Camera rotation must not change θ or the truth of an identity.
- **Identity Atlas:** reference for six vertices, twelve edges, eight faces, reciprocal axes, and calculus/Pythagorean relationships.
- **Calculus Lab:** three synchronized orthogonal unit circles, position/velocity/acceleration geometry, definite integrals and calibrated projected-angle recovery.
- **Practice:** five guided tasks; explicitly separate discovery from demonstrations. The user must perform the relevant work rather than pass on an untouched initial page.

## Mathematical anchors (do not silently change)

Let s=sin θ, c=cos θ. Fixed labels: +X cos, −X sec; +Y sin, −Y csc; +Z tan, −Z cot. The symbolic coordinates are (a,b) for s^a c^b: sin=(1,0), csc=(−1,0), cos=(0,1), sec=(0,−1), tan=(1,−1), cot=(−1,1). They are not physical positions or trig values. Opposite vertices cancel on their original domain. Unity faces are sin·sec·cot and csc·cos·tan. The other six face products are the squares of the individual functions.

Disjoint skew-edge crossings select four distinct labels. Their product is the reciprocal of the remaining edge product; this is an algebraic complement rule, not a physical collision. There are 24 skew-edge pairs. In the special midpoint view, project along m1−m2: Bm1=Bm2=p, Bm3=−2p. General camera views need not cross at midpoints. Generic strict crossing-pair counts are 2 or 6. For sorted absolute direction components a≥b≥c≥0, strict crossings are 0 if c=0, 2 if c>0 and a≥b+c, and 6 if c>0 and a<b+c. Numerical screen tests have tolerances near the boundaries. Do not count endpoint contacts or overlaps.

P=(c,s,0), Q=(0,c,s), R=(s,0,c) are the synchronized circle points; cyclic permutation is a 120° rotation about (1,1,1). The triangle is equilateral, L²=2−sin 2θ, derivative triangle Lv²=2+sin 2θ. L²+Lv²=4. Signed centroid heights h=(s+c)/√3 and hv=(c−s)/√3 recover sine and cosine. For radians, U′(θ)=U(θ+π/2), U″=−U, and ∫_a^b U dθ=U′(a)−U′(b). The other four scalar trig functions require their ordinary nonlinear calculus rules.

With cyclic permutation matrix S and projection B=I−nnᵀ, the three labeled projected points are columns of Y=cB+sBS. The least-squares Gram matrix is [[2,g],[g,2]], g=−nᵀSn∈[−1,1/2]. Determinant ≥3, design-matrix condition number ≤√3. This assumes labeled visible points, calibrated origin, orientation and scale, orthographic projection and ideal synchronization. It does not prove camera hardware superiority.

## V4.1 implementation map

All CSS and JavaScript are inline. Inspect the actual file before patching.

- Fixed geometry, projection, vertex/edge/face data and circle positions are existing source-of-truth definitions.
- `TA` is the exact symbolic module: `parse`, `canon`, `compile`, `value`, `singularity`, and related helpers. Exact rational coefficients use BigInt; sparse Laurent terms are keyed by sine/cosine exponents. Canonicalization uses c²=1−s².
- `compile` retains original domain restrictions and constructs four local rational charts for stable numerical evaluation. Each chart rotates to the nearest cardinal axis, using t=tan(δ/2), sin δ=2t/(1+t²), cos δ=(1−t²)/(1+t²). Exact cancellation determines the local order before floating-point evaluation. Scaled Horner and an exact dyadic polynomial fallback mitigate polynomial cancellation. The final trigonometric argument and output are binary64, not arbitrary precision.
- `singularity` distinguishes removable holes from poles at excluded cardinal angles using chart order and limit. The current two-bit mask covers sine and cosine zeros, not arbitrary denominator roots.
- `crossingPairs`, `selectCross`, `setExpression`, `updateEyeResult`, `buildModel` and `setWorkspace` coordinate the interface. The selection should survive rotation away from a previously selected crossing.
- `readShadow` implements the calibrated least-squares reconstruction. Camera state is distinct from mathematical angle state.

Supported grammar: same-angle sin, cos, tan, cot, sec, csc; integer constants, arithmetic, parentheses, bounded integer powers; division/negative powers require a nonzero single monomial denominator in the current algebra engine. Implicit multiplication is supported; multiplication/division associate left to right. A defined base raised to zero is 1 even when the base is zero; an undefined base remains undefined. sin^-1 is a reciprocal power, NOT arcsine. Complex inputs, arbitrary angles inside functions and general-purpose CAS operations are not supported. Keep expression-size bounds and reject unsupported inputs clearly.

## Verification before accepting a patch

Recorded V4.1 checks (from the original release review package; not rerun during documentation): 1,224 accepted generated expressions out of 1,232; 4,896 exact rational checks; 6,120 cardinal/domain checks; 24,480 180-digit mpmath comparisons; max scaled error 2.2385e−13; 48 SymPy singularity checks passed. Browser checks passed all five challenges and reported no page errors; 390 px mobile viewport had no horizontal overflow. A later external AI reported 40,000-expression fuzz testing without failures on supported inputs; treat this as a reported review, not an independently reproduced result.

The release review package originally supplied `test_v41_math.py` (Python, Node, mpmath, SymPy), `test_v41_browser.py` (Python Playwright and Chromium), recorded results and a SHA-256 checksum. These artifacts are archived under [research/verification/v4.1](research/verification/v4.1/). See the [research reproduction guide](research/README.md) for commands using the root-level HTML baseline. The [original Python experiments and recorded results](research/experiments/) are also archived. Do not invent test results.

Minimum regression cases:
| Input | Expected result / domain |
|---|---|
| sin sec cot | 1, excluded at sin=0 and cos=0 |
| sin^2+cos^2 | 1 everywhere |
| sec^2-tan^2 | 1 except cos=0; removable holes |
| cos / sin^-1 | sin·cos, sin=0 still excluded |
| 1/tan | cot, both sin=0 and cos=0 excluded |
| (1-cos)/sin^2 | hole at 0° limit 1/2; pole order 2 at 180° |
| (1-sin)^4/cos^8 | hole at 90° limit 1/16; pole order 8 at 270° |
| previous expression at 89.99° | ≈0.06250000190386 |
| previous expression at 89.999° | ≈0.062500000019038 |

Also test negative/scaled Pythagorean expressions, zero powers, invalid syntax and complexity bounds. Compare independent exact rational algebra and high-precision numerical evaluation. In browser: start blank, verify practice cannot be completed by pressing Check alone, disable examples during practice, select the cosine-producing crossing and rotate away, test 0/2/6 view presets and midpoint ratio, recover an arbitrary angle, verify L²+Lv²=4, and inspect mobile layout. Record actual tools used, seeds, accepted/rejected inputs, errors, and browser screenshots where feasible.

## Next scoped work (not yet implemented)

1. **V4.2 readability/polish (completed):** exact display-only factor extraction and shorter equivalent representations, with V4.1 immutable. Next focus: broader denominator input and non-cardinal singularities, with a separate exact domain model. Do not alter the V4.1 numerical baseline silently.
2. **General denominator research:** a separate design/implementation step. The two-bit mask is insufficient once denominators such as 1+cos or sin+cos are allowed. Model original undefined subexpressions and roots explicitly; rational charts and exact polynomial root isolation are candidate methods, not implemented features. Simplification may add artificial exclusions or remove original holes. For sin/(1+cos) the angle 0° is valid, whereas (1−cos)/sin is undefined there; neither is defined at 180°. A representation may be algebraically equivalent on a shared domain without being domain-equivalent. Test repeated roots, zero denominators, arbitrary noncardinal roots, cancellations and cardinal/periodic endpoints. Consider canonical equivalence before rejecting denominators that simplify to a monomial.
3. **Numerical optimization:** compare exactly equivalent candidate formulas by operation count and measured numerical error, keeping original domains and reliable evaluation separate from display. Benchmark fairly against optimized CAS and hand-simplified methods, including setup costs.
4. **Research validation:** controlled educational study against flat hexagon, unit circle and formula sheets. Optical readout and linked modules are experimental branches; ordinary complex multiplication, Fourier and oscillator simulations do not require an octahedron. Require octahedron-specific mechanisms and a fair baseline before claiming practical advantages.

## Working rules for future AI contributors

Read the baseline and history before editing. State the patch scope; preserve the original math, coordinate conventions, workspace behavior and offline operation. Avoid rewriting everything for small changes. Test existing functions as well as new ones; separate proofs, finite-sample tests, external reports and speculative applications. Don't claim novelty, universal accuracy, speedup, hardware performance or educational effectiveness without evidence. Keep old snapshots, a versioned changelog, reproducible test scripts/results and user-facing documentation in Git. Ask for the user's direction when changes alter the core project rather than a local improvement.

The creator originated the spatial mnemonic and directed the exploration. AI assistants supported derivation, implementation, critique, and testing. Credit the investigator and cite established precedents in the research paper.
