import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPL Auction Intelligence", layout="wide")
st.title("IPL Auction Intelligence")
st.caption("Pre-auction scouting tool — data covers IPL 2008–2026 (2024 auction gap documented)")

batting = pd.read_csv("data/clean/player_season_metrics_batting.csv")
bowling = pd.read_csv("data/clean/player_season_metrics_bowling.csv")

player = st.selectbox("Search a player", sorted(batting["full_name"].unique()))

col1, col2 = st.columns(2)
with col1:
    st.subheader("Batting")
    st.dataframe(batting[batting["full_name"] == player].sort_values("season").drop(columns=["player"]))
with col2:
    st.subheader("Bowling")
    st.dataframe(bowling[bowling["full_name"] == player].sort_values("season").drop(columns=["player"]))