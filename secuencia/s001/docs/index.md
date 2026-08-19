# DoEVC s001 documentation

This directory contains the human-maintained documentation for sequence s001.

Current implemented functionality includes:

- `ProjectMetadata` for validated sequence metadata
- `ModelParameters` for deterministic model configuration
- `calculate_effective_velocity()` for debt-adjusted productivity

Generated API documentation is produced with:

```bash
python -m pdoc doevc_s001 -o site
```
