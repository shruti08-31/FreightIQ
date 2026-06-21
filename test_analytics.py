import pandas as pd

df = pd.read_csv("distance_data.csv")

result = df[
    (
        (df["origin"].astype(str).str.upper() == "DELHI") &
        (df["destination"].astype(str).str.upper() == "HARIDWAR")
    )
    |
    (
        (df["origin"].astype(str).str.upper() == "HARIDWAR") &
        (df["destination"].astype(str).str.upper() == "DELHI")
    )
]

print(result)

print("\nRows Found:", len(result))