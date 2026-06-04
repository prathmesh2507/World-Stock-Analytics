import streamlit as st
import pandas as pd
from datetime import datetime

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Global Stock Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------


@st.cache_data
def load_data():
    df = pd.read_csv("combined_data/final_data.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()

# ------------------------------------------------
# Theme CSS
# ------------------------------------------------

st.markdown(
    """
<style>

/* Main App */
.stApp{
    background:#0F172A;
    color:white;
}

/* Remove top spacing */
.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    max-width:1400px;
}

/* Hero Card */
.hero-card{
    background: linear-gradient(
        135deg,
        #1E293B,
        #0F172A
    );

    padding:30px 40px;
    border-radius:25px;

    border:1px solid rgba(255,255,255,0.1);

    box-shadow:
    0px 10px 40px rgba(0,0,0,0.4);
}

/* Titles */
.hero-title{
    font-size:42px;
    font-weight:800;
    color:white;
}

.hero-subtitle{
    font-size:18px;
    color:#CBD5E1;
    margin-top:10px;
}

/* Small info */
.hero-info{
    color:#94A3B8;
    font-size:14px;
}

/* KPI Cards */
.metric-card{
    background:#1E293B;

    border-radius:20px;

    padding:20px;

    text-align:center;

    border:1px solid rgba(255,255,255,0.05);

    transition:0.3s;
}

.metric-card:hover{
    transform:translateY(-5px);
}

.metric-title{
    color:#94A3B8;
    font-size:14px;
}

.metric-value{
    font-size:28px;
    font-weight:700;
    color:white;
}

.metric-change{
    color:#22C55E;
    font-size:16px;
}


/* Remove Streamlit Header */
header {
    visibility: hidden;
}

/* Remove Top Toolbar Space */
[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

/* Remove top padding */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Remove extra top margin */
.main .block-container {
    padding-top: 1rem !important;
}

.kpi-card{

background:rgba(30,41,59,0.92);

padding:28px;

border-radius:24px;

height:220px;

display:flex;

flex-direction:column;

justify-content:center;

align-items:center;

border:1px solid rgba(255,255,255,0.07);

transition:0.3s ease;

box-shadow:
0 8px 20px rgba(0,0,0,.25);

}

.kpi-card:hover{

transform:translateY(-8px);

box-shadow:
0 12px 30px rgba(56,189,248,.2);

}

.kpi-icon{

font-size:38px;

margin-bottom:10px;

}

.kpi-title{

font-size:15px;

color:#94A3B8;

}

.kpi-value{

font-size:24px;

font-weight:800;

margin-top:12px;

color:white;

text-align:center;

}

.kpi-change{

font-size:24px;

font-weight:700;

margin-top:12px;

color:#22C55E;

}

</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------
# HERO SECTION
# ------------------------------------------------

latest_date = df["Date"].max()

st.markdown(
    f"""
<div class="hero-card">

<div class="hero-title">
🌍 Global Stock Intelligence Dashboard
</div>

<div class="hero-subtitle">
Track market trends, discover top performers,
and analyze global stock movements through
interactive analytics.
</div>

<br>

<div class="hero-info">

📅 Last Updated:
{latest_date.strftime('%d %B %Y')}

&nbsp;&nbsp;&nbsp;&nbsp;

📈 Markets: Global

</div>

</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------
# DATA PREPARATION
# ------------------------------------------------
filter1, filter2, filter3, filter4 = st.columns(4)

with filter1:

    selected_country = st.selectbox(
        "🌍 Country", ["All"] + sorted(df["Country"].unique())
    )

with filter2:

    selected_stock = st.selectbox("📈 Stock", ["All"] + sorted(df["Ticker"].unique()))

with filter3:

    selected_dates = st.date_input(
        "📅 Date Range", value=(df["Date"].min(), df["Date"].max())
    )

with filter4:

    st.write("")

    reset = st.button("Reset Filters", use_container_width=True)

filtered_df = df.copy()

if selected_country != "All":

    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

if selected_stock != "All":

    filtered_df = filtered_df[filtered_df["Ticker"] == selected_stock]


st.markdown("## 📊 Market Snapshot")
st.markdown(
    """
<p style="
margin-top:-10px;
margin-bottom:15px;
color:#94A3B8;
">
Quick overview of today's market leaders and movers
</p>
""",
    unsafe_allow_html=True,
)


col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 1.2, 1.2, 1.2], gap="medium")


df = df.sort_values(["Ticker", "Date"])

df["Daily_Return"] = df.groupby("Ticker")["Close"].pct_change() * 100

latest_date = df["Date"].max()

filtered_df = df[df["Date"] == latest_date].copy()

# Best Performer
best_stock = filtered_df.loc[filtered_df["Daily_Return"].idxmax()]

# Worst Performer
worst_stock = filtered_df.loc[filtered_df["Daily_Return"].idxmin()]

# Highest Volume
volume_stock = filtered_df.loc[filtered_df["Volume"].idxmax()]

# Countries Covered
country_count = filtered_df["Country"].nunique()

# Strongest Market
country_perf = filtered_df.groupby("Country")["Daily_Return"].mean().reset_index()

best_country = country_perf.loc[country_perf["Daily_Return"].idxmax()]


with col1:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-title">Best Performer</div>
        <div class="kpi-value">{best_stock['Ticker']}</div>
        <div class="kpi-change">
            {best_stock['Daily_Return']:.2f}%
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-icon">🔥</div>
        <div class="kpi-title">Strongest Market</div>
        <div class="kpi-value">{best_country['Country']}</div>
        <div class="kpi-change">
            {best_country['Daily_Return']:.2f}%
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
    <div class="kpi-card">
    <div class="kpi-icon">💰</div>
    <div class="kpi-title">Highest Volume</div>
    <div class="kpi-value">{volume_stock['Ticker']}</div>
    <div class="kpi-change">
    {volume_stock['Volume']:,.0f}
    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
    <div class="kpi-card">
    <div class="kpi-icon">📉</div>
    <div class="kpi-title">Biggest Decliner</div>
    <div class="kpi-value">{worst_stock['Ticker']}</div>
    <div class="kpi-change" style="color:#EF4444;">
    {worst_stock['Daily_Return']:.2f}%
    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        f"""
    <div class="kpi-card">
    <div class="kpi-icon">🌍</div>
    <div class="kpi-title">Markets Covered</div>
    <div class="kpi-value">
    {country_count}
    </div>
    <div class="kpi-change">
    Countries
    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
