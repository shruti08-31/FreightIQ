from database.db import get_connection


def check_odc(
    length,
    width,
    height,
    vehicle_category
):

    conn = get_connection()

    vehicle = conn.execute(
        """
        SELECT *
        FROM vehicles
        WHERE Category = ?
        """,
        (vehicle_category,)
    ).fetchone()

    conn.close()

    if not vehicle:

        return {
            "odc_required": True,
            "vehicle_suitable": False,
            "reason": "Vehicle not found"
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
        "odc_allowed": vehicle["ODC_Allowed"]
    }