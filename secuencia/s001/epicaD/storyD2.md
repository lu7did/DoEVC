Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica D" continuando por la historia denominada "Historia D2".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia D2 — Función objetivo económica configurable

Como investigador, quiero definir una función objetivo que cuantifique el valor económico de una trayectoria de simulación, para guiar la búsqueda del u_k óptimo.

La función objetivo de referencia combina:
- Valor acumulado de funcionalidad entregada (positivo).
- Penalización por deuda técnica remanente (negativo).
- Penalización por sprints totales consumidos (configurable).

Criterios de aceptación:
- Existe una clase o función ObjectiveFunction con parámetros de peso configurables.
- Puede evaluarse sobre la lista de SprintState producida por A4.
- Es compatible con la búsqueda por grilla de D1.
- Hay tests que verifican que distintas ponderaciones producen distintos óptimos en escenarios controlados.
