# DoEVC s003

Secuencia independiente, preparada para recibir sus propias épicas e historias.

## Estado

- Versión: 1.0
- Build: 004
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
  asignación fija y detención temprana al completar backlog y deuda.
