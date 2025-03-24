# 🏀 NBA Stats Dashboard (2024–2025 Season)

This is a live, interactive **Streamlit dashboard** that displays aggregated player statistics for the **2024–2025 NBA regular season**, using data from [nba_api](https://github.com/swar/nba_api).

The app supports sortable tables, team filters, minutes/game and games played filters, and automatically updates daily using GitHub Actions.

---

## 🚀 Live App

🔗 [View the live app on Streamlit Cloud](https://hthindi1993nbastatsdashboard20242025seasononly.streamlit.app)

---

## 📊 Features

- Player stats aggregated by team and across teams (multi-team players)
- Sortable table with:
  - PPG, MPG, FG%, 3P%, FT%, TS%, eFG%, and advanced metrics
- Filters:
  - Filter by team
  - Minimum games played
  - Minimum minutes per game (MPG)
- Auto-updates daily via `scheduler.py` + GitHub Actions

---

## 🗃 Project Structure


---

## 🛠 Tech Stack

- Python 3.10
- Streamlit
- nba_api
- Pandas / NumPy
- SQLite (for data storage)
- GitHub Actions (for automation)

---

## 🔄 Auto Update (via GitHub Actions)

- `scheduler.py` pulls the latest game logs daily from `nba_api`
- Updates the local SQLite DB
- Commits and pushes changes to the repo
- Streamlit app uses this updated database

🕑 Runs daily at **2:00 AM CST** (`8:00 AM UTC`)

---

## 🧪 Local Setup (Optional)

```bash
# Clone the repo
git clone https://github.com/hthindi-1993/nbastats_dashboard_2024_2025_season_only.git
cd nbastats_dashboard_2024_2025_season_only

# Install dependencies
pip install -r requirements.txt

# Run the app locally
streamlit run streamlit_app.py
