import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_loader import load_physio, DURATION_COLORS

st.set_page_config(page_title="Cardiovascular", page_icon="❤️", layout="wide")
st.title("❤️ Cardiovascular System")
st.caption("Orthostatic intolerance & fluid-shift effects — literature-compiled")

physio = load_physio()
cardio = physio[physio['system'] == 'Cardiovascular'].copy()

st.markdown("### Orthostatic Intolerance Incidence by Mission Duration")
oi = cardio[cardio['measure'] == 'Orthostatic intolerance incidence']
fig = px.bar(
    oi, x='mission_duration_category', y='value', color='mission_duration_category',
    color_discrete_map=DURATION_COLORS,
    labels={'value': '% of astronauts affected', 'mission_duration_category': 'Mission duration'},
    hover_data=['source_citation'],
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, width='stretch')
st.caption(
    "Long-duration missions show a dramatically higher incidence of orthostatic intolerance "
    "(dizziness/fainting risk upon standing) than short-duration ones — one of the clearest "
    "duration effects in the whole project."
)

st.markdown("### Fluid Shift Effects (Early In-flight)")
fluid = cardio[cardio['body_site_or_context'] == 'Early in-flight']
if not fluid.empty:
    fig2 = px.bar(
        fluid, x='measure', y='value',
        labels={'value': '% change from baseline', 'measure': ''},
        color_discrete_sequence=['#5D8AA8'],
        hover_data=['source_citation'],
    )
    st.plotly_chart(fig2, width='stretch')
    st.caption(
        "Early in-flight, fluid shifts toward the upper body actually *increase* cardiac "
        "output and stroke volume — before deconditioning sets in over a longer mission."
    )

with st.expander("📖 Sources for this page"):
    for _, row in cardio[['source_citation', 'source_url']].drop_duplicates().iterrows():
        st.markdown(f"- {row['source_citation']} — [{row['source_url']}]({row['source_url']})")

st.warning(
    "⚠️ **Limitation**: resting heart rate, blood pressure, and heart rate variability (HRV) "
    "are **not available** in any of our 3 datasets — a real gap in open, individual-level "
    "cardiovascular data. See `docs/data_coverage_analysis.md` for why this wasn't pursued "
    "further within this project's timeline."
)
