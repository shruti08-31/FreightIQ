from database.db import get_connection


def recommend_route(
    origin,
    destination
):

    conn = get_connection()

    route = conn.execute(
        """
        SELECT *
        FROM distances
        WHERE UPPER(origin)=UPPER(?)
        AND UPPER(destination)=UPPER(?)
        """,
        (origin, destination)
    ).fetchone()

    if route:

        conn.close()

        return dict(route)

    # =====================================
    # REVERSE ROUTE CHECK
    # =====================================

    route = conn.execute(
        """
        SELECT *
        FROM distances
        WHERE UPPER(origin)=UPPER(?)
        AND UPPER(destination)=UPPER(?)
        """,
        (destination, origin)
    ).fetchone()

    if route:

        conn.close()

        return dict(route)

    # =====================================
    # PARTIAL DESTINATION SEARCH
    # =====================================

    route = conn.execute(
        """
        SELECT *
        FROM distances
        WHERE UPPER(origin)=UPPER(?)
        LIMIT 1
        """,
        (origin,)
    ).fetchone()

    conn.close()

    if route:

        return {
            "warning": "Exact route not found",
            "nearest_route": dict(route)
        }

    return {
        "error": f"No route found between {origin} and {destination}"
    }