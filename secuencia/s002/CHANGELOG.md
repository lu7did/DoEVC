# Changelog

## [1.0 build 005] - 2026-10-07

### Added

- `BacklogFirstPolicy`, seleccionable desde el simulador determinista.

## [1.0 build 004] - 2026-10-07

### Added

- `DebtFirstPolicy`, seleccionable desde el simulador determinista.

## [1.0 build 003] - 2026-10-07

### Added

- `SprintState` y `simulate_sprint()` para modelar transiciones deterministas
  con una fracción fija de remediación.
- `simulate_deterministic_sprints()` para observar una trayectoria completa de
  hasta `K` sprints y detenerla cuando backlog y deuda llegan a cero.

## [1.0 build 002] - 2026-10-07

### Added

- `calculate_effective_velocity()` para modelar la pérdida de productividad
  asociada a la deuda técnica.

## [1.0 build 001] - 2026-10-07

### Added

- Estructura inicial de la secuencia s002.
- `ModelParameters` para la historia A1, con validación y serialización.
- Pruebas Pytest con Hypothesis, documentación pdoc, workflow de GitHub Actions
  y controles pre-commit de Black y Ruff.
