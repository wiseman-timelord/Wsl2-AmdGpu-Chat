# Script: `./scriptz/menu_displays.py`

# Imports
def show_model_menu(model_files):
    print("Multiple models found:")
    for i, model_file in enumerate(model_files):
        print(f"{i+1}. {model_file}")
    
    selection = int(input("Enter the number of the model you wish to use: ")) - 1
    if 0 <= selection < len(model_files):
        return model_files[selection]
    else:
        print("Invalid selection.")
        return show_model_menu(model_files)  # Recurse if invalid
