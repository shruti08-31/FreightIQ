from database.db import get_connection

# DISTANCE LOOKUP
def get_route(origin, destination):

    conn = get_connection()

    route = conn.execute(
        """
        SELECT *
        FROM distances
        WHERE
            UPPER(origin)=UPPER(?)
            AND UPPER(destination)=UPPER(?)
        """,
        (origin, destination)
    ).fetchone()

    conn.close()

    return route


def get_all_origins():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT DISTINCT origin
        FROM distances
        ORDER BY origin
        """
    ).fetchall()

    conn.close()

    return [r["origin"] for r in rows]


def get_destinations(origin):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT DISTINCT destination
        FROM distances
        WHERE UPPER(origin)=UPPER(?)
        ORDER BY destination
        """,
        (origin,)
    ).fetchall()

    conn.close()

    return [r["destination"] for r in rows]


# VEHICLES
def get_all_vehicles():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT Vehicle_Name
        FROM vehicles
        ORDER BY Vehicle_Name
        """
    ).fetchall()

    conn.close()

    return [r["Vehicle_Name"] for r in rows]


def get_vehicle_details(vehicle):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM vehicles
        WHERE Vehicle_Name=?
        """,
        (vehicle,)
    ).fetchone()

    conn.close()

    return row
    
# TRANSPORTERS

def get_all_transporters():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT DISTINCT Transporter
        FROM transporters
        ORDER BY Transporter
        """
    ).fetchall()

    conn.close()

    return [r["Transporter"] for r in rows]


def get_transporter_details(name):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM transporters
        WHERE Transporter = ?
        """,
        (name,)
    ).fetchone()

    conn.close()

    return row
