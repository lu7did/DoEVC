Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica C" continuando por la historia denominada "Historia C2".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia C2 — Ejecutar N simulaciones Monte Carlo

Como investigador, quiero ejecutar múltiples corridas del simulador con parámetros aleatorios, para estimar distribuciones de resultados bajo incertidumbre.

Criterios de aceptación:
- Existe una función run_monte_carlo(n_runs, policy, seed) que ejecuta N corridas.
- Cada corrida usa parámetros muestreados con C1.
- Devuelve tanto los resultados individuales por corrida como resultados agregados.
- La política es seleccionable (usa la interfaz Policy de B4).
- Con la misma semilla, los resultados son reproducibles.
- Hay tests que verifican reproducibilidad y que se ejecutan exactamente n_runs corridas.
