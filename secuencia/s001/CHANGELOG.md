# CHANGELOG

## [1.0 build 004] - 2026-08-19

### Added

- `simulate_deterministic_sprints()` implementing story A4 to chain `K`
  fixed-split sprints into one deterministic trajectory.
- Regression tests covering known trajectories, explicit initial states, and
  early stop behavior once backlog and debt are both zero.

## [1.0 build 003] - 2026-08-19

### Added

- `SprintState` and `simulate_sprint()` implementing story A3 for one-sprint
  deterministic state transitions with a fixed remediation fraction.
- Regression and property-based tests covering the sprint formulas, clamping to
  non-negative backlog and debt, and validation of `u_k` inside `[0, 1]`.

## [1.0 build 002] - 2026-08-19

### Added

- `calculate_effective_velocity()` implementing story A2 with the formula
  `V_k = V_0 / (1 + gamma * D_k)`.
- Unit and property-based tests covering zero debt, decreasing velocity under
  increasing debt, formula compliance, and invalid negative debt.

## [1.0 build 001] - 2026-08-19

### Added

- `ModelParameters` as the validated Python structure for the deterministic
  model parameters required by story A1.
- Regression tests for serialization, printable representation, and invalid
  negative values for the model parameters.

## [1.0 build 000] - 2026-05-20

### Added

- Initial scaffold for sequence `s001` with source package, tests, docs,
  examples, and scripts directories.
- GitHub Actions workflow dedicated to validating `secuencia/s001`.
- Base `ProjectMetadata` object with validation and serialization helpers.
