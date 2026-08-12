"""
data_loader.py — shared data access for all dashboard pages.

Centralizing this means every page loads data the same way, and paths work
regardless of the working directory Streamlit was launched from.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_RAW = PROJECT_ROOT / "data" / "raw"

DURATION_COLORS = {"Short": "#E8A87C", "Long": "#5D8AA8", "Mixed": "#A8A8A8"}


@st.cache_data
def load_astronauts() -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED / "astronauts_clean.csv")


@st.cache_data
def load_physio() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW / "physiological_effects.csv")


@st.cache_data
def load_cbc() -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED / "i4_cbc_clean_flagged.csv")


@st.cache_data
def load_cbc_recovery_summary() -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED / "i4_cbc_recovery_summary.csv", index_col=0)


TIMEPOINT_ORDER = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]
