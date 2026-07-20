import streamlit as st
import pandas as pd

from database.data_lookup_db import (
    get_route,
    get_all_origins,
    get_destinations,
    get_all_transporters,
    get_transporter_details,
    get_all_vehicles,
    get_vehicle_details
)

# Importing the engine write operations provided
from ai.data_lookup_engine import (
    add_route,
    update_route,
    delete_route,
    add_vehicle,
    update_vehicle,
    delete_vehicle,
    add_transporter,
    update_transporter,
    delete_transporter
)

from ai.vehicle_engine import recommend_vehicle

# ===================================================
# PAGE CONFIG
# ===================================================
st.set_page_config(
    page_title="CDX Logistics Data Center",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================================
# PREMIUM ENTERPRISE STYLING & SIDEBAR UI OVERHAUL
# ===================================================
st.markdown(
    """
<style>
.block-container {
    padding-top: 1.5rem;
}

/* Minimalist Card & Metric layouts */
.profile-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
}

.kpi-container {
    display: flex;
    gap: 12px;
    margin-bottom: 15px;
}

.kpi-box {
    flex: 1;
    background: #1f2937;
    border: 1px solid #374151;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
}

.kpi-label {
    font-size: 0.75rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}

.kpi-value {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f3f4f6;
}

/* Subtle Left-Border Snackbars */
.status-card-green {
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 4px solid #10b981;
    padding: 12px 16px;
    border-radius: 6px;
    color: #10b981;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 15px;
}

.status-card-yellow {
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 4px solid #f59e0b;
    padding: 12px 16px;
    border-radius: 6px;
    color: #f59e0b;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 15px;
}

.status-card-blue {
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 4px solid #3b82f6;
    padding: 12px 16px;
    border-radius: 6px;
    color: #3b82f6;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

/* Timeline data fresh badge */
.timeline-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    margin-right: 6px;
}

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

/* Animate & Anchor Highlight Current Active Page */
section[data-testid="stSidebar"] [aria-current="page"] {
    background: #1E293B !important;
    border: 1px solid #1E293B !important;
    border-left: 4px solid #38BDF8 !important;
    padding-left: 10px !important;
    font-weight: 600;
    color: #F8FAFC !important;
}
</style>
""",
    unsafe_allow_html=True
)

# ==================================================
# SIDEBAR CUSTOM COMPONENT BUILDER
# ==================================================
with st.sidebar:
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
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #1E293B;'>", unsafe_allow_html=True)
    st.caption("""
    **CDX FreightIQ v1.0** Powered by:  
    Python • Streamlit  
    SQLite • Gemini AI
    """)

# SVG Icons
SVG_MAP = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" y1="3" x2="9" y2="18"></line><line x1="15" y1="6" x2="15" y2="21"></line></svg>'
SVG_TRUCK = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>'
SVG_BOX = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>'

# ===================================================
# HEADER
# ===================================================
st.title("Operational Data Explorer")
st.caption(
    """
    Enterprise Logistics Intelligence Dashboard | Lookup route distances, transporter records,
    vehicle specifications and shipment fitment directly from the logistics master database.
    """
)
st.divider()

# ===================================================
# TABS
# ===================================================
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Routes",
        "Transporters",
        "Vehicles",
        "Shipment Fitment"
    ]
)

# ===================================================
# ROUTE LOOKUP & MANAGEMENT
# ===================================================
with tab1:
    st.markdown(f"### {SVG_MAP} Route Distance & Matrix Lookup", unsafe_allow_html=True)
    
    raw_origins = get_all_origins()
    origins = [""] + list(raw_origins) if raw_origins else [""]
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        origin = st.selectbox(
            "Origin", 
            origins, 
            key="origin_lookup",
            help="Leave blank to view all starting origins for a chosen destination."
        )
        
        if origin:
            raw_destinations = get_destinations(origin)
            destinations = [""] + list(raw_destinations) if raw_destinations else [""]
        else:
            all_dest_set = set()
            for orig in raw_origins:
                dests = get_destinations(orig)
                if dests:
                    all_dest_set.update(dests)
            destinations = [""] + sorted(list(all_dest_set))
            
        destination = st.selectbox(
            "Destination", 
            destinations, 
            key="destination_lookup",
            help="Leave blank to view all possible destinations from your chosen origin."
        )
        
        search_clicked = st.button("Query Route System", use_container_width=True, type="primary")
        
    with col2:
        if search_clicked:
            if origin and destination:
                route_raw = get_route(origin, destination)
                if route_raw:
                    route = dict(route_raw)
                    st.markdown('<div class="status-card-green">✓ Point-to-Point Route Record Retrieved</div>', unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div class="profile-card">
                            <div style="font-size: 0.85rem; color:#9ca3af; margin-bottom: 2px;">TOTAL DISTANCE</div>
                            <div style="font-size: 2.5rem; font-weight:800; color:#10b981; line-height:1;">{route.get('distance_km', 'N/A')} <span style="font-size:1.25rem;">KM</span></div>
                            <div style="margin-top: 15px; font-size:0.85rem; color:#e5e7eb;">
                                <span class="timeline-dot"></span>Data Freshness Line: Validated System Record
                            </div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("State Approval Status", route.get("state") if route.get("state") else "N/A")
                    with c2:
                        st.metric("Audit Timestamp", str(route.get("updated_on", "N/A")))
                        
                    with st.expander("Database Payload Object"):
                        st.dataframe(pd.DataFrame([route]), use_container_width=True, hide_index=True)
                else:
                    st.markdown('<div class="status-card-yellow">⚠ No matching route path found in master ledger.</div>', unsafe_allow_html=True)
            
            elif origin and not destination:
                st.markdown(f'<div class="status-card-blue">ℹ Showing all outward destination paths from <strong>{origin}</strong></div>', unsafe_allow_html=True)
                
                connected_destinations = get_destinations(origin)
                if connected_destinations:
                    matrix_data = []
                    for dest in connected_destinations:
                        r_details = get_route(origin, dest)
                        if r_details:
                            r_dict = dict(r_details)
                            matrix_data.append({
                                "Destination Node": dest,
                                "Distance": f"{r_dict.get('distance_km', 'N/A')} KM",
                                "State Link": r_dict.get('state') if r_dict.get('state') else "N/A",
                                "Last Updated": str(r_dict.get('updated_on', 'N/A'))
                            })
                    
                    df_matrix = pd.DataFrame(matrix_data)
                    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
                else:
                    st.caption("No downstream destinations registered for this node.")

            elif destination and not origin:
                st.markdown(f'<div class="status-card-blue">ℹ Reverse Mapping: Showing all inbound origins feeding to <strong>{destination}</strong></div>', unsafe_allow_html=True)
                
                reverse_matrix = []
                for orig in raw_origins:
                    dests_for_orig = get_destinations(orig)
                    if dests_for_orig and destination in dests_for_orig:
                        r_details = get_route(orig, destination)
                        if r_details:
                            r_dict = dict(r_details)
                            reverse_matrix.append({
                                "Origin Node Source": orig,
                                "Distance Link": f"{r_dict.get('distance_km', 'N/A')} KM",
                                "State Corridor": r_dict.get('state') if r_dict.get('state') else "N/A",
                                "System Record Date": str(r_dict.get('updated_on', 'N/A'))
                            })
                
                if reverse_matrix:
                    df_rev_matrix = pd.DataFrame(reverse_matrix)
                    st.dataframe(df_rev_matrix, use_container_width=True, hide_index=True)
                else:
                    st.caption("No inbound origin supply paths registered for this node target.")
                    
            else:
                st.markdown('<div class="status-card-yellow">⚠ Please select at least an Origin or a Destination parameter to fetch metrics.</div>', unsafe_allow_html=True)

    # WRITE OPERATIONS
    st.markdown("<br><hr style='border-top: 1px dashed #1E293B;'><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Route Data Mutation Services")
    
    rt_col1, rt_col2 = st.columns(2)
    with rt_col1:
        with st.expander("➕ Add / Update Route Record"):
            with st.form("add_update_route_form"):
                ro = st.text_input("Origin")
                rd = st.text_input("Destination")
                dist = st.number_input("Distance (KM)", min_value=0.0, step=0.1)
                action_mode = st.radio("Mutation Intent", ["Add New Node Mapping", "Update Existing Metric"])
                
                if st.form_submit_button("Commit Route Change", use_container_width=True, type="primary"):
                    if ro and rd:
                        if action_mode == "Add New Node Mapping":
                            res = add_route(ro, rd, dist)
                        else:
                            res = update_route(ro, rd, dist)
                        
                        if res.get("success"):
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message"))
                    else:
                        st.warning("Please specify both valid Origin and Destination arguments.")
                        
    with rt_col2:
        with st.expander("❌ Delete Route Record"):
            with st.form("delete_route_form"):
                del_ro = st.text_input("Target Origin")
                del_rd = st.text_input("Target Destination")
                
                if st.form_submit_button("Execute Route Purge", use_container_width=True):
                    if del_ro and del_rd:
                        res = delete_route(del_ro, del_rd)
                        if res.get("success"):
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message"))
                    else:
                        st.warning("Both parameters are string-mandatory descriptors to match rows.")

# ===================================================
# TRANSPORTER LOOKUP & MANAGEMENT
# ===================================================
with tab2:
    st.markdown(f"### {SVG_TRUCK} Transporter Profile Directory", unsafe_allow_html=True)
    
    transporters = get_all_transporters()
    transporter = st.selectbox("Transporter Name", transporters)
    
    if transporter:
        details_raw = get_transporter_details(transporter)
        
        if details_raw:
            details = dict(details_raw)
            st.markdown(
                f"""
                <div class="status-card-blue" style="text-align: right;">
                    <strong>IBA Ledger Standing:</strong> Valid Until {details.get('IBA Validity', 'N/A')}
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-box">
                        <div class="kpi-label">Operation Category</div>
                        <div class="kpi-value" style="color: #3b82f6;">{details.get('Category', 'N/A')}</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">MSME Framework Status</div>
                        <div class="kpi-value">{details.get('MSME Status', 'N/A')}</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">IBA Registration Code</div>
                        <div class="kpi-value" style="font-family: monospace; letter-spacing: 1px;">{details.get('IBA Code', 'N/A')}</div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            with st.expander("Database Payload Object"):
                st.dataframe(pd.DataFrame([details]), use_container_width=True, hide_index=True)

    # WRITE OPERATIONS
    st.markdown("<br><hr style='border-top: 1px dashed #1E293B;'><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Transporter Data Mutation Services")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        with st.expander("➕ Add / Update Transporter Profile"):
            with st.form("add_update_transporter_form"):
                t_name = st.text_input("Transporter Legal Entity Designation")
                t_cat = st.text_input("Operation Category Strategy")
                t_msme = st.text_input("MSME Status Rating")
                t_iba = st.text_input("IBA Identity Registration Code")
                t_val = st.text_input("IBA Validity Date Window")
                t_mode = st.radio("Mutation Intent", ["Register New Fleet Vendor", "Update Profile Parameters"], key="t_mode")
                
                if st.form_submit_button("Commit Transporter Ledger Record", use_container_width=True, type="primary"):
                    if t_name:
                        if t_mode == "Register New Fleet Vendor":
                            res = add_transporter(t_name, t_cat, t_msme, t_iba, t_val)
                        else:
                            res = update_transporter(t_name, t_cat, t_msme, t_iba, t_val)
                            
                        if res.get("success"):
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message"))
                    else:
                        st.warning("The primary unique account name cannot be null.")
                        
    with t_col2:
        with st.expander("❌ Delete Transporter File"):
            with st.form("delete_transporter_form"):
                del_t_name = st.text_input("Target Transporter Name String")
                
                if st.form_submit_button("Purge Transporter Record", use_container_width=True):
                    if del_t_name:
                        res = delete_transporter(del_t_name)
                        if res.get("success"):
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message"))
                    else:
                        st.warning("Please supply a valid key variable to evaluate drops.")

# ===================================================
# VEHICLE LOOKUP & MANAGEMENT
# ===================================================
with tab3:
    st.markdown(f"### {SVG_TRUCK} Fleet Vehicle Specifications", unsafe_allow_html=True)
    
    vehicles = get_all_vehicles()
    vehicle = st.selectbox("Select Target Vehicle Classification", vehicles)
    
    if vehicle:
        details_raw = get_vehicle_details(vehicle)
        
        if details_raw:
            details = dict(details_raw)
            is_odc_allowed = str(details.get("ODC_Allowed", "No")).strip().lower() == "yes"
            odc_display_color = "#10b981" if is_odc_allowed else "#ef4444"
            
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-box">
                        <div class="kpi-label">Class Category</div>
                        <div class="kpi-value">{details.get('Category', 'N/A')}</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">Axles Layout</div>
                        <div class="kpi-value">{details.get('Axles', 'N/A')}</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">Max Capacity Payload</div>
                        <div class="kpi-value">{details.get('Max_Weight_MT', 'N/A')} MT</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">ODC Authorization</div>
                        <div class="kpi-value" style="color: {odc_display_color};">{details.get('ODC_Allowed', 'No')}</div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            capacity = pd.DataFrame({
                "Dimensional Vector Parameter": ["Clearance Length", "Structural Width", "Maximum Height Limit"],
                "Engineered Fleet Value Capacity": [f"{details.get('Length_mm', 0)} mm", f"{details.get('Width_mm', 0)} mm", f"{details.get('Height_mm', 0)} mm"]
            })
            
            st.dataframe(capacity, use_container_width=True, hide_index=True)
            
            with st.expander("Database Payload Object"):
                st.dataframe(pd.DataFrame([details]), use_container_width=True, hide_index=True)

    # WRITE OPERATIONS
    st.markdown("<br><hr style='border-top: 1px dashed #1E293B;'><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Vehicle Data Mutation Services")
    
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        with st.expander("➕ Add / Update Vehicle Profile Blueprint"):
            with st.form("add_update_vehicle_form"):
                v_name = st.text_input("Vehicle Variant Model Identifier")
                v_cat = st.text_input("Chassis Footprint Class Category")
                v_weight = st.number_input("Max Weight Allowance Limit (MT)", min_value=0.0, step=0.1)
                v_axles = st.number_input("Axle Hub Deployment Count Layout", min_value=0, step=1)
                v_odc = st.text_input("ODC Authorization Status Clearance Flag", placeholder="Yes / No")
                v_mode = st.radio("Mutation Intent", ["Deploy New Fleet Asset Class", "Update Blueprint Metrics"], key="v_mode")
                
                if st.form_submit_button("Commit Specification Blueprint", use_container_width=True, type="primary"):
                    if v_name:
                        if v_mode == "Deploy New Fleet Asset Class":
                            res = add_vehicle(v_name, v_cat, v_weight, v_axles, v_odc)
                        else:
                            res = update_vehicle(v_name, v_cat, v_weight, v_axles, v_odc)
                            
                        if res.get("success"):
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message"))
                    else:
                        st.warning("The primary index vehicle model designator string cannot be empty.")
                        
    with v_col2:
        with st.expander("❌ Delete Vehicle Specification Blueprint"):
            with st.form("delete_vehicle_form"):
                del_v_name = st.text_input("Target Model Class Identifier")
                
                if st.form_submit_button("Purge Specification Asset", use_container_width=True):
                    if del_v_name:
                        res = delete_vehicle(del_v_name)
                        if res.get("success"):
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message"))
                    else:
                        st.warning("Please supply a valid row variable model identifier to match lines.")

# ===================================================
# SHIPMENT FITMENT
# ===================================================
with tab4:
    st.markdown(f"### {SVG_BOX} Shipment Volumetric Fitment Engine", unsafe_allow_html=True)
    
    col_inputs, col_results = st.columns([1, 1.2])
    
    with col_inputs:
        weight = st.number_input("Cargo Weight (MT)", min_value=0.0, value=25.0)
        length = st.number_input("Max Length Dimension (mm)", min_value=0, value=8000)
        width = st.number_input("Max Width Dimension (mm)", min_value=0, value=2400)
        height = st.number_input("Max Height Dimension (mm)", min_value=0, value=3000)
        fitment_clicked = st.button("Evaluate Allocation Suitability", use_container_width=True, type="primary")
        
    with col_results:
        if fitment_clicked:
            result = recommend_vehicle(weight, length, width, height)
            
            if "error" in result:
                st.markdown(f'<div class="status-card-yellow">⚠ Out-Of-Gauge Exception: {result["error"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-card-green">✓ Optimum Fleet Allocation Target Assigned</div>', unsafe_allow_html=True)
                
                st.metric("Primary Recommended Unit Target", result['vehicle'])
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Fleet Category", result["category"])
                with c2:
                    st.metric("Axles Configuration", result["axles"])
                with c3:
                    st.metric("Max Payload Ceiling", f"{result['max_weight']} MT")
                
                comparison = pd.DataFrame({
                    "Dimensional / Mass Constraint Matrix": ["Payload Weight", "Total Length Bounds", "Total Width Bounds", "Total Height Bounds"],
                    "Input Shipment Demand": [f"{weight} MT", f"{length} mm", f"{width} mm", f"{height} mm"],
                    "Assigned Vessel Capacity Threshold": [f"{result['max_weight']} MT", f"{result['length_capacity']} mm", f"{result['width_capacity']} mm", f"{result['height_capacity']} mm"]
                })
                st.dataframe(comparison, use_container_width=True, hide_index=True)
                
                if result["odc_required"]:
                    st.markdown(
                        """
                        <div class="status-card-yellow">
                            <strong>⚠ ODC REGULATORY PERMIT REQUIRED</strong><br/>
                            This envelope deployment variant footprint exceeds international standard dimensions. Special permit mandatory.
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div class="status-card-green">
                            <strong>✓ STANDARD ROUTING ROUTE OPERATIONS CLEARED</strong><br/>
                            Shipment envelope sits correctly within standard bounds. Normal transit protocols apply.
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                if result.get("alternative_vehicle"):
                    st.markdown(
                        f"""
                        <div class="profile-card" style="border-left: 4px solid #3b82f6;">
                            <div style="font-size:0.75rem; color:#9ca3af; font-weight:bold;">HYDRAULIC REDUNDANCY STRATEGY BACKUP AVAILABLE</div>
                            <div style="font-size:1.1rem; font-weight:700; margin-top:4px; color:#f3f4f6;">{result['alternative_vehicle']}</div>
                            <div style="font-size:0.85rem; color:#9ca3af;">Category: {result.get('alternative_category', 'N/A')}</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
