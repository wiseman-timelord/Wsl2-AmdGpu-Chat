# Script: `./scripts/model_interaction.py`

# Imports
import os
import math
import subprocess
from ctransformers import AutoModelForCausalLM

class ModelManager:
    def __init__(self, available_threads, gpu_memory):
        self.available_threads = available_threads
        self.gpu_memory = gpu_memory
        self.models = {}
        self.current_model = None

    def get_gpu_name(self):
        try:
            result = subprocess.run(["lspci", "|", "grep", "-i", "vga"], capture_output=True, text=True, shell=True)
            gpu_info = result.stdout.strip()
            if gpu_info:
                return gpu_info.split(':')[-1].strip()
        except subprocess.CalledProcessError:
            print("Unable to determine GPU name. Defaulting to 'Unknown GPU'.")
        return "Unknown GPU"

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
            
            temp_model = AutoModelForCausalLM.from_pretrained(model_file, model_type="qwen2")
            num_layers = temp_model.config.num_layers
            model_size = os.path.getsize(model_file) / (1024 * 1024)  # Size in MB
            
            layer_size = model_size / num_layers
            gpu_layers = min(num_layers, math.floor(self.gpu_memory / layer_size))
            
            print(f"Model has {num_layers} layers. Loading {gpu_layers} layers to GPU.")
            
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