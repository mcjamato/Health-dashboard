import streamlit as st

st.title("🛠️ Admin Tools")
if st.session_state.user_role != "Admin":
    st.error("Unauthorized")
    st.stop()

db = st.session_state.db
df = db.get_df()

edited_df = st.data_editor(df, num_rows="dynamic")

if st.button("Save Changes"):
    with db._get_conn() as conn:
        edited_df.to_sql("health_logs", conn, if_exists="replace", index=False)
    st.success("Database Updated")