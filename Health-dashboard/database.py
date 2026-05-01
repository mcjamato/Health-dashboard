import sqlite3
import pandas as pd

class HealthDB:
    def __init__(self, db_name="health_data.db"):
        self.db_name = db_name
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def _init_db(self):
        with self._get_conn() as conn:
            # Health Data Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS health_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, age INTEGER, weight_lbs REAL, height_ft INTEGER, height_in INTEGER,
                    log_date DATE, calories INTEGER, foods TEXT,
                    exercise_type TEXT, duration INTEGER,
                    mood TEXT, sleep_hours REAL, stress_level INTEGER
                )
            """)
            # RBAC User Table
            conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)")
            # Default Credentials
            conn.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin123', 'Admin')")
            conn.execute("INSERT OR IGNORE INTO users VALUES ('analyst', 'data456', 'User')")
            conn.commit()

    def run_query(self, query, params=()):
        with self._get_conn() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor

    def get_df(self):
        with self._get_conn() as conn:
            return pd.read_sql("SELECT * FROM health_logs ORDER BY log_date DESC", conn)

    def authenticate(self, username, password):
        query = "SELECT role FROM users WHERE username=? AND password=?"
        with self._get_conn() as conn:
            res = conn.execute(query, (username, password)).fetchone()
            return res[0] if res else None