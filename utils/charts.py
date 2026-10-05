import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------------
# 2026 FORECAST BAR CHART
# ---------------------------------------------------------

def forecast_chart(data, top_n=10):

    chart_data = (
        data.nlargest(
            top_n,
            "EstimatedVoteShare_2026"
        )
        .sort_values("EstimatedVoteShare_2026")
    )

    fig = px.bar(
        chart_data,
        x="EstimatedVoteShare_2026",
        y="PartyName",
        orientation="h",
        text="EstimatedVoteShare_2026",
        labels={
            "EstimatedVoteShare_2026":
                "Estimated vote share (%)",
            "PartyName":
                "Political party",
        },
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    fig.update_layout(
        height=520,
        showlegend=False,
        margin=dict(
            l=10,
            r=60,
            t=20,
            b=10
        ),
    )

    return fig


# ---------------------------------------------------------
# HISTORICAL PARTY TREND
# ---------------------------------------------------------

def trend_chart(data, parties):

    chart_data = data[
        data["PartyName"].isin(parties)
    ].copy()

    fig = px.line(
        chart_data,
        x="Year",
        y="VoteShare",
        color="PartyName",
        markers=True,
        labels={
            "Year": "Election year",
            "VoteShare": "Vote share (%)",
            "PartyName": "Political party",
        },
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=9),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=sorted(
            chart_data["Year"]
            .dropna()
            .unique()
        ),
    )

    fig.update_layout(
        height=520,
        legend_title_text="Party",
        hovermode="x unified",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
    )

    return fig


# ---------------------------------------------------------
# MODEL PERFORMANCE
# ---------------------------------------------------------

def model_chart(data, metric="MAE"):

    ascending = metric != "R2"

    chart_data = data.sort_values(
        metric,
        ascending=ascending
    ).copy()

    fig = px.bar(
        chart_data,
        x="Model",
        y=metric,
        text=metric,
        labels={
            "Model": "Model",
            metric: metric,
        },
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
    )

    fig.update_layout(
        height=460,
        showlegend=False,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
    )

    return fig


# ---------------------------------------------------------
# FEATURE IMPORTANCE
# ---------------------------------------------------------

def importance_chart(data, top_n=10):

    chart_data = (
        data.nlargest(
            top_n,
            "Importance"
        )
        .sort_values("Importance")
    )

    fig = px.bar(
        chart_data,
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        labels={
            "Importance":
                "Feature importance",
            "Feature":
                "Feature",
        },
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
    )

    fig.update_layout(
        height=520,
        showlegend=False,
        margin=dict(
            l=10,
            r=50,
            t=20,
            b=10
        ),
    )

    return fig


# ---------------------------------------------------------
# DISTRICT RESULTS
# ---------------------------------------------------------

def district_chart(data, top_n=10):

    chart_data = (
        data.nlargest(
            top_n,
            "LocalVoteShare"
        )
        .sort_values("LocalVoteShare")
    )

    fig = px.bar(
        chart_data,
        x="LocalVoteShare",
        y="PartyName",
        orientation="h",
        text="LocalVoteShare",
        labels={
            "LocalVoteShare":
                "Local vote share (%)",
            "PartyName":
                "Political party",
        },
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    fig.update_layout(
        height=500,
        showlegend=False,
        margin=dict(
            l=10,
            r=50,
            t=20,
            b=10
        ),
    )

    return fig


# ---------------------------------------------------------
# FORECAST UNCERTAINTY
# ---------------------------------------------------------

def uncertainty_chart(row):

    party = row["PartyName"]

    lower = row["LowerEstimate"]
    estimate = row["EstimatedVoteShare_2026"]
    upper = row["UpperEstimate"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[lower, upper],
            y=[party, party],
            mode="lines",
            line=dict(width=10),
            name="Estimated range",
            hovertemplate=(
                "Range: %{x:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[estimate],
            y=[party],
            mode="markers+text",
            marker=dict(size=18),
            text=[f"{estimate:.2f}%"],
            textposition="top center",
            name="Baseline estimate",
            hovertemplate=(
                "Baseline: %{x:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        height=260,
        xaxis_title="Estimated vote share (%)",
        yaxis_title="",
        showlegend=True,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
    )
