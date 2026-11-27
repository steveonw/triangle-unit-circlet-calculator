# Trig Atlas V4.4 numerical optimization experiment

**Status:** experimental evaluation study, not a new application release. The archived V4.3 and V4.3.1 applications were not modified. The numerical engine of V4.3.1 is byte-for-byte identical to V4.3 (direct comparison of the extracted `TA` blocks from GitHub). The local run used the original V4.3 file, SHA-256 `8f0f2a3eaf1c5967ef6123e6008b734f4be575e78b17dfa3ecfd88c12d5c6fa9`; the extracted engine SHA-256 was `d15f5bf58984ca843d35501540e2b9afd796f6de4248d46cd68129da43a3b340`, matching the independent V4.3.1 review.

Repository: https://github.com/steveonw/triangle-unit-circlet-calculator

## Objective

The independent reviewer found a Laurent expression whose scaled numerical error was about 2.83e-11, compared with high-precision arithmetic. The existing evaluator uses scaled Horner evaluation, switching to exact BigInt polynomial evaluation on the binary64 half-angle coordinate `t` when `abs(v) < bound * 1e-10`. Compare earlier switching thresholds, always-exact evaluation, direct original-expression evaluation, expanded canonical algebra, and the existing readable expression (with and without a stable conjugate rewrite for `1 +/- sin` or `1 +/- cos`). The threshold trials use the original chart implementation except for the threshold and measurement instrumentation. They do not change the parser, symbolic representation, domain, roots, hole/pole limits, or general rational evaluation.

## Reproduction

Requires Python 3, mpmath and Node.js with BigInt support. Tested on Linux, Node.js v22.16.0, Python 3.13.5, mpmath 1.3.0, AMD EPYC 9V74 CPU. From the extracted package directory:

```sh
python -m pip install mpmath
python benchmark_optimizer.py Trig_Atlas_v4_3_Rational.html
python probe_conditioning.py Trig_Atlas_v4_3_Rational.html > conditioning_results.json
```

The same scripts can take the V4.3.1 HTML as their input. `optimizer_results.json` contains numerical and timing summaries, all rejection records, worst examples, environment and hashes. `optimizer_workload.json` contains the exact generated inputs; they are reproducibly generated with Python random seed 20261127 and angle seed 20261128. `optimizer_results.log` is recorded stdout. `conditioning_results.json` contains the separate conditioning investigation and 48 root-centered probes. No external browser dependencies are needed for these math-only experiments.

## Workload and methods

2,025 distinct expression strings: 1,100 randomized Laurent expressions, 500 random rational expressions, 204 near-cardinal cancellation cases, 120 interior cancellation cases, 90 near-rational-pole expressions, 10 targeted cases, and one reviewer case. 2,013 accepted (1,461 Laurent and 552 general); 11 identically zero denominators and one complexity rejection. Six seeded generic angles per expression, with additional targeted angles at offsets of 1e-3, 1e-6 and 1e-9 degrees near selected roots and axes. No exact original exclusions enter numerical comparisons. The engine's reported root representatives are used to choose probes; this experiment is not a proof of root completeness. All 15,211 finite-reference points were compared with 180-digit mpmath using an independent literal-expression parser/evaluator. The reference uses the exact binary64 degree input. Error is `abs(estimate - reference) / max(1, abs(reference))`; nonfinite results are counted separately, not silently treated as zero error.

The conventional and displayed-expression baselines compile mathematical expressions to whitelisted arithmetic functions of locally computed binary64 sine and cosine. The expanded Laurent baseline evaluates the canonical polynomial and denominator directly in sine/cosine coordinates; the expanded general baseline uses ordinary binary64 Horner on the exact reduced rational charts. The readable-form baseline evaluates the actual display string, which can be a recognized monomial, factored form, canonical polynomial or unchanged input. The stable-readable variant rewrites canceling offsets using `1 +/- u = v^2/(1 -/+ u)` when the sign and value indicate cancellation. These are experimental numeric evaluators, not newly certified simplification engines or domain authorities. Every timed strategy checks the existing original-domain restrictions. 299 Laurent expressions had factored display results; all display expressions parsed in the independent benchmark grammar. The five threshold trials (`1e-8`, `1e-6`, `1e-4`, `1e-2`, always exact) use the same original Laurent chart formula with different switch conditions; the general rational engine remains unchanged for all threshold trials.

Seven timed repetitions in seeded randomized order, after warmup, per strategy and engine path. The Laurent workload had 42,884 evaluations per repetition; setup, symbolic compilation, reference calculation, and browser rendering are excluded. Timing includes angle conversion and domain checks, plus the same finite-check/checksum overhead. Results are local to this Node/CPU workload, not an end-to-end or general CAS benchmark. The alternating development/holdout labels in the JSON are descriptive subsets, not an independently sampled held-out study; the targeted generation correlates some coefficients with those subsets.

## Main results

Independent exact Fraction cardinal-domain checks: 8,052; zero discrepancies. 45,370 boundary comparisons between threshold variants and baseline, including selected general roots and cardinal values: zero discrepancies. The unmodified baseline and instrumented default-threshold evaluator were bit-identical at every numerical point tested. The threshold comparisons reuse the original domain guard, so the boundary comparison is a regression check, not an independent root proof.

### Laurent path (10,721 evaluation points)

| Strategy | 99th-percentile scaled error | Max scaled error | Errors > 1e-12 | Median ns/eval | Exact fallback fraction* |
|---|---:|---:|---:|---:|---:|
| Conventional direct | 0.271 | 1 | 547 | 518.3 | — |
| Expanded canonical | 6.77e62 | 4.27e109 | 1109 | 1514.4 | — |
| Readable display | 1.49e-8 | 2.54 | 340 | 588.4 | — |
| Stable readable display | 1.42e-8 | 0.00680 | 335 | 578.3 | — |
| Current (1e-10) | 2.38e-10 | 1.08e-8 | 151 | 766.9 | 4.525% |
| 1e-8 | 1.34e-12 | 5.63e-9 | 113 | 745.1 | 5.289% |
| **1e-6** | **1.02e-12** | **5.15e-9** | **108** | **782.7** | **6.109%** |
| 1e-4 | 1.13e-12 | 5.15e-9 | 110 | 844.7 | 7.080% |
| 1e-2 | 1.13e-12 | 5.15e-9 | 110 | 894.0 | 8.485% |
| Always exact | 1.13e-12 | 5.15e-9 | 110 | 2502.4 | 100% |

*Among the 10,607 nonzero-chart, nonzero-coordinate evaluations eligible for the Horner fallback; always-exact still bypasses zero charts and exact cardinal limits. No Laurent results were nonfinite. Maxima and percentiles are workload statistics, not analytic error bounds. Larger cutoff triggers exact evaluation sooner. The 1e-6 cutoff increased fallback count from 480 to 648, and measured median time by about 2.1%; repetition ranges overlap (baseline 673–1057 ns, 1e-6 697–985 ns), so the experiment does not establish a precise overhead.

On the 6,594 ordinary random Laurent points, baseline maximum scaled error 3.7453e-10 decreased to 3.5249e-14 at the 1e-6 threshold. The reviewer case at 313.9 degrees went from 2.8324e-11 to 1.7488e-16. On near-cardinal cancellation cases, the stable readable candidate achieved maximum error 3.28e-15; the 1e-2 chart cutoff achieved 1.77e-15. The direct and expanded methods can catastrophically lose cancellation. The stable readable strategy is not globally optimal: its worst random Laurent error was 0.0068.

Recommendation: treat 1e-6 as the best tested *candidate* cutoff for the next release, not as a proven universal threshold. Always-exact took approximately 3.3 times the baseline time and did not resolve coordinate conditioning. Confirm the candidate on the archived larger independent suite and fresh high-precision adversarial inputs before changing the app.

### General rational path (4,490 points)

The original exact-dyadic numerator/denominator evaluator is unchanged by the Laurent thresholds. All original evaluator results were finite in this sample. Its maximum scaled error was 2.3522e-5, at `1/(2*sin-1)^3` evaluated at 30.000000001 degrees. For the ordinary random rational group (not the deliberately near-pole family), maximum was 6.36e-13. The ordinary floating-Horner rational baseline produced 156 nonfinite results over the general workload, as well as large finite errors. The direct original-expression baseline had four nonfinite results; the stable-readable variant had none but is not a uniformly accurate replacement. The measured general baseline median was 2428.9 ns/eval; the threshold trials have the same general algorithm and their timing differences are noise.

## Second experiment: polynomial cancellation versus input-coordinate conditioning

Evaluate the exact chart polynomials in 180-digit arithmetic at (a) the high-precision tangent-half-angle coordinate and (b) the exact dyadic value of the actual binary64 coordinate. Compare both to the independent original-expression reference.

| Case | Original engine error | High-precision chart at binary64 t | High-precision chart at high-precision t |
|---|---:|---:|---:|
| Reviewer expression, 313.9° | 2.83e-11 | 1.83e-15 | ~7.73e-177 |
| `10000000*(4*sin-3*cos)`, 36.86989764684402° | 5.15e-9 | 5.15e-9 | ~1.30e-174 |
| `1/(2*sin-1)^3`, 30.000000001° | 2.35e-5 | 2.35e-5 | ~1.01e-149 |

The tiny residuals in the last column are finite-reference arithmetic, not exact mathematical errors. The reviewer case is dominated by polynomial evaluation cancellation. The latter two cases are dominated by rounding the half-angle coordinate before exact polynomial evaluation. Exact arithmetic in a rounded coordinate does not supply high-precision trigonometry.

## Root-centered proof-of-concept

For a known exact angle alpha, evaluate `sin(theta)-sin(alpha)` as `2*cos((theta+alpha)/2)*sin((theta-alpha)/2)`. This preserves the small angular difference directly and avoids subtracting two nearly equal sine values. Also `sin(theta)-cos(theta) = sqrt(2)*sin(theta-45°)` and analogous phase-shift identities. For three expressions and their six certified rational-degree roots, tested both sides at four offsets (48 points):

| Nominal offset from root | Current engine maximum scaled error | Root-centered maximum scaled error |
|---|---:|---:|
| 0.001° | 1.66e-11 | 5.59e-16 |
| 0.000001° | 1.66e-8 | 7.87e-16 |
| 0.000000001° | 2.35e-5 | 5.35e-16 |
| 0.000000000001° | 1.45e-2 | 5.74e-16 |

The targeted centered identities are mathematically equivalent for these known roots. This experiment uses exact binary64 input degrees, not a promise about angle-measurement accuracy. Arbitrary irrational roots need their own high-precision representations/offset calculations and more general verified factorization. The root-centered method has NOT been integrated into the Atlas; no general root-centered performance benchmark or browser regression was done. Do not assume a root's rounded displayed angle is an exact root.

## Next steps

1. Candidate V4.4 reliability update: switch Laurent fallback cutoff from 1e-10 to 1e-6, preserve prior release and engine domain behavior, rerun all maintained and independent suites.
2. Investigate condition-aware strategies rather than relying exclusively on polynomial cancellation. Separate evaluation rounding from coordinate rounding; test exact certified root-centered forms first, then high-precision coordinate evaluation for general roots. Consider a numerical precision warning for extremely sensitive values.
3. Keep symbolic equivalence, human-readable display, numerical strategy, and original domain separate. Shorter displays alone do not imply better numerical behavior. Preserve the visual octahedral discovery interface.

The archived run is finite-sample numerical evidence, not proof of universal numerical accuracy, an educational study, or a deployed release. All released HTML files are unchanged.
