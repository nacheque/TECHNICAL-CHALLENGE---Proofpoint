from flask import Flask
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

    #creamos columnas temporales para comparar
    #los replace() usan expresiones regulares que eliminan los espacios al medio entre titulos y los pasa a minuscula
    df['Series_norm'] = df['SeriesName'].str.strip().str.replace(r'\s+', ' ', regex=True).str.lower()
    df['Title_norm'] = df['EpisodeTitle'].str.strip().str.replace(r'\s+', ' ', regex=True).str.lower()

    #consignas de prioridad para elegir el mejor registro
    #las agregamos en columnas temporales para ver que condiciones cumple cada registro
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


df = pd.read_csv("input.csv")
df = normalize_data(df)
df = remove_duplicates(df)
print(df)