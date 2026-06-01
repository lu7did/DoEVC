Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica F" continuando por la historia denominada "Historia F2".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia F2 — Boxplot de distribución de u_k óptimo

Como investigador, quiero visualizar la distribución del u_k óptimo a lo largo de corridas Monte Carlo, para entender la variabilidad de la estrategia óptima bajo incertidumbre.

Criterios de aceptación:
- Existe una función plot_optimal_u_distribution(results, filepath) que genera un PNG con boxplot.
- Recibe los resultados de C2/C3 (lista de métricas por corrida).
- Usa matplotlib con modo no interactivo.
- Hay tests que verifican que el archivo se crea correctamente con datos de entrada válidos.
