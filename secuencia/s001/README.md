# DoEVC s001

DoEVC s001 is the first sequence scaffold for the DoEVC project. It is a
Python 3.13 package prepared for iterative development with tests,
documentation, and CI automation.

## Status

- Version: 1.0
- Build: 020
- Python: 3.13
- License: Creative Commons CC0 1.0

`CONTEXT.md` is preserved in this sequence as the construction reference.

## Available functionality

- `doevc_s001.ProjectMetadata`: validated metadata container for sequence s001.
- `doevc_s001.ProjectMetadata.to_dict()`: serialization helper.
- `doevc_s001.ModelParameters`: validated parameter structure for the model.
- `doevc_s001.ModelParameters.to_dict()`: serialization helper for simulation
  inputs.
- `doevc_s001.UniformParameterSampler`: reproducible uniform sampler for story
  C1 model parameters.
- `doevc_s001.sample_uniform_parameters()`: convenience helper to sample one
  complete `ModelParameters` instance from a seed.
- `doevc_s001.Policy`: story B4 common protocol that lets deterministic and
  Monte Carlo engines accept interchangeable policy objects via `decide_u(...)`.
- `doevc_s001.DebtFirstPolicy`: naive story B1 baseline with `u_k = 1` while
  technical debt remains and `u_k = 0` once it reaches zero.
- `doevc_s001.BacklogFirstPolicy`: story B2 baseline with `u_k = 0` while
  backlog remains, then `u_k = 1` when only technical debt is left.
- `doevc_s001.ProportionalDebtPolicy`: story B3 baseline using
  `u_k = D_k / (B_k + D_k)` with safe handling of the zero-work edge case.
- `doevc_s001.simulate_deterministic_sprints()`: chains up to `K` sprints using
  any `Policy`.
- `doevc_s001.run_monte_carlo()`: executes reproducible Monte Carlo batches and
  returns both individual run results and aggregate outcomes.
- `doevc_s001.aggregate_metrics()`: computes mean, standard deviation, min, max,
  and percentiles across Monte Carlo run metrics.
- `doevc_s001.export_monte_carlo_metrics_csv()`: exports stable per-run metric
  columns for external analysis.
- `doevc_s001.FixedRemediationPolicy`: reusable constant-`u` policy for grid
  search and deterministic comparisons.
- `doevc_s001.EconomicObjectiveFunction`: configurable economic score combining
  delivered value, residual debt penalty, and sprint penalty weights.
- `doevc_s001.OptimalLocalPolicy`: story D3 policy that recomputes the
  locally optimal remediation fraction from the current sprint state.
- `doevc_s001.compare_policies()`: story D4 helper that evaluates the same
  scenario across multiple policies in deterministic or Monte Carlo mode.
- `doevc_s001.export_sprint_states_csv()`: story E1 helper that exports one
  CSV row per deterministic sprint state.
- `doevc_s001.export_metrics_csv()`: story E1 helper that exports aggregate
  Monte Carlo metric summaries to CSV.
- `doevc_s001.save_scenario()`: story E2 helper that stores parameters,
  policy name, and seed in a reproducible JSON scenario file.
- `doevc_s001.load_and_run()`: story E3 helper that rebuilds a saved scenario
  from JSON and replays the deterministic simulation.
- `doevc_s001.plot_simulation()`: story F1 helper that writes a PNG chart for
  deterministic sprint backlog and technical debt trajectories.
- `doevc_s001.plot_optimal_u_distribution()`: story F2 helper that writes a
  PNG boxplot for the per-run optimal remediation distribution in Monte Carlo
  experiments.
- `doevc_s001.plot_sensitivity_heatmap()`: story F3 helper that writes a PNG
  heatmap for the average remediation produced by a policy across two named
  parameter sweeps.
- `doevc_s001.search_optimal_remediation_fraction()`: evaluates a fixed `u`
  grid and returns the remediation fraction that optimizes a configurable
  objective.
- `doevc_s001.calculate_effective_velocity()`: computes `V_k` from `V0`,
  `gamma`, and the current technical debt.
- `doevc_s001.SprintState`: immutable snapshot for a single sprint transition.
- `doevc_s001.SprintState.to_dict()`: serialization helper for sprint outputs.
- `doevc_s001.simulate_sprint()`: advances the deterministic model one sprint
  with a fixed remediation fraction.
- `doevc_s001.get_version_label()`: human-readable version label.

## Repository structure

| Path | Purpose |
| --- | --- |
| `src/doevc_s001/` | Python package source code |
| `tests/` | Automated test suite |
| `docs/` | Basic project documentation |
| `script/` | Auxiliary scripts excluded from CI validation scope |
| `ejemplos/` | Example assets excluded from CI validation scope |

## Local setup

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Local validation

```bash
ruff check src tests
black --check src tests
pydocstyle src/doevc_s001
mypy src/doevc_s001
pyright src/doevc_s001
pytest
bandit -q -r src/doevc_s001
python -m pdoc doevc_s001 -o site
```

## Documentation

Basic documentation is written in `docs/` and API documentation is generated
with `pdoc`.
