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

    # File paths
    vehicle_file = os.path.join(ROOT_DIR, "vehicle_master.csv")
    distance_file = os.path.join(ROOT_DIR, "distance_data.csv")
    transporter_file = os.path.join(ROOT_DIR, "Transporter_updated_details.csv")
    shipment_pred_file = os.path.join(ROOT_DIR, "shipment_prediction_data.xlsx")
    distance_pred_file = os.path.join(ROOT_DIR, "distance_Prediction_data.csv")
    packaging_file = os.path.join(ROOT_DIR, "Packaging_Dataset.xlsx")

    # Check if files exist
    files = [
        vehicle_file,
        distance_file,
        transporter_file,
        shipment_pred_file,
        distance_pred_file,
        packaging_file,
    ]

    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")

    # Read files
    vehicle_df = pd.read_csv(vehicle_file)
    distance_df = pd.read_csv(distance_file)
    transporter_df = pd.read_csv(transporter_file)
    shipment_pred_df = pd.read_excel(shipment_pred_file)
    distance_pred_df = pd.read_csv(distance_pred_file)
    packaging_df = pd.read_excel(packaging_file)

    # Print record counts
    print(f"Vehicles Records: {len(vehicle_df)}")
    print(f"Distance Records: {len(distance_df)}")
    print(f"Transporter Records: {len(transporter_df)}")
    print(f"Shipment Prediction Records: {len(shipment_pred_df)}")
    print(f"Distance Prediction Records: {len(distance_pred_df)}")
    print(f"Packaging Records: {len(packaging_df)}")

    # Store data into SQLite
    vehicle_df.to_sql("vehicles", conn, if_exists="replace", index=False)
    distance_df.to_sql("distances", conn, if_exists="replace", index=False)
    transporter_df.to_sql("transporters", conn, if_exists="replace", index=False)
    shipment_pred_df.to_sql("shipment_predictions", conn, if_exists="replace", index=False)
    distance_pred_df.to_sql("distance_predictions", conn, if_exists="replace", index=False)
    packaging_df.to_sql("packaging", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully with all 6 tables")


if __name__ == "__main__":
    print("🚀 Starting database initialization...")
    initialize_database()
