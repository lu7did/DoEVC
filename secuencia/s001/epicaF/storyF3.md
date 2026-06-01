Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica F" continuando por la historia denominada "Historia F3".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia F3 — Heatmap de sensibilidad (2 parámetros × u promedio)

Como investigador, quiero un heatmap que muestre cómo varía el u_k promedio óptimo en función de dos parámetros del modelo, para identificar zonas de alta sensibilidad experimental.

Esta historia tiene riesgo de integración muy alto: combina D1, D2 y C2.

Criterios de aceptación:
- Existe una función plot_sensitivity_heatmap(param1_range, param2_range, base_params, policy, filepath) que genera un PNG.
- Los ejes del heatmap representan los rangos de los dos parámetros seleccionados.
- El color de cada celda representa el u_k promedio de la simulación con esa combinación de parámetros.
- Los parámetros a variar son configurables (nombres de atributos de ModelParameters).
- Usa matplotlib con modo no interactivo.
- Hay tests que verifican que el archivo se genera y que la matriz de valores tiene las dimensiones correctas.
