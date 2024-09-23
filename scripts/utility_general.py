# Script: `./scripts/utility_general.py`

# Imports
import os
import json

# Set up basic logging
logging.basicConfig(filename='./data/agent.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

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

def load_persistence_txt(txt_file):
    with open(txt_file, 'r') as f:
        return dict(line.strip().split('=') for line in f if '=' in line)
