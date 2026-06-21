import streamlit as st

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Packaging Planner",
    page_icon="📦",  
    layout="wide",
    initial_sidebar_state="expanded"
)

from ai.packaging_engine import recommend_packaging
from ai.packaging_engine import generate_packaging_summary

# ==================================================
# PREMIUM ENTERPRISE STYLING & SIDEBAR UI OVERHAUL
# ==================================================
st.markdown("""
<style>
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
.block-container { padding-top:1.5rem; }

/* Clean metric value display styling */
[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* Elegant sub-label text */
.metric-subtext {
    font-size: 13px;
    color: #64748B;
    margin-top: -4px;
}

/* Modern, theme-aware AI Analysis Container */
.analysis-container {
    background-color: rgba(255, 255, 255, 0.04); 
    padding: 24px; 
    border-radius: 8px; 
    border-left: 5px solid #3B82F6; /* Professional Accent */
    font-size: 15px;
    line-height: 1.7;
}

/* Light theme safety layer */
@media (prefers-color-scheme: light) {
    .analysis-container {
        background-color: #F8FAFC;
        border-left: 5px solid #1E3A8A;
    }
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
    
    # Space between header and footer where pages list populates natively
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    
    # Sidebar Branding Footer Block
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #1E293B;'>", unsafe_allow_html=True)
    st.caption("""
    **CDX FreightIQ v1.0** Powered by:  
    Python • Streamlit  
    SQLite • Gemini AI
    """)

# ==================================================
# MAIN INTERFACE WORKSPACE
# ==================================================
# App Header
st.title("Packaging Planning Assistant")
st.caption("Determine packaging categories, material specs, and dimensional structural boundaries seamlessly.")
st.divider()

# =====================================
# INPUTS
# =====================================
st.subheader("Job Details")

col1, col2 = st.columns(2, gap="large")

with col1:
    weight = st.number_input(
        "Weight (Kg)",
        min_value=0.0,
        value=500.0,
        help="Total weight of the shipment in kilograms."
    )

    length = st.number_input(
        "Length (mm)",
        min_value=0,
        value=3000
    )

with col2:
    fragile = st.selectbox(
        "Is the Material Fragile?",
        ["Yes", "No"],
        index=0
    )

    # Clean nested row for width and height matching the dashboard grid
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        width = st.number_input("Width (mm)", min_value=0, value=2000)
    with sub_col2:
        height = st.number_input("Height (mm)", min_value=0, value=1800)

st.write("") # Spacer
generate_btn = st.button("Generate Packaging Plan", use_container_width=True, type="primary")
st.divider()

# =====================================
# RECOMMENDATIONS & DASHBOARD
# =====================================
if generate_btn:
    with st.spinner("Processing physical dimensions and mapping constraints..."):
        result = recommend_packaging(
            weight,
            length,
            width,
            height,
            fragile
        )
        summary = generate_packaging_summary(result)

    st.toast("Packaging plan calculated successfully.")

    st.subheader("Executive Dashboard")

    # Row 1: Tactical Classifications
    m_col1, m_col2, m_col3 = st.columns(3, gap="medium")

    with m_col1:
        with st.container(border=True):
            st.metric(label="Packaging Type", value=result["packaging_type"])
            st.markdown(f"<div class='metric-subtext'>Category: {result['packaging_category']}</div>", unsafe_allow_html=True)

    with m_col2:
        with st.container(border=True):
            st.metric(label="Engineering Drawing", value=result["engineering_drawing"])
            status_text = "Required due to scale/weight boundaries" if result["engineering_drawing"] == "Required" else "Standard parameters apply"
            st.markdown(f"<div class='metric-subtext'>{status_text}</div>", unsafe_allow_html=True)

    with m_col3:
        with st.container(border=True):
            st.metric(label="Material Planning", value=result["material_planning"])
            st.markdown("<div class='metric-subtext'>Material sizing evaluation mandatory</div>", unsafe_allow_html=True)

    # Row 2: Physical & Dimensional Calculations
    p_col1, p_col2, p_col3 = st.columns(3, gap="medium")

    with p_col1:
        with st.container(border=True):
            st.metric(label="Calculated Volume", value=f"{result['volume']} m³")

    with p_col2:
        with st.container(border=True):
            st.metric(label="Surface Area", value=f"{result['surface_area']} m²")

    with p_col3:
        with st.container(border=True):
            is_oversized = "Yes" if result["oversized"] else "No"
            st.metric(label="Oversized Cargo Condition", value=is_oversized)

    st.write("") # Spacer

    # Styled AI Packaging Analysis Container
    with st.container(border=True):
        st.markdown("### AI Packaging Analysis")
        
        st.markdown(
            f"""
            <div class="analysis-container">
                {summary}
            </div>
            """, 
            unsafe_allow_html=True
        )