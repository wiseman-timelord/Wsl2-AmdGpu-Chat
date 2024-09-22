# Wsl2-AmdGpu-Chat
Trying to make the best chatbot I can, for non-Rocm Amd GPU on Wsl2.

### DESCRIPTION:
The Wsl2-AmdGpu-Chat is a Python-based chatbot interface that leverages GGUF models for inference using AMD GPU acceleration within a WSL2 environment. It dynamically loads models from a specified directory, presents them to the user for selection, and provides an interactive conversational interface. The program ensures proper configuration persistence, allowing users to save and reuse settings across sessions.

### FEATURES:
- Dynamic Model Loading: Automatically scans the ./Models folder for available .gguf models and loads the selected one for inference.
- GPU-Accelerated Inference: Uses the ctransformers library to take advantage of AMD GPU acceleration for fast and efficient text generation.
- Interactive Chat Interface: Allows users to interact with the loaded model in a conversational loop.
- Model Selection Menu: Displays a dynamic menu for users to choose from multiple models, if available.
- Configuration Persistence: Saves user settings, such as the selected WSL distribution, in a persistent JSON file (persistence.json), ensuring settings are maintained across sessions.
- Batch Script Integration: Works seamlessly with a Windows batch script for WSL2 environment setup, model installation, and script execution.
- Utility Functions: Centralized utility functions for configuration management and file handling.
- Easy Setup and Execution: A single batch file handles WSL2 initialization, Python environment setup, and running of the chatbot.

### DEVELOPMENT:
- Outstanding Work on the Scripts...
1. **Update the Main Script (`wsl2_amdgpu_chat.py`)**:
   - Ensure it checks for the existence of the `./data` folder, creates it if it doesn’t exist.
   - Ensure it checks for `./data/persistence.json`, creates the file if it doesn’t exist, and maintains a JSON layout for settings (such as WSL distribution).
   - Optionally call utility functions for these tasks (from `utility_general.py`) to keep the main script clean.
2. **Create or Update `utility_general.py`**:
   - Add functions for:
     - Creating the `./data` folder.
     - Checking if `persistence.json` exists.
     - Reading from and writing to `persistence.json`.
     - If necessary, initialize `persistence.json` with default values if it doesn’t exist (such as an empty settings object).
3. **Improve Model Interaction**:
   - Add validation to ensure that if the user selects an invalid model number, the menu re-prompts without crashing.
   - Ensure that large models can be handled efficiently by testing different GGUF models and verifying response generation time.
4. **Error Handling in Menu (`menus_displays.py`)**:
   - Add input validation for the model selection menu to prevent crashes if the user inputs non-numeric values or selects invalid indices.
5. **Testing and Validation**:
   - Test the Python scripts and ensure seamless integration with the batch file.
   - Test multiple GGUF models in the `./Models` folder to ensure model loading and inference work as expected.
   - Test persistence handling for WSL distribution and other future settings in `persistence.json`.

### FILES STRUCTURE:
```
.\scripts
.\Wsl2-AmdGpu-Chat.Bat
.\wsl2_amdgpu_chat.py
.\scripts\menus_displays.py
.\scripts\model_interaction.py
.\scripts\utility_general.py
```
