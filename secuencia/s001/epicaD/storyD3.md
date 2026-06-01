Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica D" continuando por la historia denominada "Historia D3".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia D3 — Política óptima local (implementa interfaz Policy)

Como investigador, quiero una política que en cada sprint elija el u_k que maximiza la función objetivo, para comparar la estrategia óptima local contra las políticas heurísticas.

Esta historia tiene riesgo de integración muy alto: combina D1, D2 y la interfaz Policy de B4.

Criterios de aceptación:
- Existe una clase OptimalLocalPolicy que implementa la interfaz Policy (B4).
- En cada llamada a decide_u(), evalúa la grilla de u para el estado actual y devuelve el óptimo.
- Recibe la función objetivo (D2) como parámetro de construcción.
- Es intercambiable con las políticas B1, B2 y B3 en el motor de simulación.
- Hay tests de integración que verifican que produce mejores resultados que al menos una política heurística en un escenario conocido.
