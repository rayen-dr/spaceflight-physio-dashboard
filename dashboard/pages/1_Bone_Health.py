import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_loader import load_physio, DURATION_COLORS

st.set_page_config(page_title="Bone Health", page_icon="🦴", layout="wide")
st.title("🦴 Bone Health")
st.caption("Bone mineral density change by skeletal site — literature-compiled, see docs/data_sources.md")

physio = load_physio()
bone = physio[physio['system'] == 'Bone'].copy()

durations = st.multiselect(
    "Filter by mission duration category",
    options=sorted(bone['mission_duration_category'].unique()),
    default=sorted(bone['mission_duration_category'].unique()),
)
bone_f = bone[bone['mission_duration_category'].isin(durations)]

col1, col2 = st.columns(2)
col1.metric("Findings shown", len(bone_f))
col2.metric("Skeletal sites covered", bone_f['body_site_or_context'].nunique())

st.markdown("### % Change by Skeletal Site")
site_data = bone_f[bone_f['metric_type'].isin(['percent_change_per_month', 'percent_change_total'])]
fig = px.bar(
    site_data.sort_values('value'),
    x='value', y='body_site_or_context', color='mission_duration_category',
    color_discrete_map=DURATION_COLORS, orientation='h',
    labels={'value': '% change', 'body_site_or_context': 'Skeletal site'},
    hover_data=['measure', 'source_citation'],
)
fig.add_vline(x=0, line_color='black', line_width=1)
st.plotly_chart(fig, width='stretch')

st.markdown("### 1-Year Post-Flight Recovery")
recovery = bone[bone['metric_type'] == 'percent_recovered_astronauts']
if not recovery.empty:
    fig2 = px.bar(
        recovery, x='body_site_or_context', y='value',
        labels={'value': '% of astronauts back to baseline at 1 year', 'body_site_or_context': 'Site'},
        color_discrete_sequence=['#5D8AA8'],
    )
    st.plotly_chart(fig2, width='stretch')
    st.caption(
        "Even a year after return, most astronauts have not fully recovered pre-flight bone "
        "density at the hip or spine — a key finding worth highlighting in your report."
    )

with st.expander("📖 Sources for this page"):
    for _, row in bone_f[['source_citation', 'source_url']].drop_duplicates().iterrows():
        st.markdown(f"- {row['source_citation']} — [{row['source_url']}]({row['source_url']})")

st.warning(
    "⚠️ **Limitation**: this data is aggregated across published studies (cross-study means), "
    "not longitudinal measurements on individual astronauts. No BMD-vs-lean-mass relationship "
    "or bone turnover markers are available in any of our datasets — see "
    "`docs/data_coverage_analysis.md`."
)
