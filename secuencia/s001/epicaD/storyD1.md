Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica D" comenzando por la historia denominada "Historia D1".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia D1 — Búsqueda por grilla de u_k óptimo

Como investigador, quiero explorar distintos valores fijos de u_k en una grilla uniforme, para encontrar el que minimiza una función objetivo dada.

Criterios de aceptación:
- La grilla evalúa u ∈ {0.00, 0.01, ..., 1.00} (paso configurable).
- Para cada valor de u se ejecuta una simulación determinística completa (A4).
- Se devuelve el valor de u que optimiza la función objetivo.
- La función objetivo es configurable (recibida como parámetro).
- Hay tests que verifican que el u óptimo encontrado minimiza/maximiza correctamente en casos conocidos.
