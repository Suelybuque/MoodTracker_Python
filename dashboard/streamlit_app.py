import os
import sys
from datetime import date, datetime
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------
# Path setup
# ---------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from pipeline.db import MoodDB
from pipeline.transform import Transformer

# ---------------------
# Streamlit Setup
# ---------------------
st.set_page_config(
    page_title="Mood & Energy Dashboard",
    page_icon="😊",
    layout="wide"
)

db = MoodDB()
records = db.fetch_all()
df = pd.DataFrame(records) if records else pd.DataFrame()


# Timestamps 
if not df.empty and "date" in df.columns:
  df['date'] = pd.to_datetime(df['date'])

t = Transformer.from_records(records) if records else None

# ---------------------
# Sidebar - Add Entry
# ---------------------
st.sidebar.header("Add a new entry")

for key, default in [("mood", 3), ("energy", 3), ("stress", 3), ("notes", "")]:
    if key not in st.session_state:
        st.session_state[key] = default


def submit_entry():
    db.insert(
        datetime.now(),
        st.session_state.mood,
        st.session_state.energy,
        st.session_state.stress,
        st.session_state.notes
    )

    st.success("Entry saved!")

    # Reset fields
    st.session_state.mood = 3
    st.session_state.energy = 3
    st.session_state.stress = 3
    st.session_state.notes = ""

    # Reload data
    global df, t
    records = db.fetch_all()
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
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
    st.info("No data yet. Use the sidebar to add your first entry!")
else:
    # --- Weekly Summary ---
    summary = t.weekly_summary()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Mood", summary.get("avg_mood", "-"))
    col2.metric("Avg Energy", summary.get("avg_energy", "-"))
    col3.metric("Avg Stress", summary.get("avg_stress", "-"))

    st.markdown("---")

    # --- Rolling Trend Chart ---
    st.subheader("📈 Rolling Trend (7-day)")
    trend = t.rolling_trend(7)
    trend['time'] = trend['date'].dt.strftime('%H:%M')   # hora:minuto
    trend['day'] = trend['date'].dt.strftime('%d-%m-%Y') # dia-mês-ano

    if not trend.empty:
        fig = px.line(
            trend,
            x="date",
            y=["mood", "energy", "stress"],
             color='variable',
            hover_data={'day': trend['day']},
            markers=True,
            labels={"value": "Score", "date": "Date"},
            title="Mood, Energy, Stress Over Time"
        )

        fig.update_traces(line=dict(width=4))
        fig.update_xaxes(
            tickformat="%H:%M<br>%d/%m/%Y",
            tickangle=0
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Raw Table ---
    st.subheader("📊 Raw Entries")
    st.dataframe(df.sort_values("date", ascending=False).reset_index(drop=True))
