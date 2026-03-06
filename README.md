# Technical Challenge (Part 1)

Este proyecto es una solución automatizada desarrollada en Python utilizando `pandas` para el procesamiento, limpieza y deduplicación de un catálogo de episodios de series de televisión.

## Objetivos del Proyecto
El script principal toma un archivo CSV crudo con datos inconsistentes y aplica un pipeline de calidad de datos para generar un catálogo limpio y confiable, cumpliendo con estrictas reglas de negocio.

## Características Principales (Features)

1. **Normalización de Datos:**
   - Corrección de formatos de texto (capitalización de títulos de series).
   - Manejo de valores nulos o faltantes inyectando *Safe Defaults* (`0` para números, `Unknown` para fechas, `Untitled Episode` para títulos).
   - Descarte automático de registros completamente inválidos (sin temporada, episodio ni fecha).

2. **Motor de Deduplicación Inteligente:**
   - Normalización invisible de llaves de búsqueda (minúsculas y colapso de espacios).
   - Sistema de priorización: en caso de episodios duplicados, el algoritmo ordena y conserva automáticamente la versión con los datos más completos (priorizando fechas reales y títulos válidos).
   - Resolución de conflictos para episodios con números de temporada o capítulo faltantes.

3. **Generación Automática de Reportes:**
   - Creación dinámica de un archivo Markdown (`report.md`) que detalla las métricas del procesamiento (registros procesados, descartados, corregidos y duplicados eliminados).

## Instrucciones de Ejecución

1. Asegúrate de tener instalado Python y la librería `pandas`:
   ```bash
   pip install pandas
