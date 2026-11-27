# Trig Atlas — triangle unit circlet calculator

An interactive three-dimensional approach to trigonometric identities, symbolic calculation, domain reasoning and calculus. The original investigator proposed arranging the six trigonometric functions on an octahedron and exploring its relationships as an "eye calculator." The project was developed with AI assistance.

## Run the calculator

Download [Trig Atlas V4.1 — Reliability](Trig_Atlas_v4_1_Reliability.html) and open it in a modern browser. The standalone HTML contains all code and styling; it does not need a build step, server, or internet connection.

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
| [V1 — original octahedron](archive/v1/trig_octahedron.html) | Static trigonometric identity model |
| [V2 — three circles](archive/v2/trig_octahedron_three_circles.html) | Synchronized circles and geometric relationships |
| [V3 — calculus](archive/v3/trig_octahedron_calculus.html) | Derivatives, integrals and projection |
| [V4 — Eye Calculator](archive/v4/Trig_Atlas_v4_Eye_Calculator.html) | Integrated expression builder and guided exploration |
| [V4.1 — Reliability](Trig_Atlas_v4_1_Reliability.html) | Current stable research baseline |

The archived HTML files retain their original contents. Their Git upload dates are archival dates rather than a reconstruction of the original development chronology.

## What is established, and what is experimental?

The underlying trigonometry and much of the geometry are established mathematics. The octahedral interface, its integration with symbolic computation, and potential educational benefits are the focus of this exploration. The research paper includes numerical simulations and a limited benchmark, not a general-purpose CAS speed claim or a peer-reviewed result. Linked-module computation and optical sensing remain research directions, not demonstrated hardware.

V4.1 uses exact rational symbolic operations and local tangent-half-angle charts for improved numerical stability near excluded angles. The expression grammar is specialized to one angle and currently restricts division to monomial denominators. Recorded tests are described in the history and handover; they do not prove universal numerical accuracy.

## Contributing

Start with the AI handover and use V4.1 as the regression baseline. Preserve the original domain, geometry, and offline operation when changing the calculator. Record tests, limitations and version changes, and distinguish exact mathematical claims from simulations and proposals.

See [LICENSE](LICENSE) for the repository license.
