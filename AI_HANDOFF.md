# AI handover — Trig Atlas

## Start here

Trig Atlas is a user-directed, AI-assisted exploratory mathematics project. The user's original idea was to arrange the six trig functions on an octahedron and use rotation, through-view crossings, and synchronized unit circles as an "eye calculator." Keep the geometry central: this is not simply a generic CAS with a 3D ornament.

**Latest working version:** [Trig_Atlas_v4_3_1_Presentation.html](Trig_Atlas_v4_3_1_Presentation.html) (Git blob SHA 6547f5756fa413246f5dff45b9e192c19ead0515; SHA-256 f4153ac068cf1da07c1ba0a2b06aecdbadd62f5eec35db8ad306bf7be75cff15). See [V4.3.1 verification](research/verification/v4.3.1/README.md). Its symbolic engine is byte-for-byte identical to [V4.3](Trig_Atlas_v4_3_Rational.html) (Git blob SHA 47d8d19697a3ab18948c1203f997319bc81cb411; [V4.3 verification](research/verification/v4.3/README.md)), which is preserved as the general-rational engine baseline. Preserve [V4.2](Trig_Atlas_v4_2_Readability.html) as the verified readability baseline. **Preserved numerical regression baseline:** [Trig_Atlas_v4_1_Reliability.html](Trig_Atlas_v4_1_Reliability.html). Open directly in a modern browser; no external dependencies or network required. Git blob SHA: db7a7ac9518f772d7147aea4c95eb3084b1cfcf8. Preserve it as a reference when making changes. [HISTORY.md](HISTORY.md) explains prior versions. [Research paper](research/Trig_Atlas_Research_Paper.md) records the theory and experiments (November 26, 2026, exploratory and not peer reviewed).

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
- `singularity` distinguishes removable holes from poles at excluded cardinal angles using chart order and limit. The legacy two-bit mask covers sine and cosine zeros only. For general V4.3 results use the independently tracked root list (`roots`), exact domain polynomial (`x`) in `rcharts`, and `TA.singularity(result,deg)`. Never assume the mask alone describes the general domain.
- `crossingPairs`, `selectCross`, `setExpression`, `updateEyeResult`, `buildModel` and `setWorkspace` coordinate the interface. The selection should survive rotation away from a previously selected crossing.
- `readShadow` implements the calibrated least-squares reconstruction. Camera state is distinct from mathematical angle state.

Supported grammar: same-angle sin, cos, tan, cot, sec, csc; integer constants, arithmetic, parentheses, bounded integer powers; V4.3 supports nonzero general rational denominators/negative powers through a bounded rational-chart fallback; the legacy Laurent path remains unchanged. Implicit multiplication is supported; multiplication/division associate left to right. A defined base raised to zero is 1 even when the base is zero; an undefined base remains undefined. sin^-1 is a reciprocal power, NOT arcsine. Complex inputs, arbitrary angles inside functions and general-purpose CAS operations are not supported. Keep expression-size bounds and reject unsupported inputs clearly.

## Verification before accepting a patch

Recorded V4.1 checks (from the original release review package; not rerun during documentation): 1,224 accepted generated expressions out of 1,232; 4,896 exact rational checks; 6,120 cardinal/domain checks; 24,480 180-digit mpmath comparisons; max scaled error 2.2385e−13; 48 SymPy singularity checks passed. Browser checks passed all five challenges and reported no page errors; 390 px mobile viewport had no horizontal overflow. A later external AI review first reported a "40,000-expression" fuzz test in conversation. That reviewer later found its generator had cycled (287 distinct expressions), corrected the figure, and archived a fixed harness with actual outputs in [research/verification/independent_review](research/verification/independent_review/README.md): 40,000 distinct expressions on V4.1, V4.3 and V4.3.1 and 3,000 general-rational expressions on V4.3 and V4.3.1, all with 0 failures. Cite the archived results, not the conversational figure. They were run by the reviewer; a maintainer can rerun them with `run_all.sh`.

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

## V4.3.1 presentation layer (implemented)

V4.3.1 adds `prettyExpression(text)` and `answerText(result)` in the interface script, just before `updateEyeResult`. When a general-path result's `text` equals its raw `source`, the answer box shows a typeset version: spaced `+ − · /`, `·` for implicit multiplication, superscript exponents (with leading zeros removed, so `sin^03` shows as `sin³`, as the engine reads it), and `−` for unary minus. Constant general results have `-` replaced by `−`. Recognized short forms and Laurent results are shown unchanged.

Rules: never change `result.text`, because the guided-practice checks compare it (for example `r.text==='1'`). Never put display logic inside `TA`. Any display change must pass `research/verification/independent_review/scripts/display_roundtrip.js`, which feeds every typeset answer back into `TA.compile` and requires identical exclusions and bit-identical values. The empty-input prompt uses `#eyeError.neutral` (muted) and has done so since V4.2. Real errors remain orange.

## Independent review suite

`research/verification/independent_review/` is a test suite written separately from the release tests: a separate double-precision reference evaluator (`scripts/common.js`), Laurent and general-rational fuzz tests, 21 hand-derived hole/pole cases, 50-digit near-pole checks, 60-digit adjudication of each run's worst disagreement, a display round-trip test, and a Chromium smoke test. Run `bash research/verification/independent_review/run_all.sh <app.html> results/<version> [--rational] [--display]` from the repository root. Use `mulberry32` (in `common.js`) for any new random generation. Do not use a floating-point LCG: the first draft did, and its stream cycled after 10,466 draws.

Known accuracy observation (not a failure): on the Laurent path, the app's largest observed relative error was 2.8×10⁻¹¹ (one expression at 313.9°, confirmed with 60 digits). The V4.1 evaluator falls back to exact dyadic Horner evaluation only when cancellation exceeds 10¹⁰, so errors up to about 10¹⁰·ε are possible below that threshold. The general rational path always evaluates its numerator and denominator polynomials exactly (BigInt) at the binary64 tangent value, before one final floating-point division.

## V4.3 general rational engine (implemented)

`RG` is a fallback inside `TA`, preserving V4.2 results for previously supported expressions. Its AST evaluator constructs four exact local rational functions (reduced numerator/denominator BigInt polynomials) and separate square-free exclusion polynomials. Domain union uses polynomial GCD/LCM; inversion adds roots of the original divisor numerator before cancellation. Degree 48, coefficient/work limits and at most 32 distinguishable roots bound the fallback. Two half-angle charts cover the period for exact Sturm root isolation; the nearest cardinal chart is used for numerical evaluation. Exact dyadic polynomial evaluation mitigates cancellation, not intrinsic ill-conditioning. The graph breaks at all exclusions. A root-selection button uses its floating-point representative; other typed rounded values need not select the root. The rational charts and domain polynomials, not the display string or legacy mask, are authoritative. Common rational-degree roots are certified using a root-of-unity polynomial (m ≤ 24). Other angles and nonrational limits are approximate.

The independent suite passed 6,392 exact value comparisons, 9,408 domain checks, 8,715 100-digit comparisons, 280 exact chart/domain identities, 445 root classifications, 249 finite-limit checks and the earlier V4.1/V4.2 tests. See [V4.3 source, tests and results](research/verification/v4.3/README.md). No universal accuracy, complete factorization or arbitrary-angle CAS claim.

## V4.4 numerical optimization experiment (research only)

Read the [optimization experiment report](research/verification/v4.4-optimizer/README.md). The latest deployed application remains V4.3.1; the experiment loaded the hash-verified V4.3 file with an identical TA block, and instrumented a copy in memory. A 1e-6 Laurent Horner fallback threshold (instead of 1e-10) is the recommended candidate from this workload: 2,013 accepted expressions, 15,211 180-digit reference points, random Laurent max scaled error 3.75e-10 -> 3.52e-14, reviewer-case error 2.83e-11 -> 1.75e-16, median timing 767 -> 783 ns/evaluation with overlapping repetition ranges. No domain change was observed in 8,052 independent exact cardinal checks or 45,370 variant/baseline boundary comparisons. Do not call these universal error bounds.

Near off-axis poles, exact Horner on a binary64 half-angle coordinate can still be inaccurate. High-precision chart evaluation at the exact angle versus the rounded coordinate isolated that issue. For a few certified exact roots, root-centered identities such as sin(theta)-sin(alpha)=2*cos((theta+alpha)/2)*sin((theta-alpha)/2) proved useful in a 48-point experiment. Do not silently snap a typed angle to a displayed approximate root. General root-centered factorization and high-precision angle evaluation remain unimplemented. The full reproduction ZIP is separate from GitHub; the report is archived here. Next patch: trial the 1e-6 cutoff, rerun original and independent suites, preserve prior releases, then separately investigate more general conditioning-aware strategies.

## Next scoped work (not yet implemented)

0. **Laurent evaluator threshold:** consider lowering the 10¹⁰ cancellation threshold that triggers exact evaluation, or always using exact evaluation, then measure accuracy with the independent review suite and the V4.1 high-precision suite. Preserve results and domains.
1. **V4.4 numerical optimization research:** compare exactly equivalent rational representations, their operation counts and conditioning using independent high-precision references. Improve readable factored forms for general rational expressions (V4.3.1 typesets them but does not factor them); do not change the original domain or replace the V4.1/V4.2 regression baseline.
2. **V4.3 follow-up:** stress-test clustered roots, repeated roots, rational-degree certification, non-cardinal hole limits and angles close to poles. Improve the representation of selected algebraic roots and expose the exact original-domain conditions. Keep explicit bounds; do not claim universal correctness from sample tests. For sin/(1+cos), 0° is valid, whereas (1−cos)/sin is undefined there.
3. **Numerical optimization:** compare exactly equivalent candidate formulas by operation count and measured numerical error, keeping original domains and reliable evaluation separate from display. Benchmark fairly against optimized CAS and hand-simplified methods, including setup costs.
4. **Research validation:** controlled educational study against flat hexagon, unit circle and formula sheets. Optical readout and linked modules are experimental branches; ordinary complex multiplication, Fourier and oscillator simulations do not require an octahedron. Require octahedron-specific mechanisms and a fair baseline before claiming practical advantages.

## Working rules for future AI contributors

Read the baseline and history before editing. State the patch scope; preserve the original math, coordinate conventions, workspace behavior and offline operation. Avoid rewriting everything for small changes. Test existing functions as well as new ones; separate proofs, finite-sample tests, external reports and speculative applications. Don't claim novelty, universal accuracy, speedup, hardware performance or educational effectiveness without evidence. Keep old snapshots, a versioned changelog, reproducible test scripts/results and user-facing documentation in Git. Ask for the user's direction when changes alter the core project rather than a local improvement.

The creator originated the spatial mnemonic and directed the exploration. AI assistants supported derivation, implementation, critique, and testing. Credit the investigator and cite established precedents in the research paper.
