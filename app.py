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

height:200px;

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

font-size:34px;

margin-bottom:10px;

}

.kpi-title{

font-size:15px;

color:#94A3B8;

}

.kpi-value{

font-size:20px;

line-height:1.2;

font-weight:800;

margin-top:12px;

color:white;

text-align:center;

}

.kpi-change{

font-size:18px;

font-weight:700;

margin-top:12px;

color:#22C55E;

}


/* FILTER BOX */

.filter-wrapper{

background:rgba(30,41,59,.88);

padding:22px;

border-radius:22px;

border:1px solid rgba(255,255,255,.07);

margin-bottom:25px;

box-shadow:
0 8px 25px rgba(0,0,0,.25);

}

/* Streamlit Selectbox */

.stSelectbox > div > div{

background:#1E293B !important;

border-radius:14px !important;

border:1px solid rgba(255,255,255,.08);

color:white !important;

}

/* Date Input */

.stDateInput > div{

background:#1E293B !important;

border-radius:14px;

}

/* Button */

.stButton button{

background:#38BDF8;

color:white;

border:none;

border-radius:14px;

height:50px;

font-weight:700;

width:100%;

margin-top:28px;

}

.stButton button:hover{

background:#0EA5E9;

}

/* Labels */

label{

font-weight:600 !important;

color:#CBD5E1 !important;

}

.stDateInput input{

background:#1E293B !important;

color:white !important;

border:none !important;

}

.stDateInput{

background:#1E293B !important;

border-radius:14px;

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
# ====================================================
# DATA PREP
# ====================================================

df = df.sort_values(["Ticker", "Date"])

df["Daily_Return"] = df.groupby("Ticker")["Close"].pct_change() * 100

# ====================================================
# FILTER TITLE
# ====================================================

st.markdown(
    """
<h2 style="
margin-bottom:20px;
">
🔎 Explore Market Data
</h2>
""",
    unsafe_allow_html=True,
)

# ====================================================
# FILTERS
# ====================================================

c1, c2, c3, c4 = st.columns([1.1, 1.2, 1.4, 0.7])

with c1:

    selected_country = st.selectbox(
        "🌍 Country", ["All"] + sorted(df["Country"].dropna().unique())
    )

with c2:

    country_filtered = df.copy()

    if selected_country != "All":

        country_filtered = country_filtered[
            country_filtered["Country"] == selected_country
        ]

    selected_stock = st.selectbox(
        "📈 Stock", ["All"] + sorted(country_filtered["Ticker"].dropna().unique())
    )

with c3:

    selected_dates = st.date_input(
        "📅 Date Range", value=(df["Date"].min(), df["Date"].max())
    )

with c4:

    st.markdown("<br>", unsafe_allow_html=True)

    reset = st.button("Reset Filters", use_container_width=True)

# ====================================================
# APPLY FILTERS
# ====================================================

filtered_df = df.copy()

if selected_country != "All":

    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

if selected_stock != "All":

    filtered_df = filtered_df[filtered_df["Ticker"] == selected_stock]

start_date, end_date = selected_dates

filtered_df = filtered_df[
    (filtered_df["Date"] >= pd.to_datetime(start_date))
    & (filtered_df["Date"] <= pd.to_datetime(end_date))
]

latest_filtered = filtered_df[filtered_df["Date"] == filtered_df["Date"].max()].copy()

# ====================================================
# KPI CALCULATIONS
# ====================================================

best_stock = latest_filtered.loc[latest_filtered["Daily_Return"].idxmax()]

worst_stock = latest_filtered.loc[latest_filtered["Daily_Return"].idxmin()]

volume_stock = latest_filtered.loc[latest_filtered["Volume"].idxmax()]

avg_return = latest_filtered["Daily_Return"].mean()

trend = "Bullish 📈" if avg_return > 0 else "Bearish 📉"

stock_count = latest_filtered["Ticker"].nunique()

# ====================================================
# SNAPSHOT TITLE
# ====================================================

st.markdown("## 📊 Market Snapshot")

st.markdown(
    """
<p style="
margin-top:-10px;
margin-bottom:15px;
color:#94A3B8;
">
Quick overview of market leaders and movers
</p>
""",
    unsafe_allow_html=True,
)

# ====================================================
# KPI ROW
# ====================================================

col1, col2, col3, col4, col5 = st.columns(5)

# ------------------------------------------------

with col1:

    st.markdown(
        f"""
    <div class="kpi-card">

    <div class="kpi-icon">
    🚀
    </div>

    <div class="kpi-title">
    Top Gainer
    </div>

    <div class="kpi-value">
    {best_stock['Stock_Name']}
    </div>

    <div style="color:#94A3B8;">
    {best_stock['Ticker']}
    </div>

    <div class="kpi-change">
    {best_stock['Daily_Return']:.2f}%
    </div>

    </div>
    """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------

with col2:

    st.markdown(
        f"""
    <div class="kpi-card">

    <div class="kpi-icon">
    📉
    </div>

    <div class="kpi-title">
    Biggest Drop
    </div>

    <div class="kpi-value">
    {worst_stock['Stock_Name']}
    </div>

    <div style="color:#94A3B8;">
    {worst_stock['Ticker']}
    </div>

    <div class="kpi-change"
    style="color:#EF4444;">
    {worst_stock['Daily_Return']:.2f}%
    </div>

    </div>
    """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------

with col3:

    st.markdown(
        f"""
    <div class="kpi-card">

    <div class="kpi-icon">
    💰
    </div>

    <div class="kpi-title">
    Most Traded
    </div>

    <div class="kpi-value">
    {volume_stock['Stock_Name']}
    </div>

    <div style="color:#94A3B8;">
    {volume_stock['Ticker']}
    </div>

    <div class="kpi-change">
    {volume_stock['Volume']:,.0f}
    </div>

    </div>
    """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------

with col4:

    st.markdown(
        f"""
    <div class="kpi-card">

    <div class="kpi-icon">
    📊
    </div>

    <div class="kpi-title">
    Market Trend
    </div>

    <div class="kpi-value">
    {avg_return:.2f}%
    </div>

    <div class="kpi-change">
    {trend}
    </div>

    </div>
    """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------

with col5:

    st.markdown(
        f"""
    <div class="kpi-card">

    <div class="kpi-icon">
    🔎
    </div>

    <div class="kpi-title">
    Stocks In View
    </div>

    <div class="kpi-value">
    {stock_count}
    </div>

    <div class="kpi-change">
    Companies
    </div>

    </div>
    """,
        unsafe_allow_html=True,
    )
