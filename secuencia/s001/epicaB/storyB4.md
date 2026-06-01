Basado en la descripción del proyecto general documentada en @secuencia/s001/PROJECT.md procederemos a desarrollar las historias
contenidas en la épica denominada "Epica B" continuando por la historia denominada "Historia B4".
Debes implementar de acuerdo al contexto del proyecto contenido en @secuencia/s001/CONTEXT.md el código python necesario para
implementar esta historia. También debes generar el código para el testeo mediante PyTest de la regresión que permita verificar y
validar los criterios de aceptación de la historia agregándolo a los existentes.
Una vez finalizado el desarrollo debes realizar las validaciones indicadas
en el contexto previamente leido y realizar el commit en GitHub una vez que la validación local se complete exitosamente.

Historia B4 — Interfaz común de políticas

Como desarrollador, quiero que todas las políticas implementen una interfaz común, para poder intercambiarlas sin modificar el motor de simulación.

Esta historia implica refactorización: las políticas B1, B2 y B3 deben adaptarse para cumplir la interfaz.

Criterios de aceptación:
- Existe una clase abstracta o protocolo Python llamado Policy.
- Cada política implementa el método decide_u(state: SprintState, params: ModelParameters) -> float.
- El motor de simulación (A4) acepta cualquier objeto Policy sin depender de clases concretas.
- Los tests existentes de B1, B2 y B3 siguen pasando tras la refactorización.
- Hay tests de integración que verifican que cada política puede intercambiarse en el motor.
