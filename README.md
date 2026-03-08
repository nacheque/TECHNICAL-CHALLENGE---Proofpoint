# Parte 1: The Streaming Service’s Lost Episodes

Este proyecto es una solución automatizada desarrollada en Python utilizando `pandas` para el procesamiento, limpieza y deduplicación de un catálogo de episodios de series de televisión.

## Objetivos del Proyecto
El script principal toma un archivo CSV crudo con datos inconsistentes y aplica un pipeline de calidad de datos para generar un catálogo limpio y confiable, cumpliendo con estrictas reglas de negocio.

## Características Principales

1. **Normalización de Datos:**
   - Corrección de formatos de texto (capitalización de títulos de series).
   - Manejo de valores nulos o faltantes inyectando *valores por defecto* (`0` para números, `Unknown` para fechas, `Untitled Episode` para títulos).
   - Descarte automático de registros completamente inválidos (sin temporada, episodio ni fecha).

2. **Motor de Deduplicación:**
   - Normalización invisible de llaves de búsqueda (minúsculas y colapso de espacios).
   - Sistema de priorización: en caso de episodios duplicados, el algoritmo ordena y conserva automáticamente la versión con los datos más completos (priorizando fechas reales y títulos válidos).
   - Resolución de conflictos para episodios con números de temporada o capítulo faltantes.

3. **Generación Automática de Reportes:**
   - Creación dinámica de un archivo Markdown (`report.md`) que detalla las métricas del procesamiento (registros procesados, descartados, corregidos y duplicados eliminados).

## Instrucciones de Ejecución

1. Asegúrate de tener instalado Python y la librería `pandas`:
   ```bash
   pip install pandas
   ```
2. Asegúrate de tener el csv de entrada `input.csv` dentro de la misma carpeta.
3. Ejecuta el script:
   ```bash
   python main.py
   ```

# Parte 2: Análisis de Frecuencia de Palabras

Como segundo requerimiento, se desarrolló un script independiente (`word_frequency.py`) que lee un archivo de texto plano y genera un ranking de las 10 palabras más utilizadas.

## Características de la solución:
* **Limpieza:** Utiliza Expresiones Regulares (módulo `re`) para ignorar signos de puntuación, números y caracteres especiales, filtrando únicamente palabras.
* **Normalización:** La comparación es 100% *case-insensitive* (ignora mayúsculas y minúsculas).
* **Conteo:** Implementa la estructura de datos `Counter` de la librería nativa `collections` para un conteo y ordenamiento.

**Cómo ejecutar esta parte:**
1. Asegúrate de tener un archivo llamado `input.txt` con el texto a analizar en la misma carpeta.
2. Ejecuta el script:
   ```bash
   python word_frequency.py
   ```

# Estructura del repositorio
📁 TECHNICAL-CHALLENGE---Proofpoint/
 ├── 📁 B_Streaming_Service/
 │    ├── main.py
 │    ├── input.csv
 │    └── episodes_clean.csv (y report.md)
 ├── 📁 C_Words_Frecuency/
 │    ├── word_frequency.py
 │    └── input.txt
 ├── README.md
 ├── ANSWERS.md
 ├── requirements.txt
 └── .gitignore