import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="P&G Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# P&G brand palette
# ---------------------------------------------------------------------------
PG_BLUE = "#004B93"        # primary brand blue
PG_DARK_NAVY = "#12284C"   # deep navy for text/contrast
PG_LIGHT_BLUE = "#4A90D9"  # secondary blue
PG_SKY = "#8FC1E3"         # tertiary/light accent
PG_GOLD = "#F2A900"        # accent gold, used sparingly
PG_GRAY = "#8C9BAB"        # neutral
PG_ALERT = "#D9534F"       # muted red-orange, only for "Behind Pace"

STATUS_COLORS = {
    "On Track": PG_BLUE,
    "On Track / Raised Bar": PG_BLUE,
    "On Track (long lead)": PG_LIGHT_BLUE,
    ">99% / On Track": PG_LIGHT_BLUE,
    "Exceeded": PG_GOLD,
    "Maintained": PG_GRAY,
    "Portfolio Complete": PG_GOLD,
    "Behind Pace": PG_ALERT,
}

BRAND_SEQUENCE = [PG_BLUE, PG_GOLD, PG_LIGHT_BLUE, PG_DARK_NAVY, PG_SKY, PG_GRAY]

PLOTLY_LAYOUT_DEFAULTS = dict(
    font=dict(family="Arial, sans-serif", color=PG_DARK_NAVY),
    title_font=dict(family="Arial, sans-serif", color=PG_DARK_NAVY, size=18),
    legend=dict(orientation="h", font=dict(color=PG_DARK_NAVY)),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    colorway=BRAND_SEQUENCE,
)

def style_fig(fig, **overrides):
    layout = {**PLOTLY_LAYOUT_DEFAULTS, **overrides}
    fig.update_layout(**layout)
    fig.update_xaxes(gridcolor="#E6EBF2", zerolinecolor="#E6EBF2")
    fig.update_yaxes(gridcolor="#E6EBF2", zerolinecolor="#E6EBF2")
    return fig

# ---------------------------------------------------------------------------
# Custom CSS — P&G blue header banner + styled metric cards
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .pg-banner {{
        background: linear-gradient(90deg, {PG_DARK_NAVY} 0%, {PG_BLUE} 60%, {PG_LIGHT_BLUE} 100%);
        padding: 1.6rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.2rem;
    }}
    .pg-banner h1 {{
        color: #FFFFFF;
        font-size: 1.8rem;
        margin: 0;
        font-weight: 700;
    }}
    .pg-banner p {{
        color: #D6E4F5;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }}
    div[data-testid="stMetric"] {{
        background-color: #F0F4F8;
        border-left: 4px solid {PG_BLUE};
        border-radius: 6px;
        padding: 0.8rem 1rem;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {PG_DARK_NAVY};
    }}
    div[data-testid="stMetricValue"] {{
        color: {PG_BLUE};
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #F0F4F8;
        border-radius: 6px 6px 0 0;
        color: {PG_DARK_NAVY};
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {PG_BLUE} !important;
        color: #FFFFFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    highlights = pd.read_csv("data/financial_highlights.csv")
    income = pd.read_csv("data/income_statement.csv")
    segments = pd.read_csv("data/segment_mix.csv")
    geo = pd.read_csv("data/geographic_mix.csv")
    goals = pd.read_csv("data/ambition2030_goals.csv")
    trends = pd.read_csv("data/ambition2030_trends.csv")
    return highlights, income, segments, geo, goals, trends

highlights, income, segments, geo, goals, trends = load_data()

YEARS = ["2021", "2022", "2023", "2024", "2025", "2026"]

def get_metric(df, name):
    row = df[df.iloc[:, 0] == name]
    return row[YEARS].values.flatten().astype(float) if not row.empty else None

# ---------------------------------------------------------------------------
# Header banner
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="pg-banner">
        <h1>Procter &amp; Gamble — Performance Dashboard</h1>
        <p>Financial data from P&amp;G's FY2025 and FY2026 Annual Reports (audited, cross-checked across
        both filings) · Sustainability data from P&amp;G's Ambition 2030 Mid-Point Progress Update, August 2025</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["📈 Financial Performance", "🌍 Ambition 2030 Sustainability", "🧭 Segment & Geographic Mix"])

# ---------------------------------------------------------------------------
# TAB 1: Financial Performance
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Six-Year Financial Trend (FY2021–FY2026)")

    col1, col2, col3, col4 = st.columns(4)
    net_sales = get_metric(highlights, "Net Sales ($B)")
    op_margin = get_metric(highlights, "Net Earnings Margin (%)")
    eps = get_metric(highlights, "Diluted EPS ($)")
    ocf = get_metric(highlights, "Operating Cash Flow ($B)")

    col1.metric("FY2026 Net Sales", f"${net_sales[-1]:.1f}B", f"{(net_sales[-1]/net_sales[-2]-1)*100:+.1f}% YoY")
    col2.metric("FY2026 Net Earnings Margin", f"{op_margin[-1]*100:.1f}%", f"{(op_margin[-1]-op_margin[-2])*100:+.1f} pp YoY")
    col3.metric("FY2026 Diluted EPS", f"${eps[-1]:.2f}", f"{(eps[-1]/eps[-2]-1)*100:+.1f}% YoY")
    col4.metric("FY2026 Operating Cash Flow", f"${ocf[-1]:.1f}B", f"{(ocf[-1]/ocf[-2]-1)*100:+.1f}% YoY")

    left, right = st.columns(2)

    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=YEARS, y=net_sales, mode="lines+markers", name="Net Sales ($B)",
                                  line=dict(color=PG_BLUE, width=3), marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=YEARS, y=ocf, mode="lines+markers", name="Operating Cash Flow ($B)",
                                  line=dict(color=PG_GOLD, width=3), marker=dict(size=8)))
        style_fig(fig, title="Net Sales vs. Operating Cash Flow", yaxis_title="$ Billions")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        diluted = get_metric(highlights, "Diluted EPS ($)")
        core = get_metric(highlights, "Core EPS ($)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=YEARS, y=diluted, mode="lines+markers", name="Diluted EPS",
                                  line=dict(color=PG_BLUE, width=3), marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=YEARS, y=core, mode="lines+markers", name="Core EPS",
                                  line=dict(color=PG_GOLD, width=3), marker=dict(size=8)))
        style_fig(fig, title="Diluted vs. Core EPS", yaxis_title="$ per Share")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Margin Trend: Is Growth Coming Cheaply or Expensively?")
    income_years = ["2023", "2024", "2025", "2026"]
    net_sales_is = income[income.iloc[:, 0] == "Net Sales"][income_years].values.flatten().astype(float)
    cogs = income[income.iloc[:, 0] == "Cost of products sold"][income_years].values.flatten().astype(float)
    op_inc = income[income.iloc[:, 0] == "Operating Income"][income_years].values.flatten().astype(float)
    gross_margin = 1 - (cogs / net_sales_is)
    operating_margin = op_inc / net_sales_is

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=income_years, y=gross_margin * 100, mode="lines+markers", name="Gross Margin %",
                              line=dict(color=PG_BLUE, width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=income_years, y=operating_margin * 100, mode="lines+markers", name="Operating Margin %",
                              line=dict(color=PG_DARK_NAVY, width=3), marker=dict(size=8)))
    style_fig(fig, yaxis_title="% of Net Sales")
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "**Reading the trend:** FY2026 net sales grew 3% to $87.0B, but both gross margin (51.2%→50.2%) "
        "and operating margin (24.3%→22.7%) declined versus FY2025 — P&G's strongest margin year in this "
        "six-year window. Growth returned alongside rising costs rather than expanding profitability, a "
        "reversal from the prior year's pattern."
    )

    with st.expander("View full audited Income Statement ($ millions, FY2023–FY2026)"):
        st.dataframe(income, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# TAB 2: Ambition 2030 Sustainability
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Ambition 2030: Progress Toward Environmental Goals")
    st.caption("Progress figures as of fiscal year end 2024 (FY23/24), per P&G's August 2025 mid-point update.")

    pillars = goals["Pillar"].unique()
    pillar_cols = st.columns(len(pillars))
    for col, pillar in zip(pillar_cols, pillars):
        avg_progress = goals.loc[goals["Pillar"] == pillar, "% of Target Achieved"].mean()
        col.metric(f"{pillar} — Avg. % of Target", f"{avg_progress*100:.0f}%")

    st.markdown("#### Goal-by-Goal Progress")
    selected_pillar = st.selectbox("Filter by pillar", ["All"] + list(pillars))
    display_df = goals if selected_pillar == "All" else goals[goals["Pillar"] == selected_pillar]
    display_df = display_df.sort_values("% of Target Achieved")

    fig = px.bar(
        display_df,
        x="% of Target Achieved",
        y="2030 Goal",
        color="Status",
        orientation="h",
        title="Progress vs. 2030 Target, by Goal",
        text=display_df["% of Target Achieved"].apply(lambda x: f"{x*100:.0f}%"),
        color_discrete_map=STATUS_COLORS,
    )
    style_fig(fig, height=600, xaxis_tickformat=".0%", yaxis_title="", xaxis_title="% of Target Achieved")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Multi-Year Trend: Is Progress Accelerating or Slowing?")
    trend_colors = [PG_BLUE, PG_GOLD, PG_LIGHT_BLUE]
    fig2 = go.Figure()
    for i, col in enumerate(trends.columns[1:]):
        fig2.add_trace(go.Scatter(x=trends["Period"], y=trends[col], mode="lines+markers", name=col,
                                   line=dict(color=trend_colors[i % len(trend_colors)], width=3), marker=dict(size=8)))
    style_fig(fig2, yaxis_title="% Progress", yaxis_range=[0, 100])
    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "**Reading the trend:** Renewable electricity purchasing plateaued years ago (97%→99%→99%), while "
        "packaging recyclability is still climbing but each period's gain is smaller than the last "
        "(55→73→78→80). Scope 1&2 GHG reduction shows the same decelerating pattern. Meanwhile, Scope 3 "
        "supply-chain emissions — the hardest goal, since it depends on suppliers — sits at just 9% of its "
        "40% target, and P&G's own report estimates only about three-quarters of that goal may be feasible "
        "by 2030."
    )

    with st.expander("View full goal detail, including P&G's own 'Perspective and Path Forward' text"):
        st.dataframe(
            goals[["Pillar", "2030 Goal", "2030 Target (value)", "Progress as of FY23/24 (value)", "Status", "Perspective / Path Forward (summary)"]],
            use_container_width=True,
            hide_index=True,
        )

# ---------------------------------------------------------------------------
# TAB 3: Segment & Geographic Mix
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Where P&G's Revenue Comes From (FY2026)")

    blue_shades = [PG_DARK_NAVY, PG_BLUE, PG_LIGHT_BLUE, PG_SKY, PG_GOLD, PG_GRAY]

    left, right = st.columns(2)
    with left:
        fig = px.pie(
            segments, names="Reportable Segment", values="% of Net Sales FY2026",
            title="Net Sales by Business Segment", hole=0.45,
            color_discrete_sequence=blue_shades,
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.pie(
            geo, names="Region", values="FY2026",
            title="Net Sales by Geographic Region", hole=0.45,
            color_discrete_sequence=blue_shades,
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Segment Profitability: Sales Share vs. Earnings Share (FY2026)")
    seg_compare = segments[["Reportable Segment", "% of Net Sales FY2026", "% of Net Earnings FY2026"]].melt(
        id_vars="Reportable Segment", var_name="Measure", value_name="Share"
    )
    fig = px.bar(
        seg_compare, x="Reportable Segment", y="Share", color="Measure", barmode="group",
        title="Which Segments Punch Above Their Weight?",
        color_discrete_sequence=[PG_BLUE, PG_GOLD],
    )
    style_fig(fig, yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "**Reading the mix:** Grooming is the clearest example of a segment earning more than its sales "
        "share suggests — 8% of net sales but 9% of net earnings in FY2026 — pointing to above-average "
        "margins in that business relative to the portfolio overall."
    )

st.divider()
st.caption(
    "Built as an independent analysis of P&G's public financial filings and sustainability reporting. "
    "Not affiliated with or endorsed by Procter & Gamble. Sources: P&G FY2025 & FY2026 Annual Reports; "
    "P&G Ambition 2030 Mid-Point Progress Update (August 2025)."
)
