# Independent review tests (V4.1, V4.3, V4.3.1)

These tests were written and run by an AI reviewer (Claude, Anthropic) at the user's request. They were written separately from the release test suites in `../v4.1`, `../v4.2` and `../v4.3`, and they use a separately written reference evaluator. Every number below comes from the archived scripts in [scripts/](scripts/), run on the archived HTML files. The raw outputs are in [results/](results/).

## Correction to an earlier reported figure

Before this archive existed, the reviewer reported in conversation a "40,000-expression" fuzz test of V4.1 and a "3,000-expression" test of V4.3 with no failures. Those runs used a linear congruential generator, `state = (state*1103515245 + 12345) % 2**31`, on JavaScript numbers. The product exceeds 2⁵³, so it lost precision and fell into a cycle of 10,466 draws. **The "40,000" run actually contained 287 distinct expressions, and the "3,000" run 267, of which 70 used the general rational path.** No failures were found in those runs, but they were far smaller than reported, so they are superseded and not archived.

The archived harnesses use `mulberry32` (exact 32-bit integer arithmetic), test only distinct expressions, and record `distinctExpressions` and `drawsNeeded` in every summary.

## What is tested

| Script | Purpose |
|---|---|
| [common.js](scripts/common.js) | Loads the inline `TA` engine from an HTML file in Node.js. Contains the reference evaluator, written separately from the app: same documented grammar, literal definitions of the six functions, NaN for any division by an exact zero. Also contains the seeded RNG. |
| [fuzz_laurent.js](scripts/fuzz_laurent.js) | 40,000 distinct random expressions (seed 20261126) using products, quotients, sums and powers. At 0°/90°/180°/270° the defined-or-undefined answer and the value must match the reference. At four random generic angles per expression (at least 1° from an axis, \|value\| < 10⁶), the scaled error must be below 10⁻⁶. For Laurent-path results it also checks that the two-bit domain mask agrees with `TA.value`. |
| [fuzz_rational.js](scripts/fuzz_rational.js) | 3,000 distinct random expressions (seed 20261127) with frequent compound divisors (V4.3+). It runs the same axis-angle and generic-angle checks (six angles each). It confirms that every reported off-axis exclusion makes some divisor vanish (< 10⁻⁹). A 0.05° grid scan searches for divisor zeros the app did not report. A flag counts as an *axis artifact* only if the smallest divisor keeps shrinking all the way to the nearest axis angle and the app already excludes that angle. Otherwise it is a failure. A built-in **detector self-test** hides the real exclusions of four known expressions and requires the scan to find them, and to stay quiet when they are supplied. |
| [singularity_cases.js](scripts/singularity_cases.js) | 21 hand-written cases with hole limits and pole orders derived by hand: the AI_HANDOFF regression table plus seven general-denominator cases. |
| [near_pole_mpmath.py](scripts/near_pole_mpmath.py) | Eight values near excluded angles compared with 50-digit mpmath at the exact binary64 angle, alongside a naive double-precision evaluation. |
| [mp_reference.py](scripts/mp_reference.py) | 60-digit port of the reference evaluator. It adjudicates the largest app-vs-reference disagreement of each fuzz run, so it is clear which side was wrong. |
| [display_roundtrip.js](scripts/display_roundtrip.js) | V4.3.1 only. 3,000 distinct random expressions (seed 20261128) plus 10 hand-picked ones. Every typeset general-path answer must contain no ASCII `* ^ -`, must re-parse, and must give identical exclusions and bit-identical values at eight angles. |
| [browser_smoke.py](scripts/browser_smoke.py) | Chromium. Checks page errors, the 2- and 6-crossing presets, the example crossing, the near-pole example, prompt color versus error color, general-answer display (`--expect-pretty` for V4.3.1), and overflow at 390 px. |
| [run_all.sh](run_all.sh) | Runs the set for one HTML file and writes `results/<version>/`. |

## Results

Run on 2026-11-27 (UTC). Environment: Linux; Node.js 22.23.5; Python 3.13.18; mpmath 1.3.0; Playwright 1.63.0; Google Chrome for Testing 153.0.8010.12. The release suites rerun for V4.3.1 also used SymPy 1.14.0.

| Tested file | SHA-256 | `TA` engine block SHA-256 |
|---|---|---|
| Trig_Atlas_v4_1_Reliability.html | `48076548518e2be6237f73b2fd925c2889a335e019395a511c5783f9fd09661b` | `0d9bf8da858376c6cbd18aa031b352fe0646d47057a6cc45e91cfb207c5d8474` |
| Trig_Atlas_v4_3_Rational.html | `8f0f2a3eaf1c5967ef6123e6008b734f4be575e78b17dfa3ecfd88c12d5c6fa9` | `d15f5bf58984ca843d35501540e2b9afd796f6de4248d46cd68129da43a3b340` |
| Trig_Atlas_v4_3_1_Presentation.html | `f4153ac068cf1da07c1ba0a2b06aecdbadd62f5eec35db8ad306bf7be75cff15` | `d15f5bf58984ca843d35501540e2b9afd796f6de4248d46cd68129da43a3b340` (identical to V4.3) |

### Laurent-grammar fuzz (40,000 distinct expressions, 45,340 draws)

| | V4.1 | V4.3 | V4.3.1 |
|---|---:|---:|---:|
| Accepted | 32,175 | 39,600 (32,175 Laurent + 7,425 general) | same as V4.3 |
| Rejected | 7,825 | 400 | same as V4.3 |
| Axis-angle domain checks | 128,700 | 158,400 | same |
| Axis-angle value checks (defined cases) | 14,704 | 14,967 | same |
| Generic-angle value checks | 124,654 | 153,357 | same |
| Mask vs `value()` disagreements | 0 | 0 | 0 |
| Largest app-vs-reference scaled disagreement | 2.83e-11 | 2.83e-11 | 2.83e-11 |
| Failures | **0** | **0** | **0** |

Rejection reasons. V4.1: 7,793 "Division and negative powers require a single nonzero monomial denominator" (the documented V4.1 grammar limit), 29 "Expression too large for this prototype", 3 "Expression too long". V4.3: 246 "General rational expression exceeds the degree / complexity limit", 122 "Denominator is identically zero — no valid angle", 29 "Expression too large for this prototype", 3 "Expression too long". Every rejected expression is listed with its message in `laurent_rejected.txt`.

**Adjudication of the largest disagreement** (`worst_case_laurent.log`). The case is a long same-angle expression at 313.9°. Against 60-digit arithmetic, the app's error is 2.83×10⁻¹¹ and the double-precision reference's error is 1.17×10⁻¹⁴. Here the app is the less accurate of the two. This is consistent with the V4.1 evaluator design: it switches to exact dyadic Horner evaluation only when cancellation exceeds a factor of 10¹⁰, so milder cancellation can amplify rounding by up to that factor. It is within this suite's 10⁻⁶ tolerance and is not counted as a failure. It is a known accuracy bound, not a guarantee of ~10⁻¹³ accuracy everywhere. The same Laurent path, and so the same value, is used in V4.3 and V4.3.1.

### General rational fuzz (3,000 distinct expressions, 3,235 draws; V4.3 and V4.3.1)

- 2,971 accepted (990 general path, 1,981 Laurent path). 29 rejected: 14 identically zero denominators, 13 over the degree/complexity limit, 2 "Expression too long". All are listed in `rational_rejected.txt`.
- 11,884 axis-angle domain checks, 1,228 axis-angle value checks and 17,517 generic-angle value checks. **0 failures.**
- 1,811 off-axis exclusions reported by the app; **all 1,811 confirmed** by a vanishing divisor in the reference.
- Completeness scan: 111 flags, **all 111 axis artifacts**. Each was a divisor that vanishes to high order at 0°, 90°, 180° or 270° (already excluded by the app) and stays below 10⁻⁹ for some distance from the axis. All flags are in `rational_scan_flags.json`. Detector self-test: 4/4 hidden exclusions caught, 4/4 quiet when shown.
- Largest scaled disagreement 1.00×10⁻¹² at 0.551°. Adjudicated with 60 digits: the **app's** error was 3.8×10⁻¹⁷ and the **reference's** was 1.0×10⁻¹².
- V4.1 is not run on this suite, because it rejects non-monomial divisors by design.

### Hand-written singularity cases (21)

V4.3 and V4.3.1: 21/21 pass. V4.1: 14/14 Laurent cases pass. The 7 general-denominator cases are rejected, as documented for V4.1. Displays and exclusions are in `singularity_cases.json`.

### Near-pole precision (8 values, 50-digit mpmath)

Worst relative error **4.8×10⁻¹⁶** in all three versions. For example, `(1-sin)^4/cos^8` at 89.999° gives 0.06250000001903859, against the true 0.0625000000190385887…; naive double precision gives 0.06250001856853964. At 89.999999° naive evaluation gives 0.0176 (wrong in the first digit), while the app gives 0.06250000000000001.

### Display round trip (V4.3.1)

3,000 distinct random expressions plus 10 hand-picked ones; 856 used the general path. 850 had their raw input typeset; 6 already used a recognized short form. 6,800 round-trip value comparisons. **0 failures.**

### Browser smoke test

| | V4.1 | V4.3 | V4.3.1 |
|---|---|---|---|
| Page errors | none | none | none |
| 2 / 6 crossing presets | 2 / 6 | 2 / 6 | 2 / 6 |
| Example crossing | `= cos` | `= cos` | `= cos` |
| Empty prompt color | **orange** (expected; fixed in V4.2), recorded as a failure | muted | muted |
| General answer `1/(2*sin-1)` | rejected (V4.1 grammar) | `1/(2*sin-1)` (raw) | `1 / (2 · sin − 1)` |
| 390 px overflow | none | none | none |

Screenshots are kept only for V4.3.1 (`results/v4.3.1/browser_*.png`).

## Limitations

- The reference evaluator uses double precision. Its disagreement with the app bounds the *difference*, not the app's error. Only the worst case of each run, and the eight near-pole values, are adjudicated at high precision.
- Generic-angle checks skip values above 10⁶ (10⁵ in the rational suite) and angles within 1° (Laurent) or 0.05° (rational) of an axis or within 0.05° of a reported exclusion. The tolerance is 10⁻⁶ scaled; actual disagreements were far smaller.
- The completeness scan uses a 0.05° grid and a 2×10⁻³ pre-filter, and reports at most one flag per expression. It could miss two exclusions closer together than the grid, or a divisor zero whose neighborhood never drops below the pre-filter on the grid. Exclusions within 0.2° of an axis are not scanned.
- The random generators cover the documented grammar, but not uniformly: expression depth is at most 3 levels, integer constants are 1–3, and exponents are in {−3…3}. Hand-written cases cover specific known behaviors.
- Domain checks at axis angles use exact 0/±1 sine and cosine values. Off-axis domain checks are numerical.
- All results are finite samples on one machine. They are not proofs of correctness or universal accuracy.

## Reproduce

From the repository root:

```sh
python -m pip install mpmath playwright
python -m playwright install chromium        # or set CHROMIUM_PATH to an existing Chrome/Chromium
bash research/verification/independent_review/run_all.sh Trig_Atlas_v4_1_Reliability.html results/v4.1
bash research/verification/independent_review/run_all.sh Trig_Atlas_v4_3_Rational.html results/v4.3 --rational
bash research/verification/independent_review/run_all.sh Trig_Atlas_v4_3_1_Presentation.html results/v4.3.1 --rational --display
```

Node.js 18 or later is required (BigInt). The fuzz scripts take `--n`, `--seed` and `--out`. The general rational fuzz takes several minutes on two CPU cores, because of the completeness scan. The Laurent fuzz takes from seconds (V4.1) to about two minutes (V4.3+), and everything else takes seconds. Results are deterministic for a given seed, apart from timing and screenshots.

Provenance notes. The V4.3 `fuzz_rational` output was produced by a standalone invocation of the same script before `run_all.sh` was used for that folder. The `worst_case_*` logs for V4.1, V4.3 and V4.3.1 were produced with the same `mp_reference.py` command that `run_all.sh` now runs, added after those runs. The V4.1 browser smoke test exits with status 1 because of the orange prompt, as recorded in its log.
