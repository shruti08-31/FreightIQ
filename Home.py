import streamlit as st

# PAGE CONFIG
st.set_page_config(
    page_title="CDX FreightIQ",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PREMIUM ENTERPRISE STYLING & SIDEBAR UI OVERHAUL

st.markdown("""
<style>
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
.block-container { padding-top:1.5rem; }

/* Dashboard Card Theme */
.hero-card {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 35px;
    margin-bottom: 25px;
}

.dept-badge {
    background-color: #0284C7;
    color: #F0F9FF;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 11px;
    letter-spacing: 0.75px;
    text-transform: uppercase;
    border: 1px solid #38BDF8;
    display: inline-block;
    margin-bottom: 12px;
}

/* Professional Getting Started Pipeline */
.pipeline-container {
    border-top: 1px solid #334155;
    padding-top: 20px;
    margin-top: 15px;
}
.pipeline-title {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}
.pipeline-row {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}
.pipeline-step {
    background: #0F172A;
    border: 1px solid #1E293B;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 13px;
    color: #CBD5E1;
    display: flex;
    align-items: center;
}
.step-index {
    color: #38BDF8;
    font-weight: bold;
    margin-right: 8px;
}

/* Section Typographics */
.sub-section-header {
    font-size: 18px;
    font-weight: 600;
    color: #F1F5F9;
    margin-top: 25px;
    margin-bottom: 15px;
    letter-spacing: -0.2px;
    border-left: 3px solid #0284C7;
    padding-left: 10px;
}

/* Capability Cards */
.cap-box {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 6px;
    padding: 15px 18px;
    height: 100%;
}
.cap-title {
    font-size: 14px;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 6px;
}
.cap-list {
    margin: 0;
    padding-left: 14px;
    color: #94A3B8;
    font-size: 13px;
}
.cap-list li {
    margin-bottom: 4px;
}

/* Interactive Explanatory Blocks */
.interactive-content {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 6px;
    padding: 16px;
    margin-top: 5px;
}

.onboard-step {
    margin-bottom: 14px;
}
.onboard-step:last-child {
    margin-bottom: 0;
}
.step-num {
    color: #38BDF8;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.step-name {
    color: #E2E8F0;
    font-weight: 500;
    font-size: 14px;
}
.step-desc {
    color: #64748B;
    font-size: 13px;
    margin-top: 2px;
}

/* Technical Footer */
.footer-box {
    margin-top: 45px;
    border-top: 1px solid #1E293B;
    padding-top: 20px;
    padding-bottom: 20px;
}
.footer-title {
    font-size: 14px;
    font-weight: 600;
    color: #94A3B8;
    margin-bottom: 4px;
}
.footer-desc {
    font-size: 13px;
    color: #64748B;
    line-height: 1.5;
}
.stack-badge {
    background: #1E293B;
    color: #94A3B8;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid #334155;
    font-family: monospace;
    display: inline-block;
    margin-top: 8px;
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

with st.sidebar:
    # 2. Sidebar Header Block
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

# 1. WELCOME BANNER & PROFESSIONAL PIPELINE

st.markdown("""
<div class="hero-card">
    <div class="dept-badge">Heavy Electrical Equipment Plant — Central Despatch Division</div>
    <h1 style="margin:0 0 4px 0; color:#F8FAFC; font-size:34px; font-weight:700; letter-spacing:-0.5px;">Welcome to CDX FreightIQ</h1>
    <p style="color:#38BDF8; font-size:16px; font-weight:500; margin:0 0 16px 0; letter-spacing:0.25px;">Your AI-powered Logistics Planning Assistant</p>
    <p style="color:#CBD5E1; font-size:14.5px; max-width:900px; line-height:1.6; margin:0; font-weight: 400;">
        Plan shipments, select vehicles, validate ODC cargo, analyze routes, generate packaging plans, 
        and interact with logistics AI — all from one platform.
    </p>
    <div class="pipeline-container">
        <div class="pipeline-title">System Deployment Sequence</div>
        <div class="pipeline-row">
            <div class="pipeline-step"><span class="step-index">01</span> Explore Logistics Dashboard</div>
            <div class="pipeline-step"><span class="step-index">02</span> Find Suitable Vehicle</div>
            <div class="pipeline-step"><span class="step-index">03</span> Generate Packaging Plan</div>
            <div class="pipeline-step"><span class="step-index">04</span> Ask Logistics AI</div>
            <div class="pipeline-step"><span class="step-index">05</span> Verify Database Records</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# 2. INTERACTIVE ON-DEMAND SYSTEM SECTIONS

st.markdown('<div class="sub-section-header">System Insights & User Guidance</div>', unsafe_allow_html=True)


with st.expander("Platform Functional Capabilities", expanded=False):
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        st.markdown("""
        <div class="cap-box">
            <div class="cap-title">Vehicle Recommendation</div>
            <ul class="cap-list">
                <li>Suggests optimal mechanical or hydraulic multi-axle trailers</li>
                <li>Matches vehicle configurations dynamically to weight and mass</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="cap-box">
            <div class="cap-title">ODC Assessment Framework</div>
            <ul class="cap-list">
                <li>Automated checking of structural cargo limits</li>
                <li>Flags regulatory clearances and state-boundary thresholds</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="cap-box">
            <div class="cap-title">Route Intelligence Module</div>
            <ul class="cap-list">
                <li>Queries validated point-to-point regional transit matrices</li>
                <li>Provides detailed mileage and structural route availability analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_cap2:
        st.markdown("""
        <div class="cap-box">
            <div class="cap-title">Packaging Planning Engine</div>
            <ul class="cap-list">
                <li>Automated engineering box selection based on center of gravity</li>
                <li>Calculates surface areas and estimates raw packaging materials</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="cap-box">
            <div class="cap-title">AI Logistics Assistant</div>
            <ul class="cap-list">
                <li>Accepts unformatted raw manifest text to bypass rigid input screens</li>
                <li>Generates executive summaries and analysis logs automatically</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Interactive Section 2: Recommended Operations Order
with st.expander("New Here? Recommended Operations Order", expanded=False):
    st.markdown("""
    <div class="interactive-content">
        <div class="onboard-step">
            <span class="step-num">Step 1</span> — <span class="step-name">Logistics Dashboard</span>
            <div class="step-desc">Establish baseline context by checking current inventory metrics, coverage spans, and engine indicators.</div>
        </div>
        <div class="onboard-step">
            <span class="step-num">Step 2</span> — <span class="step-name">Vehicle Allocator</span>
            <div class="step-desc">Input item parameters to isolate appropriate chassis allocations and run structural safety filters.</div>
        </div>
        <div class="onboard-step">
            <span class="step-num">Step 3</span> — <span class="step-name">Packaging Guide</span>
            <div class="step-desc">Determine volumetric spacing, target material requirements, and specific structural drawings.</div>
        </div>
        <div class="onboard-step">
            <span class="step-num">Step 4</span> — <span class="step-name">Logistics AI</span>
            <div class="step-desc">Leverage natural language reasoning to analyze ad-hoc scenarios and draft standard planning reports.</div>
        </div>
        <div class="onboard-step">
            <span class="step-num">Step 5</span> — <span class="step-name">Database Lookup</span>
            <div class="step-desc">Query master logistics records to audit point-to-point travel limits and station networks manually.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# 3. FOOTER ABOUT PROJECT

st.markdown("""
<div class="footer-box">
    <div class="footer-title">About CDX FreightIQ</div>
    <div class="footer-desc">
        An AI-powered logistics planning platform developed to support vehicle selection, route intelligence, 
        ODC compliance verification, packaging planning, and shipment decision support.
    </div>
    <div class="stack-badge">Technology Stack: Python • Streamlit • SQLite • Gemini AI</div>
</div>
""", unsafe_allow_html=True)
