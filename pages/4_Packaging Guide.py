import sys
import os
import streamlit as st
import pandas as pd

# Force Python to look at the project root folder for imports
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from ai.packaging_engine import recommend_packaging, generate_packaging_summary, summarize_report

def render_packaging_planner():
    st.set_page_config(layout="wide", page_title="AI Packaging Planner", page_icon="📦")
    
    st.title("📦 AI Packaging Recommendation System")
    st.caption("Recommend suitable industrial packaging using historical packaging records and engineering rules.")
    st.markdown("---")
    
    # =========================================================================
    # STEP 1: INPUT COLUMNS
    # =========================================================================
    col_in_left, col_in_right = st.columns(2)
    
    with col_in_left:
        st.subheader("📦 Shipment Details")
        p_type = st.selectbox(
            "Product Type Cluster", 
            [
                "Casting", "Defence Equipment", "Forging", "Heat Exchanger",
                "Hydro Turbine", "Motor", "Spare Parts", "Steam Turbine", "Turbo Generator"
            ], 
            index=6
        )
        
        p_subtype = st.selectbox(
            "Product Subtype Category",
            [
                "Armoured Component", "Bearing", "Bearing Housing", "Blade", "Bolt Kit",
                "Casing", "Coupling", "Exciter", "Francis Runner", "Heat Exchanger",
                "Kaplan Runner", "Large Motor", "Launcher Assembly", "Pelton Wheel",
                "Rotor", "Rotor Forging", "Seal Kit", "Shaft", "Small Motor", "Stator", "Valve Body"
            ],
            index=1
        )
        
        col_dim1, col_dim2 = st.columns(2)
        with col_dim1:
            w_kg = st.number_input("Mass / Weight (Kg)", min_value=0.0, value=15.0, step=1.0)
            l_mm = st.number_input("Length Dimension (mm)", min_value=0.0, value=1705.0, step=10.0)
        with col_dim2:
            wd_mm = st.number_input("Width Dimension (mm)", min_value=0.0, value=1058.0, step=10.0)
            h_mm = st.number_input("Height Dimension (mm)", min_value=0.0, value=3061.0, step=10.0)

    with col_in_right:
        st.subheader("⚙️ Additional Shipment Information")
        col_safe1, col_safe2 = st.columns(2)
        with col_safe1:
            geom = st.selectbox("Structural Geometry Complexity", ["Simple", "Medium", "Complex"], index=0)
            prec_surf = st.selectbox("Precision / Finished Surface?", ["No", "Yes"], index=0)
        with col_safe2:
            h_val = st.selectbox("High-Value Inventory asset?", ["No", "Yes"], index=0)
            exp_bound = st.selectbox("International Export Bound?", ["No", "Yes"], index=0)
            un_cg = st.selectbox("Uneven Center of Gravity (CG)?", ["No", "Yes"], index=0)
            proj_parts = st.selectbox("Projecting / Fragile Outer Elements?", ["Yes", "No"], index=0)

    st.markdown("---")
    
    # =========================================================================
    # STEP 2: TRIGGER ENGINE ANALYSIS (Saved to Session State)
    # =========================================================================
    if st.button("🔍 Generate Packaging Plan", type="primary", use_container_width=True):
        with st.spinner("Analyzing shipment details and finding similar historical packaging records..."):
            
            payload = recommend_packaging(
                product_type=p_type, product_subtype=p_subtype, weight=w_kg, 
                length=l_mm, width=wd_mm, height=h_mm, geometry=geom, 
                precision_surface=prec_surf, high_value=h_val, export=exp_bound, 
                uneven_cg=un_cg, projecting_parts=proj_parts
            )
            
            # Save results into session state to prevent reload wiping the screen
            st.session_state["pkg_results"] = generate_packaging_summary(payload)
            st.session_state["pkg_summary_text"] = None  # Reset summary if new generation occurs

    # =========================================================================
    # STEP 3: RENDER RESULTS IF AVAILABLE
    # =========================================================================
    if "pkg_results" in st.session_state:
        summary_output = st.session_state["pkg_results"]
        cards = summary_output["dashboard_cards"]
        ai_analysis = summary_output["ai_analysis"]
        jobs = summary_output["historical_table"]
        
        st.success("Packaging recommendation generated successfully.")
        st.markdown("---")

        # --- EXECUTIVE DASHBOARD ---
        st.header("📊 Executive Dashboard")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(cards["packaging_type"]["title"], cards["packaging_type"]["value"], cards["packaging_type"]["subtitle"], delta_color="off")
        with c2:
            st.metric(cards["duty_category"]["title"], cards["duty_category"]["value"], cards["duty_category"]["subtitle"], delta_color="off")
        with c3:
            st.metric(cards["engineering_drawing"]["title"], cards["engineering_drawing"]["value"], cards["engineering_drawing"]["subtitle"], delta_color="off")
            
        st.write("") # Spacing
        
        c4, c5, c6 = st.columns(3)
        with c4:
            st.metric(cards["material_planning"]["title"], cards["material_planning"]["value"], cards["material_planning"]["subtitle"], delta_color="off")
        with c5:
            st.metric(cards["oversized_status"]["title"], cards["oversized_status"]["value"], cards["oversized_status"]["subtitle"], delta_color="off")
        with c6:
            st.metric(cards["model_confidence"]["title"], cards["model_confidence"]["value"], cards["model_confidence"]["subtitle"], delta_color="off")

        st.markdown("---")

        # --- AI PACKAGING ANALYSIS ---
        st.markdown(ai_analysis)
        
        st.markdown("---")

        # --- OPTIONAL SUMMARY FEATURE ---
        st.subheader("📝 Report Summary")
        want_summary = st.radio("Would you like a brief summary of the above report?", ["No", "Yes"], index=0, horizontal=True)
        
        if want_summary == "Yes":
            if st.session_state.get("pkg_summary_text") is None:
                with st.spinner("Summarizing report..."):
                    st.session_state["pkg_summary_text"] = summarize_report(ai_analysis)
            
            st.info(st.session_state["pkg_summary_text"])

        st.markdown("---")

        # --- HISTORICAL SIMILAR JOBS ---
        st.header("📋 Historical Similar Jobs")
        if jobs:
            table_data = []
            for j in jobs:
                table_data.append({
                    "Job ID": j.get("job_id"),
                    "Weight (Kg)": j["weight"],
                    "Length (mm)": j["length"],
                    "Width (mm)": j["width"],
                    "Height (mm)": j["height"],
                    "Assigned Packaging": j["packaging_type"],
                    "Similarity Index": f"{j.get('similarity', 100.0)}%"
                })
            df_jobs = pd.DataFrame(table_data)
            st.dataframe(df_jobs, use_container_width=True, hide_index=True)
        else:
            st.info("No matching historical records found for these parameters.")

        st.markdown("---")

        # --- REPORT DOWNLOADING ---
        st.subheader("💾 Download Report")
        
        export_text = f"EXECUTIVE SUMMARY\n" \
                      f"Packaging Type: {cards['packaging_type']['value']}\n" \
                      f"Duty Category: {cards['duty_category']['value']}\n" \
                      f"Engineering Drawing: {cards['engineering_drawing']['value']}\n" \
                      f"Material Planning: {cards['material_planning']['value']}\n" \
                      f"Model Confidence: {cards['model_confidence']['value']}\n\n" \
                      f"=========================================\n\n" \
                      f"{ai_analysis}"
                      
        if st.session_state.get("pkg_summary_text"):
            export_text += f"\n\n=========================================\n\nAI SUMMARY:\n{st.session_state['pkg_summary_text']}"

        st.download_button(
            label="📄 Download Report (TXT)",
            data=export_text,
            file_name=f"PACKAGING_PLAN_REPORT_2026.txt",
            mime="text/plain",
            use_container_width=True
        )

# Explicitly execute to guarantee page loads reliably within sub-page structures
if __name__ == "__main__":
    render_packaging_planner()
