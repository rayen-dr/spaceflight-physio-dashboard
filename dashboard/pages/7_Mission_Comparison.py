import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_loader import PROJECT_ROOT
import pandas as pd

st.set_page_config(page_title="Mission Comparison", page_icon="🛰️", layout="wide")
st.title("🛰️ Mission Comparison")
st.caption("Missions parsed from astronaut flight records — name and year only, see limitation below")

missions = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "missions_exploded.csv")

vehicle_types = st.multiselect(
    "Filter by vehicle type", sorted(missions['vehicle_type'].unique()),
    default=sorted(missions['vehicle_type'].unique()),
)
filtered = missions[missions['vehicle_type'].isin(vehicle_types)]

st.markdown("### Missions per Year")
by_year = filtered.groupby('year')['mission_name'].nunique().reset_index(name='num_missions')
fig = px.bar(by_year, x='year', y='num_missions', labels={'num_missions': 'Distinct missions'})
st.plotly_chart(fig, width='stretch')

st.markdown("### Crew Size by Mission (Top 20 Largest Crews Recorded)")
crew_size = (
    filtered.groupby(['mission_name', 'year'])['astronaut_name']
    .nunique().reset_index(name='crew_size')
    .sort_values('crew_size', ascending=False).head(20)
)
st.dataframe(crew_size, width='stretch', hide_index=True)

st.markdown("### Vehicle Type Breakdown")
fig2 = px.pie(filtered, names='vehicle_type', title=None)
st.plotly_chart(fig2, width='stretch')

st.warning(
    "⚠️ **Limitation**: only mission name and launch year are recoverable from the source "
    "data — no exact date, no return date, no per-mission duration, and no official mission "
    "type classification (vehicle type here is a best-effort text match, not authoritative). "
    "See `docs/data_coverage_analysis.md`."
)
