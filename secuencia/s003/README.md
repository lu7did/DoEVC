# DoEVC s003

Secuencia independiente, preparada para recibir sus propias épicas e historias.

## Estado

- Versión: 1.0
- Build: 012
- Python: 3.13
- Licencia: Creative Commons CC0 1.0

## Funciones disponibles

- `get_version_label()`: identifica el build inicial de la secuencia.
- `ModelParameters`: estructura inmutable y serializable para los parámetros
  del modelo.
- `calculate_effective_velocity()`: calcula `V_k` afectada por deuda técnica.
- `simulate_sprint()`: calcula el estado siguiente de un sprint con una
  asignación fija de remediación.
- `SprintState`: conserva las entradas, capacidades y estados resultantes del
  sprint.
- `simulate_sprints()`: encadena hasta `K` sprints determinísticos con una
  asignación fija o cualquier `Policy`.
- `Policy`: protocolo intercambiable que define `decide_u()`.
- `DebtFirstPolicy`: asigna toda la capacidad a remediación mientras exista
  deuda técnica.
- `BacklogFirstPolicy`: asigna toda la capacidad a entrega mientras exista
  backlog funcional.
- `ProportionalPolicy`: asigna remediación según la proporción de deuda sobre
  el trabajo total restante.
- `sample_model_parameters()`: genera parámetros completos con distribuciones
  uniformes reproducibles mediante semilla.
- `run_monte_carlo()`: ejecuta múltiples simulaciones con parámetros
  muestreados, una `Policy` seleccionable y resultados agregados.
- `aggregate_metrics()`: resume las métricas por corrida mediante media,
  desvío estándar, mínimo y máximo.
- `find_optimal_allocation()`: explora una grilla configurable de asignaciones
  fijas y optimiza un objetivo de simulación recibido.
