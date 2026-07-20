import os
from collections import Counter
from groq import Groq
from dotenv import load_dotenv
from database.packaging_db import get_similar_packaging

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"
CONTACT_INFO = "Information is not available in the current CDX database."

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
        lifting_method, base_support = "Heavy Crane", "Heavy Steel Skid"
        duty_category = "Ultra-Heavy Duty"
    elif weight > 1000:
        lifting_method, base_support = "EOT Crane", "Steel Base"
        duty_category = "Heavy Duty"
    elif weight > 500:
        lifting_method, base_support = "Crane", "Wooden Skid Frame"
        duty_category = "Medium-Heavy Duty"
    elif weight >= 100:
        lifting_method, base_support = "Forklift", "Wooden Skid Frame"
        duty_category = "Medium Duty"
    elif weight >= 20:
        lifting_method, base_support = "Forklift", "Wooden Skid Frame"
        duty_category = "Light-Medium Duty"
    else:
        lifting_method, base_support = "Manual", "Foam"
        duty_category = "Light Duty"

    # Dynamic reasons for engineering requirements
    if oversized == "Yes":
        drawing_reason = "Oversized Dimensions"
    elif weight > 1000:
        drawing_reason = f"Weight > 1000 kg ({weight} kg)"
    elif high_value == "Yes":
        drawing_reason = "High Value Asset"
    else:
        drawing_reason = "Standard Criteria"

    if oversized == "Yes":
        planning_reason = "Oversized Dimensions"
    elif weight > 500:
        planning_reason = f"Weight > 500 kg ({weight} kg)"
    else:
        planning_reason = "Standard Criteria"

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
        
        confidence_pct = f"{int((consensus_count / len(history)) * 100)}%"
        confidence_reason = f"{consensus_count} out of {len(history)} similar jobs"
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
        
        confidence_pct = "85%"
        confidence_reason = "Matrix Fallback Rules"

    # =====================================
    # 4. DASHBOARD CARDS PREPARATION
    # =====================================
    dashboard_cards = {
        "packaging_type": {
            "title": "Packaging Type",
            "value": final_packaging,
            "subtitle": f"Source: {decision_source}"
        },
        "duty_category": {
            "title": "Category",
            "value": duty_category,
            "subtitle": "Based on weight & load"
        },
        "engineering_drawing": {
            "title": "Engineering Drawing",
            "value": engineering_drawing,
            "subtitle": f"Reason: {drawing_reason}"
        },
        "material_planning": {
            "title": "Material Planning",
            "value": material_planning,
            "subtitle": f"Reason: {planning_reason}"
        },
        "oversized_status": {
            "title": "Oversized",
            "value": oversized,
            "subtitle": "Oversized Cargo" if oversized == "Yes" else "Standard Cargo"
        },
        "model_confidence": {  # Renamed from ai_confidence
            "title": "Model Confidence",
            "value": confidence_pct,
            "subtitle": f"Based on: {confidence_reason}"
        }
    }

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
            "decision_source": decision_source
        },
        "dashboard_cards": dashboard_cards
    }


def generate_packaging_summary(result):
    # =====================================
    # 5. DERIVED ENGINEERING FACTS FOR LLM
    # =====================================
    weight = result['shipment']['weight']
    oversized = result['shipment']['oversized']
    
    heavy_load = "True" if weight > 1000 else "False"
    fragile = "True" if (result['safety_specs']['precision_surface'] == "Yes" or result['safety_specs']['geometry'] == "Complex") else "False"
    complex_geom = "Yes" if result['safety_specs']['geometry'] == "Complex" else "No"
    
    # Restrictive engineering prompt 
    prompt = f"""You are a Senior Industrial Packaging Engineer working for an engineering logistics company.

Your job is NOT to summarize the input.
Produce a professional Packaging Planning Assessment.

Follow EXACTLY this structure.

# Packaging Planning Assessment
Provide a short executive summary.

---

## 1. Packaging Overview
State
- Recommended packaging
- Why it was selected
- Duty classification
- Major risks

---

## 2. Shipment Assessment
Explain
- Weight influence
- Dimension influence
- Volume influence
- Surface area influence
Explain WHY each affects packaging.

---

## 3. Structural Assessment
Discuss
- Geometry
- Uneven center of gravity
- Projecting parts
- Precision surfaces
Explain structural implications.

---

## 4. Material Handling
Explain
- lifting method
- base support
- loading method
- unloading precautions

---

## 5. Protection Requirements
Discuss
- cushioning
- vibration isolation
- moisture protection
- export protection
- corrosion prevention

---

## 6. Engineering Requirements
Discuss
- engineering drawing
- engineering approval
- material planning
Explain why they are required.

---

## 7. Historical Decision Analysis
Use the historical records.
Mention
- number of similar jobs
- consensus percentage
Explain why historical data supports this recommendation.
Never invent statistics.

---

## 8. Final Engineering Recommendation
Write a professional conclusion in 4-6 sentences.
Never use conversational language.
Never say "based on the provided data".
Never repeat values already shown in the dashboard.
Write like an engineering report.
Output in Markdown.

### INTERPRETED ENGINEERING FACTS FOR YOUR ASSESSMENT (DO NOT REPEAT RAW NUMBERS):

Risk Flags:
- Heavy Load = {heavy_load}
- Fragile = {fragile}
- Oversized = {oversized}
- High Value = {result['safety_specs']['high_value']}
- Export = {result['safety_specs']['export']}
- Complex Geometry = {complex_geom}

Engineering Constraints:
- Recommended Packaging = {result['decision']['recommended_packaging']}
- Duty Category = {result['dashboard_cards']['duty_category']['value']}
- Lifting Method = {result['logistics']['lifting_method']}
- Base Support = {result['logistics']['base_support']}
- Engineering Drawing = {result['engineering']['drawing_required']}
- Material Planning = {result['engineering']['material_planning']}

Historical Context:
- Historical Matches = {result['historical_analysis']['jobs_found']}
- Consensus = {result['historical_analysis']['consensus_count']} out of {max(1, result['historical_analysis']['jobs_found'])}
- Model Confidence = {result['dashboard_cards']['model_confidence']['value']}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Senior Industrial Packaging Engineer. Generate objective, highly detailed, data-validated engineering justifications in strict Markdown formatting. Never hallucinate data. Never summarize raw input metrics."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        ai_analysis_text = response.choices[0].message.content.strip()
    except Exception:
        ai_analysis_text = f"# Packaging Planning Assessment\n\n{CONTACT_INFO}"

    # Return clean, structured data for the UI
    return {
        "dashboard_cards": result["dashboard_cards"],
        "historical_table": result["historical_analysis"]["jobs"],
        "ai_analysis": ai_analysis_text
    }


def summarize_report(report_text):
    """
    Called conditionally by the Streamlit frontend if the user requests a summary.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system", 
                    "content": "You are an AI assistant. Extract the 4 to 5 most critical engineering takeaways from the following packaging report. Format strictly as a concise bulleted list. Do not include pleasantries."
                },
                {"role": "user", "content": report_text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Summary generation failed."
