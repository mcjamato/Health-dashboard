import streamlit as st
from datetime import datetime

st.title("🌙 Wellbeing")
db = st.session_state.db

with st.form("well"):
    sleep = st.number_input("Sleep Hours", 0.0, 24.0, 7.0)
    mood = st.selectbox("Mood", ["Low", "Neutral", "Good"])
    stress = st.slider("Stress", 1, 10, 5)
    date = st.date_input("Date", datetime.today())
    if st.form_submit_button("Save"):
        db.run_query("INSERT INTO health_logs (sleep_hours, mood, stress_level, log_date) VALUES (?, ?, ?, ?)", (sleep, mood, stress, str(date)))
        st.success("Saved")