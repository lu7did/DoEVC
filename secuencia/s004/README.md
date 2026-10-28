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
