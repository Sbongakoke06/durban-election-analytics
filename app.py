import streamlit as st

from utils.data_loader import load_dashboard_data
from utils.charts import (
    forecast_chart,
    trend_chart,
    model_chart,
    importance_chart,
    district_chart,
    uncertainty_chart,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="eThekwini Election Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# LOAD DATA
# =========================================================

try:
    data = load_dashboard_data()

except Exception as error:
    st.error("The dashboard could not load the project data.")
    st.exception(error)
    st.stop()


historical = data["historical"]
forecast = data["forecast"]
models = data["models"]
importance = data["importance"]
districts = data["districts"]
project = data["project"]


# =========================================================
# PREPARE DATA
# =========================================================

forecast = forecast.sort_values(
    "EstimatedVoteShare_2026",
    ascending=False
).reset_index(drop=True)

models = models.sort_values(
    "MAE",
    ascending=True
).reset_index(drop=True)

leader = forecast.iloc[0]
best_model = models.iloc[0]


# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .hero {
        padding: 34px;
        border-radius: 20px;
        background: linear-gradient(
            120deg,
            #071426,
            #102a43,
            #164e63
        );
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .hero-title {
        color: white;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #dbeafe;
        font-size: 17px;
    }

    .status {
        display: inline-block;
        margin-top: 17px;
        padding: 7px 14px;
        border-radius: 30px;
        background: rgba(255,255,255,0.12);
        color: white;
        font-size: 12px;
        letter-spacing: 1px;
    }

    .notice {
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #f59e0b;
        background: rgba(245,158,11,0.10);
        margin-top: 10px;
        margin-bottom: 22px;
    }

    .insight {
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        background: rgba(59,130,246,0.08);
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .method-card {
        padding: 20px;
        border-radius: 14px;
        background: rgba(148,163,184,0.08);
        border: 1px solid rgba(148,163,184,0.20);
        margin-bottom: 15px;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.20);
        padding: 15px;
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📊 Election Intelligence")

    st.caption(
        "eThekwini Metropolitan Municipality"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Historical Analysis",
            "2026 Forecast",
            "Model Laboratory",
            "District Explorer",
            "Methodology",
        ],
    )

    st.divider()

    st.markdown("### Project Scope")

    st.write("**Election:** Local Government")
    st.write("**Municipality:** eThekwini")
    st.write("**Ballot:** Proportional Representation")
    st.write("**Historical elections:** 2011, 2016, 2021")
    st.write("**Forecast date:** 4 November 2026")

    st.divider()

    st.warning(
        "2026 values are analytical model estimates "
        "and are not observed election results."
    )

# =========================================================
# PROFESSIONAL DASHBOARD HEADER
# =========================================================

st.title("📊 eThekwini Election Intelligence")

st.markdown(
    """
    ### 2026 South African Local Government Election Analytics

    **eThekwini Metropolitan Municipality**

    Historical electoral analytics • Machine learning evaluation •
    2026 PR vote-share forecasting
    """
)

st.success("● ANALYTICS SYSTEM ACTIVE")

st.divider()

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    st.header("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Highest Baseline Estimate",
        leader["PartyName"]
    )

    col2.metric(
        "2026 Baseline Share",
        f"{leader['EstimatedVoteShare_2026']:.2f}%"
    )

    col3.metric(
        "Lowest-MAE Approach",
        best_model["Model"]
    )

    col4.metric(
        "Validation MAE",
        f"{best_model['MAE']:.3f} pp"
    )

    st.markdown(
        """
        <div class="notice">
            <b>2026 Forecast Notice</b><br>
            Values for 2026 are model-generated baseline estimates.
            They are not actual or official election results.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.7, 1])

    with left:

        st.subheader("2026 Baseline Estimates")

        st.plotly_chart(
            forecast_chart(
                forecast,
                top_n=10
            ),
            use_container_width=True
        )

    with right:

        st.subheader("Highest Baseline Estimates")

        for _, row in forecast.head(5).iterrows():

            st.metric(
                label=row["PartyName"],
                value=f"{row['EstimatedVoteShare_2026']:.2f}%"
            )

    st.divider()

    st.subheader("Historical Electoral Trajectory")

    preferred_parties = [
        "AFRICAN NATIONAL CONGRESS",
        "DEMOCRATIC ALLIANCE",
        "ECONOMIC FREEDOM FIGHTERS",
        "INKATHA FREEDOM PARTY",
    ]

    default_parties = [
        party
        for party in preferred_parties
        if party in historical["PartyName"].values
    ]

    if default_parties:

        st.plotly_chart(
            trend_chart(
                historical,
                default_parties
            ),
            use_container_width=True
        )

    else:

        st.info(
            "Historical party data is available, "
            "but the default parties were not found."
        )

    st.markdown(
        """
        <div class="insight">
            <b>Analytical insight:</b>
            The final baseline approach was selected using
            out-of-time validation performance rather than
            automatically preferring the most complex model.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HISTORICAL ANALYSIS
# =========================================================

elif page == "Historical Analysis":

    st.header("Historical Election Analysis")

    st.write(
        """
        Explore historical Proportional Representation
        voting patterns across the 2011, 2016 and 2021
        eThekwini local government elections.
        """
    )

    available_parties = sorted(
        historical["PartyName"]
        .dropna()
        .unique()
        .tolist()
    )

    preferred_parties = [
        "AFRICAN NATIONAL CONGRESS",
        "DEMOCRATIC ALLIANCE",
        "ECONOMIC FREEDOM FIGHTERS",
        "INKATHA FREEDOM PARTY",
    ]

    default_parties = [
        party
        for party in preferred_parties
        if party in available_parties
    ]

    selected_parties = st.multiselect(
        "Select political parties",
        options=available_parties,
        default=default_parties
    )

    if selected_parties:

        st.plotly_chart(
            trend_chart(
                historical,
                selected_parties
            ),
            use_container_width=True
        )

    else:

        st.info(
            "Select at least one political party "
            "to display the historical trend."
        )

    st.divider()

    available_years = sorted(
        historical["Year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    selected_year = st.selectbox(
        "Inspect election year",
        options=available_years,
        index=len(available_years) - 1
    )

    year_data = historical[
        historical["Year"].astype(int)
        == selected_year
    ].copy()

    year_data = year_data.sort_values(
        "VoteShare",
        ascending=False
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Political Parties",
        f"{year_data['PartyName'].nunique():,}"
    )

    c2.metric(
        "Valid PR Votes",
        f"{year_data['PartyVotes'].sum():,.0f}"
    )

    if not year_data.empty:

        c3.metric(
            "Highest Vote Share",
            year_data.iloc[0]["PartyName"]
        )

    st.subheader(
        f"Party Results — {selected_year}"
    )

    st.dataframe(
        year_data[
            [
                "PartyName",
                "PartyVotes",
                "VoteShare",
            ]
        ].head(20),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# 2026 FORECAST
# =========================================================

elif page == "2026 Forecast":

    st.header("2026 Baseline Forecast")

    st.markdown(
        """
        <div class="notice">
            <b>Important interpretation</b><br>
            This section presents statistical baseline
            estimates for 4 November 2026.
            These values are not official results and
            should not be interpreted as certainty about
            the election outcome.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Highest Baseline Estimate",
        leader["PartyName"]
    )

    c2.metric(
        "Estimated Share",
        f"{leader['EstimatedVoteShare_2026']:.2f}%"
    )

    majority_gap = (
        50.0 -
        float(
            leader["EstimatedVoteShare_2026"]
        )
    )

    c3.metric(
        "Distance from 50%",
        f"{majority_gap:.2f} pp"
    )

    max_parties = min(
        20,
        len(forecast)
    )

    min_parties = min(
        5,
        max_parties
    )

    default_n = min(
        10,
        max_parties
    )

    if max_parties > min_parties:

        top_n = st.slider(
            "Number of parties to display",
            min_value=min_parties,
            max_value=max_parties,
            value=default_n
        )

    else:

        top_n = max_parties

    st.plotly_chart(
        forecast_chart(
            forecast,
            top_n=top_n
        ),
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Forecast Uncertainty Explorer"
    )

    selected_party = st.selectbox(
        "Select a political party",
        options=forecast["PartyName"].tolist()
    )

    party_row = forecast[
        forecast["PartyName"]
        == selected_party
    ].iloc[0]

    u1, u2, u3 = st.columns(3)

    u1.metric(
        "Lower Estimate",
        f"{party_row['LowerEstimate']:.2f}%"
    )

    u2.metric(
        "Baseline Estimate",
        f"{party_row['EstimatedVoteShare_2026']:.2f}%"
    )

    u3.metric(
        "Upper Estimate",
        f"{party_row['UpperEstimate']:.2f}%"
    )

    st.plotly_chart(
        uncertainty_chart(
            party_row
        ),
        use_container_width=True
    )

    st.caption(
        "The lower and upper values are descriptive "
        "empirical error bands. They are not formal "
        "statistical confidence intervals."
    )

    st.divider()

    st.subheader("Full 2026 Baseline Table")

    st.dataframe(
        forecast[
            [
                "PartyName",
                "EstimatedVoteShare_2026",
                "LowerEstimate",
                "UpperEstimate",
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# MODEL LABORATORY
# =========================================================

elif page == "Model Laboratory":

    st.header("Machine Learning Laboratory")

    st.write(
        """
        This section compares the forecasting approaches
        evaluated using historical election transitions.
        """
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Lowest-MAE Approach",
        best_model["Model"]
    )

    c2.metric(
        "Lowest MAE",
        f"{best_model['MAE']:.3f} pp"
    )

    c3.metric(
        "Held-Out Observations",
        "18,123"
    )

    metric = st.selectbox(
        "Evaluation metric",
        options=[
            "MAE",
            "RMSE",
            "R2",
        ]
    )

    st.plotly_chart(
        model_chart(
            models,
            metric
        ),
        use_container_width=True
    )

    st.subheader("Model Performance Table")

    st.dataframe(
        models,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        <div class="insight">
            <b>Model-selection rationale:</b><br>
            MAE was used as the primary selection metric
            because the error can be interpreted directly
            in percentage points. The naive baseline
            recorded the lowest MAE on the held-out
            evaluation data.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader(
        "Random Forest Feature Importance"
    )

    if not importance.empty:

        st.plotly_chart(
            importance_chart(
                importance
            ),
            use_container_width=True
        )

        strongest = importance.sort_values(
            "Importance",
            ascending=False
        ).iloc[0]

        st.info(
            f"Highest Random Forest feature importance: "
            f"{strongest['Feature']} "
            f"({strongest['Importance']:.3f}). "
            f"Feature importance describes the fitted model "
            f"and should not be interpreted as causation."
        )

    else:

        st.info(
            "No feature-importance data is available."
        )


# =========================================================
# DISTRICT EXPLORER
# =========================================================

elif page == "District Explorer":

    st.header("Voting District Explorer")

    st.write(
        """
        Explore historical PR results at voting-district
        level.
        """
    )

    district_years = sorted(
        districts["Year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    selected_year = st.selectbox(
        "Election year",
        options=district_years,
        index=len(district_years) - 1
    )

    filtered_year = districts[
        districts["Year"].astype(int)
        == selected_year
    ].copy()

    district_options = sorted(
        filtered_year["VotingDistrict"]
        .dropna()
        .unique()
        .tolist()
    )

    if len(district_options) == 0:

        st.warning(
            "No voting districts are available "
            "for this election year."
        )

    else:

        selected_district = st.selectbox(
            "Voting district",
            options=district_options
        )

        district_data = filtered_year[
            filtered_year["VotingDistrict"]
            == selected_district
        ].copy()

        district_data = district_data.sort_values(
            "LocalVoteShare",
            ascending=False
        )

        if district_data.empty:

            st.warning(
                "No results were found for "
                "this voting district."
            )

        else:

            district_leader = district_data.iloc[0]

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Registered Voters",
                f"{district_data['RegisteredVoters'].max():,.0f}"
            )

            c2.metric(
                "Valid PR Votes",
                f"{district_data['DistrictTotalVotes'].max():,.0f}"
            )

            c3.metric(
                "Highest Vote Share",
                district_leader["PartyName"]
            )

            st.plotly_chart(
                district_chart(
                    district_data,
                    top_n=10
                ),
                use_container_width=True
            )

            st.subheader("District Results")

            st.dataframe(
                district_data[
                    [
                        "PartyName",
                        "PartyVotes",
                        "LocalVoteShare",
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# METHODOLOGY
# =========================================================

elif page == "Methodology":

    st.header(
        "Methodology & Responsible Interpretation"
    )

    st.markdown(
        """
        <div class="method-card">
            <h4>1. Historical Data</h4>

            Historical eThekwini local-government election
            data from 2011, 2016 and 2021 were used.

            Proportional Representation results provide the
            basis for longitudinal comparison across the
            available election cycles.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="method-card">
            <h4>2. Machine Learning Design</h4>

            Historical district-party observations were
            transformed into supervised-learning pairs.

            The 2011→2016 transition was used for training,
            while 2016→2021 provided an out-of-time
            evaluation period.

            The analysis compared Linear Regression,
            Decision Tree, Random Forest and a naive
            historical baseline.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="method-card">
            <h4>3. Model Evaluation</h4>

            MAE, RMSE and R² were used to evaluate
            predictive performance.

            MAE was treated as the primary selection
            metric because it can be interpreted directly
            as an average percentage-point error.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="method-card">
            <h4>4. Baseline Forecast</h4>

            The 2026 values are model-generated baseline
            estimates and are kept separate from historical
            observations.

            The displayed lower and upper estimates are
            descriptive empirical error bands rather than
            formal confidence intervals.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="method-card">
            <h4>5. Limitations</h4>

            The historical record contains only a small
            number of local-government election cycles.

            Voting behaviour can also be affected by
            turnout, new parties, campaign events,
            candidate effects, demographic changes and
            other factors not represented in the
            historical variables.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="method-card">
            <h4>6. Responsible Use</h4>

            Forecast values should always be identified as
            estimates. Historical observations, model
            outputs and uncertainty information should
            remain clearly separated.

            The dashboard is intended as an analytical
            and educational tool rather than an official
            election-results system.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "eThekwini Election Intelligence | "
    "Data Science & Machine Learning Project | "
    "2026 values are analytical estimates, not official results."
)