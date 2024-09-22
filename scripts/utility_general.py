# Script: `./scriptz/utility_general.py`

# Imports
import json

# Read from a JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Write to a JSON file
def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Read from a TXT file
def load_persistence(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Write to a TXT file
def save_persistence(data, file_path):
    with open(file_path, 'w') as file:
        file.write(data)
