import os
from collections import Counter
from groq import Groq
from dotenv import load_dotenv
from database.packaging_db import get_similar_packaging

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"
CONTACT_INFO = "Information is not available in the current CDX database."

def evaluate_packaging_needs(product_type, product_subtype, weight, length, width, height, 
                        geometry, precision_surface, high_value, export, 
                        uneven_cg, projecting_parts):
    
    volume = round((length * width * height) / 1_000_000_000, 2)
    surface_area = round(
        2 * ((length / 1000) * (width / 1000) + (width / 1000) * (height / 1000) + (length / 1000) * (height / 1000)), 2
    )
    oversized = "Yes" if (length > 6000 or width > 3000 or height > 3000) else "No"
    
    if weight > 15000:
        lifting_method, base_support = "Heavy Crane", "Heavy Steel Skid"
    elif weight > 1000:
        lifting_method, base_support = "EOT Crane", "Steel Base"
    elif weight > 500:
        lifting_method, base_support = "Crane", "Wooden Skid Frame"
    elif weight >= 20:
        lifting_method, base_support = "Forklift", "Wooden Skid Frame"
    else:
        lifting_method, base_support = "Manual", "Foam"

    engineering_drawing = "Required" if (oversized == "Yes" or weight > 1000 or high_value == "Yes") else "Not Required"
    material_planning = "Required" if (oversized == "Yes" or weight > 500) else "Not Required"
    engineering_approval = "Pending" if engineering_drawing == "Required" else "Not Required"

    try:
        history = get_similar_packaging(weight, length, width, height, geometry, high_value, export, lifting_method)
    except Exception:
        history = []

    if history:
        counts = Counter(job["packaging_type"] for job in history)
        final_packaging = counts.most_common(1)[0][0]
        consensus_count = counts.most_common(1)[0][1]
        decision_source = "Historical Packaging Records"
        decision_reason = f"{consensus_count} out of {len(history)} similar jobs matching this profile used {final_packaging}."
    else:
        decision_source = "Static Safety Matrix Fallback"
        if weight > 15000: final_packaging = "Customized Structural Frame"
        elif weight > 1000: final_packaging = "Fabricated Steel Frame"
        elif weight > 100: final_packaging = "Reinforced Wooden Box"
        else: final_packaging = "Corrugated Box"
        consensus_count = 0
        decision_reason = "No closely matching structural patterns found in history. Applied engineering rule matrices."

    return {
        "meta": {"product_type": product_type, "product_subtype": product_subtype},
        "shipment": {"weight": weight, "length": length, "width": width, "height": height, "volume": volume, "surface_area": surface_area, "oversized": oversized},
        "safety_specs": {"geometry": geometry, "precision_surface": precision_surface, "high_value": high_value, "export": export, "uneven_cg": uneven_cg, "projecting_parts": projecting_parts},
        "logistics": {"lifting_method": lifting_method, "base_support": base_support},
        "engineering": {"drawing_required": engineering_drawing, "material_planning": material_planning, "approval_status": engineering_approval},
        "historical_analysis": {"jobs_found": len(history), "consensus_count": consensus_count, "jobs": history},
        "decision": {"recommended_packaging": final_packaging, "decision_source": decision_source, "decision_reason": decision_reason}
    }


def recommend_packaging(product_type, product_subtype, weight, length, width, height, 
                        geometry, precision_surface, high_value, export, 
                        uneven_cg, projecting_parts):
    
    # =====================================
    # 1. DERIVED FEATURES & CRITERIA VALIDATIONS
    # =====================================
    volume = round((length * width * height) / 1_000_000_000, 2)
    surface_area = round(
        2 * (
            (length / 1000) * (width / 1000) +
            (width / 1000) * (height / 1000) +
            (length / 1000) * (height / 1000)
        ), 2
    )
    oversized = "Yes" if (length > 6000 or width > 3000 or height > 3000) else "No"
    
    # Auto-calculating logistics handling constraints based on engineering scale matrices
    if weight > 15000:
        lifting_method = "Heavy Crane"
        base_support = "Heavy Steel Skid"
    elif weight > 1000:
        lifting_method = "EOT Crane"
        base_support = "Steel Base"
    elif weight > 500:
        lifting_method = "Crane"
        base_support = "Wooden Skid Frame"
    elif weight >= 20:
        lifting_method = "Forklift"
        base_support = "Wooden Skid Frame"
    else:
        lifting_method = "Manual"
        base_support = "Foam"

    engineering_drawing = "Required" if (oversized == "Yes" or weight > 1000 or high_value == "Yes") else "Not Required"
    material_planning = "Required" if (oversized == "Yes" or weight > 500) else "Not Required"
    engineering_approval = "Pending" if engineering_drawing == "Required" else "Not Required"

    # =====================================
    # 2. HISTORICAL SEARCH
    # =====================================
    try:
        history = get_similar_packaging(
            weight, length, width, height, 
            geometry, high_value, export, lifting_method
        )
    except Exception:
        history = []

    # =====================================
    # 3. HISTORICAL CONSENSUS ANALYSIS ENGINE
    # =====================================
    if history:
        counts = Counter(job["packaging_type"] for job in history)
        final_packaging = counts.most_common(1)[0][0]
        consensus_count = counts.most_common(1)[0][1]
        decision_source = "Historical Packaging Records"
        decision_reason = f"{consensus_count} out of {len(history)} similar jobs matching this profile used {final_packaging}."
    else:
        decision_source = "Static Safety Matrix Fallback"
        if weight > 15000:
            final_packaging = "Customized Structural Frame"
        elif weight > 1000:
            final_packaging = "Fabricated Steel Frame"
        elif weight > 100:
            final_packaging = "Reinforced Wooden Box"
        else:
            final_packaging = "Corrugated Box"
        consensus_count = 0
        decision_reason = "No closely matching structural patterns found in history. Applied engineering rule matrices."

    return {
        "meta": {
            "product_type": product_type,
            "product_subtype": product_subtype
        },
        "shipment": {
            "weight": weight,
            "length": length,
            "width": width,
            "height": height,
            "volume": volume,
            "surface_area": surface_area,
            "oversized": oversized
        },
        "safety_specs": {
            "geometry": geometry,
            "precision_surface": precision_surface,
            "high_value": high_value,
            "export": export,
            "uneven_cg": uneven_cg,
            "projecting_parts": projecting_parts
        },
        "logistics": {
            "lifting_method": lifting_method,
            "base_support": base_support
        },
        "engineering": {
            "drawing_required": engineering_drawing,
            "material_planning": material_planning,
            "approval_status": engineering_approval
        },
        "historical_analysis": {
            "jobs_found": len(history),
            "consensus_count": consensus_count,
            "jobs": history
        },
        "decision": {
            "recommended_packaging": final_packaging,
            "decision_source": decision_source,
            "decision_reason": decision_reason
        }
    }


def generate_packaging_summary(result):
    # =====================================
    # 4. STRUCTURED EVIDENCE COMPILER
    # =====================================
    jobs = result["historical_analysis"]["jobs"]
    job_history_str = ""
    
    for idx, job in enumerate(jobs, 1):
        job_history_str += (
            f"Job {idx}\n"
            f"Weight : {job['weight']} Kg\n"
            f"Dimensions : {job['length']} × {job['width']} × {job['height']} mm\n"
            f"Packaging : {job['packaging_type']}\n\n"
        )

    # Base UI layout block output parameters
    report_header = (
        f"Recommended Packaging\n------------------------------\n{result['decision']['recommended_packaging']}\n\n"
        f"Recommendation Source\n------------------------------\n{result['decision']['decision_source']}\n\n"
        f"Historical Evidence\n------------------------------\nFound {result['historical_analysis']['jobs_found']} similar completed packaging jobs.\n\n"
        f"{job_history_str.strip()}\n\n"
        f"Historical Consensus\n------------------------------\n{result['historical_analysis']['consensus_count']} out of {result['historical_analysis']['jobs_found']} similar jobs used {result['decision']['recommended_packaging']}.\n\n"
        f"AI Professional Justification & Field Analysis\n------------------------------\n"
    )

    # Clean LLM context layout detailing prompt requirements
    prompt = f"""
System Input Payload Summary:
- Product Type: {result['meta']['product_type']}
- Product Subtype: {result['meta']['product_subtype']}
- Weight: {result['shipment']['weight']} Kg
- Dimensions: {result['shipment']['length']} × {result['shipment']['width']} × {result['shipment']['height']} mm
- Volume: {result['shipment']['volume']} m³
- Surface Area: {result['shipment']['surface_area']} m²
- Geometry: {result['safety_specs']['geometry']}
- Precision Surface: {result['safety_specs']['precision_surface']}
- High Value Asset: {result['safety_specs']['high_value']}
- Export Bound: {result['safety_specs']['export']}
- Uneven Center of Gravity (CG): {result['safety_specs']['uneven_cg']}
- Projecting Parts: {result['safety_specs']['projecting_parts']}
- Derived Handling/Lifting Method: {result['logistics']['lifting_method']}
- Derived Base Support Structure: {result['logistics']['base_support']}
- Engineering Drawing Required: {result['engineering']['drawing_required']}
- Engineering Approval Status: {result['engineering']['approval_status']}
- Recommended Packaging Type: {result['decision']['recommended_packaging']}

Write a detailed, formal engineering justification report for the user. 
You MUST explicitly break down the explanation to address how the following specific fields influenced the final decision:
1. Uneven_CG & Projecting_Parts: Explain how weight distribution shifts and fragile outcroppings mandate internal cushioning, tie-downs, or specialized base supports.
2. Derived Lifting_Method & Base_Support: Explain how the calculated handling mechanism (e.g., Crane, Forklift) and foundational frame (e.g., Skid, Foam) safely carry the physical load parameters.
3. Engineering_Drawing_Required & Engineering_Approval: Detail the mandatory technical safety checks and design validation protocols triggered by these statuses.
4. Final Packaging_Type: Conclude with why this specific container style represents the most structurally sound choice based on similar historical database jobs.

Do not use conversational greetings, introductory text, or repeat raw data tables. Write plain, authoritative facts.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional industrial logistics safety compliance officer. Provide an objective, highly detailed, data-validated engineering justification broken down clearly by operational topics. Do not use generic conversational text."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return report_header + response.choices[0].message.content.strip()
    except Exception:
        return report_header + CONTACT_INFO
