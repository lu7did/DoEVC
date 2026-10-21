# Changelog

## [1.0 build 011] - 2026-10-21

### Added

- Métricas por corrida y `aggregate_metrics()` para resumir resultados Monte
  Carlo de C3.

## [1.0 build 010] - 2026-10-21

### Added

- `run_monte_carlo()` y resultados por corrida y agregados para experimentos
  reproducibles de C2.

## [1.0 build 009] - 2026-10-21

### Added

- `sample_model_parameters()` para muestreo uniforme reproducible de los
  parámetros de incertidumbre de C1.

## [1.0 build 008] - 2026-10-21

### Changed

- Las políticas B1-B3 implementan el protocolo intercambiable `Policy` con
  `decide_u(state, params)`; `simulate_sprints()` acepta cualquier política.

## [1.0 build 007] - 2026-10-21

### Added

- `proportional_allocation()` como política B3 basada en la deuda relativa.

## [1.0 build 006] - 2026-10-21

### Added

- `backlog_first_allocation()` como política B2, seleccionable por
  `simulate_sprints()` usando backlog y deuda del sprint.

## [1.0 build 005] - 2026-10-21

### Added

- `debt_first_allocation()` como política B1 e integración de políticas
  seleccionables en `simulate_sprints()`.

## [1.0 build 004] - 2026-10-21

### Added

- `simulate_sprints()` para trayectorias determinísticas de hasta `K` sprints
  en la historia A4.

## [1.0 build 003] - 2026-10-21

### Added

- `SprintState` y `simulate_sprint()` para la transición de un sprint A3.

## [1.0 build 002] - 2026-10-21

### Added

- Esqueleto independiente de s003 y automatización de calidad.
- `ModelParameters` validado y serializable para la historia A1.
- `calculate_effective_velocity()` para la historia A2.
