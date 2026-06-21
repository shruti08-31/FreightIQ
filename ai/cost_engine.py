from ai.odc_checker import check_odc


def estimate_cost(
    distance,
    rate_per_km,
    length,
    width,
    height,
    vehicle_category,
    odc_charge=0
):

    odc_result = check_odc(
        length,
        width,
        height,
        vehicle_category
    )

    transport_cost = distance * rate_per_km

    total_cost = transport_cost

    if odc_result["odc_required"]:
        total_cost += odc_charge

    return {

        "distance": distance,

        "rate_per_km": rate_per_km,

        "transport_cost": transport_cost,

        "odc_required": odc_result["odc_required"],

        "odc_charge": odc_charge,

        "total_cost": round(total_cost, 2)
    }