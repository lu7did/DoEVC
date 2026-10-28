# S004

Paquete Python 3.13 iniciado desde cero para las historias de la secuencia
S004.

**Version:** 1.0 build 000

## Funciones disponibles

- `s004.get_project_info()`: devuelve los metadatos de version del paquete.
- `s004.calculate_effective_velocity()`: calcula la velocidad efectiva
  degradada por deuda técnica.
- `s004.simulate_sprint()`: simula un sprint con una fracción fija de
  remediación.
- `s004.DebtFirstPolicy`: asigna toda la capacidad a remediar deuda mientras
  exista deuda técnica.
- `s004.BacklogFirstPolicy`: prioriza el backlog funcional antes de remediar
  deuda técnica.
- `s004.ProportionalPolicy`: asigna remediación proporcional a la deuda
  relativa.
- `s004.sample_model_parameters()`: muestrea parámetros inciertos con semilla
  reproducible.
- `s004.run_monte_carlo()`: ejecuta corridas reproducibles y agrega sus
  resultados.
- `s004.aggregate_metrics()`: resume métricas por corrida con estadísticos
  poblacionales.
- `s004.grid_search_remediation()`: optimiza una fracción fija de remediación
  sobre una grilla uniforme.
- `s004.ObjectiveFunction`: valora funcionalidad entregada, deuda y duración
  de una trayectoria.
- `s004.OptimalLocalPolicy`: selecciona el valor de remediación óptimo en cada
  sprint.

## Desarrollo

Instale las herramientas y ejecute las verificaciones:

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 -m pytest
pre-commit run --all-files
```

La documentacion HTML se genera con:

```powershell
py -3.13 -m pdoc s004 -o site
```
