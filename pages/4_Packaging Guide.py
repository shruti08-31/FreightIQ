# pages/4_Packaging Guide.py
import sys
import os
import streamlit as st
import pandas as pd

# Force Python to look at the project root folder for imports
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from ai.packaging_engine import recommend_packaging, generate_packaging_summary

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
                "Casting",
                "Defence Equipment",
                "Forging",
                "Heat Exchanger",
                "Hydro Turbine",
                "Motor",
                "Spare Parts",
                "Steam Turbine",
                "Turbo Generator"
            ], 
            index=6
        )
        
        p_subtype = st.selectbox(
            "Product Subtype Category",
            [
                "Armoured Component",
                "Bearing",
                "Bearing Housing",
                "Blade",
                "Bolt Kit",
                "Casing",
                "Coupling",
                "Exciter",
                "Francis Runner",
                "Heat Exchanger",
                "Kaplan Runner",
                "Large Motor",
                "Launcher Assembly",
                "Pelton Wheel",
                "Rotor",
                "Rotor Forging",
                "Seal Kit",
                "Shaft",
                "Small Motor",
                "Stator",
                "Valve Body"
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

    # =========================================================================
    # STEP 2: CALCULATED METRICS
    # =========================================================================
    st.markdown("---")
    st.subheader("📊 Calculated Metrics")
    calc_vol = (l_mm * wd_mm * h_mm) / 1_000_000_000
    calc_surf = 2 * (((l_mm/1000) * (wd_mm/1000)) + ((wd_mm/1000) * (h_mm/1000)) + ((l_mm/1000) * (h_mm/1000)))
    is_oversized = "Yes" if (l_mm > 6000 or wd_mm > 3000 or h_mm > 3000) else "No"

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Weight", f"{w_kg:.1f} Kg")
    m_col2.metric("Volume", f"{calc_vol:.2f} m³")
    m_col3.metric("Surface Area", f"{calc_surf:.2f} m²")
    m_col4.metric("Oversized", is_oversized)

    st.markdown("---")
    
    # TRIGGER ENGINE ANALYSIS BUTTON
    if st.button("🔍 Recommend Packaging", type="primary", use_container_width=True):
        with st.spinner("Analyzing shipment details and finding similar historical packaging records..."):
            
            payload = recommend_packaging(
                product_type=p_type, product_subtype=p_subtype, weight=w_kg, 
                length=l_mm, width=wd_mm, height=h_mm, geometry=geom, 
                precision_surface=prec_surf, high_value=h_val, export=exp_bound, 
                uneven_cg=un_cg, projecting_parts=proj_parts
            )
            
            summary_output = generate_packaging_summary(payload)
            jobs = payload["historical_analysis"]["jobs"]
            
            # =========================================================================
            # STEP 3: RESULTS & HIGHLIGHTED HIGHLIGHT CARD
            # =========================================================================
            st.success("Packaging recommendation generated successfully.")
            
            # Extract consensus variables for the dynamic helper sentence
            jobs_found = payload['historical_analysis']['jobs_found']
            consensus = payload['historical_analysis']['consensus_count']
            rec_packaging = payload["decision"]["recommended_packaging"]
            
            d_col1, d_col2, d_col3 = st.columns(3)
            d_col1.metric("Recommended Packaging", rec_packaging)
            d_col2.metric("Recommendation Based On", payload["decision"]["decision_source"])
            d_col3.metric("Similar Historical Jobs", f"{jobs_found} / 5 Matches")
            
            # Practical, data-backed reasoning helper sentence
            if jobs_found > 0:
                st.info(f"💡 **Reason:** Selected because {consensus} out of {jobs_found} similar historical shipments used {rec_packaging.lower()}.")
            
            st.markdown("#### Historical Match Confidence")
            if jobs_found > 0:
                conf_pct = (consensus / jobs_found)
            else:
                conf_pct = 1.0
            
            st.progress(conf_pct)
            st.write(f"**Confidence:** {conf_pct*100:.0f}% based on historical packaging records.")
            st.markdown("---")

            # =========================================================================
            # STEP 4: DATA BLOCKS
            # =========================================================================
            
            with st.expander("Handling Requirements", expanded=True):
                col_der1, col_der2 = st.columns(2)
                with col_der1:
                    st.info(f"**Primary Material Handling Lift:** {payload['logistics']['lifting_method']}")
                with col_der2:
                    st.info(f"**Base Support Frame:** {payload['logistics']['base_support']}")

            with st.expander("Top 5 Similar Historical Jobs", expanded=True):
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
                    st.dataframe(df_jobs, use_container_width=True)
                else:
                    st.info("No matching historical records found.")

            with st.expander("Recommendation Summary", expanded=True):
                # Clean the summary text to remove repetitive tables/historical text lists
                cleaned_summary = summary_output
                
                redundant_phrases = [
                    "Recommendation Source",
                    "Historical Packaging Records",
                    "Historical Evidence",
                    "Historical Consensus",
                    "Found 5 similar completed packaging jobs."
                ]
                
                for phrase in redundant_phrases:
                    cleaned_summary = cleaned_summary.replace(phrase, "")
                
                # Strip out any remaining line-by-line raw text mappings like "Job 1 Weight..."
                lines = [line for line in cleaned_summary.splitlines() if not line.strip().startswith("Job ")]
                cleaned_summary = "\n".join(lines).strip()
                
                st.markdown(cleaned_summary)

            # =========================================================================
            # STEP 5: REPORT DOWNLOADING
            # =========================================================================
            st.markdown("---")
            st.subheader("Download Report")
            st.download_button(
                label="📄 Download Report (TXT)",
                data=summary_output,
                file_name=f"PACKAGING_PLAN_REPORT_2026.txt",
                mime="text/plain",
                use_container_width=True
            )

# Explicitly execute to guarantee page loads reliably within sub-page structures
render_packaging_planner()
