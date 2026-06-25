# app/streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

BLUE_DARK   = "#185FA5"
BLUE_LIGHT  = "#B5D4F4"
RED_DARK    = "#E24B4A"
RED_LIGHT   = "#FAA0A0"
BG          = "#F7F9FC"
TEXT        = "#1A1A2E"

CLUSTER_COLORS = {
    0: BLUE_DARK,
    1: BLUE_LIGHT,
    2: RED_DARK,
    3: RED_LIGHT,
}

CLUSTER_LABELS = {
    0: "Moderately Constrained (High Volatility)",
    1: "Relatively Free & Stable",
    2: "Improving Press Freedom",
    3: "Severely Constrained & Stable",
}

st.set_page_config(
    page_title="Press Freedom Dashboard",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(f"""
<style>
  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {TEXT};
  }}
  .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}

  /* KPI cards */
  .kpi-row {{ display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
  .kpi-card {{
    flex: 1;
    min-width: 160px;
    background: white;
    border-left: 4px solid {BLUE_DARK};
    border-radius: 6px;
    padding: 1rem 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
  }}
  .kpi-card.red {{ border-left-color: {RED_DARK}; }}
  .kpi-card .label {{ font-size: .72rem; text-transform: uppercase;
                      letter-spacing: .06em; color: #6b7280; }}
  .kpi-card .value {{ font-size: 1.6rem; font-weight: 700;
                      line-height: 1.2; margin-top: .2rem; }}
  .kpi-card .sub   {{ font-size: .75rem; color: #9ca3af; margin-top: .15rem; }}

  /* Section headers */
  h2 {{ border-bottom: 2px solid {BLUE_LIGHT}; padding-bottom: .35rem;
        margin-top: 2rem !important; font-size: 1.25rem !important; }}

  /* Note box */
  .note-box {{
    background: #EFF6FF;
    border-left: 3px solid {BLUE_DARK};
    border-radius: 4px;
    padding: .6rem .9rem;
    font-size: .82rem;
    color: #374151;
    margin-bottom: 1rem;
  }}
</style>
""", unsafe_allow_html=True)


# Data loading
@st.cache_data
def load_data():
    df       = pd.read_csv("data/clean_press_freedom.csv")
    features = pd.read_csv("outputs/country_features.csv", index_col=0)
    features["Cluster"] = features["Cluster"].astype(int)
    return df, features

df, features = load_data()

annual      = df.groupby("Year")["Score"].mean().reset_index()
latest_year = df["Year"].max()
first_year  = df["Year"].min()
latest      = df[df["Year"] == latest_year]
trend_change = (
    annual.loc[annual["Year"] == latest_year, "Score"].values[0]
    - annual.loc[annual["Year"] == first_year, "Score"].values[0]
)

has_region = "Region" in df.columns


# SIDEBAR

with st.sidebar:
    st.markdown("## Press Freedom")
    st.markdown(f"**{first_year}–{latest_year}** · RSF Index")
    st.divider()

    selected_year = st.slider(
        "Map year",
        int(df["Year"].min()),
        int(df["Year"].max()),
        int(latest_year),
    )

    st.divider()

    selected_country = st.selectbox(
        "Country explorer",
        sorted(df["Country"].unique()),
        index=sorted(df["Country"].unique()).index("France")
            if "France" in df["Country"].unique() else 0,
    )

    if has_region:
        st.divider()
        regions = sorted(df["Region"].unique())
        selected_regions = st.multiselect(
            "Filter regions (map & charts)",
            regions,
            default=regions,
        )
    else:
        selected_regions = None

    st.divider()
    st.markdown(
        "<span style='font-size:.75rem;color:#9ca3af;'>"
        "Note: Higher RSF score = worse press freedom."
        "</span>",
        unsafe_allow_html=True,
    )


# HEADER

st.title("Global Press Freedom Dashboard")
st.markdown(
    "<div class='note-box'>"
    "Data: Reporters Without Borders (RSF) Press Freedom Index, 2013–2021. "
    "<strong>Higher scores indicate worse press freedom conditions.</strong>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("""
### Executive Summary
This project explores global press freedom patterns using the Reporters Without Borders (RSF) Press Freedom Index (2013–2021).
The analysis investigates:
- Long-term global trends
- Regional differences
- Country-level improvements and deteriorations
- Country groupings using unsupervised machine learning

**Important:** Higher RSF scores indicate worse press freedom.
""")

# KPIs
n_countries = df["Country"].nunique()
worst_country  = latest.loc[latest["Score"].idxmax(), "Country"]
best_country   = latest.loc[latest["Score"].idxmin(), "Country"]
direction      = "↑ worse" if trend_change > 0 else "↓ better"

st.markdown(f"""
<div class='kpi-row'>
  <div class='kpi-card'>
    <div class='label'>Countries</div>
    <div class='value'>{n_countries}</div>
    <div class='sub'>{first_year}–{latest_year}</div>
  </div>
  <div class='kpi-card {"red" if trend_change > 0 else ""}'>
    <div class='label'>Global Score Change</div>
    <div class='value'>{trend_change:+.2f}</div>
    <div class='sub'>{direction} since {first_year}</div>
  </div>
  <div class='kpi-card'>
    <div class='label'>Freest ({latest_year})</div>
    <div class='value' style='font-size:1.1rem'>{best_country}</div>
    <div class='sub'>Lowest RSF score</div>
  </div>
  <div class='kpi-card red'>
    <div class='label'>Most Restricted ({latest_year})</div>
    <div class='value' style='font-size:1.1rem'>{worst_country}</div>
    <div class='sub'>Highest RSF score</div>
  </div>
</div>
""", unsafe_allow_html=True)


# WORLD MAP

st.header("World Map")

map_df = df[df["Year"] == selected_year]
if has_region and selected_regions:
    map_df = map_df[map_df["Region"].isin(selected_regions)]

fig_map = px.choropleth(
    map_df,
    locations="Code",
    color="Score",
    hover_name="Country",
    color_continuous_scale="RdBu_r",
    range_color=[df["Score"].min(), df["Score"].max()],
    labels={"Score": "RSF Score"},
    title=f"Press Freedom Index — {selected_year}",
)
fig_map.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
    paper_bgcolor="white",
    geo=dict(bgcolor="white", showframe=False),
    coloraxis_colorbar=dict(title="RSF Score", thickness=12, len=0.6),
    font_family="Inter",
)
st.plotly_chart(fig_map, width='stretch')


# GLOBAL & REGIONAL TRENDS

st.header("Trends Over Time")

col_a, col_b = st.columns(2)

with col_a:
    fig_global = go.Figure()
    fig_global.add_trace(go.Scatter(
        x=annual["Year"], y=annual["Score"],
        mode="lines+markers",
        line=dict(color=BLUE_DARK, width=2.5),
        marker=dict(size=7),
        name="Global average",
    ))
    fig_global.update_layout(
        title="Global Average Score (2013–2021)",
        yaxis_title="Avg RSF Score (higher = worse)",
        xaxis=dict(dtick=1),
        paper_bgcolor="white", plot_bgcolor=BG,
        font_family="Inter", margin=dict(t=40, b=30),
    )
    st.plotly_chart(fig_global, width='stretch')

with col_b:
    if has_region:
        regional_annual = (
            df[df["Region"].isin(selected_regions)]
            .groupby(["Year", "Region"])["Score"]
            .mean()
            .reset_index()
        )
        fig_regional = px.line(
            regional_annual,
            x="Year", y="Score", color="Region",
            color_discrete_sequence=px.colors.diverging.RdBu_r,
            labels={"Score": "Avg RSF Score"},
            title="Regional Average Score Over Time",
        )
        fig_regional.update_traces(mode="lines+markers", marker_size=5)
        fig_regional.update_layout(
            paper_bgcolor="white", plot_bgcolor=BG,
            font_family="Inter", margin=dict(t=40, b=30),
            legend=dict(font_size=11),
        )
        st.plotly_chart(fig_regional, width='stretch')
    else:
        st.info("Regional data not available — re-run notebook with `country_converter` to enable this panel.")


# TEMPORAL STABILITY

st.header("Temporal Stability")

pivot_df = df.pivot(index="Country", columns="Year", values="Score")
correlations = [
    pivot_df[y].corr(pivot_df[y + 1])
    for y in pivot_df.columns[:-1]
]
corr_df = pd.DataFrame({
    "Year1": pivot_df.columns[:-1],
    "Year2": pivot_df.columns[1:],
    "Correlation": correlations,
})
avg_corr = corr_df["Correlation"].mean()

col_ts1, col_ts2 = st.columns([2, 1])
with col_ts1:
    st.dataframe(corr_df.round(3), width='stretch')
with col_ts2:
    st.metric("Average Correlation", f"{avg_corr:.3f}")

st.info(
    "Country rankings are highly persistent over time. "
    "Most changes occur gradually rather than abruptly."
)


# COUNTRY EXPLORER

st.header("Country Explorer")

country_df = df[df["Country"] == selected_country].sort_values("Year")
country_features = features.loc[selected_country] if selected_country in features.index else None

col1, col2 = st.columns([3, 1])

with col1:
    fig_country = go.Figure()
    fig_country.add_trace(go.Scatter(
        x=country_df["Year"], y=country_df["Score"],
        mode="lines+markers",
        line=dict(color=BLUE_DARK, width=2.5),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(181, 212, 244, 0.33)",
    ))
    fig_country.update_layout(
        title=f"{selected_country} — Press Freedom Score ({first_year}–{latest_year})",
        yaxis_title="RSF Score (higher = worse)",
        xaxis=dict(dtick=1),
        paper_bgcolor="white", plot_bgcolor=BG,
        font_family="Inter", margin=dict(t=40, b=30),
    )
    st.plotly_chart(fig_country, width='stretch')

with col2:
    if country_features is not None:
        cluster_id = int(country_features["Cluster"])
        st.markdown("**Country profile**")
        st.markdown(f"**Cluster:** {cluster_id} — {CLUSTER_LABELS[cluster_id]}")
        st.metric("Mean Score", f"{country_features['MeanScore']:.1f}")
        st.metric("Volatility (σ)", f"{country_features['Volatility']:.2f}")
        st.metric("Trend", f"{country_features['Trend']:+.2f}",
                  delta_color="inverse")
    else:
        st.info("No cluster data for this country.")


# REGIONAL COMPARISON

if has_region:
    st.header("Regional Comparison")

    box_df = latest.copy()
    if selected_regions:
        box_df = box_df[box_df["Region"].isin(selected_regions)]

    fig_box = px.box(
        box_df.sort_values("Score"),
        x="Region", y="Score",
        color="Region",
        color_discrete_sequence=px.colors.diverging.RdBu_r,
        labels={"Score": "RSF Score"},
        title=f"Score Distribution by Region ({latest_year})",
    )
    fig_box.update_layout(
        showlegend=False,
        paper_bgcolor="white", plot_bgcolor=BG,
        font_family="Inter", margin=dict(t=40, b=80),
        xaxis=dict(tickangle=-35),
    )
    st.plotly_chart(fig_box, width='stretch')

    from scipy.stats import kruskal
    groups = [g["Score"].values for _, g in latest.groupby("Region")]
    H, p_value = kruskal(*groups)
    n = len(latest)
    k = latest["Region"].nunique()
    effect_size = (H - k + 1) / (n - k)

    st.subheader("Statistical Test")
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Kruskal-Wallis H", f"{H:.2f}")
    col_s2.metric("p-value", f"{p_value:.2e}")
    col_s3.metric("Effect Size (ε²)", f"{effect_size:.3f}")


# COUNTRY CHANGES

st.header("Biggest Country Changes (2013–2021)")

pivot = df.pivot(index="Country", columns="Year", values="Score")
pivot["Change"] = pivot[latest_year] - pivot[first_year]
pivot = pivot.dropna(subset=["Change"])

top_imp  = pivot.nsmallest(10, "Change")[["Change"]].reset_index()
top_det  = pivot.nlargest(10, "Change")[["Change"]].reset_index()

col_i, col_d = st.columns(2)

with col_i:
    fig_imp = px.bar(
        top_imp.sort_values("Change"),
        x="Change", y="Country", orientation="h",
        color_discrete_sequence=[BLUE_DARK],
        title="Top 10 Improvements (score fell = better freedom)",
        labels={"Change": "Score change"},
    )
    fig_imp.update_layout(
        paper_bgcolor="white", plot_bgcolor=BG,
        font_family="Inter", margin=dict(t=40, b=20),
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_imp, width='stretch')

with col_d:
    fig_det = px.bar(
        top_det.sort_values("Change", ascending=False),
        x="Change", y="Country", orientation="h",
        color_discrete_sequence=[RED_DARK],
        title="Top 10 Deteriorations (score rose = worse freedom)",
        labels={"Change": "Score change"},
    )
    fig_det.update_layout(
        paper_bgcolor="white", plot_bgcolor=BG,
        font_family="Inter", margin=dict(t=40, b=20),
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_det, width='stretch')


# MOST VOLATILE COUNTRIES

st.header("Most Volatile Countries")

volatility = (
    df.groupby("Country")["Score"]
      .std()
      .sort_values(ascending=False)
      .head(10)
)
vol_df = volatility.reset_index()
vol_df.columns = ["Country", "Volatility"]

fig_vol = px.bar(
    vol_df.sort_values("Volatility"),
    x="Volatility", y="Country", orientation="h",
    color_discrete_sequence=[RED_DARK],
    title="Top 10 Most Volatile Countries (Std Dev of Score, 2013–2021)",
    labels={"Volatility": "Volatility (σ)"},
)
fig_vol.update_layout(
    paper_bgcolor="white", plot_bgcolor=BG,
    font_family="Inter", margin=dict(t=40, b=20),
)
st.plotly_chart(fig_vol, width='stretch')
st.header("Country Clusters")
st.markdown(
    "<div class='note-box'>"
    "K-Means clustering on three features: mean score, score volatility, and long-term trend. "
    "Cluster colours match the notebook palette."
    "</div>",
    unsafe_allow_html=True,
)

features_plot = features.copy().reset_index()
features_plot["ClusterLabel"] = features_plot["Cluster"].map(CLUSTER_LABELS)
features_plot["Color"]        = features_plot["Cluster"].map(CLUSTER_COLORS)

fig_scatter = px.scatter(
    features_plot,
    x="MeanScore", y="Volatility",
    color="ClusterLabel",
    color_discrete_map={v: CLUSTER_COLORS[k] for k, v in CLUSTER_LABELS.items()},
    hover_name="Country",
    hover_data={"Trend": ":.2f", "MeanScore": ":.1f", "Volatility": ":.2f"},
    labels={"MeanScore": "Avg RSF Score", "Volatility": "Volatility (σ)",
            "ClusterLabel": "Cluster"},
    title="Country Clusters: Press Freedom Score vs Volatility",
    size_max=12,
)
fig_scatter.update_traces(marker=dict(size=9, opacity=0.85))
fig_scatter.update_layout(
    paper_bgcolor="white", plot_bgcolor=BG,
    font_family="Inter", margin=dict(t=40, b=20),
    legend=dict(title="Cluster", font_size=12, orientation="h",
                yanchor="bottom", y=-0.25, xanchor="left", x=0),
)
st.plotly_chart(fig_scatter, width='stretch')

# Cluster summary table
with st.expander("Cluster profiles & sample countries"):
    profile = (
        features.groupby("Cluster")
        .agg(Countries=("MeanScore", "count"),
             MeanScore=("MeanScore", "mean"),
             Volatility=("Volatility", "mean"),
             Trend=("Trend", "mean"))
        .round(2)
    )
    profile.index = profile.index.map(lambda i: f"{i} — {CLUSTER_LABELS[i]}")
    st.dataframe(profile, width='stretch')

    st.markdown("**Sample countries per cluster:**")
    for c in sorted(features["Cluster"].unique()):
        sample = features[features["Cluster"] == c].index.tolist()[:8]
        st.markdown(f"**{c} — {CLUSTER_LABELS[c]}:** {', '.join(sample)}")


# SCORE DISTRIBUTION

st.header("Score Distribution")

fig_hist, ax = plt.subplots(figsize=(10, 3.5))
ax.hist(df["Score"], bins=35, color=BLUE_DARK, edgecolor="white", linewidth=0.5)
ax.axvline(df["Score"].mean(), color=RED_DARK, linestyle="--", linewidth=1.5,
           label=f"Global mean ({df['Score'].mean():.1f})")
ax.set_xlabel("RSF Score (higher = worse)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title("Distribution of All Press Freedom Scores (2013–2021)", fontsize=13)
ax.legend(fontsize=10)
ax.set_facecolor(BG)
fig_hist.patch.set_facecolor("white")
plt.tight_layout()
st.pyplot(fig_hist)


# ANALYSIS SUMMARY

st.header("Analysis Summary")

summary = pd.DataFrame({
    "Metric": [
        "Countries Analyzed",
        "Time Period",
        "Global Change",
        "Avg Year-to-Year Correlation",
        "Kruskal-Wallis p-value",
        "Effect Size (ε²)",
        "Silhouette Score",
    ],
    "Value": [
        str(df["Country"].nunique()),
        f"{first_year}–{latest_year}",
        f"{trend_change:+.2f} points",
        f"{avg_corr:.3f}",
        f"{p_value:.2e}",
        f"{effect_size:.3f}",
        "0.455",
    ],
})
st.dataframe(summary, hide_index=True, width='stretch')


# KEY FINDINGS

st.header("Key Findings")

st.success(
    "• Relative country positions are highly persistent over time (ρ ≈ 0.99)\n"
    "• Regional differences explain a substantial share of variation in press freedom outcomes (ε² = 0.478)\n"
    "• Most countries exhibit gradual change rather than large long-term shifts\n"
    "• Statistical clustering reveals meaningful country profiles without requiring external variables"
)

st.markdown(
    "<div style='font-size:.75rem;color:#9ca3af;margin-top:1.5rem;'>"
    "Data: Reporters Without Borders (RSF) · "
    "Analysis: Global Press Freedom Trends (2013–2021)"
    "</div>",
    unsafe_allow_html=True,
)