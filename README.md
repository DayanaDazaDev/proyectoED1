# Proyecto 1: Calculadora Bitwise + Persistencia
Implementación web (Flask) con operaciones a nivel de bits y persistencia JSON de historial.

## 🚀 Ejecución
1. Activar entorno, ejecute: `python3 -m venv .venv`
2. en la terminal ejecute: `.venv/Scripts/activate`
3. Ejecutar: `python main.py`
4. Abrir: `http://localhost:5000`

## 💾 Persistencia JSON
- Las operaciones se guardan automáticamente en `datos/historial.json`.
- El panel deslizable (🕒) muestra el historial en tiempo real.
- Endpoint `/api/historial/limpiar` permite resetearlo.

## 🧪 Pruebas Unitarias
```bash
python tests/test_bitwise.py
```

El proyecto tiene persistencia de datos, diseño UI/UX bastante intuitivo y moderno, separe la capa de datos de presentacion (arquitectura limpia)
Limite los registros, cuando se tiene 50 registros, se muestra una paginacion de los registros. Esto muestra gestión de memoria y prevención de archivos gigantes en este caso es la limitaciond e varias operaciones hechas en la calculadora.
Tambien maneje correctamente el formato UTF-8 en los archivos JSON.
