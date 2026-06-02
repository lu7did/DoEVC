# DoEVC s001

DoEVC s001 is the first sequence scaffold for the DoEVC project. It is a
Python 3.13 package prepared for iterative development with tests,
documentation, and CI automation.

## Status

- Version: 1.0
- Build: 005
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
- `doevc_s001.Policy`: common policy protocol for deterministic and Monte Carlo
  execution.
- `doevc_s001.DebtFirstPolicy`, `doevc_s001.BacklogFirstPolicy`, and
  `doevc_s001.ProportionalDebtPolicy`: interchangeable baseline remediation
  policies.
- `doevc_s001.simulate_deterministic_sprints()`: chains up to `K` sprints using
  any `Policy`.
- `doevc_s001.run_monte_carlo()`: executes reproducible Monte Carlo batches and
  returns both individual run results and aggregate outcomes.
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
