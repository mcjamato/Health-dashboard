import streamlit as st
from datetime import datetime

st.title("🏃 Performance")
db = st.session_state.db

with st.form("perf"):
    ex = st.text_input("Exercise Type")
    dur = st.number_input("Duration (min)", 0, 500)
    date = st.date_input("Date", datetime.today())
    if st.form_submit_button("Save"):
        db.run_query("INSERT INTO health_logs (exercise_type, duration, log_date) VALUES (?, ?, ?)", (ex, dur, str(date)))
        st.success("Saved")