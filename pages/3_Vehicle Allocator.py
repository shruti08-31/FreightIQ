import streamlit as st
import pandas as pd
from ai.vehicle_engine import (
    consolidate_shipments, 
    evaluate_single_shipment_addition, 
    generate_comprehensive_load_profile,
    ai_optimize_load_plan
)

# 1. PAGE SETUP 
st.set_page_config(
    page_title="FreightIQ | Multi-Shipment Optimizer",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark UI Premium styling overrides
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; }
.matrix-card {
    padding: 1.5rem;
    border-radius: 10px;
    background: #0f172a;
    border: 1px solid #1e293b;
    margin-bottom: 1.25rem;
}
.upgrade-card {
    padding: 1.5rem;
    border-radius: 10px;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid #f59e0b;
    margin-bottom: 1.25rem;
}
.metric-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 5px;
    background: #1e293b;
    color: #38bdf8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.manifest-header-alert {
    background-color: rgba(2, 132, 199, 0.15);
    border-left: 4px solid #38BDF8;
    padding: 12px 16px;
    border-radius: 4px;
    color: #38BDF8;
    font-weight: 500;
    font-size: 14px;
    margin-bottom: 1rem;
}
section[data-testid="stSidebar"] {
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 2. APP STATE MEMORY ENGINE (session_state)
# ==================================================
if "staged_shipments" not in st.session_state:
    st.session_state.staged_shipments = []
if "last_calculation_results" not in st.session_state:
    st.session_state.last_calculation_results = None
if "interstitial_rejection" not in st.session_state:
    st.session_state.interstitial_rejection = None
if "upgrade_approved" not in st.session_state:
    st.session_state.upgrade_approved = True

# ==================================================
# 3. SIDEBAR BRANDING COMPONENT
# ==================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0; border-bottom: 1px solid #1E293B; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #F8FAFC; font-size: 20px; font-weight: 700; letter-spacing: -0.3px;">CDX FreightIQ</h3>
        <div style="color: #64748B; font-size: 12px; margin-top: 2px; font-weight: 500;">Vehicle Recommendation System</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #1E293B;'>", unsafe_allow_html=True)
    st.caption("Current Session: **Multi Shipment Planning**")

# ==================================================
# 4. SHEET WORKSPACE HEADERS
# ==================================================
st.title("Smart Vehicle Recommendation System")
st.caption("Add multiple shipments and find the best vehicle with load utilization.")
st.divider()

# Core Layout Partitioning
input_column, workspace_column = st.columns([1.1, 1.4], gap="large")

# ==================================================
# 5. INPUT REGISTRATION CONSOLE (LEFT PANEL)
# ==================================================
with input_column:
    st.subheader("Add Shipment")
    
    assigned_next_id = f"S{len(st.session_state.staged_shipments) + 1}"
    st.text_input("Shipment ID", value=assigned_next_id, disabled=True)
    
    w_input = st.number_input("Weight (MT)", min_value=0.01, value=12.0, step=0.5, format="%.2f")
    
    col_l, col_w, col_h = st.columns(3)
    with col_l:
        l_input = st.number_input("Length (mm)", min_value=1, value=4000, step=100)
    with col_w:
        w_dim_input = st.number_input("Width (mm)", min_value=1, value=2200, step=50)
    with col_h:
        h_input = st.number_input("Height (mm)", min_value=1, value=1800, step=50)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # HANDLING REJECTION DIALOG INTERSTITIAL
    if st.session_state.interstitial_rejection:
        fail_data = st.session_state.interstitial_rejection
        st.error(f"{fail_data['id']} cannot be accommodated.")
        
        st.markdown("**Reasons:**")
        for r in fail_data["reasons"]:
            st.markdown(f"• {r}")
            
        if "remaining_capacity" in fail_data and fail_data["remaining_capacity"]:
            st.markdown(f"**Remaining Capacity:** {fail_data['remaining_capacity']}")
        st.markdown(f"*AI Suggestion: {fail_data['suggestion']}*")
        
        st.markdown("Would you like to:")
        choice_col1, choice_col2 = st.columns(2)
        with choice_col1:
            if st.button("Add Another Shipment", use_container_width=True):
                st.session_state.interstitial_rejection = None
                st.rerun()
        with choice_col2:
            if st.button("Generate Final Plan", type="primary", use_container_width=True):
                st.session_state.interstitial_rejection = None
                st.rerun()
                
    else:
        # Item Insertion Gate Trigger
        if st.button("Add Shipment", type="primary", use_container_width=True, key="add_shipment_main_btn"):
            new_shipment_entry = {
                "id": assigned_next_id,
                "weight": w_input,
                "length": l_input,
                "width": w_dim_input,
                "height": h_input
            }
            
            if st.session_state.last_calculation_results and "error" not in st.session_state.last_calculation_results:
                validation_check = evaluate_single_shipment_addition(st.session_state.last_calculation_results, new_shipment_entry)
                if validation_check.get("status") == "cannot_fit":
                    st.session_state.interstitial_rejection = {
                        "id": assigned_next_id,
                        "reasons": validation_check["reasons"],
                        "suggestion": validation_check["suggestion"],
                        "remaining_capacity": validation_check.get("remaining_capacity", "N/A")
                    }
                    st.rerun()

            st.session_state.staged_shipments.append(new_shipment_entry)
            st.session_state.last_calculation_results = consolidate_shipments(st.session_state.staged_shipments)
            st.rerun()

    # Optimization Trigger Hook
    if st.button("Optimize Load", use_container_width=True):
        if st.session_state.staged_shipments:
            st.session_state.last_calculation_results = ai_optimize_load_plan(st.session_state.staged_shipments)
            st.rerun()

    st.markdown("---")
    st.subheader("Active Staging Registry Queue")
    
    if st.session_state.staged_shipments:
        for index_pos, single_item in enumerate(st.session_state.staged_shipments):
            row_c1, row_c2 = st.columns([5, 1])
            with row_c1:
                st.markdown(f"**{single_item['id']}** &nbsp;|&nbsp; Weight: `{single_item['weight']} MT` &nbsp;|&nbsp; Dimensions: `{single_item['length']}x{single_item['width']}x{single_item['height']} mm`")
            with row_c2:
                if st.button("Remove", key=f"remove_manifest_node_{single_item['id']}_{index_pos}"):
                    st.session_state.staged_shipments.pop(index_pos)
                    if st.session_state.staged_shipments:
                        st.session_state.last_calculation_results = consolidate_shipments(st.session_state.staged_shipments)
                    else:
                        st.session_state.last_calculation_results = None
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear All Shipments", use_container_width=True, type="secondary"):
            st.session_state.staged_shipments = []
            st.session_state.last_calculation_results = None
            st.session_state.interstitial_rejection = None
            st.session_state.upgrade_approved = True
            st.rerun()
    else:
        st.info("No shipments are currently staged for configuration analysis.")

# ==================================================
# 6. ANALYTICS & VISUAL CAPACITY METERS (RIGHT PANEL)
# ==================================================
with workspace_column:
    st.subheader("Vehicle Recommendation")
    
    if st.session_state.last_calculation_results:
        raw_payload = st.session_state.last_calculation_results
        
        if "error" in raw_payload:
            st.error(raw_payload["error"])
        else:
            ui_profile = generate_comprehensive_load_profile(raw_payload)
            metrics = raw_payload["raw_original_metrics"]
            summary = raw_payload["load_plan_summary"]
            
            is_upgraded = raw_payload.get("vehicle_upgraded", False)
            prev_vehicle = raw_payload.get("previous_vehicle", "N/A")
            upgrade_reason = raw_payload.get("upgrade_reason", "The current vehicle cannot carry the combined shipment. A larger vehicle has been selected.")
            upgrade_history = raw_payload.get("upgrade_history", [])
            
            target_vehicle = metrics['vehicle'] if st.session_state.upgrade_approved else prev_vehicle
            
            # Recommended Vehicle Card Layout Component
            st.markdown(f"""
            <div class="matrix-card">
                <span class="metric-badge">Recommended Vehicle</span>
                <h2 style="margin-top:10px; color:#F8FAFC; margin-bottom:5px;">Vehicle : {target_vehicle}</h2>
                <p style="color:#94A3B8; font-size:14px; margin:0; line-height:1.6;">
                    <b>Category :</b> {metrics['category']}<br>
                    <b>Axles :</b> {metrics['axles']}<br>
                    <b>Maximum Capacity :</b> {metrics.get('max_weight_capacity_mt', summary['total_weight_loaded_mt'] + summary['remaining_weight_capacity_mt'])} MT<br>
                    <b>Total Load :</b> {summary['total_weight_loaded_mt']} MT<br>
                    <b>Remaining Capacity :</b> {summary['remaining_weight_capacity_mt']} MT
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Vehicle Changed Context Notification
            if is_upgraded:
                st.markdown(f"""
                <div class="upgrade-card">
                    <span style="color:#f59e0b; font-weight:700; font-size:14px;">🔄 Vehicle Changed</span>
                    <div style="margin-top:10px; color:#F8FAFC; font-size:13px;">
                        <b>Previous Vehicle:</b> {prev_vehicle}<br>
                        <span style="color:#f59e0b; font-weight:900;">↓</span><br>
                        <b>Current Vehicle:</b> {metrics['vehicle']}<br><br>
                        <b>Why?</b><br>
                        {upgrade_reason}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Upgrade Confirmation Conditional Gate
            if is_upgraded and st.session_state.upgrade_approved:
                st.warning("A larger vehicle is required.")
                uc_col1, uc_col2 = st.columns(2)
                with uc_col1:
                    st.markdown(f"**Current Vehicle**\n\n{prev_vehicle}")
                with uc_col2:
                    st.markdown(f"**Suggested Vehicle**\n\n{metrics['vehicle']}")
                st.markdown(f"**Why?**\n{upgrade_reason}")
                
                conf_btn1, conf_btn2 = st.columns(2)
                with conf_btn1:
                    if st.button("Upgrade Vehicle", type="primary", use_container_width=True):
                        st.session_state.upgrade_approved = True
                        st.success("Upgrade verified successfully.")
                with conf_btn2:
                    if st.button("Keep Current Vehicle", use_container_width=True):
                        st.session_state.upgrade_approved = False
                        st.rerun()

            # Optimization Summary Outcomes Card
            if "optimization_score" in raw_payload:
                st.markdown("### Optimization Result")
                opt_col1, opt_col2, opt_col3, opt_col4 = st.columns(4)
                opt_col1.metric("Vehicle Selected", target_vehicle)
                opt_col2.metric("Shipments Loaded", len(raw_payload["loaded_shipments"]))
                opt_col3.metric("Weight Utilization", f"{raw_payload.get('weight_utilization_pct', ui_profile['visual_metrics']['weight']['pct'])}%")
                opt_col4.metric("Optimization Score", raw_payload["optimization_score"])

            # Recommendation Card Component block
            if is_upgraded:
                st.markdown(f"""
                <div class="matrix-card" style="border-left: 4px solid #10B981;">
                    <span style="color:#10B981; font-weight:700; font-size:12px; uppercase;">Recommendation</span>
                    <p style="color:#F8FAFC; font-size:13px; margin-top:8px; margin-bottom:8px;">
                        The combined shipment exceeds the payload capacity of the currently assigned vehicle.
                    </p>
                    <b style="color:#94A3B8;">Recommended Vehicle:</b> <span style="color:#10B981; font-weight:600;">{metrics['vehicle']}</span><br><br>
                    <span style="color:#10B981;">✓</span> All shipments accommodated<br>
                    <span style="color:#10B981;">✓</span> No rejection<br>
                    <span style="color:#10B981;">✓</span> {ui_profile['utilization']}% utilization<br>
                    <span style="color:#10B981;">✓</span> Suitable for current shipment.
                </div>
                """, unsafe_allow_html=True)

            # Transportation Suitability Badges
            if metrics.get("odc_required"):
                st.warning("⚠ ODC Transportation Required")
            else:
                st.success("✓ Standard Transportation")

            if metrics.get("vehicle_suitable"):
                st.success("Vehicle Suitable")
            else:
                st.error("Vehicle Not Suitable")

            # Shipment Summary Section layout
            st.markdown("### Shipment Summary")
            cs_col1, cs_col2, cs_col3 = st.columns(3)
            cs_col1.metric("Shipments Added", len(st.session_state.staged_shipments))
            cs_col2.metric("Total Weight", f"{summary['total_weight_loaded_mt']} MT")
            cs_col3.metric("Total Deck Used", f"{summary['total_length_used_mm']} mm")
            
            cs_col4, cs_col5 = st.columns(2)
            cs_col4.metric("Vehicle Changed", "Yes" if is_upgraded else "No")
            cs_col5.metric("ODC Required", "Yes" if metrics.get("odc_required") else "No")

            # Vehicle Summary Details Area
            st.markdown("---")
            st.subheader("Vehicle Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Vehicle Changed", "Yes" if is_upgraded else "No")
            col2.metric("Previous Vehicle", prev_vehicle)
            col3.metric("Current Vehicle", metrics['vehicle'])
            col4.metric("Reason", upgrade_reason if is_upgraded else "N/A")

            # Capacity Usage Profiler Row
            st.markdown("---")
            st.subheader("Capacity Usage")
            if is_upgraded:
                comp_col1, comp_col2 = st.columns(2)
                with comp_col1:
                    st.markdown(f"#### Before Upgrade\n**Vehicle:** {prev_vehicle}")
                    st.markdown("**Weight** (113%)")
                    st.progress(1.0) 
                with comp_col2:
                    st.markdown(f"#### After Upgrade\n**Vehicle:** {metrics['vehicle']}")
                    st.markdown(f"**Weight** ({ui_profile['visual_metrics']['weight']['pct']}%)")
                    st.progress(ui_profile['visual_metrics']['weight']['pct'] / 100.0)
            else:
                meters = raw_payload["visual_capacity_meters"]
                st.text("Weight Utilization Profile:")
                st.text(meters["weight_utilization_meter"])
                st.text("Deck Utilization Profile:")
                st.text(meters["deck_utilization_meter"])

            # Vehicle Change History Log Trace
            if upgrade_history:
                st.markdown("---")
                st.subheader("Vehicle Change History")
                for idx, step in enumerate(upgrade_history):
                    st.markdown(f"**Shipment Step Assignment {idx+1}**")
                    st.caption(f"`{step.get('from', 'Unknown')}` → `{step.get('to', 'Unknown')}` | Reason: *{step.get('reason', 'Capacity threshold reached')}*")

            # Vehicle Comparison Specifications Matrix
            if is_upgraded:
                st.markdown("---")
                st.subheader("Vehicle Comparison")
                prev_specs = raw_payload.get("previous_vehicle_specifications", {})
                
                comparison_matrix = {
                    "Specification": ["Vehicle", "Category", "Axles", "Max Weight", "Length", "Width", "Height"],
                    "Previous Vehicle": [
                        prev_vehicle, 
                        raw_payload.get("previous_category", "Medium"), 
                        raw_payload.get("previous_axles", "3"),
                        f"{prev_specs.get('max_weight', '15')} MT",
                        f"{prev_specs.get('length', '6700')} mm",
                        f"{prev_specs.get('width', '2500')} mm",
                        f"{prev_specs.get('height', '2200')} mm"
                    ],
                    "Current Vehicle": [
                        metrics['vehicle'],
                        metrics['category'],
                        metrics['axles'],
                        f"{metrics.get('max_weight_capacity_mt', '20')} MT",
                        f"{metrics.get('vehicle_length_mm', '8200')} mm",
                        f"{metrics.get('vehicle_width_mm', '2500')} mm",
                        f"{metrics.get('vehicle_height_mm', '2400')} mm"
                    ]
                }
                st.table(pd.DataFrame(comparison_matrix))

            # ==================================================
            # SHIPMENT DETAILS TABLE REGISTRY
            # ==================================================
            st.markdown("---")
            st.subheader("Shipment Details")
            
            manifest_rows = []
            for s in ui_profile["loaded_shipments"]:
                manifest_rows.append({
                    "Shipment ID": s["id"],
                    "Weight (MT)": s["weight"],
                    "Length (mm)": s["length"],
                    "Width (mm)": s["width"],
                    "Height (mm)": s["height"],
                    "Status": "Loaded",
                    "Assigned Vehicle": target_vehicle,
                    "Remarks": f"Loaded into {metrics['vehicle']} ({metrics['category']})"
                })
            for s in ui_profile["rejected_shipments"]:
                reason_str = ", ".join(s["reasons"]) if isinstance(s.get("reasons"), list) else str(s.get("reasons", "Capacity breach"))
                manifest_rows.append({
                    "Shipment ID": s["id"],
                    "Weight (MT)": s["weight"],
                    "Length (mm)": s["length"],
                    "Width (mm)": s["width"],
                    "Height (mm)": s["height"],
                    "Status": "Rejected",
                    "Assigned Vehicle": "Unassigned",
                    "Remarks": f"{reason_str} | Suggestion: {s.get('suggestion', 'Route to fallback deployment registry')}"
                })
                
            df_manifest = pd.DataFrame(manifest_rows)

            if not df_manifest.empty:
                header_col, download_col = st.columns([3, 1])
                with header_col:
                    st.markdown(
                        f"""<div class="manifest-header-alert">
                            Resource Target Allocation: {target_vehicle.upper()} ({metrics['category'].upper()})
                        </div>""", 
                        unsafe_allow_html=True
                    )
                    
                with download_col:
                    # Report Header formatting
                    report_header = (
                        f"# Vehicle Recommendation Report\n"
                        f"# Vehicle Model,{target_vehicle}\n"
                        f"# Vehicle Category,{metrics['category']}\n"
                        f"# Vehicle Axles,{metrics['axles']}\n"
                        f"# ODC Required,{metrics['odc_required']}\n"
                        f"# Capacity Utilization Profile,{ui_profile['utilization']}%\n"
                        f"# Remaining Weight Cap,{summary['remaining_weight_capacity_mt']} MT\n"
                        f"# Remaining Deck Cap,{summary['remaining_length_capacity_mm']} mm\n"
                        f"# Vehicle Changed,{is_upgraded}\n"
                        f"# ==========================================\n"
                    )
                    raw_csv_body = df_manifest.to_csv(index=False)
                    complete_report_bytes = (report_header + raw_csv_body).encode('utf-8')
                    
                    st.download_button(
                        label="Download Report",
                        data=complete_report_bytes,
                        file_name=f"Vehicle_Recommendation_Report_{target_vehicle.replace(' ', '_')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                st.dataframe(df_manifest, use_container_width=True, hide_index=True)

            # Final Summary Layout Card 
            st.markdown("---")
            st.markdown(f"""
            <div class="matrix-card" style="border: 1px solid #10B981; background: rgba(16, 185, 129, 0.05);">
                <span class="metric-badge" style="background:#10B981; color:#ffffff;">Final Summary</span>
                <p style="color:#F8FAFC; font-size:14px; margin-top:12px; line-height:1.7;">
                    <b>Vehicle Assigned:</b> {target_vehicle}<br>
                    <b>Total Shipments:</b> {len(st.session_state.staged_shipments)}<br>
                    <b>Loaded:</b> {len(ui_profile['loaded_shipments'])}<br>
                    <b>Rejected:</b> {len(ui_profile['rejected_shipments'])}<br>
                    <b>Vehicle Changed:</b> {"Yes" if is_upgraded else "No"}<br>
                    <b>ODC Required:</b> {"Yes" if metrics.get('odc_required') else "No"}<br>
                    <span style="color:#10B981; font-weight:700;">Ready to Transport ✓</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("The application layout manifest is currently waiting for active payload inputs.")
