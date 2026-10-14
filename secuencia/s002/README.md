# DoEVC s002

Paquete Python 3.13 para el segundo ciclo del modelo DoEVC.

## Estado

- Versión: 1.0
- Build: 019
- Licencia: Creative Commons CC0 1.0

## Funciones disponibles

- `ModelParameters`: estructura inmutable y validada para los parámetros
  `B0`, `D0`, `V0`, `alpha`, `beta`, `gamma`, `theta`, `lambda_`, `rho` y
  `K`.
- `ModelParameters.to_dict()`: serializa los parámetros para experimentos
  reproducibles.
- `calculate_effective_velocity()`: calcula la velocidad efectiva afectada por
  deuda técnica mediante `V_k = V0 / (1 + gamma * D_k)`.
- `SprintState` y `simulate_sprint()`: ejecutan la transición determinista de
  un sprint con una fracción de remediación fija.
- `simulate_deterministic_sprints()`: encadena hasta `K` sprints con una
  fracción fija y finaliza anticipadamente cuando no queda trabajo.
- `DebtFirstPolicy`: política baseline que remedia toda la deuda antes de
  entregar funcionalidad.
- `BacklogFirstPolicy`: política que entrega el backlog antes de remediar deuda.
- `ProportionalPolicy`: política que asigna remediación según la deuda relativa.
- `Policy`: contrato intercambiable para políticas del simulador.
- `sample_model_parameters()`: muestrea parámetros inciertos uniformes y
  reproducibles a partir de una semilla.
- `run_monte_carlo()`: ejecuta corridas reproducibles con resultados individuales.
- `MonteCarloResult.aggregate_metrics()`: resume métricas de cada corrida.
- `grid_search_remediation()`: evalúa fracciones fijas para optimizar un
  objetivo configurable.
- `ObjectiveFunction`: cuantifica valor entregado, deuda remanente y duración.
- `OptimalLocalPolicy`: selecciona por grilla la mejor decisión del próximo
  sprint.
- `compare_policies()`: compara políticas en escenarios deterministas o Monte
  Carlo equivalentes.
- `export_sprint_states_csv()` y `export_metrics_csv()`: exportan trayectorias
  y métricas agregadas en formato CSV.
- `save_scenario()`: persiste parámetros, política y semilla en JSON.
- `load_and_run()`: reconstruye y ejecuta un escenario JSON reproducible.
- `plot_simulation()`: genera un PNG no interactivo de backlog y deuda.
- `plot_optimal_u_distribution()`: genera un boxplot PNG de remediación por
  corrida Monte Carlo.

## Instalación y validación

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pre-commit install
ruff check src tests
black --check src tests
pytest
python -m pdoc doevc_s002 -o site
```

La documentación generada se almacena en `site/`. Los directorios `script/` y
`ejemplos/` se excluyen de la validación automática.
