import streamlit as st
import pandas as pd
from ai.analytics import (
    get_dashboard_metrics,
    route_statistics,
    get_transporter_counts,
    get_database_coverage,
    get_top_route_origins,
    get_interactive_routes,
    get_origin_list
)

# PAGE CONFIG 
st.set_page_config(
    page_title="Logistics Dashboard",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
.block-container { padding-top:2rem; padding-left: 3rem; padding-right: 3rem; max-width: 100%; background-color: #0b1119; color: #e2e8f0; }

/* Global Background */
.stApp { background-color: #0b1119; }

/* Section Headers */
.section-title { font-size:14px; font-weight:700; margin-top:35px; margin-bottom:15px; color:#F1F5F9; letter-spacing: 1px; text-transform: uppercase; display: flex; align-items: center; gap: 8px;}

/* Custom KPI Cards (Top Row) */
.kpi-card { background:#111827; border:1px solid #1F2937; border-radius:8px; padding:20px; text-align:center; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); height: 100%; }
.kpi-border-blue { border-top: 3px solid #38BDF8; }
.kpi-border-green { border-top: 3px solid #34D399; }
.kpi-border-purple { border-top: 3px solid #A78BFA; }
.kpi-border-orange { border-top: 3px solid #FB923C; }

.kpi-icon { font-size: 24px; margin-bottom: 10px; }
.kpi-value { font-size: 26px; font-weight:700; color:white; line-height:1.2; margin-bottom: 5px; }
.kpi-title { color:white; font-weight:600; font-size:14px; margin-bottom: 2px; }
.kpi-subtitle { color:#6B7280; font-size:11px; }

/* Database Overview Cards */
.db-card { background:#111827; border:1px solid #1F2937; border-radius:8px; padding:15px; text-align:center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
.db-title { font-size: 11px; color:#9CA3AF; margin-bottom: 8px; }
.db-value { font-size: 20px; font-weight: 700; color: white; margin-bottom: 4px; }
.db-subtitle { font-size: 10px; color:#6B7280; }

/* Transporter Summary Cards */
.transporter-card { background:#111827; border:1px solid #1F2937; border-radius:8px; padding:20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
.transporter-left { display: flex; flex-direction: column; }
.transporter-lbl { font-size: 11px; color: #9CA3AF; font-weight: 500; margin-bottom: 4px; }
.transporter-val { font-size: 20px; font-weight: 700; color: white;}
.transporter-icon { font-size: 22px; color: #6B7280; }
.val-purple { color: #A78BFA; }

/* Tables */
.custom-table { width:100%; color:#d1d5db; font-size:12px; border-collapse: collapse; }
.custom-table td { padding: 12px 10px; border-bottom: 1px solid #1F2937; }
.custom-table tr:last-child td { border-bottom: none; }
.custom-table td:nth-child(2) { text-align: right; font-weight: 700; color: white; }

/* Side Bar Nav System */
section[data-testid="stSidebar"] {
    background-color: #0b1119;
    border-right: 1px solid #1E293B;
}

/* Expander Customization */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    font-size: 14px !important;
    color: #e2e8f0 !important;
    background-color: #111827 !important;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; margin-top: 20px;">
        <h3 style="margin: 0; color: #F8FAFC; font-size: 16px; font-weight: 700;">CDX FreightIQ</h3>
        <div style="color: #64748B; font-size: 11px; margin-top: 2px;">Smart Logistics System</div>
    </div>
    <hr style='margin: 10px 0; border: 0; border-top: 1px solid #1E293B;'>
    """, unsafe_allow_html=True)
    st.caption("""
    <div style="font-size: 10px; color: #64748B; line-height: 1.5;">
    CDX FreightIQ v1.0 Powered by:<br>
    Python • Streamlit<br>
    SQLite • Gemini AI
    </div>
    """, unsafe_allow_html=True)

# ROW 1 — HEADER & EXECUTIVE KPI CARDS

head_col1, head_col2 = st.columns([8, 2])
with head_col1:
    st.markdown("<h1 style='margin-bottom:5px; font-size: 26px; color: white; font-weight: 700;'>📊 Logistics Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div style='color: #9CA3AF; font-size: 13px; margin-bottom: 25px;'>Real-time fleet, route and transporter intelligence</div>", unsafe_allow_html=True)
with head_col2:
    st.markdown('<div style="background:#022c16; color:#4ade80; padding:6px 12px; border-radius:5px; text-align:center; border:1px solid #14532d; font-weight:500; font-size:11px; float:right; margin-top:10px;">● Status: Connected</div>', unsafe_allow_html=True)

# Data Fetching
metrics = get_dashboard_metrics()
route_stats = route_statistics()
db_cov = get_database_coverage()

k1, k2, k3, k4 = st.columns(4)
cards_data = [
    (metrics["total_vehicles"], "Vehicles", "Available Fleet", "🚚", "kpi-border-blue"),
    (metrics["total_routes"], "Routes", "Across India", "🗺️", "kpi-border-green"),
    (metrics["total_transporters"], "Transporters", "Active Partners", "🏢", "kpi-border-purple"),
    (metrics["odc_vehicles"], "ODC Vehicles", "Heavy Lifters", "⚠️", "kpi-border-orange")
]
for col, data in zip([k1, k2, k3, k4], cards_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card {data[4]}">
            <div class="kpi-icon">{data[3]}</div>
            <div class="kpi-value">{data[0]}</div>
            <div class="kpi-title">{data[1]}</div>
            <div class="kpi-subtitle">{data[2]}</div>
        </div>
        """, unsafe_allow_html=True)

# ROW 2 — DATABASE OVERVIEW

st.markdown('<div class="section-title">🗄️ DATABASE OVERVIEW</div>', unsafe_allow_html=True)
o1, o2, o3 = st.columns(3)

network_metrics = [
    ("Origin Locations", f"{db_cov['unique_origins']}", "Mapped Source Hubs"),
    ("Unique Destinations", f"{db_cov['unique_destinations']}", "Delivery Checkpoints"),
    ("Total Routes", f"{metrics['total_routes']}", "Active Corridors")
]
for col, (title, val, subtitle) in zip([o1, o2, o3], network_metrics):
    with col:
        st.markdown(f"""
        <div class="db-card">
            <div class="db-title">{title}</div>
            <div class="db-value">{val}</div>
            <div class="db-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

# ROW 3 — TRANSPORTER SUMMARY

st.markdown('<div class="section-title">🤝 TRANSPORTER SUMMARY</div>', unsafe_allow_html=True)
t_data = get_transporter_counts()

p1, p2, p3 = st.columns(3)
with p1:
    st.markdown(f"""
    <div class="transporter-card">
        <div class="transporter-left">
            <div class="transporter-lbl">Mechanical Transporters</div>
            <div class="transporter-val">{t_data['Mechanical']} Vendors</div>
        </div>
        <div class="transporter-icon">⚙️</div>
    </div>
    """, unsafe_allow_html=True)
with p2:
    st.markdown(f"""
    <div class="transporter-card">
        <div class="transporter-left">
            <div class="transporter-lbl">Hydraulic Transporters</div>
            <div class="transporter-val">{t_data['Hydraulic']} Vendors</div>
        </div>
        <div class="transporter-icon">🏗️</div>
    </div>
    """, unsafe_allow_html=True)
with p3:
    st.markdown(f"""
    <div class="transporter-card">
        <div class="transporter-left">
            <div class="transporter-lbl">Total Empaneled Base</div>
            <div class="transporter-val val-purple">{metrics['total_transporters']} Active Groups</div>
        </div>
        <div class="transporter-icon">🏢</div>
    </div>
    """, unsafe_allow_html=True)

# ROW 4 & 5 — ROUTE ANALYSIS (EXPANDERS)
st.markdown('<div class="section-title">🛣️ Route Analysis</div>', unsafe_allow_html=True)
st.markdown('<hr style="border-top: 1px solid #1E293B; margin-top: 0; margin-bottom: 20px;">', unsafe_allow_html=True)

# 1. Top Origin Locations Expander
with st.expander("Top Origin Locations", expanded=False):
    st.markdown('<div style="font-size: 12px; color: #e2e8f0; margin-bottom: 10px;">Number of top origin locations:</div>', unsafe_allow_html=True)
    top_n = st.slider("Number of top origin locations:", min_value=1, max_value=15, value=5, step=1, label_visibility="collapsed")

    top_origins_data = get_top_route_origins(limit=top_n)
    if top_origins_data:
        df_top_origins = pd.DataFrame(top_origins_data)
        if len(df_top_origins.columns) >= 2:
            df_top_origins.columns = ["Origin", "Routes"]

        col_chart, col_table = st.columns([2, 1.2])
        
        with col_chart:
            st.markdown('<div style="font-size: 10px; color:#9CA3AF; margin-bottom:10px;">Source Node Volume Distribution Matrix</div>', unsafe_allow_html=True)
            st.bar_chart(data=df_top_origins, x="Origin", y="Routes", color="#7DD3FC", height=300)
            
        with col_table:
            st.markdown('<div style="font-size: 10px; color:#9CA3AF; margin-bottom:10px;">Tabular Data Output</div>', unsafe_allow_html=True)
            st.dataframe(df_top_origins, use_container_width=True, hide_index=True)

# 2. Route Search Expander
with st.expander("Route Search", expanded=False):

    st.markdown(
        '<div style="font-size:12px;color:#9CA3AF;margin-bottom:15px;">'
        'Search transportation corridors using origin and distance.'
        '</div>',
        unsafe_allow_html=True
    )

    origins = get_origin_list()
    origins.insert(0, "All Origins")

    c1, c2 = st.columns([1, 2])

    with c1:
        selected_origin = st.selectbox(
            "Origin",
            origins,
            help="You can type to search."
        )

    with c2:
        selected_range = st.slider(
            "Distance (KM)",
            min_value=int(route_stats["min_distance"]),
            max_value=int(route_stats["max_distance"]),
            value=(
                int(route_stats["min_distance"]),
                int(route_stats["max_distance"])
            )
        )

    origin_filter = None if selected_origin == "All Origins" else selected_origin

    routes = get_interactive_routes(
        min_km=selected_range[0],
        max_km=selected_range[1],
        origin_filter=origin_filter
    )

    st.markdown("---")

    if routes:

        df = pd.DataFrame(
            routes,
            columns=[
                "Origin",
                "Destination",
                "Distance (KM)",
                "Route Type",
                "Description",
                "Last Updated",
                "Approval No."
            ]
        )

        st.success(f"{len(df)} routes found")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No routes found.")

# ROW 6 — COMBINED FLEET & ODC OVERVIEW

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">🚛 Fleet & ODC Capability Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="db-card">
        <div class="db-title">Total Network Capacity</div>
        <div class="db-value">{metrics['total_capacity_mt']} MT</div>
        <div class="db-subtitle">(Combined General & ODC)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="db-card">
        <div class="db-title">Average Asset Capacity</div>
        <div class="db-value">{metrics['avg_capacity_mt']} MT</div>
        <div class="db-subtitle">Per Vehicle/Frame</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="db-card">
        <div class="db-title">Peak Payload Capacity</div>
        <div class="db-value" style="color: #34D399;">{metrics['highest_capacity_mt']} MT</div>
        <div class="db-subtitle">Max Single-Asset Rating</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="db-card">
        <div class="db-title">Active Asset Roster</div>
        <div class="db-value" style="color: #38BDF8;">{metrics['total_vehicles']} Units</div>
        <div class="db-subtitle">Across {metrics['vehicle_categories']} Specialized Types</div>
    </div>
    """, unsafe_allow_html=True)


# ROW 7 — ROUTE STATISTICS

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📍 Route Statistics</div>', unsafe_allow_html=True)

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(f"""
    <div style="font-size:12px; color:#9CA3AF; font-weight:600;">Longest Route</div>
    <div style="font-size:24px; color:white; font-weight:700;">{int(route_stats['max_distance'])} KM</div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown(f"""
    <div style="font-size:12px; color:#9CA3AF; font-weight:600;">Shortest Route</div>
    <div style="font-size:24px; color:white; font-weight:700;">{int(route_stats['min_distance'])} KM</div>
    """, unsafe_allow_html=True)
with r3:
    st.markdown(f"""
    <div style="font-size:12px; color:#9CA3AF; font-weight:600;">Average Route Distance</div>
    <div style="font-size:24px; color:white; font-weight:700;">{int(route_stats['avg_distance'])} KM</div>
    """, unsafe_allow_html=True)
