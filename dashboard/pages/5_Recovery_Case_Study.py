import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_loader import load_cbc, TIMEPOINT_ORDER

st.set_page_config(page_title="Recovery Case Study", page_icon="🩸", layout="wide")
st.title("🩸 Recovery Case Study — Inspiration4 Blood Panel")
st.caption(
    "Real longitudinal data: 4 astronauts, 23 blood analytes, tracked from 92 days before "
    "launch to 194 days after return. Source: NASA OSDR, OSD-569 / LSDS-7."
)

st.info(
    "📌 This is the **only truly longitudinal, individual-level dataset** in this project — "
    "everything on the other pages is cross-study aggregate literature data. Small n=4, "
    "but real repeated measures on real people."
)

cbc = load_cbc()

analytes = sorted(cbc['ANALYTE'].unique())
default_analytes = ['HEMOGLOBIN', 'RED BLOOD CELL COUNT', 'HEMATOCRIT']
selected = st.multiselect("Select blood analytes to plot", analytes, default=default_analytes)

subjects = sorted(cbc['SUBJECT_ID'].unique())
selected_subjects = st.multiselect("Select subjects", subjects, default=subjects)

if selected:
    plot_df = cbc[cbc['ANALYTE'].isin(selected) & cbc['SUBJECT_ID'].isin(selected_subjects)].copy()
    plot_df['TEST_DATE'] = pd.Categorical(plot_df['TEST_DATE'], categories=TIMEPOINT_ORDER, ordered=True)

    fig = px.line(
        plot_df.sort_values('timepoint_order'),
        x='TEST_DATE', y='VALUE', color='SUBJECT_ID', facet_col='ANALYTE',
        facet_col_wrap=2, markers=True,
        category_orders={'TEST_DATE': TIMEPOINT_ORDER},
        labels={'TEST_DATE': 'Timepoint', 'VALUE': 'Value'},
    )
    fig.add_vrect(x0=-0.5, x1=2.5, fillcolor="lightblue", opacity=0.15, line_width=0,
                  annotation_text="Pre-flight", annotation_position="top left")
    fig.update_layout(height=350 * ((len(selected) + 1) // 2))
    st.plotly_chart(fig, width='stretch')
else:
    st.info("Select at least one analyte above to see the chart.")

st.markdown("### ⚠️ Data Quality Note")
st.warning(
    "One data point (subject C003, timepoint L-92) shows implausible simultaneous extreme "
    "values across nearly every white-cell parameter (e.g. MPV = 330 vs. a normal range of "
    "7.5–12.5) — almost certainly a data entry or unit-scaling error, not a real finding. "
    "This point is flagged (`out_of_range`) and excluded from headline trend analysis. "
    "See `notebooks/02_statistical_analysis.ipynb` for the full investigation."
)

st.markdown("### 🔍 What we actually found (not the textbook assumption)")
st.markdown("""
We checked the well-known "spaceflight-induced anemia" pattern (red blood cells/hemoglobin
dipping after return) directly against this data — and **it's not clearly present** here.
Subject C004 stays essentially flat throughout; C002 is actually *lowest* pre-flight, not
post-flight.

**Most likely explanation**: Inspiration4 was only ~3 days — probably too short to trigger
the substantial red-cell-mass loss documented in much longer ISS missions (weeks to months).
This is itself a useful finding: it suggests these hematological effects may be
**duration-dependent**, consistent with the short-vs-long pattern we found for bone and
muscle loss elsewhere in this project.
""")

with st.expander("📊 View raw out-of-range readings"):
    st.dataframe(
        cbc[cbc['out_of_range']][['SUBJECT_ID', 'ANALYTE', 'TEST_DATE', 'VALUE', 'RANGE_MIN', 'RANGE_MAX']]
    )
