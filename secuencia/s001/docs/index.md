# DoEVC s001 documentation

This directory contains the human-maintained documentation for sequence s001.

The current public API includes `ProjectMetadata`, `ModelParameters`,
`UniformParameterSampler`, `sample_uniform_parameters()`,
`calculate_effective_velocity()`, `SprintState`, `simulate_sprint()`, and
`get_version_label()`.

Generated API documentation is produced with:

```bash
python -m pdoc doevc_s001 -o site
```
