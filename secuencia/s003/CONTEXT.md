# Contexto de construcción

`s003` es una secuencia Python 3.13 independiente. Se estructura como paquete
con `src/`, `tests/`, `docs/`, `script/` y `ejemplos/`; las dos últimas se
excluyen de la validación de push.

README documenta las funciones disponibles, CHANGELOG conserva trazabilidad y
STORIES registra cada solicitud que origine un push con su timestamp. Se usa
Creative Commons según LICENSE, pdoc para la API, Pytest/Hypothesis con 80% de
cobertura, Black, Ruff, Pylint, MyPy y Pyright antes de cada commit. La
secuencia inicia en versión 1.0 build 000; cada push exitoso actualizará el
build, README y CHANGELOG.
