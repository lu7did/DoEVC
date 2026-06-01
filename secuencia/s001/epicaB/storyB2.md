Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica B" continuando por la historia denominada "Historia B2".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia B2 — Política "backlog primero"

Como investigador, quiero una política donde u_k=0 mientras exista backlog funcional, para comparar contra la política de deuda primero.

Criterios de aceptación:
- Si B_k > 0, entonces u_k = 0.
- Si B_k = 0 y D_k > 0, entonces u_k = 1.
- Se integra con el simulador de K sprints (A4) como política seleccionable.
- Hay tests unitarios que verifican ambas ramas de la política.
