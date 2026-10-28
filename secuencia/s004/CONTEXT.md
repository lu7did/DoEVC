# Contexto de construccion de S004

Este proyecto se desarrolla desde cero para Python 3.13. Su estructura debe ser
apta para distribuirse como paquete Python y conservar una separacion clara
entre la logica funcional y cualquier logica de presentacion o interaccion.

Se mantienen los directorios `script/` y `ejemplos/`, excluidos de las
validaciones de calidad y cobertura. La automatizacion debe usar Pytest e
Hypothesis, con una cobertura minima del 80 %, y ejecutar Black, Ruff, Pylint,
MyPy, Pyright y Bandit antes de confirmar cambios y en GitHub Actions.

La version inicial es 1.0 build 000. Cada publicacion exitosa debe incrementar
el build y actualizar README.md, CHANGELOG.md, STORIES.md y la documentacion
generada con pdoc. Todas las solicitudes que lleven a una publicacion se deben
registrar con fecha y hora en STORIES.md.
