Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica B" continuando por la historia denominada "Historia B3".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia B3 — Política proporcional

Como investigador, quiero definir u_k proporcional a la deuda relativa, para tener una política heurística intermedia entre las dos anteriores.

La fórmula es:
    u_k = D_k / (B_k + D_k)

Criterios de aceptación:
- u_k = 0 si D_k = 0.
- u_k = 1 si B_k = 0 y D_k > 0.
- u_k ∈ [0, 1] en todos los casos.
- Maneja correctamente el caso borde B_k = D_k = 0 (sin división por cero).
- Se integra con el simulador de K sprints (A4) como política seleccionable.
- Hay tests unitarios que verifican los casos borde y el caso general.
