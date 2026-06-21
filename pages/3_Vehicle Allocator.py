import streamlit as st
import pandas as pd

from ai.vehicle_engine import recommend_vehicle

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Vehicle Recommendation",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS WITH PREMIUM SIDEBAR OVERHAUL
# ==================================================
st.markdown("""
<style>
.block-container{
    padding-top:2rem;
}
.matrix-card{
    padding:1.5rem;
    border-radius:10px;
    background:#0f172a;
    border:1px solid #1e293b;
    margin-bottom:1rem;
}
.metric-badge{
    display:inline-block;
    padding:5px 10px;
    border-radius:5px;
    background:#1e293b;
    color:#38bdf8;
    font-size:12px;
    font-weight:600;
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
""", unsafe_allow_html=True)

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

# ==================================================
# HEADER
# ==================================================
st.title("Vehicle Recommendation Engine")

st.caption(
    "Automated vehicle allocation based on shipment weight and dimensional profile."
)

st.divider()

# ==================================================
# INPUT PANEL
# ==================================================
left_panel, right_panel = st.columns([1, 1.5])

with left_panel:
    st.subheader("Shipment Specifications")

    weight = st.number_input(
        "Payload Weight (MT)",
        min_value=0.0,
        value=25.0
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        length = st.number_input(
            "Length (mm)",
            min_value=0,
            value=8000
        )

    with c2:
        width = st.number_input(
            "Width (mm)",
            min_value=0,
            value=2400
        )

    with c3:
        height = st.number_input(
            "Height (mm)",
            min_value=0,
            value=3000
        )

    evaluate = st.button(
        "Evaluate Vehicle",
        type="primary",
        use_container_width=True
    )

# ==================================================
# RESULTS
# ==================================================
with right_panel:
    if evaluate:
        result = recommend_vehicle(
            weight,
            length,
            width,
            height
        )

        if "error" in result:
            st.error(result["error"])
        else:
            # ----------------------------------
            # STATUS
            # ----------------------------------
            if result["odc_required"]:
                st.warning(
                    "ODC shipment detected based on cargo dimensions."
                )
            else:
                st.success(
                    "Shipment falls within standard transport limits."
                )

            if not result["vehicle_suitable"]:
                st.error(
                    "Selected vehicle cannot safely execute this shipment."
                )

            # ----------------------------------
            # PRIMARY VEHICLE CARD
            # ----------------------------------
            st.markdown(
                f"""
                <div class="matrix-card">
                    <span class="metric-badge">
                    Recommended Vehicle
                    </span>
                    <h2 style="margin-top:15px;">
                    {result['vehicle']}
                    </h2>
                    <p>
                    Weight Capacity:
                    {result['min_weight']} MT
                    -
                    {result['max_weight']} MT
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # ----------------------------------
            # METRICS
            # ----------------------------------
            m1, m2, m3, m4 = st.columns(4)

            with m1:
                st.metric(
                    "Category",
                    result["category"]
                )

            with m2:
                st.metric(
                    "Axles",
                    result["axles"]
                )

            with m3:
                st.metric(
                    "Capacity",
                    f"{result['max_weight']} MT"
                )

            with m4:
                tier = (
                    "ODC Ready"
                    if result["odc_allowed"] == "Yes"
                    else "Standard"
                )
                st.metric(
                    "Vehicle Type",
                    tier
                )

            # ----------------------------------
            # UTILIZATION
            # ----------------------------------
            st.markdown("### Capacity Utilization")

            st.metric(
                "Weight Utilization",
                f"{result['utilization_percent']}%"
            )

            st.progress(
                result["utilization_percent"] / 100
            )

            # ----------------------------------
            # DIMENSION CAPACITY
            # ----------------------------------
            st.markdown("### Vehicle Capacity Profile")

            d1, d2, d3 = st.columns(3)

            with d1:
                st.metric(
                    "Length Capacity",
                    f"{result['length_capacity']:,} mm"
                )

            with d2:
                st.metric(
                    "Width Capacity",
                    f"{result['width_capacity']:,} mm"
                )

            with d3:
                st.metric(
                    "Height Capacity",
                    f"{result['height_capacity']:,} mm"
                )

            # ----------------------------------
            # VOLUME
            # ----------------------------------
            v1, v2 = st.columns(2)

            with v1:
                st.metric(
                    "Shipment Volume",
                    f"{result['shipment_volume']} m³"
                )

            with v2:
                st.metric(
                    "Vehicle Volume Capacity",
                    f"{result['vehicle_volume_capacity']} m³"
                )

            # ----------------------------------
            # ALTERNATIVE VEHICLE
            # ----------------------------------
            if result["alternative_vehicle"]:
                st.markdown("### Alternative Recommendation")
                st.info(
                    f"""
                    Vehicle: {result['alternative_vehicle']}
                    
                    Category: {result['alternative_category']}
                    
                    Axles: {result['alternative_axles']}
                    """
                )

            # ----------------------------------
            # DIAGNOSTIC TABLE
            # ----------------------------------
            with st.expander(
                "Vehicle Diagnostic Matrix",
                expanded=True
            ):
                df = pd.DataFrame({
                    "Property": [
                        "Vehicle Name",
                        "Category",
                        "Weight Range",
                        "Axles",
                        "Length Capacity",
                        "Width Capacity",
                        "Height Capacity",
                        "ODC Allowed",
                        "ODC Required",
                        "Vehicle Suitable"
                    ],
                    "Value": [
                        result["vehicle"],
                        result["category"],
                        f"{result['min_weight']} - {result['max_weight']} MT",
                        result["axles"],
                        result["length_capacity"],
                        result["width_capacity"],
                        result["height_capacity"],
                        result["odc_allowed"],
                        result["odc_required"],
                        result["vehicle_suitable"]
                    ]
                })

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )