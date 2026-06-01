Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica C" comenzando por la historia denominada "Historia C1".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia C1 — Definir distribuciones uniformes de parámetros

Como investigador, quiero definir parámetros aleatorios con distribución uniforme y semilla configurable, para explorar la incertidumbre del modelo de forma reproducible.

Rangos de referencia:
- s  ~ U(1.0, 1.4)
- γ  ~ U(0.00, 0.05)
- θ  ~ U(0.0, 0.9)
- (1-β) ~ U(0.5, 0.9)
- λ  ~ U(0.2, 1.0)

Criterios de aceptación:
- Existe una función o clase que muestrea un conjunto completo de ModelParameters aleatorios.
- Se pueden fijar semillas aleatorias para reproducibilidad.
- Con la misma semilla, dos muestreos producen el mismo resultado.
- Hay tests con semilla fija que verifican reproducibilidad.
