TRIG ATLAS - PYTHON REPRODUCTION PACKAGE

This archive contains the Python research scripts from the full research package, without the paper or HTML prototypes. Scripts are copied unchanged.

Requirements: Python 3; NumPy for crossings, calculus, and networks (pip install numpy). The symbolic calculator uses only the standard library.

Suggested runs from the extracted directory:
  python trig_atlas_calculator_reviewed.py 'sin sec cot' --angle 37
  python trig_atlas_calculator_reviewed.py --benchmark
  python trig_crossings.py
  python trig_calculus_monte_carlo.py
  python trig_atlas_ten_networks.py

Use the reviewed calculator for current tests. The earlier calculator is in prototype_history/ for comparison; it predates a domain-check correction. The results/ directory contains saved reference outputs. Timings depend on hardware; simulations use fixed random seeds. These scripts test mathematical models and are not evidence of a physical device or human learning speed.

Suggested independent review: inspect domain preservation, verify geometry and numerical assumptions, rerun tests, and compare performance against optimized conventional methods.
