from database.db import get_connection

# =====================================================
# DASHBOARD METRICS
# =====================================================

def get_dashboard_metrics():
    conn = get_connection()

    try:
        total_vehicles = conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
        total_routes = conn.execute("SELECT COUNT(*) FROM distances").fetchone()[0]
        total_transporters = conn.execute("SELECT COUNT(*) FROM transporters").fetchone()[0]

        odc_vehicles = conn.execute(
            "SELECT COUNT(*) FROM vehicles WHERE ODC_Allowed='Yes'"
        ).fetchone()[0]

        non_odc_vehicles = conn.execute(
            "SELECT COUNT(*) FROM vehicles WHERE ODC_Allowed='No'"
        ).fetchone()[0]

        vehicle_categories = conn.execute(
            "SELECT COUNT(DISTINCT Category) FROM vehicles"
        ).fetchone()[0]

        # capacity metrics (used in your dashboard)
        total_capacity = conn.execute(
            "SELECT SUM(Max_Weight_MT) FROM vehicles"
        ).fetchone()[0] or 0

        avg_capacity = conn.execute(
            "SELECT AVG(Max_Weight_MT) FROM vehicles"
        ).fetchone()[0] or 0

        highest_capacity = conn.execute(
            "SELECT MAX(Max_Weight_MT) FROM vehicles"
        ).fetchone()[0] or 0

        odc_capacity = conn.execute(
            "SELECT SUM(Max_Weight_MT) FROM vehicles WHERE ODC_Allowed='Yes'"
        ).fetchone()[0] or 0

        avg_odc_capacity = conn.execute(
            "SELECT AVG(Max_Weight_MT) FROM vehicles WHERE ODC_Allowed='Yes'"
        ).fetchone()[0] or 0

        return {
            "total_vehicles": total_vehicles,
            "total_routes": total_routes,
            "total_transporters": total_transporters,
            "odc_vehicles": odc_vehicles,
            "non_odc_vehicles": non_odc_vehicles,
            "vehicle_categories": vehicle_categories,
            "total_capacity_mt": round(total_capacity, 2),
            "avg_capacity_mt": round(avg_capacity, 2),
            "highest_capacity_mt": round(highest_capacity, 2),
            "total_odc_capacity_mt": round(odc_capacity, 2),
            "avg_odc_capacity_mt": round(avg_odc_capacity, 2)
        }

    finally:
        conn.close()


# =====================================================
# ROUTE STATISTICS
# =====================================================

def route_statistics():
    conn = get_connection()

    try:
        row = conn.execute("""
            SELECT
                MAX(distance_km),
                MIN(distance_km),
                AVG(distance_km)
            FROM distances
        """).fetchone()

        return {
            "max_distance": row[0] or 0,
            "min_distance": row[1] or 0,
            "avg_distance": round(row[2], 2) if row[2] else 0
        }

    finally:
        conn.close()


# =====================================================
# TRANSPORTER COUNT (FOR DASHBOARD PILL METRICS)
# =====================================================

def get_transporter_counts():
    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT Category, COUNT(*) as cnt
            FROM transporters
            GROUP BY Category
        """).fetchall()

        return {row[0]: row[1] for row in rows}

    finally:
        conn.close()


# =====================================================
# DATABASE COVERAGE ANALYTICS
# =====================================================

def get_database_coverage():
    conn = get_connection()

    try:
        unique_origins = conn.execute("""
            SELECT COUNT(DISTINCT origin)
            FROM distances
        """).fetchone()[0]

        unique_destinations = conn.execute("""
            SELECT COUNT(DISTINCT destination)
            FROM distances
        """).fetchone()[0]

        return {
            "unique_origins": unique_origins,
            "unique_destinations": unique_destinations
        }

    finally:
        conn.close()


# =====================================================
# TOP ORIGINS (FOR TABLE)
# =====================================================

def get_top_route_origins(limit=10):
    conn = get_connection()

    try:
        rows = conn.execute(f"""
            SELECT origin, COUNT(*) as total
            FROM distances
            GROUP BY origin
            ORDER BY total DESC
            LIMIT {limit}
        """).fetchall()

        return [
            {"Origin": r[0], "Routes": r[1]}
            for r in rows
        ]

    finally:
        conn.close()


# =====================================================
# INTERACTIVE ROUTE FILTERING (SLIDER LOGIC)
# =====================================================

def get_interactive_routes(min_km, max_km, origin_filter=None):
    conn = get_connection()

    try:
        query = """
        SELECT
            TRIM(origin),
            TRIM(destination),
            CAST(distance_km AS INTEGER),
            CASE
                WHEN CAST(distance_km AS INTEGER) < 300 THEN 'Short Corridor'
                WHEN CAST(distance_km AS INTEGER) < 1000 THEN 'Medium Corridor'
                ELSE 'Long Corridor'
            END,
            'Standard Freight Route',
            '2025-Updated',
            'AUTO-APPROVED'
        FROM distances
        WHERE CAST(distance_km AS INTEGER) BETWEEN ? AND ?
        """

        params = [min_km, max_km]

        if origin_filter:
            query += """
            AND TRIM(UPPER(origin)) = TRIM(UPPER(?))
            """
            params.append(origin_filter)

        rows = conn.execute(query, params).fetchall()

        print("Params:", params)
        print("Rows:", rows[:5])

        return [list(r) for r in rows]
    finally:
        conn.close()

# TRANSPORTER SUMMARY (OPTIONAL EXTENSION)
# =====================================================

def transporter_summary():
    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT Category, COUNT(*) as Count
            FROM transporters
            GROUP BY Category
        """).fetchall()

        return [{"Category": r[0], "Count": r[1]} for r in rows]

    finally:
        conn.close()


# =====================================================
# COMPLETE REPORT
# =====================================================

def analytics_report():
    return {
        "dashboard": get_dashboard_metrics(),
        "route_stats": route_statistics(),
        "coverage": get_database_coverage(),
        "transporters": get_transporter_counts(),
        "top_origins": get_top_route_origins(),
        "interactive_routes": get_interactive_routes(0, 99999)
    }

# =====================================================
# GET ALL ORIGINS (FOR SEARCH DROPDOWN)
# =====================================================

def get_origin_list():
    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT DISTINCT origin
            FROM distances
            ORDER BY origin
        """).fetchall()

        return [r[0] for r in rows]

    finally:
        conn.close()
