# V4.3.1 verification — presentation release

Tested source: [Trig Atlas V4.3.1](../../../Trig_Atlas_v4_3_1_Presentation.html).

SHA-256: `f4153ac068cf1da07c1ba0a2b06aecdbadd62f5eec35db8ad306bf7be75cff15`
Git blob: `6547f5756fa413246f5dff45b9e192c19ead0515`

## What changed from V4.3

V4.3.1 is a presentation-only patch. The inline `TA` symbolic engine (parser, Laurent fast path, general rational engine, domain tracking, root isolation, hole/pole classification and numerical evaluation) is byte-for-byte identical to [V4.3](../../../Trig_Atlas_v4_3_Rational.html). The SHA-256 of the extracted `TA` block is `d15f5bf58984ca843d35501540e2b9afd796f6de4248d46cd68129da43a3b340` in both files.

1. **General-expression answer formatting.** When the general rational path has no shorter recognized form, V4.3 echoed the raw input in the answer box, for example `1/(2*sin-1)`. V4.3.1 typesets it as `1 / (2 · sin − 1)`. It uses spaced operators, `·` for multiplication (including implicit multiplication), `−` for minus, and superscript exponents. A constant general result such as `-3 / 2` is shown as `−3 / 2`. The formatter (`prettyExpression`, `answerText`) is in the interface layer. It uses the engine's own symbol normalization and token set, never changes `result.text`, the domain or any value, and falls back to the raw text if it cannot tokenize the input. Exponent digits are shown as the engine reads them: `sin^03` is displayed as `sin³`.
2. **Empty-input prompt color.** No change was needed. The muted prompt color was already introduced in V4.2 (`#eyeError.neutral`). An earlier external review incorrectly reported it as still orange in V4.3, based on V4.1 and a source search that missed the override. The independent browser check confirms the muted color in V4.2, V4.3 and V4.3.1, and the orange color for real errors.
3. Version labels: page title, header eyebrow and footer read 4.3.1.

## Preserved regression suites, rerun against V4.3.1

Run on 2026-11-27 (UTC) on Linux with Node.js 22.23.5, Python 3.13.18, mpmath 1.3.0, SymPy 1.14.0, Playwright 1.63.0 and Google Chrome for Testing 153.0.8010.12 (`CHROMIUM_PATH=/usr/bin/google-chrome`). The scripts were not modified. Outputs are the verbatim stdout of each run, with the exit status appended.

| Suite | Result file | Outcome |
|---|---|---|
| V4.3 rational math (`test_v43_rational.py`) | [v43_rational_results.txt](v43_rational_results.txt) | 374 inputs, 354 accepted (336 general, 18 legacy), 20 zero-denominator rejections; 6,392 exact chart values, 9,408 domain checks, 8,715 100-digit comparisons, 280 SymPy identities, 445 root classifications, 249 limits; max scaled error 2.87e-14; 0 failures |
| V4.3 browser (`test_v43_browser.py`) | [v43_browser_results.txt](v43_browser_results.txt) | Desktop and 390 px mobile PASS; no page errors |
| V4.1 math (`test_v41_math.py`) | [v41_math_results.txt](v41_math_results.txt) | 1,232 generated, 1,224 accepted; 4,896 exact, 6,120 domain, 24,480 180-digit comparisons; max scaled error 2.24e-13; 48 SymPy pole/limit checks; 0 failures |
| V4.1 browser (`test_v41_browser.py`) | [v41_browser_results.txt](v41_browser_results.txt) | Crossing, exact angle, hole/pole, 5 practice tasks, reference, calculus PASS; no horizontal overflow at 390 px |
| V4.2 display (`test_v42_display.py`, V4.2 vs V4.3.1) | [v42_display_results.txt](v42_display_results.txt) | 650 cases, 610 accepted; 544 factored displays proved by SymPy; 5,090 display-value comparisons; all PASS |

These outputs match the recorded V4.3 results line for line, as expected for an unchanged engine. They are finite-sample results, not proofs of universal accuracy.

## Independent checks

The independent review suite was also run against V4.3.1, including a new display round-trip test. Every typeset answer is fed back into the engine and must give identical exclusions and bit-identical values. See [independent_review/](../independent_review/README.md), results folder `results/v4.3.1/`.

## Reproduce

From the repository root, with the dependencies in the [research guide](../../README.md):

```sh
python research/verification/v4.3/test_v43_rational.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.3/test_v43_browser.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.1/test_v41_math.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.1/test_v41_browser.py Trig_Atlas_v4_3_1_Presentation.html
python research/verification/v4.2/test_v42_display.py Trig_Atlas_v4_2_Readability.html Trig_Atlas_v4_3_1_Presentation.html
bash research/verification/independent_review/run_all.sh Trig_Atlas_v4_3_1_Presentation.html results/v4.3.1 --rational --display
```

The browser suites write screenshots to `browser_screenshots/` in the working directory. Those screenshots are not archived here.
