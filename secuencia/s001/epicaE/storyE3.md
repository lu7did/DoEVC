Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica E" continuando por la historia denominada "Historia E3".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia E3 — Reproducibilidad completa desde archivo JSON

Como investigador, quiero cargar un escenario desde un archivo JSON y reproducir la simulación exacta que lo generó, para garantizar trazabilidad experimental.

Esta historia tiene riesgo de integración alto: depende de E2 y de la interfaz Policy de B4.

Criterios de aceptación:
- Existe una función load_and_run(filepath) que lee el JSON de E2, reconstruye params, política y semilla, y ejecuta la simulación.
- El resultado es idéntico al de la ejecución original (mismos SprintState por sprint).
- La política se reconstruye por nombre de clase desde un registro interno.
- Hay tests de round-trip: guardar con E2 → cargar con E3 → comparar resultados.
