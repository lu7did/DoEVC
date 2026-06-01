Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica E" comenzando por la historia denominada "Historia E1".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia E1 — Exportar estados y métricas a CSV

Como investigador, quiero exportar la trayectoria de sprints y las métricas agregadas a archivos CSV, para analizarlos en herramientas externas como Excel o R.

Criterios de aceptación:
- Existe una función export_sprint_states_csv(states, filepath) que escribe una fila por SprintState.
- Columnas mínimas: sprint, B_k, D_k, V_k, u_k, N_k, R_k.
- Existe una función export_metrics_csv(metrics, filepath) para resultados Monte Carlo (C3).
- Los archivos generados son válidos y legibles con el módulo csv estándar de Python.
- Hay tests que escriben a un archivo temporal y verifican contenido y estructura.
