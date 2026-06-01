Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica A" continuando por la historia denominada "Historia A4".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia A4 — Simular K sprints determinísticos

Como investigador, quiero ejecutar una simulación de K sprints encadenados, para observar la evolución completa del sistema.

Criterios de aceptación:
- Se genera una lista o tabla con una fila (SprintState) por sprint.
- Incluye B_k, D_k, V_k, u_k, N_k, R_k en cada sprint.
- La simulación se detiene anticipadamente si B_k=0 y D_k=0.
- La fracción u_k es un parámetro fijo recibido por la función.
- Hay tests de regresión que verifican trayectorias conocidas con parámetros fijos.
