import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_loader import load_physio

st.set_page_config(page_title="Sleep", page_icon="😴", layout="wide")
st.title("😴 Sleep")
st.caption("Sleep duration across mission phases — literature-compiled")

physio = load_physio()
sleep = physio[physio['system'] == 'Sleep'].copy()

st.markdown("### Average Sleep Duration by Context")
hours = sleep[sleep['metric_type'] == 'mean_hours']
fig = px.bar(
    hours.sort_values('value'),
    x='value', y='body_site_or_context', orientation='h',
    color='mission_duration_category',
    color_discrete_map={"Short": "#E8A87C", "Long": "#5D8AA8", "Mixed": "#A8A8A8"},
    labels={'value': 'Hours of sleep per night', 'body_site_or_context': 'Context'},
    hover_data=['source_citation'],
)
fig.add_vline(x=8.5, line_dash='dash', line_color='red', annotation_text='NASA scheduled (8.5h)')
st.plotly_chart(fig, width='stretch')
st.caption(
    "Astronauts consistently sleep 2-3 hours less than NASA's own 8.5-hour schedule, "
    "regardless of mission duration — this looks operational/environmental rather than "
    "a duration-dependent physiological adaptation."
)

st.markdown("### Nights with Less Than 6 Hours of Sleep")
disturbance = sleep[sleep['metric_type'] == 'incidence_percent']
if not disturbance.empty:
    fig2 = px.bar(
        disturbance, x='mission_duration_category', y='value',
        labels={'value': '% of nights with <6h sleep', 'mission_duration_category': 'Duration'},
        color_discrete_sequence=['#E8A87C'],
    )
    st.plotly_chart(fig2, width='stretch')

with st.expander("📖 Sources for this page"):
    for _, row in sleep[['source_citation', 'source_url']].drop_duplicates().iterrows():
        st.markdown(f"- {row['source_citation']} — [{row['source_url']}]({row['source_url']})")

st.warning(
    "⚠️ **Limitation**: no validated sleep quality or sleep efficiency score is available. "
    "'% nights <6h' is used as a rough disturbance proxy, not a clinical insomnia measure."
)
