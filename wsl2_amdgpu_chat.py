# Script: `./wsl_amdgpu_chat.py`

# Imports
import os
from scripts.model_interaction import load_model, interact_with_model, scan_for_models
from scripts.menus_displays import show_model_menu
from scripts.utility_general import load_persistence

def main():
    # Scan models and present selection menu if necessary
    model_file = scan_for_models('./Models')
    
    # Load the model using the selected file
    model, tokenizer = load_model(model_file)

    # Start chatbot loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot.")
            break
        response = interact_with_model(model, tokenizer, user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
