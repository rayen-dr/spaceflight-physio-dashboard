import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_loader import load_astronauts

st.set_page_config(page_title="Astronaut Comparison", page_icon="🧑‍🚀", layout="wide")
st.title("🧑‍🚀 Astronaut Comparison")
st.caption("570 real astronauts — source: Kaggle International Astronaut Database")

astro = load_astronauts()

col1, col2 = st.columns(2)
with col1:
    countries = st.multiselect(
        "Filter by country", sorted(astro['country'].unique()),
        default=list(astro['country'].value_counts().head(5).index),
    )
with col2:
    genders = st.multiselect("Filter by gender", sorted(astro['gender'].dropna().unique()),
                              default=list(astro['gender'].dropna().unique()))

filtered = astro[astro['country'].isin(countries) & astro['gender'].isin(genders)]
st.metric("Astronauts matching filter", len(filtered))

st.markdown("### Career Time in Space vs. Number of Flights")
fig = px.scatter(
    filtered, x='num_flights', y='total_flight_days', color='duration_category',
    hover_data=['name', 'country'],
    labels={'num_flights': 'Number of flights', 'total_flight_days': 'Total career days in space'},
)
st.plotly_chart(fig, width='stretch')

st.markdown("### Top 15 Astronauts by Total Time in Space")
top15 = filtered.nlargest(15, 'total_flight_days')[['name', 'country', 'gender', 'num_flights', 'total_flight_days']]
st.dataframe(top15, width='stretch', hide_index=True)

st.warning(
    "⚠️ **Limitation**: `total_flight_days` is cumulative across an astronaut's whole career, "
    "not a single mission. No age data is available. See `docs/data_coverage_analysis.md`."
)
