import streamlit as st
from ai.vehicle_engine import recommend_vehicle
from ai.analytics import get_dashboard_metrics

from ai.gemini_service import get_ai_response 

# PAGE CONFIG
st.set_page_config(
    page_title="CDX AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}

/* Page container layout */
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Simplified CSS for student-project look */
.welcome-box {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 1.5rem;
}

.example-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 10px;
    min-height: 140px;
}

/* ==================================================
   ADVANCED SIDEBAR INTERACTIVE STYLING (KEPT EXACTLY AS IS)
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

/* Style formatting modifications for standard sidebar button overrides */
div.stSidebar div.stButton > button {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #CBD5E1 !important;
}
div.stSidebar div.stButton > button:hover {
    border-color: #E11D48 !important;
    background-color: #0F172A !important;
    color: #F8FAFC !important;
}
</style>
""", unsafe_allow_html=True)

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

    # Core Assistant Interactive Tool Actions
    st.markdown('<div style="font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.75px; margin-bottom:10px; padding-left:2px;">Assistant Actions</div>', unsafe_allow_html=True)
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": """
<div class="welcome-box">
Conversation cleared.
How can I help you today?
</div>
"""
            }
        ]
        st.rerun()

    # Sidebar Branding Footer Block
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #1E293B;'>", unsafe_allow_html=True)
    
    st.caption("""
    **CDX FreightIQ v1.0** Powered by:  
    Python • Streamlit  
    Groq • Llama-3.3-70b
    """)

st.title("🚚 CDX Logistics Assistant")
st.caption("AI-powered assistant for logistics planning, routing, fleet recommendations, and ODC analysis.")

st.divider()

st.subheader("Example Queries")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="example-card">
    <strong>📦 Vehicle Recommendation</strong><br><br>
    Recommend a vehicle for transporting a 35 MT transformer from Agra to Mumbai with dimensions 8000 × 2400 × 3000 mm.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="example-card">
    <strong>🛣️ Route Analysis</strong><br><br>
    Analyze current route configurations, civil restrictions, and infrastructure bottlenecks between Delhi and Chennai.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="example-card">
    <strong>⚠️ ODC Check</strong><br><br>
    Is ODC regulatory clearance required for an infrastructure consignment measuring 14000 × 3500 × 4500 mm?
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================================================
# SESSION STATE & SIMPLE WELCOME TEXT
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
### Welcome

This assistant helps with logistics planning and transportation queries. 

Enter your query below or use one of the example configurations above to get started.
"""
        }
    ]

# DISPLAY CHAT

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# CHAT INPUT & PROCESSOR

user_input = st.chat_input("Describe your shipment or logistics requirement...")

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            try:
                response = get_ai_response(user_input)
            except Exception as e:
                response = f"Error: {str(e)}"
            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

st.divider()
st.caption("""
**Built using:** Python • Streamlit • Groq API 
""")
