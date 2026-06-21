import os

import re



import google.generativeai as genai



from dotenv import load_dotenv



from ai.vehicle_engine import recommend_vehicle

from ai.route_optimizer import recommend_route

from ai.odc_checker import check_odc



from ai.analytics import (

    get_dashboard_metrics,

    route_statistics,

    get_transporter_counts

)



load_dotenv()



genai.configure(

    api_key=os.getenv("GEMINI_API_KEY")

)



model = genai.GenerativeModel(

    "gemini-2.5-flash"

)



# =====================================================

# CONTACT INFO

# =====================================================



CONTACT_INFO = """

Information is not available in the current CDX database.



Please contact:



HEEP - Heavy Electrical Equipment Plant

BHEL, Haridwar, Uttarakhand - 249403



CFFP - Central Foundry Forge Plant

BHEL, Haridwar, Uttarakhand - 249403



PCRI - Pollution Control Research Institute

Sector 5A, BHEL, Haridwar, Uttarakhand - 249403



GSTIN: 05AAACB4146P1ZL



Corporate Office:

BHEL House, Siri Fort,

New Delhi - 110049, India

"""





# =====================================================

# EXTRACT QUERY DATA

# =====================================================



def extract_shipment_details(text):



    details = {}



    weight_match = re.search(

        r"(\d+(?:\.\d+)?)\s*MT",

        text,

        re.IGNORECASE

    )



    if weight_match:

        details["weight"] = float(weight_match.group(1))



    dim_match = re.search(

        r"(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+)",

        text

    )



    if dim_match:



        details["length"] = int(dim_match.group(1))

        details["width"] = int(dim_match.group(2))

        details["height"] = int(dim_match.group(3))



    route_match = re.search(

        r"from\s+([A-Za-z ]+)\s+to\s+([A-Za-z ]+)",

        text,

        re.IGNORECASE

    )



    if route_match:



        details["origin"] = (

            route_match.group(1)

            .strip()

            .upper()

        )



        details["destination"] = (

            route_match.group(2)

            .strip()

            .upper()

        )



    else:



        route_match = re.search(

            r"between\s+([A-Za-z ]+)\s+and\s+([A-Za-z ]+)",

            text,

            re.IGNORECASE

        )



        if route_match:



            details["origin"] = (

                route_match.group(1)

                .strip()

                .upper()

            )



            details["destination"] = (

                route_match.group(2)

                .strip()

                .upper()

            )



    return details





# =====================================================

# MAIN AI RESPONSE

# =====================================================



def get_ai_response(user_query):



    dashboard = get_dashboard_metrics()

    route_stats = route_statistics()

    transporter_stats = get_transporter_counts()



    shipment_data = extract_shipment_details(

        user_query

    )



    vehicle_result = None

    odc_result = None

    route_result = None



    # ==========================================

    # VEHICLE + ODC

    # ==========================================



    required = [

        "weight",

        "length",

        "width",

        "height"

    ]



    if all(

        field in shipment_data

        for field in required

    ):



        try:



            vehicle_result = recommend_vehicle(

                shipment_data["weight"],

                shipment_data["length"],

                shipment_data["width"],

                shipment_data["height"]

            )



            if (

                vehicle_result

                and "category" in vehicle_result

            ):



                odc_result = check_odc(

                    shipment_data["length"],

                    shipment_data["width"],

                    shipment_data["height"],

                    vehicle_result["category"]

                )



        except Exception:



            return CONTACT_INFO



    # ==========================================

    # ROUTE LOOKUP

    # ==========================================



    if (

        "origin" in shipment_data

        and "destination" in shipment_data

    ):



        try:



            route_result = recommend_route(

                shipment_data["origin"],

                shipment_data["destination"]

            )



            if (

                route_result is None

                or "error" in str(route_result).lower()

            ):

                return CONTACT_INFO



        except Exception:

            return CONTACT_INFO



 # ==========================================

    # PURE ANALYTICS QUESTION

    # ==========================================



    prompt = f"""

You are CDX AI Logistics Assistant.



IMPORTANT RULES:



1. Use ONLY the supplied database results.

2. Never generate or assume any logistics data.

3. Never create routes.

4. Never create vehicles.

5. Never create transporter information.

6. DYNAMIC SECTIONS: Only display a section header if there is valid data available for it. If a section's corresponding database result is None or missing, completely omit (do not display) both the section header and its content.

7. Explain data professionally.

8. Keep answers concise and business focused.

9. REVERSE ROUTE HANDLING: If the Route dictionary contains 'reverse_route': True, explicitly explain that the requested route direction was not directly available in the database, but the reverse corridor exists. Mention that the same corridor distance may be considered for planning purposes, subject to operational and route validation.



User Query:

{user_query}



Database Results



Dashboard:

{dashboard}



Route Statistics:

{route_stats}



Transporters:

{transporter_stats}



Shipment:

{shipment_data}



Vehicle:

{vehicle_result}



ODC:

{odc_result}



Route:

{route_result}



Provide only the applicable sections from this list (omit if no data exists):

### Shipment Summary

### Vehicle Analysis

### ODC Assessment

### Route Analysis

### Logistics Insights

### Final Recommendation

"""



    try:



        response = model.generate_content(

            prompt

        )



        return response.text



    except Exception:



        return CONTACT_INFO 

