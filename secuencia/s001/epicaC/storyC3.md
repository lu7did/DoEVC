Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica C" continuando por la historia denominada "Historia C3".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia C3 — Agregar métricas de salida por corrida Monte Carlo

Como investigador, quiero calcular métricas resumidas por corrida y en conjunto, para comparar el desempeño de distintas estrategias de forma cuantitativa.

Métricas requeridas por corrida:
- Sprints totales hasta convergencia (o K si no converge).
- Deuda técnica final D_K.
- u_k promedio a lo largo de la simulación.
- Backlog funcional final B_K.
- Valor económico total acumulado (si está definido en el modelo).

Criterios de aceptación:
- Existe una estructura MonteCarloResult o similar que contiene métricas por corrida.
- Existe una función aggregate_metrics() que calcula media, desvío estándar, mínimo y máximo de cada métrica sobre todas las corridas.
- Los resultados individuales se conservan para análisis posterior.
- Hay tests que verifican la correcta agregación con datos de corridas conocidas.
