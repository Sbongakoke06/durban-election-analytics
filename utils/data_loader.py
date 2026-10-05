from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ---------------------------------------------------------
# LOAD DASHBOARD DATA
# ---------------------------------------------------------

@st.cache_data
def load_dashboard_data():
    """
    Load all datasets used by the eThekwini election dashboard.
    """

    historical = pd.read_csv(
        DATA_DIR / "historical_results.csv"
    )

    forecast = pd.read_csv(
        DATA_DIR / "forecast_2026.csv"
    )

    models = pd.read_csv(
        DATA_DIR / "model_performance.csv"
    )

    importance = pd.read_csv(
        DATA_DIR / "feature_importance.csv"
    )

    districts = pd.read_csv(
        DATA_DIR / "district_results.csv"
    )

    project = pd.read_csv(
        DATA_DIR / "project_info.csv"
    )

    # -----------------------------------------------------
    # BASIC CLEANING
    # -----------------------------------------------------

    if "Year" in historical.columns:
        historical["Year"] = pd.to_numeric(
            historical["Year"],
            errors="coerce"
        )

    if "VoteShare" in historical.columns:
        historical["VoteShare"] = pd.to_numeric(
            historical["VoteShare"],
            errors="coerce"
        )

    if "EstimatedVoteShare_2026" in forecast.columns:
        forecast["EstimatedVoteShare_2026"] = pd.to_numeric(
            forecast["EstimatedVoteShare_2026"],
            errors="coerce"
        )

    if "LowerEstimate" in forecast.columns:
        forecast["LowerEstimate"] = pd.to_numeric(
            forecast["LowerEstimate"],
            errors="coerce"
        )

    if "UpperEstimate" in forecast.columns:
        forecast["UpperEstimate"] = pd.to_numeric(
            forecast["UpperEstimate"],
            errors="coerce"
        )

    if "Year" in districts.columns:
        districts["Year"] = pd.to_numeric(
            districts["Year"],
            errors="coerce"
        )

    return {
        "historical": historical,
        "forecast": forecast,
        "models": models,
        "importance": importance,
        "districts": districts,
        "project": project,
    }