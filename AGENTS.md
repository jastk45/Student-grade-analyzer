# Instrucciones del proyecto para Codex

## Contexto del proyecto

- Este es un proyecto educativo escrito en Python 3.13 y gestionado con `uv`.
- El código de producción se encuentra en `src/grades/`.
- La lógica principal del negocio está en `src/grades/grades.py`.
- Los datos de ejemplo se encuentran en `data/grades.csv`.

## Reglas de trabajo

- Antes de cambiar el código, inspecciona la estructura del repositorio y los archivos fuente relevantes.
- Cuando se solicite diseñar pruebas, primero propón un plan de pruebas y explica los comportamientos y casos límite que pretendes cubrir.
- No crees ni modifiques archivos hasta que el usuario apruebe explícitamente el plan de pruebas propuesto.
- Usa el framework `unittest` de la biblioteca estándar de Python, a menos que el usuario solicite explícitamente otro framework.
- Crea `tests/` únicamente después de la aprobación, si aún no existe.
- No modifiques el código de producción únicamente para hacer que las pruebas pasen, a menos que el usuario apruebe explícitamente ese cambio.
- Prefiere probar el comportamiento público en lugar de los detalles de implementación.

## Verificación

Ejecuta el conjunto completo de pruebas con:

```bash
uv run python -m unittest discover -s tests -v
```

Después de la implementación:

- informa qué archivos fueron creados o modificados;
- resume las pruebas añadidas;
- muestra el comando de pruebas y su resultado;
- menciona por separado cualquier cambio realizado en el código de producción.
