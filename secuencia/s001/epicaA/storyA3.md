Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica A" continuando por la historia denominada "Historia A3".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia A3 — Simular un sprint con u_k fijo

Como investigador, quiero calcular el estado k+1 a partir de B_k, D_k y u_k, para construir trayectorias de evolución del sistema.

Las ecuaciones del sprint son:

    R_k = u_k * V_k
    N_k = (1 - u_k) * V_k
    B_{k+1} = max(0, B_k - N_k)
    D_{k+1} = max(0, D_k - R_k + alpha * N_k + beta * R_k)

Criterios de aceptación:

- u_k debe estar en el rango [0, 1]; se rechaza o clampea fuera de rango.
- B_{k+1} nunca queda negativo.
- D_{k+1} nunca queda negativo.
- Se devuelve un objeto SprintState con todos los valores del sprint.
- Hay tests unitarios que verifican los criterios anteriores con parámetros conocidos.
