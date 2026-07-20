from database.data_lookup_db import (
    get_route,
    get_all_origins,
    get_destinations,
    get_vehicle_details,
    get_transporter_details
)
from database.db import get_connection
def normalize(value):
    """Strips whitespace and normalizes string values to uppercase for robust indexing."""
    return str(value).strip().upper() if value is not None else ""

def row_to_dict(row):
    """Converts a database row object to a standard Python dictionary."""
    return dict(row) if row is not None else None
# ROUTES
def lookup_route(origin="", destination=""):
    """
    Looks up route details based on origin and/or destination.
    """
    origin = normalize(origin)
    destination = normalize(destination)
    # Case 1: Both origin and destination are provided
    if origin and destination:
        route = get_route(origin, destination)
        if not route:
            return {"error": f"Route not found from '{origin}' to '{destination}'"}
        return row_to_dict(route)

    # Case 2: Only origin is provided (Find all available destinations)
    if origin and not destination:
        destinations = get_destinations(origin)
        if not destinations:
            return []
        
        # Optimized: Fetches and converts valid routes in a single pass
        routes = [get_route(origin, dest) for dest in destinations]
        return [row_to_dict(r) for r in routes if r is not None]

    # Case 3: Missing required parameters
    return {"error": "Provide at least an origin to search routes"}

def add_route(origin, destination, distance_km):
    origin = normalize(origin)
    destination = normalize(destination)
    conn = get_connection()

    try:
        existing = conn.execute(
            """
            SELECT 1
            FROM distances
            WHERE
                UPPER(origin)=?
                AND UPPER(destination)=?
            """,
            (origin, destination)
        ).fetchone()

        if existing:
            return {
                "success": False,
                "message": "Route already exists."
            }

        conn.execute(
            """
            INSERT INTO distances (origin, destination, distance_km)
            VALUES (?, ?, ?)
            """,
            (origin, destination, distance_km)
        )
        conn.commit()
        return {
            "success": True,
            "message": "Route added successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()


def update_route(origin, destination, distance_km):
    origin = normalize(origin)
    destination = normalize(destination)
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE distances
            SET distance_km=?
            WHERE
                UPPER(origin)=?
                AND UPPER(destination)=?
            """,
            (distance_km, origin, destination)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "Route not found."
            }

        return {
            "success": True,
            "message": "Route updated successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()


def delete_route(origin, destination):
    origin = normalize(origin)
    destination = normalize(destination)
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            DELETE FROM distances
            WHERE
                UPPER(origin)=?
                AND UPPER(destination)=?
            """,
            (origin, destination)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "Route not found."
            }

        return {
            "success": True,
            "message": "Route deleted successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()

# VEHICLES
def lookup_vehicle(vehicle_name):
    """
    Retrieves vehicle specification details by name.
    """
    vehicle_name = normalize(vehicle_name)
    if not vehicle_name:
        return {"error": "Vehicle name is required"}
        
    vehicle = get_vehicle_details(vehicle_name)
    if not vehicle:
        return {"error": f"Vehicle '{vehicle_name}' not found"}

    return row_to_dict(vehicle)


def add_vehicle(vehicle_name, category, max_weight_mt, axles, odc_allowed):
    vehicle_name = normalize(vehicle_name)
    conn = get_connection()

    try:
        existing = conn.execute(
            """
            SELECT 1
            FROM vehicles
            WHERE UPPER(Vehicle_Name)=?
            """,
            (vehicle_name,)
        ).fetchone()

        if existing:
            return {
                "success": False,
                "message": "Vehicle already exists."
            }

        conn.execute(
            """
            INSERT INTO vehicles (Vehicle_Name, Category, Max_Weight_MT, Axles, ODC_Allowed)
            VALUES (?, ?, ?, ?, ?)
            """,
            (vehicle_name, category, max_weight_mt, axles, odc_allowed)
        )
        conn.commit()
        return {
            "success": True,
            "message": "Vehicle added successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()


def update_vehicle(vehicle_name, category, max_weight_mt, axles, odc_allowed):
    vehicle_name = normalize(vehicle_name)
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE vehicles
            SET
                Category=?,
                Max_Weight_MT=?,
                Axles=?,
                ID_Allowed=?   -- Matches DB field structural references if necessary, or change back to explicit column name
                ODC_Allowed=?
            WHERE UPPER(Vehicle_Name)=?
            """,
            (category, max_weight_mt, axles, odc_allowed, vehicle_name)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "Vehicle not found."
            }

        return {
            "success": True,
            "message": "Vehicle updated successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()


def delete_vehicle(vehicle_name):
    vehicle_name = normalize(vehicle_name)
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            DELETE FROM vehicles
            WHERE UPPER(Vehicle_Name)=?
            """,
            (vehicle_name,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "Vehicle not found."
            }

        return {
            "success": True,
            "message": "Vehicle deleted successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()

# TRANSPORTERS
def lookup_transporter(name):
    """
    Retrieves transporter profiles by name.
    """
    name = normalize(name)
    if not name:
        return {"error": "Transporter name is required"}

    transporter = get_transporter_details(name)
    if not transporter:
        return {"error": f"Transporter '{name}' not found"}

    return row_to_dict(transporter)


def add_transporter(transporter, category, msme_status, iba_code, iba_validity):
    transporter = normalize(transporter)
    conn = get_connection()

    try:
        existing = conn.execute(
            """
            SELECT 1
            FROM transporters
            WHERE UPPER(Transporter)=?
            """,
            (transporter,)
        ).fetchone()

        if existing:
            return {
                "success": False,
                "message": "Transporter already exists."
            }

        conn.execute(
            """
            INSERT INTO transporters (Transporter, Category, [MSME Status], [IBA Code], [IBA Validity])
            VALUES (?, ?, ?, ?, ?)
            """,
            (transporter, category, msme_status, iba_code, iba_validity)
        )
        conn.commit()
        return {
            "success": True,
            "message": "Transporter added successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()


def update_transporter(transporter, category, msme_status, iba_code, iba_validity):
    transporter = normalize(transporter)
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE transporters
            SET
                Category=?,
                [MSME Status]=?,
                [IBA Code]=?,
                [IBA Validity]=?
            WHERE UPPER(Transporter)=?
            """,
            (category, msme_status, iba_code, iba_validity, transporter)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "Transporter not found."
            }

        return {
            "success": True,
            "message": "Transporter updated successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()


def delete_transporter(transporter):
    transporter = normalize(transporter)
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            DELETE FROM transporters
            WHERE UPPER(Transporter)=?
            """,
            (transporter,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "Transporter not found."
            }

        return {
            "success": True,
            "message": "Transporter deleted successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()
