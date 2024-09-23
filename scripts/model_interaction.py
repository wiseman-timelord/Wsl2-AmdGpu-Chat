# Script: `./scriptz/model_interaction.py`

# Imports
import os
from ctransformers import AutoModelForCausalLM

# Scan models in the Models directory
def scan_for_models(model_directory='./Models'):
    model_files = [f for f in os.listdir(model_directory) if f.endswith('.gguf')]
    
    if len(model_files) == 0:
        raise FileNotFoundError("No .gguf models found in the ./Models directory.")
    elif len(model_files) == 1:
        print(f"One model found: {model_files[0]}")
        return os.path.join(model_directory, model_files[0])
    else:
        return model_files  # Delegate menu display to the menu function

# Load a model from the specified file, with optional ClBlas support
def load_model(model_file, use_clblas=False):
    print(f"Loading model: {model_file}")
    
    if use_clblas:
        print("Using ClBlas for GPU acceleration")
    
    model = AutoModelForCausalLM.from_pretrained(model_file, device="gpu" if use_clblas else "cpu")
    tokenizer = model.tokenizer
    return model, tokenizer

# Interact with the model by generating a response
def interact_with_model(model, tokenizer, user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
