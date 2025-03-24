# 🛠️ DB & Table Creation Script

**File:** `db_and_table_creation.py`  
**Purpose:** Initializes the SQLite database used in the NBA Stats Dashboard project by creating necessary tables for storing game logs.

---

## 🧾 What It Does

- Creates (or recreates) the SQLite database file:  
  `sqlite3_DB/NbaPlayers_2024_2025_Traditional_And_Advanced_Stats.db`
  
- Drops and recreates the following tables:
  - `NBA_PLAYER_GAMELOGS_REGULARSEASON`
  - `NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED`

- Ensures each table has the correct schema and primary key constraints for data ingestion and upserts.

---

## ⚠️ Important Notes

- This script **drops** existing tables if they exist — use with caution if you're preserving data.
- Intended to be run **once** before using the dashboard or ingestion scripts.

---

## 🧪 How to Use

```bash
python db_and_table_creation.py

Creates or Resets:
sqlite3_DB/NbaPlayers_2024_2025_Traditional_And_Advanced_Stats.db
├── NBA_PLAYER_GAMELOGS_REGULARSEASON
├── NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED


---

## 📄 For `OneTimeHistoricalPull.py`

```markdown
# 📦 One-Time Historical Data Pull

**File:** `Archive/OneTimeHistoricalPull.py`  
**Purpose:** Pulls and stores all available **historical game data** for the 2024–2025 NBA season — both traditional and advanced stats — using the `nba_api`.

---

## 🧾 What It Does

- Loops through the desired NBA season range (typically just 2024–2025)
- Pulls game logs via `nba_api.stats.endpoints.playergamelogs`
- Saves the data into the SQLite DB:
  - `NBA_PLAYER_GAMELOGS_REGULARSEASON`
  - `NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED`

- Converts `MIN` field into a float-based `MIN_SEC` column
- Handles multi-team players and consistent schema formatting

---

## 🧪 How to Use

Make sure:
- The DB file and tables are already created via `db_and_table_creation.py`
- You’ve installed all required packages (`nba_api`, `pandas`, etc.)

Then run:

```bash
python Archive/OneTimeHistoricalPull.py


populates SQLite3 DB

sqlite3_DB/NbaPlayers_2024_2025_Traditional_And_Advanced_Stats.db
├── NBA_PLAYER_GAMELOGS_REGULARSEASON
├── NBA_PLAYER_GAMELOGS_REGULARSEASON_ADVANCED

