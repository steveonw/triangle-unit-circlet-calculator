# Trig Atlas research and reproducibility

This folder preserves the mathematical investigation and the associated research artifacts. It is separate from the browser application. The paper and code are exploratory, AI-assisted research; they are not a peer-reviewed result or a claim of exclusive mathematical novelty.

## Start here

- [Research paper](Trig_Atlas_Research_Paper.md) — November 26, 2026; theory, experiments, references and limitations.
- [Development history](../HISTORY.md) — chronology of the idea, prototypes and reviews.
- [AI handover](../AI_HANDOFF.md) — mathematical invariants, source architecture, limitations and next development steps.
- [V4.1 baseline](../Trig_Atlas_v4_1_Reliability.html) — original verified HTML; Git blob SHA db7a7ac9518f772d7147aea4c95eb3084b1cfcf8.
- [V4.3.1 latest release](../Trig_Atlas_v4_3_1_Presentation.html) — V4.3 engine with typeset general-expression answers; [verification](verification/v4.3.1/README.md).
- [Independent review tests](verification/independent_review/README.md) — separately written test suite with archived results for V4.1, V4.3 and V4.3.1.

## Original Python experiments

The scripts and outputs in [experiments/](experiments/) are byte-for-byte copies of the original Python reproduction package. The original calculator is retained for comparison, and the reviewed calculator contains the domain correction.

| Script | Investigation | Recorded output |
|---|---|---|
| [trig_crossings.py](experiments/trig_crossings.py) | Strict projected skew-edge crossings, complement identities, 1:2 midpoint geometry, 100,000 random directions | [crossings.txt](experiments/results/crossings.txt) |
| [trig_calculus_monte_carlo.py](experiments/trig_calculus_monte_carlo.py) | Derivatives, integration, triangle invariants, projected angle readout and measurement noise | [calculus.txt](experiments/results/calculus.txt) |
| [trig_atlas_calculator_reviewed.py](experiments/trig_atlas_calculator_reviewed.py) | Same-angle exponent algebra, original-domain tracking and precompiled evaluation benchmark | [benchmark.txt](experiments/results/benchmark.txt) |
| [trig_atlas_ten_networks.py](experiments/trig_atlas_ten_networks.py) | Ten-module chain/tree/star/ring/grid, Fourier synthesis, phase selection, synchronization and physical contact checks | [networks.txt](experiments/results/networks.txt) |
| [prototype_history/trig_atlas_calculator.py](experiments/prototype_history/trig_atlas_calculator.py) | Historical calculator before domain correction; not the recommended baseline | — |

### Reproduce the experiments

From the repository root, using Python 3 (NumPy required for geometry/network tests; the calculator only uses the standard library):

```sh
python -m pip install numpy
python research/experiments/trig_crossings.py
python research/experiments/trig_calculus_monte_carlo.py
python research/experiments/trig_atlas_calculator_reviewed.py --benchmark
python research/experiments/trig_atlas_ten_networks.py
python research/experiments/trig_atlas_calculator_reviewed.py 'sin sec cot' --angle 37
```

These are the original seeded experiments (20261126). The recorded outputs reflect the original environment. Numerical rounding, NumPy scalar printing and execution times can differ with environment. The benchmark is specific to the selected simplifiable workload and excludes setup costs as explained in the paper. The network simulations use explicit mathematical operations, not a demonstrated octahedral computer.

## V4.1 reliability verification

The [verification/v4.1/](verification/v4.1/) folder preserves the original review package's test scripts, instructions, results and checksum. The HTML is stored once, at the repository root, so the relative paths in the following commands differ from the original package README.

| File | Purpose |
|---|---|
| [test_v41_math.py](verification/v4.1/test_v41_math.py) | Seeded randomized differential testing with exact rational, 180-digit mpmath and SymPy pole/limit references; invokes Node.js on the inline symbolic engine |
| [test_v41_browser.py](verification/v4.1/test_v41_browser.py) | Playwright/Chromium interaction tests, five practice challenges, calculus and mobile layout checks; writes screenshots to browser_screenshots/ |
| [math_results.txt](verification/v4.1/math_results.txt) | Original recorded numeric test output |
| [browser_results.txt](verification/v4.1/browser_results.txt) | Original browser-test summary |
| [SHA256.txt](verification/v4.1/SHA256.txt) | SHA-256 of the exact tested baseline |
| [README.txt](verification/v4.1/README.txt) | Unmodified review-bundle instructions |

### Run the regression suite

Install Node.js and Python 3, then from the repository root:

```sh
python -m pip install mpmath sympy playwright
python -m playwright install chromium
python research/verification/v4.1/test_v41_math.py Trig_Atlas_v4_1_Reliability.html
python research/verification/v4.1/test_v41_browser.py Trig_Atlas_v4_1_Reliability.html
```

On systems with GNU coreutils, verify the app file from the repository root:

```sh
sha256sum -c research/verification/v4.1/SHA256.txt
```

The browser test optionally accepts CHROMIUM_PATH pointing to a local Chromium executable. Do not confuse the saved browser-result summary with a verbatim transcript of stdout.

The original math test reported 1,224 accepted expressions out of 1,232 generated; 4,896 exact rational comparisons, 6,120 cardinal/domain comparisons, 24,480 high-precision comparisons, zero failures, and 48 independent SymPy singularity checks. The maximum scaled numeric error was about 2.24e-13. These are finite-sample regression results, not a guarantee of universal accuracy.

## V4.2 readability verification

The [V4.2 verification report](verification/v4.2/README.md) records the new independent display suite and rerun of the original V4.1 suite against [V4.2](../Trig_Atlas_v4_2_Readability.html). Factored output is presentation-only and does not expand the supported input grammar.

## V4.3 general rational denominator verification

The [V4.3 report](verification/v4.3/README.md) documents the exact rational-chart fallback, root isolation and original-domain tracking. It includes the independent [math test](verification/v4.3/test_v43_rational.py), [browser test](verification/v4.3/test_v43_browser.py), [math results](verification/v4.3/rational_results.txt), [browser results](verification/v4.3/rational_browser_results.txt), and reruns of the preserved V4.1/V4.2 tests. From repository root:

```sh
python research/verification/v4.3/test_v43_rational.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.3/test_v43_browser.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.1/test_v41_math.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.1/test_v41_browser.py Trig_Atlas_v4_3_Rational.html
python research/verification/v4.2/test_v42_display.py Trig_Atlas_v4_2_Readability.html Trig_Atlas_v4_3_Rational.html
```

Dependencies are the same Python/Node.js/mpmath/SymPy/Playwright/Chromium tools documented above. The new suite recorded 445 root classifications and 8,715 high-precision comparisons with no failures, in addition to exact rational and domain checks. The tested app is the [V4.3 file](../Trig_Atlas_v4_3_Rational.html).

## V4.3.1 presentation verification

The [V4.3.1 report](verification/v4.3.1/README.md) records the display-only change and the unmodified reruns of all five preserved release suites against [V4.3.1](../Trig_Atlas_v4_3_1_Presentation.html). All passed, with output matching the recorded V4.3 results line for line. The `TA` engine block is byte-for-byte identical to V4.3.

```sh
python research/verification/v4.3/test_v43_rational.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.3/test_v43_browser.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.1/test_v41_math.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.1/test_v41_browser.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.2/test_v42_display.py Trig_Atlas_v4_2_Readability.html Trig_Atlas_v4_3_1_Presentation.html
```

## Independent review suite

[verification/independent_review/](verification/independent_review/README.md) contains tests written by an AI reviewer separately from the release suites, with their own reference evaluator, plus the actual outputs from running them on V4.1, V4.3 and V4.3.1. Highlights: a 40,000-distinct-expression fuzz test (0 failures on all three versions); a 3,000-expression general-rational fuzz test with confirmation of every reported off-axis exclusion and a self-tested completeness scan (0 failures); 21 hand-derived hole/pole cases; 50-digit near-pole checks; a V4.3.1 display round-trip test; and a browser smoke test. Seeds, dependencies, file hashes, every rejected expression, and the limits of each check are documented there. Rerun with:

```sh
python -m pip install mpmath playwright
bash research/verification/independent_review/run_all.sh Trig_Atlas_v4_3_1_Presentation.html results/v4.3.1 --rational --display
```

## Review findings and next questions

AI reviews reported independently reproducing core geometry, algebra and projection results. A V4 review identified catastrophic cancellation near a removable singularity in (1−sin θ)^4/cos^8 θ; V4.1 added local tangent-half-angle rational charts, exact cancellation and stable evaluation to address that issue. A subsequent AI review reported a 40,000-expression fuzz test without domain/value failures within the supported grammar, agreement with 50-digit arithmetic near singular angles, and successful browser tests. That conversational figure was later corrected by the same reviewer: its generator had cycled, so the run held only 287 distinct expressions. The reviewer then archived a corrected harness and its actual results in the [independent review suite](verification/independent_review/README.md). Those archived results, not the conversational figure, are the reproducible record. They were run by the reviewer, not the repository maintainer.

Remaining priorities: more readable factored display for general rational expressions (V4.3.1 typesets them but does not factor them), the Laurent evaluator's cancellation threshold (the independent review observed a 2.8×10⁻¹¹ relative error), stress tests for clustered roots and numerical conditioning, comparison of equivalent formula costs and stability, and a controlled learning study. The current grammar is deliberately restricted. Keep the original-domain model distinct from symbolic equivalence and numerical evaluation. More speculative optical-angle sensing and network applications need comparative experiments before claims of practical benefit.

## Archival scope

The paper's Markdown source, original Python experiments, recorded outputs, V4.1 regression scripts and results, and original HTML versions are available in Git. The separately distributed Word paper, PNG figures, ZIP packages and raw conversation/reviewer transcripts have not been uploaded as part of this text-source archive. The original numerical outputs were preserved, not regenerated during the archival commits.
