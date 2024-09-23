# Script: `./scripts/utility_general.py`

# Imports
import os
import json

# Create the data folder if it doesn't exist
def create_data_folder(data_path):
    if not os.path.exists(data_path):
        print(f"Creating data directory at: {data_path}")
        os.makedirs(data_path)

# Read from a JSON file
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_path} not found. Returning empty dictionary.")
        return {}

# Write to a JSON file
def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
