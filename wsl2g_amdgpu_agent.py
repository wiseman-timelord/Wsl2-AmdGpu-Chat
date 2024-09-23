# Script: `./wsl_amdgpu_chat.py`

# Imports
import os
import json
import psutil
import subprocess
from scripts.model_interaction import ModelManager
from scripts.menus_displays import MainWindow
from scripts.utility_general import create_data_folder, load_json, write_json
from scripts.agent_operation import AgentManager
from PyQt5.QtWidgets import QApplication

# Globals
DATA_DIR = './data'
PERSISTENCE_FILE = os.path.join(DATA_DIR, 'persistence.json')
PERSISTENCE_TXT = os.path.join(DATA_DIR, 'persistence.txt')

# Functions
def load_persistence_txt():
    with open(PERSISTENCE_TXT, 'r') as f:
        return dict(line.strip().split('=') for line in f if '=' in line)

def get_available_resources():
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_usage = psutil.cpu_percent(interval=1)
    available_threads = max(1, int(cpu_threads * (1 - cpu_usage / 100)))
    
    try:
        result = subprocess.run(["glxinfo", "|", "grep", "Video Memory"], capture_output=True, text=True, shell=True)
        vram_info = result.stdout.strip()
        vram_mb = int(vram_info.split()[-2])
    except (subprocess.CalledProcessError, ValueError):
        gpu_name = subprocess.run(["lspci", "|", "grep", "-i", "vga"], capture_output=True, text=True, shell=True).stdout.strip().split(':')[-1].strip()
        vram_gb = input(f"How Much VRam Does {gpu_name} Have in GB? (e.g., 4, 8, 12): ").strip()
        vram_mb = int(vram_gb) * 1024
    
    return available_threads, vram_mb

def main():
    app = QApplication([])
    
    create_data_folder(DATA_DIR)
    persistence = load_json(PERSISTENCE_FILE)
    txt_settings = load_persistence_txt()

    available_threads, vram_mb = get_available_resources()
    print(f"Available CPU Threads: {available_threads}")
    print(f"Available VRAM: {vram_mb} MB")

    model_manager = ModelManager(available_threads, vram_mb)
    agent_manager = AgentManager(model_manager)

    main_window = MainWindow(agent_manager)
    main_window.show()

    app.exec_()

    # Save persistence data
    write_json(persistence, PERSISTENCE_FILE)

# Entry Point
if __name__ == "__main__":
    main()