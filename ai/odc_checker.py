from database.db import get_connection


# --- Existing Function (Unchanged) ---
def check_odc(length, width, height, vehicle_category):
    conn = get_connection()

    vehicle = conn.execute(
        """
        SELECT *
        FROM vehicles
        WHERE Category = ?
        """,
        (vehicle_category,),
    ).fetchone()

    conn.close()

    if not vehicle:
        return {
            "odc_required": True,
            "vehicle_suitable": False,
            "reason": "Vehicle not found",
        }

    odc_required = (
        length > vehicle["Length_mm"]
        or width > vehicle["Width_mm"]
        or height > vehicle["Height_mm"]
    )

    vehicle_suitable = True

    if odc_required and vehicle["ODC_Allowed"] != "Yes":
        vehicle_suitable = False

    return {
        "odc_required": odc_required,
        "vehicle_suitable": vehicle_suitable,
        "vehicle": vehicle["Vehicle_Name"],
        "category": vehicle["Category"],
        "odc_allowed": vehicle["ODC_Allowed"],
    }


# --- New Function (For Global ODC Check) ---
def check_odc_all(length, width, height):
    # Static list of vehicles and their standard & maximum dimensions (in mm) based on BHEL tender PDFs
    vehicles = [
        {
            "Vehicle_Name": "Category D (Mini Truck)",
            "Category": "D",
            "Length_mm": 3960,
            "Width_mm": 1800,
            "Height_mm": 2000,
            "Max_Length_mm": 3960,  # No ODC allowed
            "Max_Width_mm": 1800,   # No ODC allowed
            "Max_Height_mm": 2000,  # No ODC allowed
            "ODC_Allowed": "No"
        },
        {
            "Vehicle_Name": "Category A1/A2 Truck",
            "Category": "A1/A2",
            "Length_mm": 4880,
            "Width_mm": 2050,
            "Height_mm": 2050,
            "Max_Length_mm": 4880,  # No length ODC allowed
            "Max_Width_mm": 2050,   # No width ODC allowed
            "Max_Height_mm": 2500,  # ODC allowed up to 2.5m
            "ODC_Allowed": "Yes"
        },
        {
            "Vehicle_Name": "Category A3 Truck (Taurus)",
            "Category": "A3",
            "Length_mm": 6700,
            "Width_mm": 2050,
            "Height_mm": 2050,
            "Max_Length_mm": 6700,  # No length ODC allowed
            "Max_Width_mm": 2050,   # No width ODC allowed
            "Max_Height_mm": 2500,  # ODC allowed up to 2.5m
            "ODC_Allowed": "Yes"
        },
        {
            "Vehicle_Name": "Category C1/C2/C3 Trailer",
            "Category": "Trailer",
            "Length_mm": 12200,
            "Width_mm": 2600,
            "Height_mm": 2500,
            "Max_Length_mm": 17500, # ODC up to 17.5m
            "Max_Width_mm": 6000,   # ODC up to 6.0m
            "Max_Height_mm": 3500,  # ODC up to 3.5m
            "ODC_Allowed": "Yes"
        },
        {
            "Vehicle_Name": "Category C1H/C2H/C3H High Trailer",
            "Category": "High Trailer",
            "Length_mm": 12200,
            "Width_mm": 2600,
            "Height_mm": 3500,
            "Max_Length_mm": 17500,
            "Max_Width_mm": 6000,
            "Max_Height_mm": 5000,  # ODC up to 5.0m
            "ODC_Allowed": "Yes"
        },
        {
            "Vehicle_Name": "Category H1/H2/H3/H4 Hydraulic Trailer",
            "Category": "Hydraulic",
            "Length_mm": 15500,     # Base platform length reference
            "Width_mm": 4500,
            "Height_mm": 3500,
            "Max_Length_mm": 99999, # Depends on axles deployed, dynamically scaling
            "Max_Width_mm": 6000,   # ODC up to 6.0m
            "Max_Height_mm": 5000,  # ODC up to 5.0m
            "ODC_Allowed": "Yes"
        }
    ]

    results = []
    suitable = []

    for vehicle in vehicles:
        # Check if dimensions exceed the standard dimensions (ODC condition)
        is_odc = (length > vehicle["Length_mm"] or 
                  width > vehicle["Width_mm"] or 
                  height > vehicle["Height_mm"])
        
        vehicle_ok = True
        
        # Check if it fits within absolute maximum limits (whether ODC or standard)
        if (length > vehicle["Max_Length_mm"] or 
            width > vehicle["Max_Width_mm"] or 
            height > vehicle["Max_Height_mm"]):
            vehicle_ok = False
        
        # Verify ODC restrictions
        if is_odc and vehicle["ODC_Allowed"] != "Yes":
            vehicle_ok = False

        result = {
            "vehicle": vehicle["Vehicle_Name"],
            "category": vehicle["Category"],
            "odc_required": is_odc,
            "vehicle_suitable": vehicle_ok,
            "odc_allowed": vehicle["ODC_Allowed"],
        }
        results.append(result)
        
        if vehicle_ok:
            suitable.append(result)

    return {
        "odc_required": any(r["odc_required"] for r in results),
        "total_vehicles": len(results),
        "suitable_vehicles": suitable,
        "all_results": results,
    }
