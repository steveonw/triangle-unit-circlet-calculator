# Trig Atlas V4.3 — General rational denominators

Tested application: `Trig_Atlas_v4_3_Rational.html`

SHA-256: `8f0f2a3eaf1c5967ef6123e6008b734f4be575e78b17dfa3ecfd88c12d5c6fa9`
Git blob: `47d8d19697a3ab18948c1203f997319bc81cb411`

## Architecture and scope

V4.3 preserves the existing V4.2 Laurent engine as its fast path. A fallback handles previously unsupported non-monomial denominators and negative powers. The input is still a single shared angle, with integer constants, parentheses, arithmetic, and integer powers from -12 to 12. It is not a general CAS.

Each of four local tangent-half-angle charts represents the expression as a reduced rational function N(t)/D(t), where t=tan((theta-alpha)/2) and alpha is a cardinal center. A separate square-free polynomial X(t) represents original exclusions. Arithmetic unions operand exclusions; division also adds zeros of the divisor's reduced numerator before cancellation. Negative powers invert the base while retaining its exclusions; zero powers retain the original base domain. Identically zero divisors are rejected. Thus cancelling a factor never erases the restrictions of the original expression.

Two bounded charts centered at 0 and 180 degrees cover the full circle; Sturm sequences with exact integer arithmetic count and isolate the real roots of X in [-1,1]. Shared endpoints are counted once. Root multiplicities of the reduced denominator determine pole order; otherwise the root is a removable hole and the reduced fraction gives its limit. Common rational-degree angles are certified using the root-of-unity polynomial Im((1+it)^m), m<=24. Other angles and nonrational limits are numerical approximations. Clicking an isolated-root button selects its floating-point representative; typing a rounded nearby number need not select that root. Exact algebraic domain polynomials are retained internally.

Evaluation uses the nearest of the four charts, exact polynomial cancellation, and BigInt Horner evaluation at the binary64 tangent value. This mitigates polynomial cancellation, but cannot remove the conditioning of a genuinely near-pole argument or the finite accuracy of the angle itself. Graph segments break at all discovered exclusions, including non-cardinal roots. The general path is bounded to degree 48, coefficient sizes, a work budget and at most 32 numerically distinguishable exclusions per period; unsupported/overly complex expressions are rejected. The primary display uses a recognized shorter trig expression when available, otherwise the entered expression with exact rational chart forms in the disclosure panel. General-purpose factoring or arbitrary functions of theta are not implemented.

## Verification (seed 20261126)

The new independent Python/Node/SymPy/mpmath test generated 374 unique inputs, accepted 354 (336 general and 18 legacy), and correctly rejected 20 identically zero denominator cases. No bounded rejections in that sample. Results: 6,392 exact chart-value comparisons, 9,408 original-domain checks, 8,715 100-digit numerical comparisons, 280 exact SymPy chart/domain identities, 445 isolated-root/classification checks, and 249 finite-limit checks. Maximum scaled numerical error 2.870157264219999e-14. No failures. The original V4.1 math and browser tests and V4.2 display tests also passed unchanged against V4.3. The new Chromium desktop/mobile interactions passed with no page errors or horizontal overflow at a 390 px viewport. These are finite-sample results, not universal accuracy or usability guarantees.

## Reproduce

Install Python 3, Node.js, mpmath, SymPy, Playwright and Chromium. From the repository root (the standalone review ZIP instead places all scripts and both HTML files at its root):

```sh
python -m pip install mpmath sympy playwright
python -m playwright install chromium
python research/verification/v4.3/test_v43_rational.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.3/test_v43_browser.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.1/test_v41_math.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.1/test_v41_browser.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.2/test_v42_display.py Trig_Atlas_v4_2_Readability.html Trig_Atlas_v4_3_Rational.html
```

If using an existing Chromium executable, set CHROMIUM_PATH to its path. Browser tests write screenshots into browser_screenshots/. Results in this package are the actual recorded runs. The old V4.1 and V4.2 tests were not rewritten to make V4.3 pass. The new reference evaluator uses exact rationals for integer constants, including divisions and negative powers.

## Next priorities

Broader stress testing at clustered algebraic roots, better factored human-readable output for general rational expressions, comparison with established CAS methods, and educational testing. The earlier numerical-optimization proposal remains future work. No changes were made to the octahedral geometry, projection theorem, or calculus workspace mathematics.
