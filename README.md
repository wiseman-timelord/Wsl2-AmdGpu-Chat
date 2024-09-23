# Wsl2g-AmdGpu-Agent
Status: Alpha - Trying to make the best chatbot/agent I can, for my AMD hardware that is ~5 years old, ie NonRocm-AmdGpu/Avx2 on Wsl2-Python3.
- It will be designed/tested with Qwen2.5; `Qwen2.5-7B.Q6_K.gguf` (descriptive text generation and user interaction) and `Qwen2.5-Coder-7B.Q6_K.gguf` (programming and wsl system commands) and `Qwen2.5-7B-Instruct.Q6_K.gguf` (processing of text). 
- It will be intended to run optimally on given hardware setups, offloading as many layers as is safe to the GPU. Free ram is calculated and layers are dynamically calculated depending upon the model, and assigned.
- After successfull creation, then expand to be able to use, chunking and rag (or whatever is better). 
- Keep adding features, research on internet is priority, or local files.

### DESCRIPTION:
The Wsl2g-AmdGpu-Agent is a Python-based chatbot interface that leverages GGUF models for inference using AMD GPU acceleration within a WSL2 environment. It dynamically loads models from a specified directory, presents them to the user for selection, and provides an interactive conversational interface. The program ensures proper configuration persistence, allowing users to save and reuse settings across sessions. I have done similar projects before, but the idea here is to ensure that binaries are not used, so that we can use other libraries intended for combined use with torch/ctransformers, or whatever library I go with in the end, I will investigate them.

### FEATURES:
- Dynamic Model Loading: Automatically scans the ./Models folder for available .gguf models and loads the selected one for inference.
- GPU-Accelerated Inference: Uses the ctransformers library to take advantage of AMD GPU acceleration for fast and efficient text generation.
- Interactive Chat Interface: Allows users to interact with the loaded model in a conversational loop.
- Model Selection Menu: Displays a dynamic menu for users to choose from multiple models, if available.
- Configuration Persistence: Saves user settings, such as the selected WSL distribution, in a persistent JSON file (persistence.json), ensuring settings are maintained across sessions.
- Batch Script Integration: Works seamlessly with a Windows batch script for WSL2 environment setup, model installation, and script execution.
- Utility Functions: Centralized utility functions for configuration management and file handling.
- Easy Setup and Execution: A single batch file handles WSL2 initialization, Python environment setup, and running of the chatbot.

### PREVIEW:
```
========================================================================================================================
    Wsl2g-AmdGpu-Agent
========================================================================================================================


    1. Run Wsl2-AmdGpu-Chat

    2. Install Python Requirements

    3. Install Github Requirements


========================================================================================================================
Selection; Menu Options = 1-3, Exit = X: 
```

### DEVELOPMENT:
- Outstanding Work on the Scripts...
1. Main Script - `wsl2g_amdgpu_agent.py`
The main script is almost complete but still needs a few improvements:
- **Check if the `./Models` directory exists**:
  - Add a check at the beginning to ensure the `./Models` folder exists. If it doesn't, print a helpful message and exit or create it.
  - This avoids potential errors when scanning for model files.
- **Improve Error Handling**:
  - Add try-except blocks around any file access (like `load_json`) to catch potential exceptions (e.g., permission errors, missing files).
  - Handle cases where no models are found more gracefully by printing a user-friendly message instead of raising an unhandled exception.
- **Model Selection Validation**:
  - In `menus_displays.py`, when the user selects a model, non-numeric inputs or out-of-bounds indices should be handled gracefully.
  - This validation should also be mirrored in the main script.
2. Utility Functions - `utility_general.py`
The utility script is well-implemented, but a few small updates can make it more robust:
- **Expand Error Handling**:
  - The current `load_json` function handles `FileNotFoundError` well. Consider also catching and handling JSON parsing errors (`json.JSONDecodeError`) to avoid crashes if the JSON file is corrupted or improperly formatted.
  - If parsing fails, consider printing an error message and returning a default configuration.
- **Enhance Directory Creation**:
  - You already have the `create_data_folder` function, which is useful for ensuring the `./data` directory exists. Add similar functions if other directories (e.g., `./Models`) might also need to be created during initialization.
3. Model Interaction - `model_interaction.py`
The model interaction script is functional but could be optimized for error handling and flexibility:
- **Add Input Validation**:
  - Ensure that the `load_model` function gracefully handles incorrect file paths. Use `try-except` to handle exceptions if the model file cannot be loaded.
  - You may want to print more detailed error messages if loading the model fails (e.g., invalid file format, corrupted model).
- **Optimize Model Loading for Large Models**:
  - Since you're balancing GPU and CPU usage, test the current loading scheme (with and without CLBlast) for performance bottlenecks. Ensure that large models can be distributed across CPU and GPU effectively.
  - Consider adding logic to adjust the number of layers loaded to GPU vs. CPU dynamically, based on available memory and GPU capacity.
4. Menu Display - `menus_displays.py`
The menu display script requires better input validation:
- **Add Input Validation for Model Selection**:
  - Wrap the `int(input())` statement in a try-except block to handle non-numeric input, and ensure the user re-enters a valid number.
  - You already handle invalid index selections with recursion, but consider adding a maximum number of retries or a fallback to the main menu if the user fails multiple times.
5. Testing and Validation
Testing is crucial to ensure everything works as expected:
- **Integration Testing**:
  - Ensure seamless integration between the batch script and the Python scripts. Test the `persistence.json` logic to confirm that settings (e.g., `wsl_distribution`, `clblas_installed`) are correctly read and written across sessions.
- **Model Loading**:
  - Test multiple models (especially large ones) to confirm that the system can handle them efficiently, both with and without CLBlast installed.
  - Verify that the Qwen-specific prompt formatting is applied correctly and that the model interaction works as expected.
- **ClBlast Installation**:
  - Test the `Install ClBlas` function thoroughly to ensure CLBlast installs correctly on various systems. Ensure that the persistence system correctly tracks the installed status.
6. Batch Script - `Wsl2-AmdGpu-Chat.Bat`
The batch script looks solid, but here are a few enhancements to make it more robust:
- **Error Handling for WSL Commands**:
  - After running WSL commands (e.g., installing ClBlas), check for command success using `if errorlevel 1` to ensure the process completed without errors. If there’s an error, print a helpful message and prompt the user to retry.
- **Validate Persistence File**:
  - When reading from `persistence.txt`, check if the file is empty or corrupted and handle these cases by prompting the user to re-enter the WSL distribution or reset the persistence file.


### FILES STRUCTURE:
```
.\scripts
.\Wsl2g-AmdGpu-Agent.Bat
.\wsl2g_amdgpu_agent.py
.\scripts\menus_displays.py
.\scripts\model_interaction.py
.\scripts\utility_general.py
```
