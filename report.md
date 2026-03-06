# Data Quality Report

## Metrics
* **Total number of input records:** 17
* **Total number of output records:** 9
* **Number of discarded entries:** 2
* **Number of corrected entries:** 9
* **Number of duplicates detected:** 6

## Deduplication Strategy

1. **Normalización de Textos:** Se crearon columnas temporales estandarizadas (minúsculas y colapso de espacios múltiples) para comparar cadenas de texto de forma precisa.
2. **Priorización:** Se evaluó la calidad de cada registro (presencia de fechas reales, títulos válidos y números mayores a 0). Se ordenó el DataFrame de manera descendente para empujar los registros más completos a la parte superior.
3. **Detección y Eliminación:** Se utilizó `df.duplicated(keep='first')` evaluando 3 escenarios: coincidencia exacta de llaves, y coincidencias donde faltaba la temporada o el episodio. Al mantener el primer registro ('first'), se garantizó la supervivencia del registro con mejor calidad de datos.

