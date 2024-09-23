# Script: `./wsl_amdgpu_chat.py`

# Imports
import os
import json
from scripts.model_interaction import load_model, interact_with_model, scan_for_models
from scripts.menus_displays import show_model_menu
from scripts.utility_general import create_data_folder, load_json, write_json

# Paths to persistence and data files
DATA_DIR = './data'
PERSISTENCE_FILE = os.path.join(DATA_DIR, 'persistence.json')

# Check for ClBlas installation in the persistence file
def check_clblas_installed(persistence_data):
    return persistence_data.get("clblas_installed", False)

# Prepare the Qwen-specific prompt format
def prepare_qwen_prompt(user_input, system_prompt=""):
    return f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant"

# Check for data folder and persistence file
def check_and_create_data():
    # Create the data folder if it doesn't exist
    create_data_folder(DATA_DIR)

    # If persistence.json doesn't exist, create it with default content
    if not os.path.exists(PERSISTENCE_FILE):
        print("persistence.json not found. Creating default settings.")
        default_persistence = {"wsl_distribution": "", "last_model_used": "", "clblas_installed": False}
        write_json(default_persistence, PERSISTENCE_FILE)

def main():
    # Check data folder and persistence file
    check_and_create_data()

    # Load persistence settings (WSL distribution, ClBlas installation, etc.)
    persistence = load_json(PERSISTENCE_FILE)
    clblas_installed = check_clblas_installed(persistence)

    # Scan for models and display selection menu if needed
    model_files = scan_for_models('./Models')
    
    if isinstance(model_files, list):
        # Show menu if multiple models are found
        model_file = show_model_menu(model_files)
    else:
        # Automatically load the only available model
        model_file = model_files

    # Update persistence with the last model used
    persistence['last_model_used'] = model_file
    write_json(persistence, PERSISTENCE_FILE)

    # Load and interact with the model
    model, tokenizer = load_model(model_file, use_clblas=clblas_installed)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot.")
            break
        
        # Use Qwen-specific formatting if applicable
        if "qwen" in model_file.lower():
            system_prompt = "You are a helpful assistant."
            formatted_input = prepare_qwen_prompt(user_input, system_prompt)
        else:
            formatted_input = user_input
        
        response = interact_with_model(model, tokenizer, formatted_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
