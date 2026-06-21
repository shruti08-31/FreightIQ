import pandas as pd

# Read original CSV
df = pd.read_csv("Transporter_Details.csv", dtype=str)

# Replace empty strings and whitespace-only strings with NaN
df = df.replace(r'^\s*$', pd.NA, regex=True)

# Save cleaned CSV
df.to_csv(
    "Transporter_Details_Null.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Created: Transporter_Updated.csv")
print(df.isna().sum())