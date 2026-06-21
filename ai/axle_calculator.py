from ai.vehicle_engine import recommend_vehicle


def recommend_axles(weight):

    vehicles = recommend_vehicle(weight)

    if not vehicles:
        return None

    vehicle = vehicles[0]

    return {
        "vehicle": vehicle["Vehicle_Name"],
        "min_axles": vehicle["Min_Axles"],
        "max_axles": vehicle["Max_Axles"]
    }