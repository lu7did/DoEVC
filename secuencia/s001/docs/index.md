# DoEVC s001 documentation

This directory contains the human-maintained documentation for sequence s001.

The current public API includes `ProjectMetadata`, `ModelParameters`,
`UniformParameterSampler`, `sample_uniform_parameters()`, `Policy`,
`DebtFirstPolicy`, `BacklogFirstPolicy`, `ProportionalDebtPolicy`,
`simulate_deterministic_sprints()`, `run_monte_carlo()`, `aggregate_metrics()`,
`export_monte_carlo_metrics_csv()`, `calculate_effective_velocity()`,
`FixedRemediationPolicy`, `EconomicObjectiveFunction`,
`search_optimal_remediation_fraction()`, `SprintState`, `simulate_sprint()`,
and `get_version_label()`.

Generated API documentation is produced with:

```bash
python -m pdoc doevc_s001 -o site
```
