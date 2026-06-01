Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica A" continuando por la historia denominada "Historia A2".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia A2 — Calcular velocidad efectiva V_k

Como investigador, quiero calcular la velocidad efectiva afectada por deuda, para modelar la pérdida de productividad del equipo.

La fórmula es:

    V_k = V0 / (1 + gamma * D_k)

Criterios de aceptación:

- Dado D_k = 0, se obtiene V_k = V0.
- Si D_k aumenta, V_k disminuye monotónicamente.
- V_k es siempre positivo para parámetros válidos.
- Hay tests unitarios que verifican los casos anteriores.
