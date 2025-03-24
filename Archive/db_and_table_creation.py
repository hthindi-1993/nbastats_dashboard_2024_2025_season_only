###This creates DB and createts/drops tables within that DB
import sqlite3
import os

# Get the directory where this script is located
current_dir = os.path.dirname(__file__)

# Go one level up and into 'sqlite3_DB'
db_folder = os.path.join(current_dir, '..', 'sqlite3_DB')
os.makedirs(db_folder, exist_ok=True)  # Create folder if it doesn't exist

# Full DB path
db_path = os.path.join(db_folder, 'NbaPlayers_2024_2025_Traditional_And_Advanced_Stats.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS NBA_PLAYER_GAMELOGS_REGULARSEASON")
cursor.execute("DROP TABLE IF EXISTS NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED")

# Ensure the table structure matches the DataFrame schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS NBA_PLAYER_GAMELOGS_REGULARSEASON (
        SEASON_YEAR TEXT,
        PLAYER_ID TEXT,
        PLAYER_NAME TEXT,
        NICKNAME TEXT,
        TEAM_ID TEXT,
        TEAM_ABBREVIATION TEXT,
        TEAM_NAME TEXT,
        GAME_ID TEXT,
        GAME_DATE TEXT,
        MATCHUP TEXT,
        WL TEXT,
        MIN REAL,
        FGM REAL,
        FGA REAL,
        FG_PCT REAL,
        FG3M REAL,
        FG3A REAL,
        FG3_PCT REAL,
        FTM REAL,
        FTA REAL,
        FT_PCT REAL,
        OREB REAL,
        DREB REAL,
        REB REAL,
        AST REAL,
        TOV REAL,
        STL REAL,
        BLK REAL,
        BLKA REAL,
        PF REAL,
        PFD REAL,
        PTS REAL,
        PLUS_MINUS REAL,
        DD2 INTEGER,
        TD3 INTEGER,
        AVAILABLE_FLAG TEXT,
        MIN_SEC REAL,
        SEASON_START TEXT,
        SEASON_END TEXT,
        PRIMARY KEY (PLAYER_ID, GAME_ID, SEASON_YEAR)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED (
        SEASON_YEAR TEXT,
        PLAYER_ID TEXT,
        PLAYER_NAME TEXT,
        NICKNAME TEXT,
        TEAM_ID TEXT,
        TEAM_ABBREVIATION TEXT,
        TEAM_NAME TEXT,
        GAME_ID TEXT,
        GAME_DATE TEXT,
        MATCHUP TEXT,
        WL TEXT,
        MIN REAL,
        OFF_RATING REAL,
        DEF_RATING REAL,
        NET_RATING REAL,
        AST_PCT REAL,
        AST_TO REAL,
        AST_RATIO REAL,
        OREB_PCT REAL,
        DREB_PCT REAL,
        REB_PCT REAL,
        TM_TOV_PCT REAL,
        EFG_PCT REAL,
        TS_PCT REAL,
        USG_PCT REAL,
        PACE REAL,
        PACE_PER40 REAL,
        PIE REAL,
        POSS INTEGER,
        FGM INTEGER,
        FGA INTEGER,
        FGM_PG REAL,
        FGA_PG REAL,
        FG_PCT REAL,
        AVAILABLE_FLAG TEXT,
        MIN_SEC REAL,
        SEASON_START TEXT,
        SEASON_END TEXT,
        PRIMARY KEY (PLAYER_ID, GAME_ID, SEASON_YEAR)
    )
''')

conn.commit()
conn.close()

