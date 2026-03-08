import pandas as pd

def normalize_data(df):
    #Series Name, Season Number, Episode Number, Episode Title y Air Date
    # eliminar registros sin nombre serie
    # nota: Agregamos .copy() para evitar el SettingWithCopyWarning
    df = df.dropna(subset=['SeriesName']).copy()

    # Quitar espacios extra y normalizar mayúsculas 
    df['SeriesName'] = df['SeriesName'].str.strip().str.title()
    df['EpisodeTitle'] = df['EpisodeTitle'].str.strip()
    
    #set to 0 --> season or episode missing, empty, neg, not number
    df['SeasonNumber'] = pd.to_numeric(df['SeasonNumber'], errors='coerce')
    df.loc[df['SeasonNumber'].isna() | (df['SeasonNumber'] < 0), 'SeasonNumber'] = 0
    df['SeasonNumber'] = df['SeasonNumber'].astype(int) # Fuerzo a número entero

    df['EpisodeNumber'] = pd.to_numeric(df['EpisodeNumber'], errors='coerce')
    df.loc[df['EpisodeNumber'].isna() | (df['EpisodeNumber'] < 0), 'EpisodeNumber'] = 0
    df['EpisodeNumber'] = df['EpisodeNumber'].astype(int) # Fuerzo a número entero

    #set to 'Untlited Episode' --> Episode Title is missing or empty
    df.loc[(df['EpisodeTitle'].isna()) | (df['EpisodeTitle'] == ''), 'EpisodeTitle'] = 'Untitled Episode'

    #Air Date If missing, empty, or invalid → replace with "Unknown"
    df['AirDate'] = pd.to_datetime(df['AirDate'], errors='coerce')
    #nota: Agregamos astype(object) para evitar el FutureWarning
    df['AirDate'] = df['AirDate'].astype(object)
    df.loc[df['AirDate'].isna(), 'AirDate'] = 'Unknown'

    #When Episode Number, Episode Title and Air Date are missing (the three fields), discard the record
    cond_episode_number = (df['EpisodeNumber'] == 0) | (df['EpisodeNumber'].isna())
    cond_episode_title = (df['EpisodeTitle'] == 'Untitled Episode') | (df['EpisodeTitle'].isna())
    cond_air_date = (df['AirDate'] == 'Unknown') | (df['AirDate'].isna())

    discard_record = cond_episode_number & cond_episode_title & cond_air_date
    df = df.drop(df[discard_record].index)
    
    return df

def remove_duplicates(df):

    #creamos columnas temporales para comparar, y estandarizamos los campos que tienen texto
    #los replace() usan expresiones regulares que eliminan los espacios al medio entre titulos y los pasa a minuscula
    df['Series_norm'] = df['SeriesName'].str.strip().str.replace(r'\s+', ' ', regex=True).str.lower()
    df['Title_norm'] = df['EpisodeTitle'].str.strip().str.replace(r'\s+', ' ', regex=True).str.lower()

    #consignas de prioridad para elegir el mejor registro
    #las agregamos en columnas temporales para ver que registros estan mas completos (tienen mas prioridad)
    df['has_date'] = df['AirDate'] != 'Unknown'
    df['has_title'] = df['EpisodeTitle'] != 'Untitled Episode'
    df['has_numbers'] = (df['SeasonNumber'] > 0) & (df['EpisodeNumber'] > 0)

    #las ordenamos del registro que mas condiciones cumple al que menos, con eso garantizamos que los registros mas
    #completos esten arriba y el keep='first' elimina los duplicados que queden abajo
    df = df.sort_values(by=['has_date', 'has_title', 'has_numbers'], ascending=[False, False, False])

    #Condicion A se repite (SeriesName_normalized, SeasonNumber, EpisodeNumber)
    dup_A = df.duplicated(subset=['Series_norm', 'SeasonNumber', 'EpisodeNumber'], keep='first')

    #Condicion B se repite (SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized) y season es 0
    dup_temp = df.duplicated(subset=['Series_norm', 'EpisodeNumber', 'Title_norm'], keep='first')
    dup_B = dup_temp & (df['SeasonNumber'] == 0)

    #Condicion C se repite (SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized y episode es 0
    dup_temp = df.duplicated(subset=['Series_norm', 'SeasonNumber', 'Title_norm'], keep='first')
    dup_C = dup_temp & (df['EpisodeNumber'] == 0)

    #Buscamos los registros que se verificaron como duplicados en alguno de los 3 escenarios
    discar_record = dup_A | dup_B | dup_C
    #Lo eliminamos segun su indice en el df
    df = df.drop(df[discar_record].index)

    # Borramos las columnas auxiliares
    df = df.drop(columns=['Series_norm', 'Title_norm', 'has_date', 'has_title', 'has_numbers'])
    df = df.sort_values(by=['SeriesName', 'SeasonNumber', 'EpisodeNumber']).reset_index(drop=True)

    return df

def generate_quality_report(df_inicial, df_normalizado, df_final):
    total_input = len(df_inicial)
    total_output = len(df_final)
    discarded_entries = len(df_inicial) - len(df_normalizado)
    duplicates_detected = len(df_normalizado) - len(df_final)

    #control de los registros que tuvieron que ser corregidos
    correcciones = (
        (df_normalizado['SeasonNumber'] == 0) |
        (df_normalizado['EpisodeNumber'] == 0) |
        (df_normalizado['EpisodeTitle'] == 'Untitled Episode') |
        (df_normalizado['AirDate'] == 'Unknown')
    )
    #el sum() cuenta cuantos True encontro en las correciones
    corrected_entries = correcciones.sum()

    #creacion de las especificaciones del markdown
    estrategia = """
1. **Normalización de Textos:** Se crearon columnas temporales estandarizadas (minúsculas y colapso de espacios múltiples) para comparar cadenas de texto de forma precisa.
2. **Priorización:** Se evaluó la calidad de cada registro (presencia de fechas reales, títulos válidos y números mayores a 0). Se ordenó el DataFrame de manera descendente para empujar los registros más completos a la parte superior.
3. **Detección y Eliminación:** Se utilizó `df.duplicated(keep='first')` evaluando 3 escenarios: coincidencia exacta de llaves, y coincidencias donde faltaba la temporada o el episodio. Al mantener el primer registro ('first'), se garantizó la supervivencia del registro con mejor calidad de datos.
"""

    reporte_md = f"""# Data Quality Report

## Metrics
* **Total number of input records:** {total_input}
* **Total number of output records:** {total_output}
* **Number of discarded entries:** {discarded_entries}
* **Number of corrected entries:** {corrected_entries}
* **Number of duplicates detected:** {duplicates_detected}

## Deduplication Strategy
{estrategia}
"""

    with open('report.md', 'w', encoding='utf-8') as file:
        file.write(reporte_md)

    print('Reporte generado con exito en report.md')
    print(reporte_md)

#empezamos leyendo el archivo de entrada
df_inicial = pd.read_csv("input.csv")

#normalizamos el cotenido del input segun los criterios asignados
df_normalizado = normalize_data(df_inicial)

#eliminamos registros duplicados
df_final = remove_duplicates(df_normalizado)
print(df_final)

#Transformamos el dataframe a csv, y le quitamos la columna extra de indices
df_final.to_csv('episodes_clean.csv', index=False)
generate_quality_report(df_inicial, df_normalizado, df_final)