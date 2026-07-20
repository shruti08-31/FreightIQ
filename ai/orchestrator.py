# orchestrator.py
import os
import re
from groq import Groq

# --- IMPORTS ---
from ai.vehicle_engine import (
    recommend_vehicle, consolidate_shipments, 
    ai_optimize_load_plan, generate_comprehensive_load_profile
)
from ai.route_optimizer import find_route
from ai.packaging_engine import recommend_packaging 
from ai.odc_checker import check_odc_all
from ai.data_lookup_engine import lookup_vehicle, lookup_transporter
from ai.analytics import get_dashboard_metrics, route_statistics, get_transporter_counts
from ai.axle_calculator import recommend_axles

# Initialize LLM strictly for explanation
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- 1. INTENT & EXTRACTION (Unchanged) ---
def extract_shipment_details(text):
    details = {}
    weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(MT|kg|KG|tonne|tonnes|tons|metric\s*ton|metric\s*tons)", text, re.IGNORECASE)
    if weight_match:
        val = float(weight_match.group(1))
        unit = weight_match.group(2).lower()
        details["weight"] = val / 1000.0 if "kg" in unit else val

    dim_match = re.search(r"(\d+)\s*[xX×\*]\s*(\d+)\s*[xX×\*]\s*(\d+)", text)
    if dim_match:
        details["length"], details["width"], details["height"] = int(dim_match.group(1)), int(dim_match.group(2)), int(dim_match.group(3))

    route_match = re.search(r"(?:from|between)\s+([A-Za-z ]+)\s+(?:to|and)\s+([A-Za-z ]+)", text, re.IGNORECASE)
    if route_match:
        details["origin"], details["destination"] = route_match.group(1).strip().upper(), route_match.group(2).strip().upper()
    return details

def detect_intent(user_query, shipment_data):
    q = user_query.lower()
    return {
        "packaging": any(w in q for w in ["package", "packaging", "box", "skid"]),
        "odc": "odc" in q or (all(k in shipment_data for k in ["length", "width", "height"]) and "recommend" not in q),
        "optimize": any(w in q for w in ["optimize", "consolidate", "load plan", "multiple", "combine"]),
        "vehicle": any(w in q for w in ["recommend", "allocation", "vehicle", "asset"]) and not any(w in q for w in ["optimize", "consolidate", "load plan"]),
        "route": "route" in q or ("from" in q and "to" in q),
        "lookup": any(w in q for w in ["transporter", "transport", "details"]),
        "analytics": any(w in q for w in ["dashboard", "analytics", "statistics"]),
        "axle": "axle" in q
    }

# --- 2. AI EXPLANATION LAYER ---
def format_context_data(user_query, shipment_data, primary_intent, context):
    """Formats the raw Python dictionary into a human-readable text block for the LLM."""
    
    if primary_intent == "vehicle" and "vehicle" in context:
        v = context["vehicle"]
        return f"""Original User Query:
{user_query}

Shipment Details
Weight : {shipment_data.get('weight', 'N/A')} MT
Length : {shipment_data.get('length', 'N/A')} mm
Width  : {shipment_data.get('width', 'N/A')} mm
Height : {shipment_data.get('height', 'N/A')} mm

Database Recommendation
Vehicle : {v.get('vehicle', 'N/A')}
Category : {v.get('category', 'N/A')}
Maximum Weight : {v.get('max_weight', 'N/A')} MT
Maximum Length : {v.get('length_capacity', 'N/A')} mm
Maximum Width  : {v.get('width_capacity', 'N/A')} mm
Maximum Height : {v.get('height_capacity', 'N/A')} mm
ODC Allowed    : {v.get('odc_allowed', 'N/A')}
ODC Required   : {v.get('odc_required', 'N/A')}
Alternative Vehicle : {v.get('alternative_vehicle', 'None')}
Alternative Category: {v.get('alternative_category', 'None')}

Explain why this recommendation satisfies the user's request.
"""
    
    # Generic formatter for non-vehicle intents to still include the query context
    return f"""Original User Query:
{user_query}

Database Recommendation:
{str(context)}

Explain why this recommendation satisfies the user's request.
"""

def explain_with_llm(user_query, shipment_data, primary_intent, structured_data):
    """Generates a professional explanation based on strictly formatted database output."""
    
    # Strict prompt templates based on your exact requirements
    prompts = {
        "vehicle": """You are a Logistics Planning Assistant.

The recommendation has ALREADY been made by the database and Python engine.

Never explain database field names.

Instead explain the engineering reason.

Mention:
• weight capacity
• length capacity
• width capacity
• height capacity
• ODC compatibility
• if an alternative vehicle exists explain why.

Do not mention vehicle_suitable, odc_required, category ids, dictionary keys, boolean values.

Never invent information.

Maximum 6 bullet points.""",

        "route": """Use ONLY this information.
Explain why this route is shown.
Do not assume any other route details or distances.""",

        "packaging": """Use ONLY this packaging data.
Explain:
- why this packaging was selected
- why engineering drawing is required (if applicable)
- why material planning is required (if applicable)
- summarize recommendations
Do not assume product type.""",

        "lookup": """Explain this transporter/vehicle information using only the database values.
Do not assume availability or experience.""",

        "analytics": """Summarize these logistics statistics.
Do not create additional numbers. Explain what these values indicate."""
    }

    system_prompt = prompts.get(
        primary_intent, 
        "You are a logistics assistant. Explain the following structured data clearly. Do not invent information."
    )
    
    formatted_prompt = format_context_data(user_query, shipment_data, primary_intent, structured_data)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.0 # Force deterministic output; no creative liberties
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"System processed the data successfully, but the explanation layer failed. Raw data: {structured_data}"


# --- 3. MAIN WORKFLOW ---
def process_query(user_query, shipments_payload=None):
    shipment_data = extract_shipment_details(user_query)
    intent = detect_intent(user_query, shipment_data)
    
    context = {}
    primary_intent = "general"

    # Step A: Python Business Logic -> SQLite Database
    if intent["optimize"]:
        if shipments_payload and isinstance(shipments_payload, list):
            raw_plan = ai_optimize_load_plan(shipments_payload) if "optimize" in user_query.lower() else consolidate_shipments(shipments_payload)
            context["optimization"] = generate_comprehensive_load_profile(raw_plan) if "error" not in raw_plan else raw_plan
            primary_intent = "optimization"

    elif intent["vehicle"] and all(k in shipment_data for k in ["weight", "length", "width", "height"]):
        context["vehicle"] = recommend_vehicle(shipment_data["weight"], shipment_data["length"], shipment_data["width"], shipment_data["height"])
        primary_intent = "vehicle"

    elif intent["route"] and "origin" in shipment_data and "destination" in shipment_data:
        context["route"] = find_route(shipment_data["origin"], shipment_data["destination"])
        primary_intent = "route"

    elif intent["packaging"]:
        context["packaging"] = recommend_packaging("Industrial Equipment", "Components", shipment_data.get("weight", 0) * 1000, shipment_data.get("length", 0), shipment_data.get("width", 0), shipment_data.get("height", 0))
        primary_intent = "packaging"

    elif intent["lookup"]:
        context["lookup"] = lookup_transporter(user_query) if "transporter" in user_query.lower() else lookup_vehicle(user_query)
        primary_intent = "lookup"

    elif intent["analytics"]:
        context["analytics"] = {"dashboard": get_dashboard_metrics(), "route_stats": route_statistics(), "transporter_stats": get_transporter_counts()}
        primary_intent = "analytics"
        
    elif intent["odc"] and all(k in shipment_data for k in ["length", "width", "height"]):
        context["odc"] = check_odc_all(shipment_data["length"], shipment_data["width"], shipment_data["height"])
        primary_intent = "vehicle" # Uses the vehicle prompt constraints
        
    elif intent["axle"] and "weight" in shipment_data:
        context["axle"] = recommend_axles(shipment_data["weight"])
        primary_intent = "vehicle"

    # Handle case where no DB match was triggered
    if not context:
        return "I couldn't identify the specific logistics parameters (like exact dimensions, weight, or route) required to query the database. Please provide more details."

    # Step B: Pass structured data and context to AI Explanation Layer
    final_explanation = explain_with_llm(user_query, shipment_data, primary_intent, context)
    
    return final_explanation
