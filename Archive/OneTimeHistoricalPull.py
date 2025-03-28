###This creates DB and createts/drops tables within that DB
from nba_api.stats.endpoints import leaguestandings,playergamelogs,leaguegamelog
import sqlite3
import os
import pandas as pd

# Get the directory where this script is located
current_dir = os.path.dirname(__file__)

# Go one level up and into 'sqlite3_DB'
db_folder = os.path.join(current_dir, '..', 'sqlite3_DB')
os.makedirs(db_folder, exist_ok=True)  # Create folder if it doesn't exist

# Full DB path
db_path = os.path.join(db_folder, 'NbaPlayers_2024_2025_Traditional_And_Advanced_Stats.db')

season_start_year = 2024
season_end_year = 2025

league_player_regularseason_gamelogs = pd.DataFrame()
league_player_regularseason_gamelogs_advanced = pd.DataFrame()


def get_player_game_logs(season_start_year):
    season_begin = str(season_start_year)
    season_end = str(season_start_year+1)[2:]
    df=playergamelogs.PlayerGameLogs(season_type_nullable='Regular Season',season_nullable=f'{season_begin}-{season_end}',date_to_nullable='3/26/2025').get_data_frames()[0][[
    'SEASON_YEAR', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID',
       'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP',
       'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',
       'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK',
       'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'DD2',
       'TD3','AVAILABLE_FLAG', 'MIN_SEC'
    ]]
    df['SEASON_START'] = str(season_start_year)
    df['SEASON_END'] = str(season_start_year+1)
    df['PLAYER_NAME'] = df['PLAYER_NAME'].replace('Jimmy Butler III','Jimmy Butler')    
    df['MIN_SEC'] = df['MIN_SEC'].apply(lambda x: int(x.split(':')[0])+int(x.split(':')[1])/60)
    return df

def get_player_game_logs_advanced(season_start_year):
    season_begin = str(season_start_year)
    season_end = str(season_start_year+1)[2:]
    df=playergamelogs.PlayerGameLogs(season_type_nullable='Regular Season',season_nullable=f'{season_begin}-{season_end}',date_to_nullable='3/26/2025',
    measure_type_player_game_logs_nullable='Advanced').get_data_frames()[0][['SEASON_YEAR', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID',
       'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP',
       'WL', 'MIN', 'OFF_RATING','DEF_RATING','NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO',
       'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT',
       'TS_PCT', 'USG_PCT', 'PACE', 'PACE_PER40',
       'PIE', 'POSS', 'FGM', 'FGA', 'FGM_PG', 'FGA_PG',
       'FG_PCT','AVAILABLE_FLAG', 'MIN_SEC']]
    df['SEASON_START'] = str(season_start_year)
    df['SEASON_END'] = str(season_start_year+1)
    df['PLAYER_NAME'] = df['PLAYER_NAME'].replace('Jimmy Butler III','Jimmy Butler')  
    df['MIN_SEC'] = df['MIN_SEC'].apply(lambda x: int(x.split(':')[0])+int(x.split(':')[1])/60)
    return df


for start in range(season_start_year,season_end_year):
    league_player_regularseason_gamelogs=pd.concat([league_player_regularseason_gamelogs,get_player_game_logs(start)],axis=0)
    league_player_regularseason_gamelogs_advanced=pd.concat([league_player_regularseason_gamelogs_advanced,get_player_game_logs_advanced(start)],axis=0)



def insert_league_player_regularseason_gamelogs(df, conn):
    cursor = conn.cursor()

    query = '''
        INSERT INTO NBA_PLAYER_GAMELOGS_REGULARSEASON (
            SEASON_YEAR, PLAYER_ID, PLAYER_NAME, NICKNAME, TEAM_ID, TEAM_ABBREVIATION, TEAM_NAME, GAME_ID, GAME_DATE, 
            MATCHUP, WL, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT, FTM, FTA, FT_PCT, OREB, DREB, REB, AST, TOV, 
            STL, BLK, BLKA, PF, PFD, PTS, PLUS_MINUS, DD2, TD3, AVAILABLE_FLAG, MIN_SEC, SEASON_START, SEASON_END
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(PLAYER_ID, GAME_ID, SEASON_YEAR) DO UPDATE SET
            SEASON_YEAR = excluded.SEASON_YEAR,
            PLAYER_ID = excluded.PLAYER_ID,
            PLAYER_NAME = excluded.PLAYER_NAME,
            NICKNAME = excluded.NICKNAME,
            TEAM_ID = excluded.TEAM_ID,
            TEAM_ABBREVIATION = excluded.TEAM_ABBREVIATION,
            TEAM_NAME = excluded.TEAM_NAME,
            GAME_ID = excluded.GAME_ID,
            GAME_DATE = excluded.GAME_DATE,
            MATCHUP = excluded.MATCHUP,
            WL = excluded.WL,
            MIN = excluded.MIN,
            FGM = excluded.FGM,
            FGA = excluded.FGA,
            FG_PCT = excluded.FG_PCT,
            FG3M = excluded.FG3M,
            FG3A = excluded.FG3A,
            FG3_PCT = excluded.FG3_PCT,
            FTM = excluded.FTM,
            FTA = excluded.FTA,
            FT_PCT = excluded.FT_PCT,
            OREB = excluded.OREB,
            DREB = excluded.DREB,
            REB = excluded.REB,
            AST = excluded.AST,
            TOV = excluded.TOV,
            STL = excluded.STL,
            BLK = excluded.BLK,
            BLKA = excluded.BLKA,
            PF = excluded.PF,
            PFD = excluded.PFD,
            PTS = excluded.PTS,
            PLUS_MINUS = excluded.PLUS_MINUS,
            DD2 = excluded.DD2,
            TD3 = excluded.TD3,
            AVAILABLE_FLAG = excluded.AVAILABLE_FLAG,
            MIN_SEC = excluded.MIN_SEC,
            SEASON_START = excluded.SEASON_START,
            SEASON_END = excluded.SEASON_END
    '''

    for _, row in df.iterrows():
        cursor.execute(query, tuple(row))

    conn.commit()
    conn.close()



def insert_league_player_regularseason_gamelogs_advanced(df, conn):
    cursor = conn.cursor()

    query = '''
        INSERT INTO NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED (
        SEASON_YEAR, PLAYER_ID, PLAYER_NAME, NICKNAME, TEAM_ID, TEAM_ABBREVIATION, TEAM_NAME, GAME_ID, GAME_DATE, MATCHUP,
        WL, MIN, OFF_RATING, DEF_RATING, NET_RATING, AST_PCT, AST_TO, AST_RATIO, OREB_PCT, DREB_PCT, REB_PCT, 
        TM_TOV_PCT, EFG_PCT, TS_PCT, USG_PCT, PACE, PACE_PER40, PIE, POSS, FGM, FGA, FGM_PG, FGA_PG, FG_PCT, 
        AVAILABLE_FLAG, MIN_SEC, SEASON_START, SEASON_END
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(PLAYER_ID, GAME_ID, SEASON_YEAR) DO UPDATE SET
            SEASON_YEAR = excluded.SEASON_YEAR,
            PLAYER_ID = excluded.PLAYER_ID,
            PLAYER_NAME = excluded.PLAYER_NAME,
            NICKNAME = excluded.NICKNAME,
            TEAM_ID = excluded.TEAM_ID,
            TEAM_ABBREVIATION = excluded.TEAM_ABBREVIATION,
            TEAM_NAME = excluded.TEAM_NAME,
            GAME_ID = excluded.GAME_ID,
            GAME_DATE = excluded.GAME_DATE,
            MATCHUP = excluded.MATCHUP,
            WL = excluded.WL,
            MIN = excluded.MIN,
            OFF_RATING = excluded.OFF_RATING,
            DEF_RATING = excluded.DEF_RATING,
            NET_RATING = excluded.NET_RATING,
            AST_PCT = excluded.AST_PCT,
            AST_TO = excluded.AST_TO,
            AST_RATIO = excluded.AST_RATIO,
            OREB_PCT = excluded.OREB_PCT,
            DREB_PCT = excluded.DREB_PCT,
            REB_PCT = excluded.REB_PCT,
            TM_TOV_PCT = excluded.TM_TOV_PCT,
            EFG_PCT = excluded.EFG_PCT,
            TS_PCT = excluded.TS_PCT,
            USG_PCT = excluded.USG_PCT,
            PACE = excluded.PACE,
            PACE_PER40 = excluded.PACE_PER40,
            PIE = excluded.PIE,
            POSS = excluded.POSS,
            FGM = excluded.FGM,
            FGA = excluded.FGA,
            FGM_PG = excluded.FGM_PG,
            FGA_PG = excluded.FGA_PG,
            FG_PCT = excluded.FG_PCT,
            AVAILABLE_FLAG = excluded.AVAILABLE_FLAG,
            MIN_SEC = excluded.MIN_SEC,
            SEASON_START = excluded.SEASON_START,
            SEASON_END = excluded.SEASON_END

    '''

    for _, row in df.iterrows():
        cursor.execute(query, tuple(row))

    conn.commit()
    conn.close()


insert_league_player_regularseason_gamelogs(league_player_regularseason_gamelogs, conn = sqlite3.connect(db_path))
insert_league_player_regularseason_gamelogs_advanced(league_player_regularseason_gamelogs_advanced, conn = sqlite3.connect(db_path))



