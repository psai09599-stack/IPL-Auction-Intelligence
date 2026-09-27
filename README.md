# IPL Auction Intelligence

A data pipeline and scouting tool for IPL player auctions — combining historical auction prices, ball-by-ball performance data, and player metadata to support pre-auction decision-making.

## Project Status: Phase 1 Complete ✅

Phase 1 built the full data foundation: raw auction + match data → cleaned tables → a working Streamlit app.

## Data Sources

| Source | Coverage | Notes |
|---|---|---|
| Kaggle auction dataset (`auction.csv`) | 2013–2023 | Prices originally in Lakhs, converted to Crores |
| Kaggle auction dataset (`auction_2025.csv`) | 2025 | Includes sold, unsold, and TBA (unresolved) rows |
| Cricsheet (`cricsheet_ipl/`) | 2008–2026 | Ball-by-ball data for every IPL match, 1,243 matches |
| TATA IPL 2025 Auction List (Kaggle) | 2025 | Player metadata: DOB, role, batting/bowling style, nationality |
| Manually verified (ESPNcricinfo/Wikipedia) | 37 retained players, 2025 | Retained players don't appear in auction-list datasets |

**Known data gaps** (documented, not silently ignored):
- 2024 auction data not sourced (mini-auction, mostly retentions)
- 132 of 673 auction players (2013–2025) unmatched to Cricsheet names (`unmatched_names.csv`)
- 26 of 329 players in the 2025 pool missing from `player_meta.csv`

## Pipeline (`notebooks/01_data_audit.ipynb`)

1. **Clean auction data** — fix comma-formatted numbers, lakhs→crores conversion, separate sold/unsold/TBA status
2. **Load & audit Cricsheet data** — verify readability, normalize season labels (e.g. `2007/08` → `2008`)
3. **Player ID mapping** — match auction names to Cricsheet names (exact match → surname+initial → manual resolution for ambiguous cases), producing a stable `player_id` for every matched player
4. **Player metadata** — DOB, role, batting/bowling style, nationality, sourced and merged from a Kaggle dataset + manual verification for retained players
5. **Season metrics** — parse every ball of every match into per-player, per-season batting and bowling stats

## Output Files (`data/clean/`)

| File | Rows | Description |
|---|---|---|
| `auction_history.csv` | 1,279 | Sold players, 2013–2025, standardized prices in Crores |
| `unsold_2025.csv` | 103 | Unsold players from 2025 auction |
| `player_id_map.csv` | 620 | Links auction names ↔ Cricsheet names ↔ `player_id` |
| `unmatched_names.csv` | 132 | Documented name-matching gaps |
| `player_meta.csv` | 303 | DOB, role, batting/bowling style, nationality (2025 pool) |
| `player_season_metrics_batting.csv` | — | Runs, strike rate, average per player per season |
| `player_season_metrics_bowling.csv` | — | Wickets, economy, bowling average per player per season |

## Running the App

```bash
cd IPL-Auction-Intelligence
venv\Scripts\activate
streamlit run app/Home.py
```

Search any player to see their season-by-season batting and bowling record.

## Setup (for a fresh clone)

```bash
git clone https://github.com/YOUR-USERNAME/ipl-auction-intelligence.git
cd ipl-auction-intelligence
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Raw data (`data/raw/`) is not committed — see Data Sources above for where to obtain it.

## Validation

Key stats were spot-checked against ESPNcricinfo:
- Virat Kohli's 2016 season: 973 runs, 81.08 average ✅ (matches his real record IPL season)
- Jasprit Bumrah's career shape (2015 slow start, 2019–2021 peak, missing 2023 due to injury) ✅

Minor known discrepancies: strike rate / economy figures are slightly off from official stats because wides/no-balls are currently counted as "balls faced/bowled" — documented simplification, to be refined in a later phase.

## Next: Phase 2

Feature engineering and auction valuation modeling (planned).
