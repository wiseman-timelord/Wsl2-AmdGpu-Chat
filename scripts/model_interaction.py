# Script: `./scriptz/model_interaction.py`

# Imports
import os
import math
import subprocess
from ctransformers import AutoModelForCausalLM

class ModelManager:
    def __init__(self, available_threads):
        self.available_threads = available_threads
        self.gpu_memory = self.get_available_vram()
        self.models = {}
        self.current_model = None

    def get_available_vram(self):
        try:
            # Check if glxinfo is installed
            subprocess.run(["glxinfo"], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            print("glxinfo not found. Installing mesa-utils...")
            subprocess.run(["sudo", "apt", "install", "-y", "mesa-utils"], check=True)

        # Get VRAM information
        result = subprocess.run(["glxinfo", "|", "grep", "Video Memory"], capture_output=True, text=True, shell=True)
        vram_info = result.stdout.strip()

        if vram_info:
            # Extract VRAM size in MB
            vram_mb = int(vram_info.split()[-2])
            return vram_mb
        else:
            print("Unable to determine VRAM size. Defaulting to 4GB.")
            return 4096  # Default to 4GB if unable to determine

    def scan_for_models(self, model_directory='./Models'):
        model_files = [f for f in os.listdir(model_directory) if f.endswith('.gguf')]
        if not model_files:
            raise FileNotFoundError("No .gguf models found in the ./Models directory.")
        return {os.path.splitext(f)[0]: os.path.join(model_directory, f) for f in model_files}

    def load_model(self, model_name):
        if model_name not in self.models:
            model_files = self.scan_for_models()
            if model_name not in model_files:
                raise ValueError(f"Model {model_name} not found.")
            
            model_file = model_files[model_name]
            print(f"Loading model: {model_file}")
            
            # Load the model to get its configuration
            temp_model = AutoModelForCausalLM.from_pretrained(model_file, model_type="qwen2")
            
            # Get the number of layers and model size
            num_layers = temp_model.config.num_layers
            model_size = os.path.getsize(model_file) / (1024 * 1024)  # Size in MB
            
            # Calculate the number of layers that can fit in GPU memory
            layer_size = model_size / num_layers
            gpu_layers = min(num_layers, math.floor(self.gpu_memory / layer_size))
            
            print(f"Model has {num_layers} layers. Loading {gpu_layers} layers to GPU.")
            
            # Load the model with the calculated number of GPU layers
            model = AutoModelForCausalLM.from_pretrained(
                model_file,
                model_type="qwen2",
                gpu_layers=gpu_layers,
                threads=self.available_threads
            )
            self.models[model_name] = model
        
        self.current_model = self.models[model_name]
        return self.current_model

    def interact_with_model(self, user_input):
        if not self.current_model:
            raise ValueError("No model is currently loaded.")
        
        inputs = self.current_model.tokenizer(user_input, return_tensors="pt")
        outputs = self.current_model.generate(**inputs, max_new_tokens=100)
        return self.current_model.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def prepare_qwen_prompt(self, user_input, system_prompt=""):
        return f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant"

    def filter_model_output(self, output):
        # Implement any necessary output filtering here
        return output