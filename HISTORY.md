# Trig Atlas — development history

This is a reconstructed history of the project, based on the preserved HTML prototypes, research paper, experimental scripts and review records. The earliest stages took place in conversation before the project was placed on GitHub. The archive files are original snapshots, not reconstructions. The Git commit dates reflect the archival uploads, not necessarily the dates on which the ideas were first developed.

## Origin: the six-vertex idea

The original investigator asked whether the six trigonometric functions could be placed on the six vertices of a three-dimensional shape so that relationships could be seen rather than memorized. The regular octahedron became the framework: three antipodal pairs for reciprocals, twelve edges for products and related identities, and eight triangular faces for three-factor products. The investigator subsequently asked whether looking through the shape, rotating it, and joining multiple copies could turn it into an "eye calculator."

The fixed coordinate labels are +X cos, -X sec, +Y sin, -Y csc, +Z tan, -Z cot. These are symbolic labels, not numerical coordinates. The trigonometric identity hexagon is a known antecedent; projecting the octahedron along a unity-face normal reproduces that arrangement. No exclusive mathematical priority is claimed.

## V1 — Trigonometric octahedron

Source: [original octahedron](archive/v1/trig_octahedron.html).

- The six functions were assigned to vertices, with reciprocal pairs connected through the center.
- The edge and face relationships were organized into an interactive visual reference.
- The user could rotate the object to explore apparent relationships from different viewing directions.
- The symbolic products were described as sine/cosine exponent addresses; opposite addresses cancel.

This was the first visual embodiment of the original concept. The center represents multiplicative unity as a mnemonic, not a fourth spatial coordinate.

## V2 — Three orthogonal unit circles

Source: [three-circle prototype](archive/v2/trig_octahedron_three_circles.html).

The investigator asked to add unit circles in coordinate planes. The design developed into three synchronized circles, with moving points P=(cos θ, sin θ, 0), Q=(0, cos θ, sin θ), R=(sin θ, 0, cos θ).

These points always form an equilateral triangle under the specified cyclic synchronization. Its squared side length is 2−sin(2θ); its centroid travels along the (1,1,1) diagonal. This tied the static identity mnemonic to continuously varying geometric measurements. Independent arbitrary circle phases do not generally produce the same triangle.

## V3 — Calculus and projection laboratory

Source: [calculus prototype](archive/v3/trig_octahedron_calculus.html).

- Added derivative and acceleration geometry, the complementary derivative triangle, definite-integral illustrations, and angle reconstruction from calibrated orthographic projections.
- The position and derivative triangles satisfy L² + Lv² = 4.
- Every vector coordinate has a sinusoidal derivative cycle; differentiation with respect to θ rotates the position vector by a quarter-turn. The integral of a position vector from a to b is U′(a)−U′(b).
- All three labeled projected points permit a two-parameter least-squares recovery of sine and cosine with design-matrix condition number at most √3, assuming a calibrated, unobstructed orthographic view.
- The scope was expanded to ask whether projected crossing geometry might also provide a meaningful interface for calculation.

## Research phase — crossing rules, calculator and linked modules

The mathematical investigation was recorded in the [exploratory research paper](research/Trig_Atlas_Research_Paper.md), dated November 26, 2026. The paper is an AI-assisted technical report, not a peer-reviewed publication.

For the six vertices, 24 unordered pairs of disjoint skew edges can be projected to strict interior screen crossings. If their four labels are A,B,C,D and the remaining pair E,F, then ABCD=1/(EF) on the common domain. Looking along the difference of the two edge midpoints yields a coincident projected midpoint p, and the remaining edge midpoint projects to −2p. This is a special camera orientation, not a claim about every crossing.

The seeded 100,000-view experiment reported 65,097 two-crossing views and 34,903 six-crossing views. Later analytic review addressed the nondegenerate classification: for a viewing direction n, a component whose absolute value exceeds the sum of the other two produces the two-crossing region; strict triangle inequalities produce the six-crossing region. Equality boundaries and coordinate-plane views must be treated separately, and the app counts strict segment intersections rather than endpoint contacts or overlaps.

The original Python calculator normalized same-angle products and powers into integer exponents and domain restrictions. The reviewed benchmark found about 2.17× speedup over direct evaluation and 1.79× over a cached sine/cosine baseline for its deliberately simplifiable precompiled workload. These figures do not establish superiority over optimized general-purpose mathematics software.

Ten-module simulations tested rotation composition, parallel reduction, harmonic selection, Fourier synthesis, graph diffusion and phase feedback. For near-twisted initial conditions, the ten-node ring retained a winding-one state in 256 simulations; the other tested graphs synchronized. These are simulations using explicitly specified coupling rules, not proof that attaching physical octahedra creates computation. The modular network idea remains an open research direction.

## V4 — Eye Calculator

Source: [V4 original release](archive/v4/Trig_Atlas_v4_Eye_Calculator.html).

This release brought the mathematical experiments together into a standalone, dependency-free interactive browser application. It separated three workspaces: the identity/reference model, the visual symbolic calculator, and the calculus laboratory.

The major change was a real same-angle expression compiler, not merely a table of identities. It accepted arithmetic, parentheses and bounded integer powers with monomial denominators; represented rational coefficients exactly; simplified Laurent polynomials using sin²+cos²=1; and tracked original domain restrictions independently of the simplified formula.

Visual crossing selection could construct an expression, demonstrate its complementary edge, and retain the symbolic selection even when the camera was rotated away from the visible crossing. Guided challenges linked geometric interaction to algebra and domain reasoning.

The reviewer feedback that motivated the next release included numerical cancellation near singular angles, more explicit hole-versus-pole classification, stricter separation of guided practice from example controls, and requests to improve the symbolic output and expression grammar.

## V4.1 — reliability release (preserved baseline)

Source: [V4.1](Trig_Atlas_v4_1_Reliability.html).

Rather than relying only on expanded sine/cosine expressions for numerical evaluation, V4.1 builds four local tangent-half-angle rational charts. It cancels exact vanishing polynomial factors before floating-point evaluation, uses scaled Horner evaluation and an exact dyadic polynomial fallback for severe cancellation, and classifies excluded cardinal angles by local order. This preserves the original domain while improving behavior near removable singularities and poles.

For example, (1−sin θ)^4/cos^8 θ is equivalent to 1/(1+sin θ)^4 on its original domain. At 90° it has a removable hole with limit 1/16; at 270° it has an eighth-order pole. The calculator must distinguish these even though both angles were excluded by the same original denominator.

The release also improved interaction feedback, crossing retention, explicit angle input, the five guided-practice tasks, and the practice/example separation.

The archived release package recorded these verification results (not new measurements from this archival commit):

- 1,232 generated expressions; 1,224 accepted and 8 rejected by documented complexity bounds.
- 4,896 exact rational comparisons, 6,120 cardinal/domain comparisons, 24,480 high-precision comparisons using 180-digit mpmath; zero reported failures.
- Maximum scaled numerical error approximately 2.24×10⁻¹³ in that sample.
- 48 independent SymPy pole/limit checks passed.
- Chromium desktop interaction checks passed with no page errors; the 390 px mobile viewport showed no horizontal overflow.

A separate AI review reported fuzzing 40,000 expressions without domain or value errors within the supported grammar, and agreement with 50-digit arithmetic near a singularity. It also identified the most important remaining limitations: verbose expanded output, a restriction to monomial denominators, and small visual/wording issues. These are reviewer-reported observations, not independently rerun results for this commit.

## V4.2 — readable factored identities

Source: [V4.2](Trig_Atlas_v4_2_Readability.html).

V4.2 retains the V4.1 parser, exact canonical algebra, numerical evaluator and original-domain tracking. It adds a presentation-only factor search in either sine or cosine coordinates, exact polynomial division, coefficient-by-coefficient reconstruction checks, and cancellation using v² = (1−u)(1+u). The shorter expression is shown only when its denominator does not introduce exclusions outside the original domain. The canonical form remains available in an expandable panel. A displayed denominator such as (1+sin) is not yet accepted as an input denominator.

The update also caps the integral chart height, uses neutral empty-input guidance, clarifies tangent arrow scaling and corrects the singularity graph legend.

Verification: the unchanged V4.1 suite passed 24,480 high-precision numerical comparisons, 4,896 exact rational comparisons, 6,120 cardinal/domain comparisons and 48 independent pole/limit checks. The new seeded display suite tested 650 unique expressions (610 accepted, 40 bounded rejections); 544 factored displays passed exact SymPy rational identity proofs, and 5,090 exact display-value comparisons passed. All accepted cases retained identical V4.1 canonical signatures, masks, numeric values and singularities. All five guided practice tasks and desktop/mobile browser checks passed.

General denominators and non-cardinal singularities remain the next architectural research problem, not implemented features.

## Next research and development priorities

1. Preserve V4.1 as a known-good baseline. Improve output readability and small visual issues in a separate revision, with regression checks.
2. Introduce general denominators only alongside a mathematically sound domain model. A two-bit sin/cos exclusion mask cannot represent the zeros of sin+cos, for example.
3. Keep exact equivalence, human-readable form, numerical evaluation and original domain as distinct representations.
4. Expand randomized differential and browser testing; document unsupported syntax and numerical limits.
5. Compare against existing tools in a controlled educational study, including retention and error rates.
6. Revisit calibrated geometric sensing and linked modules only with explicit operations, assumptions and measurable hypotheses.

V4.2 readability is implemented; general denominator support and later research features remain proposals.

## Provenance

The original investigator initiated the octahedral visual-calculator idea, asked the exploratory questions, and directed the project. AI assistants contributed mathematical derivation, programming, simulations, critique and documentation. The underlying trigonometry, rational parameterizations, orthographic projection mathematics and oscillator models have established antecedents. The research contribution under investigation is their combination into a spatial interface and the testable advantages it may offer.

See [AI handover](AI_HANDOFF.md) for the technical architecture and regression expectations.
