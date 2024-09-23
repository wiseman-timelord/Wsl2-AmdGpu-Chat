# Script: `./wsl_amdgpu_chat.py`

# Imports
import os
import json
import psutil
from scripts.model_interaction import ModelManager
from scripts.menus_displays import MainWindow
from scripts.utility_general import create_data_folder, load_json, write_json
from scripts.agent_operation import AgentManager
from PyQt5.QtWidgets import QApplication

DATA_DIR = './data'
PERSISTENCE_FILE = os.path.join(DATA_DIR, 'persistence.json')
PERSISTENCE_TXT = os.path.join(DATA_DIR, 'persistence.txt')

def load_persistence_txt():
    with open(PERSISTENCE_TXT, 'r') as f:
        return dict(line.strip().split('=') for line in f if '=' in line)

def get_available_resources():
    cpu_threads = psutil.cpu_count(logical=True)
    available_threads = max(1, int(cpu_threads * 0.75))  # Use up to 75% of available threads
    return available_threads

def main():
    app = QApplication([])
    
    create_data_folder(DATA_DIR)
    persistence = load_json(PERSISTENCE_FILE)
    txt_settings = load_persistence_txt()

    available_threads = get_available_resources()

    model_manager = ModelManager(available_threads)
    agent_manager = AgentManager(model_manager)

    main_window = MainWindow(agent_manager)
    main_window.show()

    app.exec_()

    # Save persistence data
    write_json(persistence, PERSISTENCE_FILE)

if __name__ == "__main__":
    main()