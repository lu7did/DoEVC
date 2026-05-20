# DoEVC documentation

This directory contains the human-maintained documentation for the project.

Generated API documentation is produced with:

```bash
python -m pdoc doEVC -o site
```

The CI workflow runs the same command to ensure that the package documentation
can be generated on every pull request.
