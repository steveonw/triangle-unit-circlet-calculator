# Trig Atlas — triangle unit circlet calculator

An interactive three-dimensional approach to trigonometric identities, symbolic calculation, domain reasoning and calculus. The original investigator proposed arranging the six trigonometric functions on an octahedron and exploring its relationships as an "eye calculator." The project was developed with AI assistance.

## Run the calculator

Download [Trig Atlas V4.3 — General rational denominators](Trig_Atlas_v4_3_Rational.html) and open it in a modern browser. The standalone HTML contains all code and styling; it does not need a build step, server, or internet connection.

- **Eye Calculator:** construct expressions by selecting vertices, edges, faces and projected crossings; inspect simplification, domain exclusions, holes, poles and graphs.
- **Identity Atlas:** explore reciprocal axes, product identities, Pythagorean relations and the eight triangular faces.
- **Calculus Lab:** follow three synchronized orthogonal unit circles, derivative triangles, definite integrals and calibrated projected-angle recovery.
- **Guided practice:** work through five challenges that connect geometry to algebra.

## Documentation and preserved versions

| Resource | Purpose |
|---|---|
| [Development history](HISTORY.md) | Origin, design evolution, experiments, reviewer feedback and roadmap |
| [AI handover](AI_HANDOFF.md) | Technical architecture, mathematical invariants, regression cases and directions for future contributors |
| [Research paper](research/Trig_Atlas_Research_Paper.md) | Exploratory theory, computational experiments, limitations and references |
| [Research & reproduction guide](research/README.md) | Original Python scripts, recorded outputs, V4.1–V4.3 verification and reproduction commands |
| [V1 — original octahedron](archive/v1/trig_octahedron.html) | Static trigonometric identity model |
| [V2 — three circles](archive/v2/trig_octahedron_three_circles.html) | Synchronized circles and geometric relationships |
| [V3 — calculus](archive/v3/trig_octahedron_calculus.html) | Derivatives, integrals and projection |
| [V4 — Eye Calculator](archive/v4/Trig_Atlas_v4_Eye_Calculator.html) | Integrated expression builder and guided exploration |
| [V4.1 — Reliability](Trig_Atlas_v4_1_Reliability.html) | Preserved reliability baseline |
| [V4.2 — Readability](Trig_Atlas_v4_2_Readability.html) | Preserved verified factored-display baseline |
| [V4.3 — General rational denominators](Trig_Atlas_v4_3_Rational.html) | Latest version: exact rational charts, original-domain root isolation and non-cardinal holes/poles |

The archived HTML files retain their original contents. Their Git upload dates are archival dates rather than a reconstruction of the original development chronology.

## What is established, and what is experimental?

The underlying trigonometry and much of the geometry are established mathematics. The octahedral interface, its integration with symbolic computation, and potential educational benefits are the focus of this exploration. The research paper includes numerical simulations and a limited benchmark, not a general-purpose CAS speed claim or a peer-reviewed result. Linked-module computation and optical sensing remain research directions, not demonstrated hardware.

V4.1 uses exact rational symbolic operations and local tangent-half-angle charts for improved numerical stability near excluded angles. V4.3 adds bounded general rational denominators and exact root isolation for original exclusions, while preserving the earlier Laurent fast path. The grammar is specialized to one angle and is not a general-purpose CAS. Recorded tests and their original source scripts are in the [research folder](research/README.md); they do not prove universal numerical accuracy.

## Contributing

Start with the AI handover and use V4.1 and V4.2 as preserved regression baselines, and V4.3 as the latest working release. Preserve the original domain, geometry, and offline operation when changing the calculator. Record tests, limitations and version changes, and distinguish exact mathematical claims from simulations and proposals.

See [LICENSE](LICENSE) for the repository license.
