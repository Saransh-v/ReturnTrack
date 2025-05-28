
import pandas as pd
import os

DATA_PATH = "returntrack_data.csv"

DEFAULT_REUSE = {
    "PP Box": 5,
    "Plastic Bin": 20,
    "Iron Trolley": 40,
    "Wooden Pallet": 15
}

WEIGHTS = {
    "PP Box": 1.2,
    "Plastic Bin": 3.0,
    "Iron Trolley": 50.0,
    "Wooden Pallet": 18.0
}

CO2_FACTORS = {
    "PP Box": 0.8,
    "Plastic Bin": 7.5,
    "Iron Trolley": 85.0,
    "Wooden Pallet": 10.0
}

COSTS = {
    "PP Box": 120,
    "Plastic Bin": 350,
    "Iron Trolley": 4500,
    "Wooden Pallet": 450
}

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["Item Type", "Quantity Returned", "Month"])

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

def add_or_merge_entry(existing_df, new_entry):
    new_df = pd.DataFrame([new_entry])
    key_cols = ["Item Type", "Month"]
    combined = pd.concat([existing_df, new_df])
    merged = combined.groupby(key_cols, as_index=False)["Quantity Returned"].sum()
    return merged

def calculate_impact(df_month, reuse_freq=DEFAULT_REUSE):
    df = df_month.copy()
    df["Reuse Frequency"] = df["Item Type"].map(reuse_freq)
    df["Adjusted Units"] = df["Quantity Returned"] / df["Reuse Frequency"]
    df["CO2 Avoided (kg)"] = df["Adjusted Units"] * df["Item Type"].map(CO2_FACTORS)
    df["Material Saved (kg)"] = df["Adjusted Units"] * df["Item Type"].map(WEIGHTS)
    df["Cost Avoided (₹)"] = df["Adjusted Units"] * df["Item Type"].map(COSTS)
    df["Truckloads Avoided"] = df["Material Saved (kg)"] / 1200
    return df.round(2)

def get_available_months(df):
    return sorted(df["Month"].unique().tolist())
