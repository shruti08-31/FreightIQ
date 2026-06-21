import streamlit as st
from ai.gemini_service import get_ai_response

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="CDX AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS & SIDEBAR UI OVERHAUL
# ==================================================
st.markdown("""
<style>
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}

/* Page container layout */
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Base text formatting for professional appearance */
p, li {
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    color: #E2E8F0 !important;
}

/* Headings enhancement */
h1 {
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

h3 {
    font-weight: 600 !important;
    color: #94A3B8 !important;
    font-size: 1.1rem !important;
    margin-top: 1.5rem !important;
}

/* Stylized welcome container for clean segregation */
.welcome-box {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.example-card{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:12px;
    padding:12px;
    margin-bottom:10px;
}

/* Clearer list item separation */
ul {
    margin-bottom: 1rem !important;
    padding-left: 1.25rem !important;
}

li {
    margin-bottom: 0.4rem !important;
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

# ==================================================
# PREMIUM SIDEBAR IMPLEMENTATION
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

    st.markdown("<hr style='margin: 20px 0 15px 0; border: 0; border-top: 1px solid #1E293B;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.75px; margin-bottom:10px; padding-left:2px;">Suggested Prompts</div>', unsafe_allow_html=True)
    
    st.markdown("""
<div style="font-size: 12.5px; color: #94A3B8; line-height: 1.5; padding: 0 2px;">
• Recommend transport configuration for a 350 MT BHEL Steam Turbine Generator from Haridwar plant<br><br>
• Is ODC regulatory clearance and route survey required for a 500 MVA Transformer?<br><br>
• Analyze civil infrastructure and bridge load capacities between Jhansi and Chennai port<br><br>
• Check availability of 24-row hydraulic multi-axle modular trailers for heavy equipment dispatch<br><br>
• Show transit risk matrix and infrastructure bottlenecks for consignment clearance on North-South corridors<br><br>
• Compare operational turn-radius and load stability of mechanical vs hydraulic trailers for power plant logistics<br><br>
• Provide maximum axle-load specifications and structural safety margins for heavy-haul transport units
</div>
""", unsafe_allow_html=True)

    # Sidebar Branding Footer Block
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #1E293B;'>", unsafe_allow_html=True)
    st.caption("""
    **CDX FreightIQ v1.0** Powered by:  
    Python • Streamlit  
    SQLite • Gemini AI
    """)

# ==================================================
# HEADER
# ==================================================
st.title("CDX AI Assistant")

st.caption(
    """
    Ask anything about logistics operations,
    vehicle recommendations, route planning,
    ODC requirements, transporters and fleet analytics.
    """
)

st.write("") # Structural spacing element

# ==================================================
# SESSION STATE
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
<div class="welcome-box">

I am your deployment and routing intelligence agent. You can ask me query setups regarding:

• Optimal vehicle allocation based on weight, volume, and material type
• Regulatory Over-Dimensional Cargo (ODC) sizing and clearance assessments
• Route hazard, infrastructure bottlenecks, and transit-time analysis
• Fleet breakdown tracking, driver availability, and carrier utilization metrics
• Historical spot rates, contract lane benchmarks, and cost efficiency performance

Simply submit your operational parameters or metrics into the terminal input box.

### Direct Query Formats:

- Recommend vehicle for 35 MT cargo from AGRA to MUMBAI with dimensions 8000 x 2400 x 3000 mm.
- Is ODC regulatory clearance needed for an infrastructure consignment sized 14000 x 3500 x 4500 mm?
- Analyze current route configurations and restrictions between DELHI and CHENNAI.
- Provide a summary of active carrier capacity and transporter availability matrices.
</div>
"""
        }
    ]

# ==================================================
# DISPLAY CHAT
# ==================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            message["content"],
            unsafe_allow_html=True
        )

# ==================================================
# CHAT INPUT
# ==================================================
user_input = st.chat_input(
    "Ask CDX AI anything..."
)

# ==================================================
# RESPONSE
# ==================================================
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
        with st.spinner("Analyzing logistics data..."):
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