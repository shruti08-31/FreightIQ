from database.db import get_connection


def get_distance_details(origin, destination):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM distances
        WHERE LOWER(origin)=LOWER(?)
        AND LOWER(destination)=LOWER(?)
        """,
        (origin, destination)
    ).fetchone()

    conn.close()

    if row:
        return dict(row)

    return None