import json
import pandas as pd

def load_data(filepath):
    """Load customer data from JSON file"""
    with open(filepath) as f:
        data = json.load(f)
    return pd.DataFrame(data)

def preprocess_data(df):
    """Preprocess customer data for analysis"""
    df_encoded = df.copy()
    df_encoded["Social Media Activity"] = df_encoded["Social Media Activity"].map({"Low": 0, "Medium": 1, "High": 2})
    df_encoded["Gender"] = df_encoded["Gender"].map({"Male": 0, "Female": 1})
    return df_encoded