import streamlit as st
from data_manager import DataManager
from llm import LLM
from db_manager import init_db, save_predictions, get_all_datasets

st.set_page_config(page_title="LLM Predictor", page_icon="🤖")

init_db()

st.title("🏈 College Football Predictor")
st.markdown("Predict the outcome of ESPN College Pick-ems using OpenAI.")

st.sidebar.title("Input Parameters")

# ----- Sidebar -----
# Assuming 14 weeks in a season
week = st.sidebar.number_input("Week", min_value=1, max_value=15, value=1)

home_teams = st.sidebar.text_area(label="Home Teams (comma-separated)", placeholder="e.g., Team A, Team B, Team C")

dataset_name = st.sidebar.text_input("Dataset Name")

submit_button = st.sidebar.button("Submit")

# ----- Main View -----
if submit_button:
    if not home_teams or not dataset_name:
        st.error("Please fill in all fields.")
    else:
        data_manager = DataManager(week)

        teams = [team.strip() for team in home_teams.split(",")]

        predictions = {}

        with st.spinner("Generating predictions..."):
            for team in teams:
                current_week, home_team, away_team = data_manager.get_current_week(team)
                home_records = data_manager.get_team_records(home_team)
                away_records = data_manager.get_team_records(away_team)

                home_games = data_manager.get_previous_weeks(home_team)
                away_games = data_manager.get_previous_weeks(away_team)

                sp_stats_home = data_manager.get_sp_stats(home_team)
                sp_stats_away = data_manager.get_sp_stats(away_team)

            
                llm = LLM(current_week, home_records, away_records, home_games, away_games, sp_stats_home, sp_stats_away)

                prediction = llm.get_results()
                key = f"{home_team} vs {away_team}"
                predictions[key] = prediction

        save_predictions(dataset_name, predictions)
        st.success(f"Predictions saved to dataset: **{dataset_name}**")
        
        st.markdown("### Predictions")
        for matchup, pred in predictions.items():
            st.markdown(f"#### {matchup}")
            with st.container():
                st.markdown(f"<div style='white-space: pre-wrap'>{pred}</div>", unsafe_allow_html=True)


