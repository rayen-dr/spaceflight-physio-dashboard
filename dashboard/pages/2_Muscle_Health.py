import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_loader import load_physio, DURATION_COLORS

st.set_page_config(page_title="Muscle Health", page_icon="💪", layout="wide")
st.title("💪 Muscle Health")
st.caption("Muscle mass & strength change by group — literature-compiled, see docs/data_sources.md")

physio = load_physio()
muscle = physio[physio['system'] == 'Muscle'].copy()

durations = st.multiselect(
    "Filter by mission duration category",
    options=sorted(muscle['mission_duration_category'].unique()),
    default=sorted(muscle['mission_duration_category'].unique()),
    key="muscle_duration_filter",
)
muscle_f = muscle[muscle['mission_duration_category'].isin(durations)]

col1, col2 = st.columns(2)
col1.metric("Findings shown", len(muscle_f))
col2.metric("Muscle groups covered", muscle_f['body_site_or_context'].nunique())

st.markdown("### % Change by Muscle Group")
st.caption("Compare orange (short-duration) vs. blue (long-duration) bars for matching muscle groups — "
           "notice long-duration losses are consistently larger.")
fig = px.bar(
    muscle_f.sort_values('value'),
    x='value', y='body_site_or_context', color='mission_duration_category',
    color_discrete_map=DURATION_COLORS, orientation='h',
    labels={'value': '% change', 'body_site_or_context': 'Muscle group'},
    hover_data=['measure', 'source_citation'],
)
fig.add_vline(x=0, line_color='black', line_width=1)
st.plotly_chart(fig, width='stretch')

with st.expander("📖 Sources for this page"):
    for _, row in muscle_f[['source_citation', 'source_url']].drop_duplicates().iterrows():
        st.markdown(f"- {row['source_citation']} — [{row['source_url']}]({row['source_url']})")

st.warning(
    "⚠️ **Limitation**: only 1 muscle strength data point exists in our data (calf twitch force, "
    "long-duration only). Type I fiber atrophy is not available in any open dataset we found — "
    "see `docs/data_coverage_analysis.md`."
)
