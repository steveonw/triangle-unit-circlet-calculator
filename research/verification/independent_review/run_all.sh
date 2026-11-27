#!/usr/bin/env bash
# Run the independent review checks for one Trig Atlas HTML file.
# Usage (from the repository root):
#   bash research/verification/independent_review/run_all.sh Trig_Atlas_v4_3_1_Presentation.html results/v4.3.1 [--rational] [--display]
#   --rational  also run fuzz_rational.js (V4.3 and later only)
#   --display   also run display_roundtrip.js and require typeset answers in the browser (V4.3.1 and later)
# Set CHROMIUM_PATH to use an existing Chrome/Chromium for the browser check.
set -u
APP="$1"; OUT="research/verification/independent_review/$2"; shift 2
S=research/verification/independent_review/scripts
RATIONAL=0; DISPLAY=0
for a in "$@"; do case "$a" in --rational) RATIONAL=1;; --display) DISPLAY=1;; esac; done
mkdir -p "$OUT"
status=0
run() { local name="$1"; shift; echo "== $name"; "$@" > "$OUT/$name.log" 2>&1; local rc=$?; echo "exit $rc" >> "$OUT/$name.log"; tail -n 3 "$OUT/$name.log"; [ $rc -eq 0 ] || status=1; }
sha256sum "$APP" > "$OUT/SHA256.txt"
run fuzz_laurent       node "$S/fuzz_laurent.js" "$APP" --out "$OUT"
[ $RATIONAL -eq 1 ] && run fuzz_rational node "$S/fuzz_rational.js" "$APP" --out "$OUT"
# Adjudicate the largest app-vs-reference disagreement of each fuzz run with 60-digit arithmetic.
run worst_case_laurent python3 "$S/mp_reference.py" "$OUT/laurent_summary.json"
[ $RATIONAL -eq 1 ] && run worst_case_rational python3 "$S/mp_reference.py" "$OUT/rational_summary.json"
run singularity_cases  node "$S/singularity_cases.js" "$APP" --out "$OUT"
run near_pole_mpmath   python3 "$S/near_pole_mpmath.py" "$APP" --out "$OUT"
[ $DISPLAY -eq 1 ] && run display_roundtrip node "$S/display_roundtrip.js" "$APP" --out "$OUT"
if [ $DISPLAY -eq 1 ]; then run browser_smoke python3 "$S/browser_smoke.py" "$APP" --out "$OUT" --expect-pretty
else run browser_smoke python3 "$S/browser_smoke.py" "$APP" --out "$OUT"; fi
exit $status
