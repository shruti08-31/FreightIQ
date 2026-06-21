import os
import pandas as pd
from database.db import get_connection


def initialize_database():

    conn = get_connection()

    ROOT_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    # CSV Files
    vehicle_file = os.path.join(
        ROOT_DIR,
        "vehicle_master.csv"
    )

    distance_file = os.path.join(
        ROOT_DIR,
        "distance_data.csv"
    )

    transporter_file = os.path.join(
        ROOT_DIR,
        "Transporter_updated_details.csv"
    )

    print(f"Vehicle CSV: {vehicle_file}")
    print(f"Distance CSV: {distance_file}")
    print(f"Transporter CSV: {transporter_file}")

    # Read CSVs
    vehicle_df = pd.read_csv(vehicle_file)
    distance_df = pd.read_csv(distance_file)
    transporter_df = pd.read_csv(transporter_file)

    print(f"Vehicles Records: {len(vehicle_df)}")
    print(f"Distance Records: {len(distance_df)}")
    print(f"Transporter Records: {len(transporter_df)}")

    # Load into SQLite
    vehicle_df.to_sql(
        "vehicles",
        conn,
        if_exists="replace",
        index=False
    )

    distance_df.to_sql(
        "distances",
        conn,
        if_exists="replace",
        index=False
    )

    transporter_df.to_sql(
        "transporters",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully")


if __name__ == "__main__":
    print("🚀 Starting database initialization...")
    initialize_database()