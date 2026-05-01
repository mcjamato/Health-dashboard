import streamlit as st
from datetime import datetime

st.title("🧠 Wellbeing & Recovery")
db = st.session_state.db

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌙 Sleep Tracker")
    sleep_qty = st.number_input("Hours of Sleep", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    
with col2:
    st.subheader("🎭 Mental Health")
    mood = st.select_slider(
        "Current Mood",
        options=["Very Low", "Low", "Neutral", "Good", "Excellent"],
        value="Neutral"
    )
    stress = st.slider("Stress Level (1 = Calm, 10 = High)", 1, 10, 5)

with st.form("wellbeing_form"):
    log_date = st.date_input("Date", datetime.today())
    notes = st.text_area("Journal/Notes", placeholder="How are you feeling today?")
    
    if st.form_submit_button("Save Wellbeing Log"):
        # Note: We use the 'foods' column to store notes for simplicity, 
        # or you can add a 'notes' column to your SQL table.
        query = """
            INSERT INTO health_logs (log_date, sleep_hours, mood, stress_level, foods) 
            VALUES (?, ?, ?, ?, ?)
        """
        db.run_query(query, (str(log_date), sleep_qty, mood, stress, notes))
        st.success("Recovery data saved!")