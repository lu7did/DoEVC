# DoEVC

DoEVC is a Python 3.13 package for the UADER PI-B 230/24 project. It provides
the initial scaffold for a technical debt simulator with Monte Carlo analysis,
optimization, persistence, and reporting.

## Status

- Version: 1.0
- Build: 001
- Python: 3.13
- License: Creative Commons CC0 1.0

`CONTEXT.md` remains in the repository as the source of the construction rules
used for this stage.

## Available functionality

- `doEVC.ModelParameters`: validated container for the core model parameters.
- `doEVC.ModelParameters.to_dict()`: serialization helper for persistence and
  testing.
- `doEVC.get_version_label()`: returns the current human-readable version label.

## Repository structure

| Path | Purpose |
| --- | --- |
| `src/doEVC/` | Python package source code |
| `tests/` | Automated test suite |
| `docs/` | Basic project documentation |
| `script/` | Auxiliary scripts excluded from CI validation scope |
| `ejemplos/` | Example assets excluded from CI validation scope |
| `.github/workflows/` | GitHub Actions automation |
| `doc/` | Existing reference documentation provided with the repository |

## Local setup

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Local validation

```bash
ruff check src tests
black --check src tests
pydocstyle src/doEVC
mypy src/doEVC
pyright src/doEVC
pytest
bandit -q -r src/doEVC
python -m pdoc doEVC -o site
```

## Documentation

Basic documentation is written in `docs/` and API documentation is generated
with `pdoc`.

## Backlog summary

- Epic A: deterministic core model.
- Epic B: decision policies.
- Epic C: Monte Carlo simulation.
- Epic D: optimization.
- Epic E: persistence and reproducibility.
- Epic F: visualization and reporting.
