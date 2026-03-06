import pandas as pd

df = pd.read_csv("input.csv")


def normalize_data(df):
    #Series Name, Season Number, Episode Number, Episode Title y Air Date
    # eliminar registros sin nombre serie
    df = df.dropna(subset=['SeriesName'])

    # Quitar espacios extra y normalizar mayúsculas 
    df['SeriesName'] = df['SeriesName'].str.strip().str.title()
    df['EpisodeTitle'] = df['EpisodeTitle'].str.strip()
    
    #set to 0 --> season or episode missing, empty, neg, not number
    df['SeasonNumber'] = pd.to_numeric(df['SeasonNumber'], errors='coerce')
    df.loc[df['SeasonNumber'].isna() | (df['SeasonNumber'] < 0), 'SeasonNumber'] = 0

    df['EpisodeNumber'] = pd.to_numeric(df['EpisodeNumber'], errors='coerce')
    df.loc[df['EpisodeNumber'].isna() | (df['EpisodeNumber'] < 0), 'EpisodeNumber'] = 0
    df['EpisodeNumber'] = df['EpisodeNumber'].astype(int) # Fuerzo a número entero

    #set to 'Untlited Episode' --> Episode Title is missing or empty
    df.loc[(df['EpisodeTitle'].isna()) | (df['EpisodeTitle'] == ''), 'EpisodeTitle'] = 'Untitled Episode'

    #Air Date If missing, empty, or invalid → replace with "Unknown"
    df['AirDate'] = pd.to_datetime(df['AirDate'], errors='coerce')
    df.loc[df['AirDate'].isna(), 'AirDate'] = 'Unknown'

    #When Episode Number, Episode Title and Air Date are missing (the three fields), discard the record
    cond_episode_number = (df['EpisodeNumber'] == 0) | (df['EpisodeNumber'].isna())
    cond_episode_title = (df['EpisodeTitle'] == 'UntitledEpisode') | (df['EpisodeTitle'].isna())
    cond_air_date = (df['AirDate'] == 'Unknown') | (df['AirDate'].isna())

    discard_record = cond_episode_number & cond_episode_title & cond_air_date
    df = df.drop(df[discard_record].index)
    
    return df

def eliminate_duplicates(df):
    pass

df = normalize_data(df)
print(df)