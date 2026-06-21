import streamlit as st
import pandas as pd

from ai.analytics import (
    get_dashboard_metrics,
    route_statistics,
    get_transporter_counts,
    get_database_coverage,
    get_top_route_origins,
    get_interactive_routes
)

# ==================================================
# PAGE CONFIG & PREMIUM CORPORATE CSS
# ==================================================
st.set_page_config(
    page_title="Logistics Operations Dashboard",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
.block-container { padding-top:1.5rem; }
.card { background:#111827; border:1px solid #1F2937; border-radius:12px; padding:20px; height:100%; }
.metric-card { background:#111827; border:1px solid #1F2937; border-radius:12px; padding:22px; text-align:center; }
.metric-value { font-size:34px; font-weight:700; color:white; line-height:1.1; }
.metric-text-label { color:white; font-weight:600; font-size:16px; margin:6px 0 2px 0; }
.metric-label { color:#9CA3AF; font-size:13px; }
.section-title { font-size:18px; font-weight:600; margin-top:25px; margin-bottom:15px; color:#F1F5F9; letter-spacing:-0.2px; border-left:3px solid #0284C7; padding-left:10px; }
.ai-status-card { background:#111827; border:1px solid #1F2937; padding:16px; border-radius:10px; text-align:center; }
.mini-overview-card { background:#111827; border:1px solid #1F2937; padding:15px; border-radius:10px; text-align:center; }
.interactive-container { background:#111827; padding:20px; border-radius:12px; margin-bottom:20px; border:1px solid #1F2937; }

/* ==================================================
   ADVANCED SIDEBAR INTERACTIVE STYLING
   ================================================== */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
}

/* Native Multi-page Link Items styling */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    border-radius: 8px;
    margin-bottom: 6px;
    padding: 8px 12px;
    border: 1px solid transparent;
    transition: all 0.25s ease-in-out;
}

/* Premium Hover Glow & Subtle Right Slide */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background: linear-gradient(90deg, rgba(2, 132, 199, 0.2), rgba(2, 132, 199, 0.02)) !important;
    border-left: 3px solid #38BDF8 !important;
    border-top: 1px solid #1E293B;
    border-right: 1px solid #1E293B;
    border-bottom: 1px solid #1E293B;
    transform: translateX(4px);
    color: #F8FAFC !important;
}

/* Animate & Anchor Highlight Current Active Page (Targeting Logistics Dashboard) */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:nth-child(2) a {
    background: #1E293B !important;
    border: 1px solid #1E293B !important;
    border-left: 4px solid #38BDF8 !important;
    padding-left: 10px !important;
    font-weight: 600;
    color: #F8FAFC !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR CUSTOM COMPONENT BUILDER
# ==================================================
with st.sidebar:
    # Sidebar Premium Header Block
    st.markdown("""
    <div style="
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0; color: #F8FAFC; font-size: 20px; font-weight: 700; letter-spacing: -0.3px;">CDX FreightIQ</h3>
        <div style="color: #64748B; font-size: 12px; margin-top: 2px; font-weight: 500;">Logistics Planning Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple semantic rule line wrapper separating nav options from platform status footer
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #1E293B;'>", unsafe_allow_html=True)
    st.caption("""
    **CDX FreightIQ v1.0** Powered by:  
    Python • Streamlit  
    SQLite • Gemini AI
    """)

# ==================================================
# ROW 1 — HEADER
# ==================================================
left, right = st.columns([8, 2])
with left:
    st.markdown("<h1 style='margin-bottom:0;'>Logistics Operations Dashboard</h1>", unsafe_allow_html=True)
    st.caption("Enterprise Logistics Intelligence Platform")
with right:
    st.markdown('<div style="background:#052E16; color:#86EFAC; padding:10px; border-radius:8px; text-align:center; border:1px solid #14532D; font-weight:600; margin-top:15px; font-size:13px;">● Status: Connected</div>', unsafe_allow_html=True)

st.divider()

# Core Data Ingestion
metrics = get_dashboard_metrics()
route_stats = route_statistics()
db_cov = get_database_coverage()

# ==================================================
# ROW 2 — EXECUTIVE KPI CARDS
# ==================================================
k1, k2, k3, k4 = st.columns(4)
cards_data = [
    (metrics["total_vehicles"], "Vehicles Managed", "Total Fleet Inventory"),
    (metrics["total_routes"], "Approved Corridors", "Active Segment Count"),
    (metrics["total_transporters"], "Logistics Partners", "Empaneled Transporters"),
    (metrics["odc_vehicles"], "ODC Heavy Lift Ready", "Specialized Fleet Frame Size")
]
for col, data in zip([k1, k2, k3, k4], cards_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data[0]}</div>
            <div class="metric-text-label">{data[1]}</div>
            <div class="metric-label">{data[2]}</div>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# ROW 3 — LOGISTICS DATABASE COVERAGE
# ==================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Logistics Database Coverage Analytics</div>', unsafe_allow_html=True)
o1, o2, o3, o4 = st.columns(4)

network_metrics = [
    ("Unique Origins Mapping", f"{db_cov['unique_origins']}", "Hub Source Gateways"),
    ("Unique Destinations", f"{db_cov['unique_destinations']}", "Active Delivery Points"),
    ("Total Network Paths", f"{metrics['total_routes']}", "Verified Segments Checked"),
    ("Distance Matrix Limits", f"{int(route_stats['min_distance'])} KM – {int(route_stats['max_distance'])} KM", "Network Bounds")
]
for col, (title, val, subtitle) in zip([o1, o2, o3, o4], network_metrics):
    with col:
        st.markdown(f"""
        <div class="mini-overview-card">
            <div class="metric-label" style="font-weight:600; color:#9CA3AF;">{title}</div>
            <div style="font-size:20px; font-weight:700; color:white; margin:6px 0;">{val}</div>
            <div style="font-size:11px; color:#6B7280;">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

# Transporter Ecosystem Allocation
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Logistics Partner Ecosystem Allocation Volumes</div>', unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
t_data = get_transporter_counts()

with p1:
    st.metric(label="Mechanical Transporters", value=f"{t_data.get('Mechanical', 0)} Vendors")
with p2:
    st.metric(label="Hydraulic Transporters", value=f"{t_data.get('Hydraulic', 0)} Vendors")
with p3:
    st.metric(label="Total Empaneled Base", value=f"{metrics['total_transporters']} Active Groups")

# ==================================================
# ROW 4 — INTERACTIVE SUPPLY CHAIN ANALYSIS OPTIONS
# ==================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Interactive Supply Chain Analysis Options</div>', unsafe_allow_html=True)

# Supply Chain Source Node Panel
st.markdown('<div class="interactive-container">', unsafe_allow_html=True)
st.markdown("##### 🏭 Supply Chain Source Node Range")

top_n = st.slider("Select maximum top active nodes to view:", min_value=0, max_value=15, value=0, step=1)

if top_n > 0:
    top_origins_df = pd.DataFrame(get_top_route_origins(limit=top_n))
    st.dataframe(top_origins_df, use_container_width=True, hide_index=True)
else:
    st.info("💡 Adjust the range slider above zero to compile node source frequencies.")
st.markdown('</div>', unsafe_allow_html=True)

# UPGRADED SECTION — NEW ROUTE FILTERS AND RANGE DISCOVERY COCKPIT
st.markdown('<div class="interactive-container">', unsafe_allow_html=True)
st.markdown("##### 🛣️ Interactive Route & Distance Discovery Cockpit")

ctrl1, ctrl2 = st.columns([2, 1])

with ctrl1:
    min_db_dist = int(route_stats['min_distance'])
    max_db_dist = int(route_stats['max_distance'])
    
    selected_range = st.slider(
        "Isolate custom corridor distance limits (KM):",
        min_value=min_db_dist,
        max_value=max_db_dist,
        value=(min_db_dist, min_db_dist),
        step=50
    )

with ctrl2:
    search_hub = st.text_input("Filter by Origin Node (e.g., AGRA, MUMBAI):", value="").strip().upper()

# Conditional Rendering: Only query backend if sliders shift
if selected_range[1] > min_db_dist:
    interactive_routes = get_interactive_routes(
        min_km=selected_range[0],
        max_km=selected_range[1],
        origin_filter=search_hub if search_hub else None
    )
    
    if interactive_routes:
        df_inter = pd.DataFrame(interactive_routes)
        df_inter.columns = ["Origin Node", "Destination Node", "Distance (KM)", "State Coverage", "Route Description", "Last Updated", "Regulatory Approval No."]
        st.dataframe(df_inter, use_container_width=True, hide_index=True)
    else:
        st.caption("No registered corridors match the requested tier profile scope constraints.")
else:
    st.info("💡 Adjust the distance slider parameters above to start crawling the spatial route grid map.")
st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# ROW 5 — FLEET CAPACITY SUMMARY
# ==================================================
st.markdown("<br>", unsafe_allow_html=True)
cap_left, odc_right = st.columns(2)

with cap_left:
    st.markdown('<div class="section-title">Total Fleet Capacity Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        <table style="width:100%; color:white; font-size:15px; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #1F2937;"><td style="padding:12px 0; color:#9CA3AF;">Total Network Uplift Capacity</td><td style="text-align:right; font-weight:700;">{metrics['total_capacity_mt']} MT</td></tr>
            <tr style="border-bottom: 1px solid #1F2937;"><td style="padding:12px 0; color:#9CA3AF;">Average Capacity Per Asset</td><td style="text-align:right; font-weight:700;">{metrics['avg_capacity_mt']} MT</td></tr>
            <tr style="border-bottom: 1px solid #1F2937;"><td style="padding:12px 0; color:#9CA3AF;">Active Asset Registrations</td><td style="text-align:right; font-weight:700;">{metrics['total_vehicles']} Units</td></tr>
            <tr><td style="padding:12px 0; color:#9CA3AF;">Unique Category Classifications</td><td style="text-align:right; font-weight:700; color:#3B82F6;">{metrics['vehicle_categories']} Types</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with odc_right:
    st.markdown('<div class="section-title">Heavy-Lift ODC Capability Analytics</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        <table style="width:100%; color:white; font-size:15px; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #1F2937;"><td style="padding:12px 0; color:#9CA3AF;">Dedicated ODC Capacity Pool</td><td style="text-align:right; font-weight:700;">{metrics['total_odc_capacity_mt']} MT</td></tr>
            <tr style="border-bottom: 1px solid #1F2937;"><td style="padding:12px 0; color:#9CA3AF;">Average ODC Capacity</td><td style="text-align:right; font-weight:700;">{metrics['avg_odc_capacity_mt']} MT</td></tr>
            <tr style="border-bottom: 1px solid #1F2937;"><td style="padding:12px 0; color:#9CA3AF;">Peak Structural Payload Allowance</td><td style="text-align:right; font-weight:700;">{metrics['highest_capacity_mt']} MT</td></tr>
            <tr><td style="padding:12px 0; color:#9CA3AF;">Specialized Heavy Duty ODC Frames</td><td style="text-align:right; font-weight:700;">{metrics['odc_vehicles']} Frames</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# ROW 6 — AI ENGINE STATUS INTELLIGENCE
# ==================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">AI Engine Status Intelligence</div>', unsafe_allow_html=True)
ai1, ai2, ai3, ai4, ai5 = st.columns(5)
ai_features = [
    "Vehicle Recommendation Engine", "Dynamic Packaging Planner", 
    "Multi-Modal Route Optimization", "Spatial Distance Intelligence", 
    "Transporter Capability Matching"
]
for col, feature in zip([ai1, ai2, ai3, ai4, ai5], ai_features):
    with col:
        st.markdown(f"""
        <div class="ai-status-card">
            <div style="color:white; font-size:13px; font-weight:500; margin-bottom:6px;">{feature}</div>
            <div style="color:#34D399; font-size:12px; font-weight:600;">● Engine Operational</div>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# ROW 7 — CALCULATED BASELINE VALUES
# ==================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Calculated Network Baseline Values</div>', unsafe_allow_html=True)
r1, r2, r3 = st.columns(3)
with r1:
    st.metric(label="Longest Mapped Route Segment", value=f"{int(route_stats['max_distance'])} KM")
with r2:
    st.metric(label="Shortest Mapped Route Segment", value=f"{int(route_stats['min_distance'])} KM")
with r3:
    st.metric(label="Calculated Mean Segment Distance", value=f"{int(route_stats['avg_distance'])} KM")