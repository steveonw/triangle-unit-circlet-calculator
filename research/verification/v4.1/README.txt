TRIG ATLAS V4.1 - RELIABILITY RELEASE

Open the HTML in a browser. No dependencies or network required for the app.

V4.1 uses local tangent-half-angle rational charts, exact cancellation of vanishing factors, scaled Horner evaluation and an exact dyadic polynomial fallback. Original domains are preserved; excluded cardinal angles are classified by local order. The final value is binary64. Supported expressions are same-angle Laurent polynomials with monomial denominators, subject to complexity bounds, not a general-purpose CAS.

Run the math tests (Python 3, Node.js, mpmath, SymPy):
  python -m pip install mpmath sympy
  python test_v41_math.py Trig_Atlas_v4_1_Reliability.html

Run browser tests (Python, Playwright, Chromium):
  python -m pip install playwright
  python -m playwright install chromium
  python test_v41_browser.py Trig_Atlas_v4_1_Reliability.html
Optionally set CHROMIUM_PATH to an existing Chromium executable. The browser test loads the HTML content directly.

The tests are finite sampled checks, not proof of universal numerical accuracy or educational effectiveness. No classroom study or low-end hardware performance test has been conducted.
