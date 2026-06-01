Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica D" continuando por la historia denominada "Historia D4".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia D4 — Comparación entre todas las políticas

Como investigador, quiero ejecutar todas las políticas disponibles sobre el mismo escenario y comparar sus resultados, para identificar cuál estrategia produce mejores métricas bajo condiciones equivalentes.

Esta historia tiene riesgo de integración muy alto: consolida épicas A, B, C y D.

Criterios de aceptación:
- Existe una función compare_policies(params, policies, objective) que corre cada política sobre los mismos parámetros.
- Devuelve una tabla comparativa con las métricas de C3 para cada política.
- Soporta tanto simulaciones determinísticas (A4) como Monte Carlo (C2).
- Hay tests que verifican que las políticas producen resultados distintos y que la tabla contiene todas las políticas evaluadas.
