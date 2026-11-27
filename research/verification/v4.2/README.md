# V4.2 verification — readability release

Tested source: [Trig Atlas V4.2](../../../Trig_Atlas_v4_2_Readability.html).

SHA-256: `bbe70bc50a4bad2686e2d4f84e8595bca11c396d931597529a00daad7cddc452`

V4.2 adds a presentation-only factor search in either sine or cosine coordinates. Exact polynomial division and coefficient-by-coefficient reconstruction verify extracted factors. Cancellation uses v²=(1−u)(1+u); a candidate is rejected if its denominator would introduce a new exclusion outside the original domain. The V4.1 parser, canonical algebra, stable numerical evaluation and singularity classifier are unchanged.

## Recorded verification

- Original V4.1 math test: 1,232 generated expressions, 1,224 accepted, 8 bounded rejections. 4,896 exact rational comparisons, 6,120 cardinal/domain comparisons, 24,480 180-digit mpmath comparisons. No failures. Maximum scaled numerical error 2.2384751778243247e-13. 48 independent SymPy pole/limit checks passed.
- V4.2 display test: seed 20261126; 650 unique expressions, 610 accepted, 40 unchanged bounded rejections. 544 factored outputs proved equal by exact SymPy rational identities after tangent-half-angle substitution. 5,090 exact display-value comparisons, including 820 allowed cardinal comparisons. Canonical signatures, domain masks, numerical values and singularities matched V4.1 on every accepted case.
- Desktop Chromium: crossing, exact angle, hole/pole, all five guided practice tasks, reference, calculus PASS; no page errors.
- Mobile viewport 390px: no horizontal overflow.

## Reproduce the preserved V4.1 regression suite on V4.2

From repository root with Python, Node.js, mpmath, SymPy and Playwright/Chromium installed:

```sh
python research/verification/v4.1/test_v41_math.py Trig_Atlas_v4_2_Readability.html
python research/verification/v4.1/test_v41_browser.py Trig_Atlas_v4_2_Readability.html
```

The new display test independently evaluates rendered expressions using Python's AST and Fraction, and verifies factored outputs using SymPy, rather than relying on the Atlas parser. It checks V4.1/V4.2 agreement before verifying display equivalence.

## Limits

The factored display is not general-purpose factorization or a new input grammar. A displayed denominator such as (1+sin) is not necessarily accepted by the input parser; general denominators, non-cardinal singularities and a richer original-domain model remain future work. The numerical tests are finite-sample evidence, not universal error bounds.
