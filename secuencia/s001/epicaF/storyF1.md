Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica F" comenzando por la historia denominada "Historia F1".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia F1 — Gráfico de B_k y D_k por sprint → PNG

Como investigador, quiero generar un gráfico con la evolución de backlog y deuda técnica a lo largo de los sprints, para visualizar la trayectoria de una simulación determinística.

Criterios de aceptación:
- Existe una función plot_simulation(states, filepath) que genera un archivo PNG.
- El gráfico muestra B_k y D_k en el eje Y, con el índice de sprint en el eje X.
- Usa matplotlib. La lógica de visualización está separada de la lógica del modelo.
- El archivo PNG se genera correctamente sin necesidad de display (modo no interactivo).
- Hay tests que verifican que el archivo se crea y tiene tamaño mayor a cero.
