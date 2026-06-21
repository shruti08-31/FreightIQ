from database.db import get_connection


def recommend_vehicle(
    weight,
    length,
    width,
    height
):
    conn = get_connection()

    try:

        # =====================================================
        # PRIMARY VEHICLE SELECTION (LOGISTICS PIPELINE STEP 1)
        # =====================================================
        # Pehle cargo mass load distribution ke hisaab se primary asset benchmark karo
        vehicle = conn.execute(
            """
            SELECT *
            FROM vehicles
            WHERE
                ? BETWEEN Min_Weight_MT
                AND Max_Weight_MT
            ORDER BY Max_Weight_MT ASC
            LIMIT 1
            """,
            (weight,)
        ).fetchone()

        if not vehicle:
            return {
                "error": "No suitable vehicle found for the given shipment profile."
            }

        # =====================================================
        # ODC CHECK (LOGISTICS PIPELINE STEP 2)
        # =====================================================
        # Vehicle specifications aur real shipment physical bounds ko match karke check karo
        odc_required = (
            length > vehicle["Length_mm"]
            or width > vehicle["Width_mm"]
            or height > vehicle["Height_mm"]
        )

        vehicle_suitable = True

        alternative_vehicle = None
        alternative_category = None
        alternative_axles = None

        # =====================================================
        # ADVANCED HYDRAULIC ESCALATION LOGIC (PROBLEM 2 FIX)
        # =====================================================
        if odc_required and vehicle["ODC_Allowed"] == "No":

            vehicle_suitable = False

            # Fixed: Is query se strict weight bounding hatayi gayi hai taaki lightweight, 
            # par massive structural dimensions wale cargo ko directly cross-match kiya ja sake.
            alternative = conn.execute(
                """
                SELECT *
                FROM vehicles
                WHERE
                    ODC_Allowed='Yes'
                    AND Length_mm >= ?
                    AND Width_mm >= ?
                    AND Height_mm >= ?
                ORDER BY Max_Weight_MT ASC
                LIMIT 1
                """,
                (
                    length,
                    width,
                    height
                )
            ).fetchone()

            if alternative:
                alternative_vehicle = alternative["Vehicle_Name"]
                alternative_category = alternative["Category"]
                alternative_axles = alternative["Axles"]

        # =====================================================
        # CAPACITY CALCULATIONS
        # =====================================================
        vehicle_volume_capacity = round(
            (
                vehicle["Length_mm"]
                * vehicle["Width_mm"]
                * vehicle["Height_mm"]
            ) / 1000000000,
            2
        )

        shipment_volume = round(
            (
                length
                * width
                * height
            ) / 1000000000,
            2
        )

        utilization_pct = round(
            (
                weight /
                vehicle["Max_Weight_MT"]
            ) * 100,
            1
        )

        utilization_pct = min(utilization_pct, 100)

        # =====================================================
        # STRUCTURAL SYSTEM RESPONSE
        # =====================================================
        return {
            "vehicle": vehicle["Vehicle_Name"],
            "category": vehicle["Category"],
            "axles": vehicle["Axles"],
            
            "min_weight": vehicle["Min_Weight_MT"],
            "max_weight": vehicle["Max_Weight_MT"],
            
            "length_capacity": vehicle["Length_mm"],
            "width_capacity": vehicle["Width_mm"],
            "height_capacity": vehicle["Height_mm"],
            
            "vehicle_volume_capacity": vehicle_volume_capacity,
            "shipment_volume": shipment_volume,
            
            "odc_allowed": vehicle["ODC_Allowed"],
            "odc_required": odc_required,
            "vehicle_suitable": vehicle_suitable,
            "utilization_percent": utilization_pct,
            
            "alternative_vehicle": alternative_vehicle,
            "alternative_category": alternative_category,
            "alternative_axles": alternative_axles
        }

    finally:
        conn.close()