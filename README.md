# DoEVC

**Diseño de Experimentos – Control de Voltaje / Design of Experiments – Voltage Control**

Repositorio de soporte para el proyecto de Investigación y Desarrollo bajo el grant **UADER PI-D 230/24**.

> *Repository to support the R&D project under grant UADER PI-D 230/24 (Universidad Autónoma de Entre Ríos).*

---

## Descripción / Description

Este repositorio contiene el código, datos y documentación asociados al proyecto de I+D **DoEVC**, cuyo objetivo es aplicar metodologías de Diseño de Experimentos (DoE) al análisis y optimización de sistemas de Control de Voltaje (VC).

*This repository contains code, data and documentation for the **DoEVC** R&D project, which applies Design of Experiments (DoE) methodology to the analysis and optimisation of Voltage Control (VC) systems.*

---

## Estructura del proyecto / Project structure

```
DoEVC/
├── src/
│   └── doEVC/            # Paquete Python principal / Main Python package
│       ├── design/       # Generación de diseños experimentales / Experimental design generation
│       ├── analysis/     # Análisis estadístico / Statistical analysis
│       └── utils/        # Utilidades generales / General utilities
├── tests/                # Pruebas unitarias / Unit tests
├── data/
│   ├── raw/              # Datos experimentales originales / Raw experimental data
│   └── processed/        # Datos procesados / Processed data
├── notebooks/            # Jupyter notebooks de análisis / Analysis notebooks
├── docs/                 # Documentación del proyecto / Project documentation
├── requirements.txt      # Dependencias Python / Python dependencies
└── pyproject.toml        # Configuración del paquete / Package configuration
```

---

## Instalación / Installation

```bash
# Clonar el repositorio / Clone the repository
git clone https://github.com/lu7did/DoEVC.git
cd DoEVC

# Crear entorno virtual (recomendado) / Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# Instalar dependencias / Install dependencies
pip install -r requirements.txt

# Instalar el paquete en modo editable / Install package in editable mode
pip install -e .
```

---

## Uso / Usage

```python
from doEVC.design import factorial, central_composite
from doEVC.analysis import anova, response_surface

# Generar un diseño factorial completo / Generate a full factorial design
design = factorial.full_factorial(factors={"V_ref": [4.8, 5.0, 5.2], "load": [10, 50, 100]})

# Ejecutar análisis ANOVA / Run ANOVA analysis
results = anova.analyze(design, response_column="V_out")
results.summary()
```

---

## Dependencias principales / Main dependencies

| Paquete | Propósito |
|---------|-----------|
| `pyDOE3` | Generación de diseños experimentales / Experimental design generation |
| `numpy` | Operaciones numéricas / Numerical operations |
| `scipy` | Análisis estadístico / Statistical analysis |
| `pandas` | Manipulación de datos / Data manipulation |
| `matplotlib` / `seaborn` | Visualización / Visualisation |
| `statsmodels` | Modelos estadísticos / Statistical models |
| `jupyter` | Cuadernos interactivos / Interactive notebooks |

---

## Grant / Financiamiento

Este trabajo es financiado por la **Universidad Autónoma de Entre Ríos (UADER)** bajo el grant de Investigación y Desarrollo **PI-D 230/24**.

*This work is funded by the **Universidad Autónoma de Entre Ríos (UADER)** under R&D grant **PI-D 230/24**.*

---

## Licencia / License

Este proyecto se distribuye bajo la licencia [CC0 1.0 Universal](LICENSE) – dominio público.

*This project is released under the [CC0 1.0 Universal](LICENSE) public domain dedication.*

---

## Contacto / Contact

**LU7DID** – Universidad Autónoma de Entre Ríos (UADER)  
GitHub: [@lu7did](https://github.com/lu7did)
