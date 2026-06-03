import streamlit as st
import pandas as pd
import joblib
import os
from pathlib import Path

# st.write("Current directory:", os.getcwd())
# st.write("Script location:", Path(__file__).resolve())
# st.write("Files here:", os.listdir(Path(__file__).parent))
# ── 1. GLOBAL PAGE CONFIGURATION ───────────────────────────────────────────
st.set_page_config(
    page_title="ATM Cash Intelligence Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── 2. NEUMORPHIC (SOFT UI) ENTERPRISE CSS THEME ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* Base Neumorphic Canvas Setup */
html, body, [class*="css"] { 
    font-family: 'Plus Jakarta Sans', sans-serif !important; 
}
.stApp { 
    background-color: #E0E5EC !important; 
}
#MainMenu, footer, header { 
    visibility: hidden; 
}
.block-container { 
    padding: 0 !important; 
    max-width: 100% !important; 
}

/* Typography & Visual Accents */
.section-label {
    font-size: 11px; 
    font-weight: 700;
    letter-spacing: 0.12em; 
    text-transform: uppercase;
    color: #7A869A; 
    margin: 32px 0 16px 4px;
    text-shadow: 1px 1px 1px #FFFFFF;
}

/* Neumorphic Extruded Top Bar */
.topbar {
    background: #E0E5EC;
    padding: 0 40px;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 4px 20px 0 rgba(163, 177, 198, 0.5);
}
.logo-container {
    display: flex;
    align-items: center;
}
.logo-sq {
    width: 36px; 
    height: 36px;
    background: #E0E5EC;
    border-radius: 10px;
    display: inline-flex;
    align-items: center; 
    justify-content: center;
    font-size: 15px; 
    font-weight: 700;
    color: #4A5568; 
    margin-right: 14px;
    box-shadow: 4px 4px 8px #B8C4D9, -4px -4px 8px #FFFFFF;
}
.logo-name { 
    font-size: 16px; 
    font-weight: 700; 
    color: #2D3748; 
    letter-spacing: -0.01em; 
}
.logo-sep { 
    display: inline-block; 
    width: 2px; 
    height: 20px; 
    background: #D1D9E6; 
    margin: 0 14px; 
    border-right: 1px solid #FFFFFF;
}
.logo-sub { 
    font-size: 12px; 
    font-weight: 600;
    color: #718096; 
}
.live-ind { 
    display: inline-flex; 
    align-items: center; 
    gap: 8px; 
    font-size: 12px; 
    font-weight: 700;
    color: #2F855A; 
    background: #E0E5EC;
    padding: 6px 16px;
    border-radius: 12px;
    box-shadow: inset 2px 2px 5px #B8C4D9, inset -2px -2px 5px #FFFFFF;
}
.live-dot { 
    width: 8px; 
    height: 8px; 
    border-radius: 50%; 
    background: #48BB78; 
    display: inline-block; 
}

/* Base Structural Layout Wrap */
.body-pad { 
    padding: 24px 40px 64px 40px; 
}

/* Flat Neumorphic Filter Board Panel */
.filter-panel {
    background: #E0E5EC;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 28px;
    box-shadow: 6px 6px 14px #B8C4D9, -6px -6px 14px #FFFFFF;
}

/* Convex Pill Shape KPI Blocks */
.kpi-band {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
    margin-bottom: 36px;
}
.kpi-cell {
    background: #E0E5EC;
    padding: 26px;
    border-radius: 16px;
    box-shadow: 6px 6px 14px #B8C4D9, -6px -6px 14px #FFFFFF;
    transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.kpi-cell:hover {
    box-shadow: 2px 2px 5px #B8C4D9, -2px -2px 5px #FFFFFF;
    transform: translateY(1px);
}
.kpi-num {
    font-weight: 800;
    font-size: 32px; 
    color: #2D3748; 
    letter-spacing: -0.02em;
    line-height: 1.2; 
    margin-bottom: 6px;
}
.kpi-lbl {
    font-size: 12px; 
    font-weight: 700;
    color: #718096; 
    display: flex;
    align-items: center; 
    gap: 8px;
}
.kpi-pip { 
    width: 8px; 
    height: 8px; 
    border-radius: 50%; 
    display: inline-block; 
    box-shadow: inset 1px 1px 2px rgba(0,0,0,0.2);
}

/* Dynamic Semantic Hues */
.kpi-red .kpi-num { color: #C53030; }
.kpi-amber .kpi-num { color: #DD6B20; }
.kpi-green .kpi-num { color: #2F855A; }

/* Data Output Base Plate */
.table-header-container {
    background: #E0E5EC;
    border-radius: 16px 16px 0 0;
    padding: 20px 28px;
    display: flex; 
    align-items: center; 
    justify-content: space-between;
    box-shadow: 6px 6px 14px #B8C4D9, -6px -6px 14px #FFFFFF;
    margin-bottom: -1px;
}
.t-title { 
    font-size: 14px; 
    font-weight: 700; 
    color: #2D3748; 
}
.t-count {
    font-size: 11px; 
    font-weight: 700;
    color: #4A5568;
    background: #E0E5EC;
    padding: 5px 12px; 
    border-radius: 8px;
    box-shadow: inset 2px 2px 5px #B8C4D9, inset -2px -2px 5px #FFFFFF;
}

/* Multi-select Soft UI Embedding Overrides */
div[data-testid="stMultiSelect"] label {
    font-size: 11px !important; 
    color: #4A5568 !important;
    font-weight: 700 !important; 
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 8px !important;
    text-shadow: 1px 1px 0px #FFFFFF;
}
div[data-testid="stMultiSelect"] > div > div {
    background: #E0E5EC !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: inset 3px 3px 6px #B8C4D9, inset -3px -3px 6px #FFFFFF !important;
    padding: 4px 6px !important;
}
div[data-testid="stDataFrame"] > div {
    border: none !important;
    border-radius: 0 0 16px 16px !important;
    background: #E0E5EC !important;
    box-shadow: 6px 6px 14px #B8C4D9, -6px -6px 14px #FFFFFF !important;
    padding: 10px !important;
}

/* Action Buttons (Neumorphic Inverted Controls) */
div[data-testid="stDownloadButton"] button {
    background: #E0E5EC !important;
    border: none !important;
    border-radius: 12px !important;
    color: #4A5568 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    width: 100% !important;
    box-shadow: 4px 4px 10px #B8C4D9, -4px -4px 10px #FFFFFF !important;
    transition: all 0.15s ease-in-out !important;
}
div[data-testid="stDownloadButton"] button:hover {
    box-shadow: inset 2px 2px 5px #B8C4D9, inset -2px -2px 5px #FFFFFF !important;
    color: #2D3748 !important;
}
div[data-testid="stLinkButton"] a {
    background: #E0E5EC !important;
    border: none !important;
    border-radius: 12px !important;
    color: #2B6CB0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    box-shadow: 4px 4px 10px #B8C4D9, -4px -4px 10px #FFFFFF !important;
    display: inline-block;
    text-align: center;
    transition: all 0.15s ease-in-out !important;
}
div[data-testid="stLinkButton"] a:hover {
    box-shadow: inset 2px 2px 5px #B8C4D9, inset -2px -2px 5px #FFFFFF !important;
    color: #2B6CB0 !important;
}

/* System Soft UI Footer Configuration */
.footer-bar {
    border-top: 1px solid rgba(255,255,255,0.4);
    padding: 28px 40px;
    display: flex; 
    justify-content: space-between;
    align-items: center;
    background: #E0E5EC; 
    margin-top: 50px;
    box-shadow: inset 0 4px 10px -5px #B8C4D9;
}
.footer-l { 
    font-size: 12px; 
    color: #718096; 
    font-weight: 600;
}
.footer-r { 
    font-size: 12px; 
    color: #4A5568; 
}
.footer-r a { 
    color: #2B6CB0; 
    text-decoration: none; 
    font-weight: 700; 
}
.footer-r a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ── 3. NAVIGATION HEADER TOPBAR ───────────────────────────────────────────
POWERBI_URL = "https://app.powerbi.com/view?r=YOUR_REPORT_ID"

st.markdown("""
<div class="topbar">
  <div class="logo-container">
    <span class="logo-sq">₳</span>
    <span class="logo-name">ATM Cash Intelligence</span>
    <span class="logo-sep"></span>
    <span class="logo-sub">Enterprise Risk Control</span>
  </div>
  <div>
    <span class="live-ind"><span class="live-dot"></span>System Active</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 4. BACKEND MACHINE LEARNING DATA WORKFLOW ─────────────────────────────
from pathlib import Path

BASE_DIR = Path(__file__).parent

MODEL_PATH = BASE_DIR / "model.pkl"
DATA_PATH = BASE_DIR / "atm_cash_management_dataset.csv"

# st.write("Model exists:", MODEL_PATH.exists())
# st.write("Model path:", MODEL_PATH)

model = joblib.load(MODEL_PATH)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

def feature_engineering(df):
    df = df.copy()
    df["Month"]   = df["Date"].dt.month
    df["Day"]     = df["Date"].dt.day
    df["Quarter"] = df["Date"].dt.quarter
    df["Is_Weekend"] = df["Day_of_Week"].isin(["Saturday","Sunday"]).astype(int)
    df["Net_Cash_Flow"]         = df["Total_Deposits"] - df["Total_Withdrawals"]
    df["Cash_Utilization"]      = df["Total_Withdrawals"] / (df["Previous_Day_Cash_Level"] + 1)
    df["Demand_Pressure_Index"] = df["Total_Withdrawals"] / (df["Nearby_Competitor_ATMs"] + 1)
    return df

df = feature_engineering(df)
X  = df.reindex(columns=model.feature_names_in_, fill_value=0)
df["Predicted_Cash_Demand"] = model.predict(X)
df["Remaining_Cash"]  = df["Previous_Day_Cash_Level"] - df["Predicted_Cash_Demand"]
df["Days_to_Cashout"] = df["Previous_Day_Cash_Level"] / (df["Predicted_Cash_Demand"] + 1)

def risk_level(x):
    if x <= 1:   return "CRITICAL"
    elif x <= 2: return "HIGH"
    elif x <= 4: return "MEDIUM"
    return "LOW"

df["Risk"] = df["Days_to_Cashout"].apply(risk_level)

# ── 5. FOREGROUND APPLICATION CONTENT ──────────────────────────────────────
st.markdown('<div class="body-pad">', unsafe_allow_html=True)

# BI Shortcut Component
top_actions_col, _ = st.columns([1, 3])
with top_actions_col:
    st.link_button("View Live Analytics Summary", POWERBI_URL)

# Interactive Filters Block
st.markdown('<p class="section-label">Target Criteria Search</p>', unsafe_allow_html=True)
st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
risk_filter     = fc1.multiselect("Risk Classification", ["CRITICAL","HIGH","MEDIUM","LOW"], default=["CRITICAL","HIGH"])
atm_filter      = fc2.multiselect("ATM Terminal Identification", df["ATM_ID"].unique(), placeholder="All Terminals Active")
location_filter = fc3.multiselect("Location Infrastructure Type", df["Location_Type"].unique(), placeholder="All Regions")
st.markdown('</div>', unsafe_allow_html=True)

# Apply Selected Filter Combinations
filtered = df.copy()
if risk_filter:     filtered = filtered[filtered["Risk"].isin(risk_filter)]
if atm_filter:      filtered = filtered[filtered["ATM_ID"].isin(atm_filter)]
if location_filter: filtered = filtered[filtered["Location_Type"].isin(location_filter)]

# Descriptive Statistics KPI Section
total    = len(filtered)
critical = len(filtered[filtered["Risk"] == "CRITICAL"])
high     = len(filtered[filtered["Risk"] == "HIGH"])
safe     = len(filtered[filtered["Risk"] == "LOW"])

st.markdown('<p class="section-label">Aggregated System Metrics</p>', unsafe_allow_html=True)
st.markdown(f"""
<div class="kpi-band">
  <div class="kpi-cell">
    <div class="kpi-num">{total:,}</div>
    <div class="kpi-lbl">Monitored Terminals</div>
  </div>
  <div class="kpi-cell kpi-red">
    <div class="kpi-num">{critical:,}</div>
    <div class="kpi-lbl"><span class="kpi-pip" style="background:#C53030"></span>Urgent Action Required</div>
  </div>
  <div class="kpi-cell kpi-amber">
    <div class="kpi-num">{high:,}</div>
    <div class="kpi-lbl"><span class="kpi-pip" style="background:#DD6B20"></span>Elevated Risk Warning</div>
  </div>
  <div class="kpi-cell kpi-green">
    <div class="kpi-num">{safe:,}</div>
    <div class="kpi-lbl"><span class="kpi-pip" style="background:#2F855A"></span>Operational Baseline Safe</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Main Replenishment Grid
st.markdown('<p class="section-label">Realtime Dispatch Register</p>', unsafe_allow_html=True)
st.markdown(f"""
<div class="table-header-container">
  <span class="t-title">Replenishment Routing Queue</span>
  <span class="t-count">{len(filtered):,} Node entries found</span>
</div>
""", unsafe_allow_html=True)

display_df = filtered[[
    "ATM_ID","Location_Type","Total_Withdrawals",
    "Previous_Day_Cash_Level","Predicted_Cash_Demand",
    "Remaining_Cash","Days_to_Cashout","Risk"
]].copy()
display_df.columns = [
    "ATM ID","Infrastructure Profile","Historic Outflow (₹)",
    "Opening Vault (₹)","Algorithmic Prediction (₹)",
    "Calculated Variance (₹)","Burn Rate (Days)","Risk Profile"
]

st.dataframe(display_df, use_container_width=True, hide_index=True, height=440)

# Export Framework Control Row
st.markdown('<p class="section-label">Export Audits & Reports</p>', unsafe_allow_html=True)
ec1, ec2, _ = st.columns([1.2, 1.2, 2.6])
with ec1:
    st.download_button(
        "📥 Download Filtered Framework",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="atm_filtered_report.csv", mime="text/csv"
    )
with ec2:
    st.download_button(
        "📦 Extract Full Baseline Ledger",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="atm_full_report.csv", mime="text/csv"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── 6. APPLICATION FOOTER META ─────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
  <span class="footer-l">ATM Cash Intelligence Automation Architecture &nbsp;·&nbsp; Enterprise Neumorphic UI v4.0</span>
  <span class="footer-r">
    Architected by <a href="mailto:nasir.swat.hussain@gmail.com"><strong>Nasir Hussain</strong></a>
  </span>
</div>
""", unsafe_allow_html=True)
