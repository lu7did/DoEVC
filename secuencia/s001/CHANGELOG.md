# CHANGELOG

## [1.0 build 018] - 2026-06-08

### Added

- `plot_simulation()` implementing story F1 to render deterministic backlog and
  technical debt trajectories as a PNG using matplotlib in non-interactive
  mode.
- Regression tests proving the plot is exported as a non-empty PNG file.

## [1.0 build 017] - 2026-06-08

### Added

- `load_and_run()` implementing story E3 by reconstructing parameters and a
  registered policy from a saved JSON scenario and replaying the simulation.
- Regression tests proving the E2→E3 round-trip reproduces the same
  deterministic sprint states and rejects unknown policy names.

## [1.0 build 016] - 2026-06-08

### Added

- `save_scenario()` implementing story E2 to persist parameters, policy name,
  and seed as standard JSON for reproducible experiments.
- Regression tests proving the JSON output is loadable with `json.load()` and
  contains the expected scenario fields.

## [1.0 build 015] - 2026-06-08

### Added

- `export_sprint_states_csv()` and `export_metrics_csv()` implementing story
  E1 for deterministic sprint trajectories and aggregate Monte Carlo metrics.
- Regression tests proving the generated CSV files are readable with the
  standard `csv` module and contain the documented structure.

## [1.0 build 014] - 2026-06-08

### Added

- `compare_policies()` plus deterministic and Monte Carlo comparison row types
  to evaluate multiple policies on the same scenario and return a comparative
  table with C3 metrics.
- Regression tests proving the comparison table includes all evaluated
  policies, yields distinct outcomes, and reuses the caller objective in Monte
  Carlo mode.

## [1.0 build 013] - 2026-06-08

### Added

- `OptimalLocalPolicy` implementing story D3 by choosing the locally optimal
  remediation fraction from the current sprint state using the configurable
  economic objective and fixed-`u` grid search.
- Integration tests proving the new policy remains interchangeable via
  `Policy` and beats at least one heuristic policy in a known scenario.

## [1.0 build 012] - 2026-06-04

### Added

- Explicit B4 integration coverage proving the `Policy` protocol lets
  `DebtFirstPolicy`, `BacklogFirstPolicy`, and `ProportionalDebtPolicy`
  interchangeably drive `simulate_deterministic_sprints()`.

## [1.0 build 011] - 2026-06-04

### Added

- Explicit regression coverage for story B3 proving `ProportionalDebtPolicy`
  remains selectable from `simulate_deterministic_sprints()`, applies the
  documented `D_k / (B_k + D_k)` heuristic, and stays inside `[0, 1]`.

## [1.0 build 010] - 2026-06-04

### Added

- Explicit regression coverage for story B2 proving `BacklogFirstPolicy`
  remains selectable from `simulate_deterministic_sprints()`, keeps
  `u_k = 0` while backlog exists, and switches to `u_k = 1` once only
  technical debt remains.

## [1.0 build 009] - 2026-06-04

### Added

- Explicit regression coverage for story B1 proving `DebtFirstPolicy` remains
  selectable from `simulate_deterministic_sprints()` and switches from
  `u_k = 1` to `u_k = 0` as soon as technical debt reaches zero.

## [1.0 build 008] - 2026-06-02

### Added

- `EconomicObjectiveFunction` implementing story D2 with configurable weights
  for delivered functionality, residual debt penalty, and sprint penalty.
- Integration of the economic objective with D1 grid search and Monte Carlo
  economic-value metrics.
- Regression tests covering known objective scores, negative-weight rejection,
  and scenarios where different weights choose different optimal remediation
  fractions.

## [1.0 build 007] - 2026-06-02

### Added

- `FixedRemediationPolicy`, `GridSearchEvaluation`, `GridSearchResult`, and
  `search_optimal_remediation_fraction()` implementing story D1 for fixed-`u`
  grid optimization.
- Regression tests covering known minimization and maximization scenarios,
  configurable step sizes, and the `D_k = 0 => u_k = 0` edge case.

## [1.0 build 006] - 2026-06-02

### Added

- Per-run Monte Carlo output metrics for convergence sprints, final backlog,
  final technical debt, and average remediation fraction.
- `aggregate_metrics()` with mean, standard deviation, min, max, and percentile
  summaries across known Monte Carlo runs.
- `export_monte_carlo_metrics_csv()` for stable CSV export of final per-run
  metrics.

## [1.0 build 005] - 2026-06-02

### Added

- `Policy`, `DebtFirstPolicy`, `BacklogFirstPolicy`, and
  `ProportionalDebtPolicy` to provide the interchangeable policy interface
  required by the Monte Carlo engine.
- `simulate_deterministic_sprints()` and `run_monte_carlo()` implementing story
  C2 with seeded reproducibility, per-run outputs, and aggregate results.
- Regression tests covering policy behavior, engine integration,
  reproducibility, and exact Monte Carlo run counts.

## [1.0 build 004] - 2026-06-02

### Added

- `UniformParameterSampler` and `sample_uniform_parameters()` implementing
  story C1 with reproducible uniform draws for `s`, `gamma`, `theta`,
  `(1 - beta)`, and `lambda_`.
- Regression tests covering seeded reproducibility, reseeding, fixed-seed
  sampling, and the documented parameter intervals.

## [1.0 build 003] - 2026-05-20

### Added

- `SprintState` and `simulate_sprint()` implementing story A3 for one-sprint
  deterministic state transitions with a fixed remediation fraction.
- Regression and property-based tests covering the sprint formulas, clamping to
  non-negative backlog and debt, and validation of `u_k` inside `[0, 1]`.

## [1.0 build 002] - 2026-05-20

### Added

- `calculate_effective_velocity()` implementing story A2 with the formula
  `V_k = V_0 / (1 + gamma * D_k)`.
- Unit and property-based tests covering zero debt, decreasing velocity under
  increasing debt, formula compliance, and invalid negative debt.

## [1.0 build 001] - 2026-05-20

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
