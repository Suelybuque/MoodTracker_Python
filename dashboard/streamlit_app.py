import os
import sys
from datetime import date
import streamlit as st
import pandas as pd
import plotly.express as px

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
from pipeline.db import MoodDB
from pipeline.transform import Transformer

# ---------------------
# Setup
# ---------------------
st.set_page_config(
    page_title="Mood & Energy Dashboard",
    page_icon="😊",
    layout="wide"
)

db = MoodDB()
records = db.fetch_all()
t = Transformer.from_records(records) if records else None
df = pd.DataFrame(records) if records else pd.DataFrame()

# ---------------------
# Sidebar Form
# ---------------------
st.sidebar.header("Add a new entry")

# Initialize session state defaults
for key, default in [("mood", 3), ("energy", 3), ("stress", 3), ("notes", "")]:
    if key not in st.session_state:
        st.session_state[key] = default


def submit_entry():
    db.insert(
        date.today(),
        st.session_state.mood,
        st.session_state.energy,
        st.session_state.stress,
        st.session_state.notes
    )
    st.success("Entry saved!")

    # Reset form
    st.session_state.mood = 3
    st.session_state.energy = 3
    st.session_state.stress = 3
    st.session_state.notes = ""

    # Refresh dataframe
    global df, t
    records = db.fetch_all()
    df = pd.DataFrame(records)
    t = Transformer.from_records(records)


with st.sidebar.form("mood_form"):
    st.slider("Mood (1-5)", 1, 5, key="mood")
    st.slider("Energy (1-5)", 1, 5, key="energy")
    st.slider("Stress (1-5)", 1, 5, key="stress")
    st.text_area("Notes / Thoughts", key="notes", placeholder="Write something...")
    st.form_submit_button("Add Entry", on_click=submit_entry)

# ---------------------
# Main Dashboard
# ---------------------
st.title("🌈 Mood & Energy Dashboard")

if df.empty:
    st.info('No data yet. Use the sidebar to add your first entry!')
else:
    # Weekly Summary Cards
    summary = t.weekly_summary()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Mood", summary.get("avg_mood", "-"))
    col2.metric("Avg Energy", summary.get("avg_energy", "-"))
    col3.metric("Avg Stress", summary.get("avg_stress", "-"))

    st.markdown("---")

    # Rolling Trend Chart
    st.subheader("📈 Rolling Trend (7-day)")
    trend = t.rolling_trend(7)
    if not trend.empty:
        fig= px.line(
            trend,
            x="date",
            y=["mood", "energy", "stress"],
            markers= True,
            labels= {"value": "Score", "date":"Date"},
            title="Mood, Energy, Stress Over Time"
        )

        fig.update_traces(line=dict(width=4))
        fig.update_xaxes(tickformat="%Y-%m-%d %H:%M")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")


    # Raw Entries Table
    st.subheader("📊 Raw Entries")
    st.dataframe(df.sort_values("date", ascending=False).reset_index(drop=True))
