# Contexto de construcción

Este proyecto usa Python 3.13 y una estructura de paquete inspirada en
cookiecutter, con raíz bajo `secuencia/`. Las carpetas `script/` y
`ejemplos/` forman parte de la estructura, pero su contenido se excluye de la
validación de push.

El proyecto conserva este archivo como referencia de las reglas de creación.
Mantiene `README.md`, `CHANGELOG.md` y `STORIES.md`: el README documenta las
funciones disponibles, el changelog conserva la trazabilidad y STORIES registra
cada petición que produzca un nuevo push con su marca de tiempo.

La licencia es Creative Commons según `LICENSE`. La documentación de API se
genera con pdoc. El proyecto comienza en versión 1.0 build 000; cada push
exitoso incrementará el build y actualizará README y CHANGELOG.

GitHub Actions valida el código en Python 3.13 con Pytest y una cobertura no
inferior al 80%. Black y Ruff se ejecutan mediante pre-commit antes de cada
commit. La lógica funcional se mantiene separada de cualquier interfaz de
usuario y se implementa como un paquete Python.
