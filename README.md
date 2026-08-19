# Student Grade Analyzer

Analizador de calificaciones de estudiantes en Python. Lee un CSV con notas y
reporta promedio, nota más alta y más baja, aprobados/reprobados y el top 5.

Proyecto de la materia **Programación Avanzada** (Maestría), gestionado con [uv](https://docs.astral.sh/uv/).

## Requisitos

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/)

## Instalación

```bash
git clone https://github.com/jastk45/Student-grade-analyzer.git
cd Student-grade-analyzer
uv sync
```

## Uso

```bash
uv run grades
```

O equivalentemente como módulo:

```bash
uv run python -m grades
```

Salida de ejemplo:

```
STUDENT GRADE ANALYZER
==============================================
Students:       120
Average score:  70.57
Highest score:  Valentina Rodriguez (100.0)
Lowest score:   Elena Torres (40.0)
Passed:         84
Failed:         36
Pass rate:      70.0%

TOP 5 STUDENTS
----------------------------------------------
 1. Valentina Rodriguez      100.0
 2. Nicolas Herrera          100.0
 3. Camila Perez              99.0
 4. Javier Morales            99.0
 5. Javier Herrera            99.0
```

## Formato del CSV

El archivo [data/grades.csv](data/grades.csv) debe tener las columnas
`student_id`, `name` y `score`, con `score` entre 0 y 100:

```csv
student_id,name,score
S001,Ada Lovelace,98
S002,Alan Turing,91
```

## Tests

`uv sync` instala pytest (declarado en el grupo `dev` de `pyproject.toml`):

```bash
uv run pytest
```

## API

Funciones expuestas en `grades` ([src/grades/grades.py](src/grades/grades.py)):

| Función | Descripción |
| --- | --- |
| `load_grades(path)` | Carga y valida los registros del CSV |
| `average_score(records)` | Promedio de las notas |
| `highest_score(records)` | Registro con la nota más alta |
| `lowest_score(records)` | Registro con la nota más baja |
| `count_passed(records, passing_score=60.0)` | Cantidad de aprobados |
| `count_failed(records, passing_score=60.0)` | Cantidad de reprobados |

## Estructura

```
├── data/grades.csv        # datos de entrada
├── src/grades/            # paquete principal
│   ├── grades.py          # lógica de análisis
│   └── __main__.py        # punto de entrada CLI
└── tests/test_grades.py   # pruebas
```
