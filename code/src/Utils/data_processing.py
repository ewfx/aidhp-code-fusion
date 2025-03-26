# Import required libraries
import pandas as pd
import json
import os
from datetime import datetime

# Preprocess customer data by encoding categorical variables
def preprocess_data(df):
    df_encoded = df.copy()
    # Encode social media activity as numerical values
    df_encoded["Social Media Activity"] = df_encoded["Social Media Activity"].map({"Low": 0, "Medium": 1, "High": 2})
    # Encode gender as numerical values
    df_encoded["Gender"] = df_encoded["Gender"].map({"Male": 0, "Female": 1})
    # Add timestamp of last update
    df_encoded["Last Updated"] = datetime.now()
    return df_encoded

# Load sample customer data from JSON file
def load_sample_data():
    # Construct path to sample_data.json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "..", "dataset", "sample_data.json")
    
    # Load and return data as pandas DataFrame
    with open(json_path, 'r') as f:
        customers = json.load(f)
    return pd.DataFrame(customers)