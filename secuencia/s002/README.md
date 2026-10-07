# DoEVC s002

Paquete Python 3.13 para el segundo ciclo del modelo DoEVC.

## Estado

- Versión: 1.0
- Build: 006
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
