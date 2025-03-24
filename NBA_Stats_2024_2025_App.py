from nba_api.stats.endpoints import leaguestandings, playergamelogs, leaguegamelog
from datetime import datetime
import numpy as np
import pandas as pd
import sqlite3
import os
import streamlit as st

# Path setup — adjust if needed
db_path = os.path.join("sqlite3_DB", "NbaPlayers_2024_2025_Traditional_And_Advanced_Stats.db")

# Helper function to read SQL query
def run_query(db_path, query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

# Query for per-player-per-team aggregation
player_team_query = """
WITH T1 AS (
    SELECT
        regstats.SEASON_YEAR AS Season,
        regstats.SEASON_START AS Season_Start,
        regstats.SEASON_END AS Season_End,
        regstats.PLAYER_ID AS PlayerID,
        regstats.PLAYER_NAME AS Name,
        regstats.TEAM_ID AS TeamID,
        regstats.TEAM_ABBREVIATION AS TeamAbbrev,
        regstats.TEAM_NAME AS Team,
        COUNT(regstats.GAME_ID) AS GamesPlayed,
        ROUND(SUM(regstats.MIN_SEC) / COUNT(regstats.MIN_SEC), 1) AS MPG,
        ROUND(AVG(regstats.PTS), 1) AS PPG,
        ROUND(AVG(regstats.REB), 1) AS TRB,
        ROUND(AVG(regstats.AST), 1) AS AST,
        ROUND(AVG(regstats.STL), 1) AS STL,
        ROUND(AVG(regstats.BLK), 1) AS BLK,
        100 * ROUND(SUM(regstats.FGM) / NULLIF(SUM(regstats.FGA), 0), 3) AS 'FG%',
        100 * ROUND(SUM(regstats.FG3M) / NULLIF(SUM(regstats.FG3A), 0), 3) AS '3PT%',
        100 * ROUND(SUM(regstats.FTM) / NULLIF(SUM(regstats.FTA), 0), 3) AS 'FT%',
        100 * ROUND(SUM(regstats.PTS) / NULLIF(2 * (SUM(regstats.FGA) + 0.44 * SUM(regstats.FTA)), 0), 3) AS 'TS%',
        100 * ROUND((SUM(regstats.FGM) + 0.5 * SUM(regstats.FG3M)) / NULLIF(SUM(regstats.FGA), 0), 3) AS 'eFG%',
        ROUND(AVG(regstats.TOV), 1) AS TOV,
        ROUND(AVG(regstats.PF), 1) AS PF,
        ROUND(100 * SUM(regstats.PLUS_MINUS) / NULLIF(SUM(advancedstats.POSS), 0), 1) AS '+/-',
        SUM(regstats.DD2) AS DoubleDouble,
        SUM(regstats.TD3) AS TripleDouble,
        MAX(regstats.Game_Date) AS LastGamePlayed
    FROM NBA_PLAYER_GAMELOGS_REGULARSEASON regstats
    JOIN NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED advancedstats
        ON regstats.PLAYER_ID = advancedstats.PLAYER_ID 
        AND regstats.GAME_ID = advancedstats.GAME_ID 
        AND regstats.SEASON_YEAR = advancedstats.SEASON_YEAR
    WHERE regstats.MIN_SEC > 0
    GROUP BY regstats.SEASON_YEAR, regstats.PLAYER_ID, regstats.TEAM_ID
)
SELECT * FROM T1;
"""

# Query for per-player overall aggregation (across teams)
player_total_query = """
WITH T2 AS (
    SELECT
        regstats.SEASON_YEAR AS Season,
        regstats.SEASON_START AS Season_Start,
        regstats.SEASON_END AS Season_End,
        regstats.PLAYER_ID AS PlayerID,
        regstats.PLAYER_NAME AS Name,
        COUNT(regstats.GAME_ID) AS GamesPlayed,
        ROUND(SUM(regstats.MIN_SEC) / COUNT(regstats.MIN_SEC), 1) AS MPG,
        ROUND(AVG(regstats.PTS), 1) AS PPG,
        ROUND(AVG(regstats.REB), 1) AS TRB,
        ROUND(AVG(regstats.AST), 1) AS AST,
        ROUND(AVG(regstats.STL), 1) AS STL,
        ROUND(AVG(regstats.BLK), 1) AS BLK,
        100 * ROUND(SUM(regstats.FGM) / NULLIF(SUM(regstats.FGA), 0), 3) AS 'FG%',
        100 * ROUND(SUM(regstats.FG3M) / NULLIF(SUM(regstats.FG3A), 0), 3) AS '3PT%',
        100 * ROUND(SUM(regstats.FTM) / NULLIF(SUM(regstats.FTA), 0), 3) AS 'FT%',
        100 * ROUND(SUM(regstats.PTS) / NULLIF(2 * (SUM(regstats.FGA) + 0.44 * SUM(regstats.FTA)), 0), 3) AS 'TS%',
        100 * ROUND((SUM(regstats.FGM) + 0.5 * SUM(regstats.FG3M)) / NULLIF(SUM(regstats.FGA), 0), 3) AS 'eFG%',
        ROUND(AVG(regstats.TOV), 1) AS TOV,
        ROUND(AVG(regstats.PF), 1) AS PF,
        ROUND(100 * SUM(regstats.PLUS_MINUS) / NULLIF(SUM(advancedstats.POSS), 0), 1) AS '+/-',
        SUM(regstats.DD2) AS DoubleDouble,
        SUM(regstats.TD3) AS TripleDouble,
        MAX(regstats.Game_Date) AS LastGamePlayed
    FROM NBA_PLAYER_GAMELOGS_REGULARSEASON regstats
    JOIN NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED advancedstats
        ON regstats.PLAYER_ID = advancedstats.PLAYER_ID 
        AND regstats.GAME_ID = advancedstats.GAME_ID 
        AND regstats.SEASON_YEAR = advancedstats.SEASON_YEAR
    WHERE regstats.MIN_SEC > 0
    GROUP BY regstats.SEASON_YEAR, regstats.PLAYER_ID
)
SELECT * FROM T2;
"""

# Run queries
df_by_team = run_query(db_path, player_team_query)
df_by_player = run_query(db_path, player_total_query)

# Identify players with multiple teams
multi_team_players = df_by_team.groupby('PlayerID').size()
multi_team_ids = multi_team_players[multi_team_players > 1].index

# Filter and update totals
multi_team_totals = df_by_player[df_by_player.PlayerID.isin(multi_team_ids)].copy()
multi_team_totals['TeamAbbrev'] = 'Total'
multi_team_totals['Team'] = 'Total'

# Combine into one DataFrame
final_df = pd.concat(
    [multi_team_totals, df_by_team.drop(columns=['TeamID'])],
    axis=0,
    ignore_index=True
)
final_df.fillna(0,inplace=True)
final_df.drop(columns=['Season','Season_Start','Season_End','PlayerID','Team'],inplace=True)

# ========== Streamlit App ==========

st.set_page_config(page_title="NBA Player Stats 2024-25", layout="wide")

st.title("🏀 NBA Player Stats (2024–2025 Season)")
st.markdown("Explore sortable and searchable traditional & advanced player stats — including multi-team player averages.")

# === Team Filter with "Select All" option ===
teams = sorted(final_df['TeamAbbrev'].unique())
select_all = st.checkbox("Select All Teams", value=True)

if select_all:
    selected_teams = st.multiselect("Filter by Team", teams, default=teams)
else:
    selected_teams = st.multiselect("Filter by Team", teams)

# Filter by team
filtered_df = final_df[final_df['TeamAbbrev'].isin(selected_teams)]

# === Games Played & MPG Filters ===
min_games = st.slider(
    "Minimum Games Played", 
    min_value=int(0), 
    max_value=int(82), 
    value=10
)

min_mpg = st.slider(
    "Minimum Minutes Per Game (MPG)", 
    min_value=float(0), 
    max_value=float(48), 
    value=10.0,
    step=float(1)
)

# Apply filters
filtered_df = filtered_df[
    (filtered_df['GamesPlayed'] >= min_games) & 
    (filtered_df['MPG'] >= min_mpg)
]

# Reorder columns: move "TeamAbbrev" right after "Name"
cols = list(filtered_df.columns)
if "Name" in cols and "TeamAbbrev" in cols:
    cols.remove("TeamAbbrev")
    name_index = cols.index("Name")
    cols.insert(name_index + 1, "TeamAbbrev")
    filtered_df = filtered_df[cols]

# === Display Table ===
st.dataframe(
    filtered_df.sort_values(by='PPG', ascending=False),
    use_container_width=True,
    hide_index=True
)
