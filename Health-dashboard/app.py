import streamlit as st
import plotly.express as px
import pandas as pd
from database import HealthDB

st.set_page_config(page_title="Health DashBoard", layout="wide")

if 'db' not in st.session_state:
    st.session_state.db = HealthDB()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

if not st.session_state.logged_in:
    st.title("🔐 Health DashBoard Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        role = st.session_state.db.authenticate(user, pw)
        if role:
            st.session_state.logged_in = True
            st.session_state.user_role = role
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

st.sidebar.write(f"Access: **{st.session_state.user_role}**")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🚀 Health Overview")
df = st.session_state.db.get_df()

# Inside your input form (e.g., in app.py or a new Profile page)
st.subheader("Physical Metrics")
weight_lbs = st.number_input("Weight (lbs)", min_value=0.0, value=150.0, step=0.1)

col_ft, col_in = st.columns(2)
with col_ft:
    ft = st.number_input("Height (Feet)", min_value=0, max_value=8, value=5)
with col_in:
    inches = st.number_input("Height (Inches)", min_value=0, max_value=11, value=9)

# Total height in inches for calculations if needed
total_inches = (ft * 12) + inches

# if not df.empty:
#     m1, m2, m3 = st.columns(3)
#     m1.metric("Weight", f"{df.iloc[0]['weight']} lbs")
#     m2.metric("Avg Calories", f"{int(df['calories'].mean())} kcal")
#     m3.metric("Avg Sleep", f"{round(df['sleep_hours'].mean(), 1)} hrs")
    
if not df.empty:
    m1, m2, m3 = st.columns(3)
    latest = df.iloc[0]
    
    # Use .get() or check if column exists to prevent KeyErrors
    weight_val = latest.get('weight_lbs', 0)
    m1.metric("Weight", f"{weight_val} lbs")
    
    # Safely handle Height
    h_ft = latest.get('height_ft', 0)
    h_in = latest.get('height_in', 0)
    m2.metric("Height", f"{int(h_ft)}' {int(h_in)}\"")
    
    # Safely calculate Sleep Average
    if 'sleep_hours' in df.columns:
        avg_sleep = round(df['sleep_hours'].mean(), 1)
        m3.metric("Avg Sleep", f"{avg_sleep} hrs")
    else:
        m3.metric("Avg Sleep", "No Data")


    
    st.subheader("Trends")
    fig = px.line(df.sort_values('log_date'), x='log_date', y=['weight', 'calories'], markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Log your first entry in the sidebar tabs.")