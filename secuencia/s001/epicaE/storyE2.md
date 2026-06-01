Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica E" continuando por la historia denominada "Historia E2".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia E2 — Guardar escenarios en JSON

Como investigador, quiero guardar un escenario completo (parámetros + política + semilla) en formato JSON, para documentar y reproducir experimentos individuales.

Criterios de aceptación:
- Existe una función save_scenario(params, policy_name, seed, filepath) que serializa el escenario a JSON.
- El archivo JSON es legible con json.load() estándar de Python.
- La política se identifica por nombre de clase (string) para permitir su reconstrucción.
- Hay tests que verifican que el JSON generado contiene todos los campos esperados.
