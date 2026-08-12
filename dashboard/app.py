import streamlit as st
from data_loader import load_astronauts, load_physio, load_cbc

st.set_page_config(page_title="Spaceflight Physiology Dashboard", page_icon="🚀", layout="wide")

st.title("🚀 Analysis of the Physiological Effects of Spaceflight")
st.markdown("""
An interactive exploration of how the human body responds to microgravity — built on
real astronaut records, published space medicine research, and a real mission's blood-panel data.

*Internship project — TUNSA (Tunisian Space Association)*
""")

astro = load_astronauts()
physio = load_physio()
cbc = load_cbc()

st.markdown("### At a glance")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Astronauts tracked", f"{len(astro):,}")
col2.metric("Literature findings", f"{len(physio)}")
col3.metric("Physiological systems", physio['system'].nunique())
col4.metric("Real longitudinal blood analytes", cbc['ANALYTE'].nunique())

st.divider()

st.markdown("### What's in this dashboard")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
**🦴 Bone Health** — density change by skeletal site, duration-dependence

**💪 Muscle Health** — mass & strength change by muscle group

**❤️ Cardiovascular** — orthostatic intolerance, fluid-shift effects

**😴 Sleep** — in-flight vs. pre/post-flight duration
""")
with c2:
    st.markdown("""
**🩸 Recovery Case Study** — real Inspiration4 blood panel, tracked 194 days post-flight

**🧑‍🚀 Astronaut Comparison** — 570 real astronauts by career flight time, country, sex

**🛰️ Mission Comparison** — explore missions by name and era
""")

st.divider()
st.info(
    "📋 **A note on scope**: every finding here is traceable to a specific source — see "
    "`docs/data_sources.md` for citations and `docs/data_coverage_analysis.md` for an honest "
    "breakdown of what this data can and cannot show (e.g. no in-flight/during-mission "
    "measurements exist in any of the underlying datasets)."
)
