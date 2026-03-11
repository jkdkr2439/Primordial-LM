
import json
from pathlib import Path
from typing import List, Tuple, Any
from primordial_llm.output.nutrients.base import BaseNutrient

class LlamaNutrient(BaseNutrient):
    """Nutrient for Llama/Mistral/DeepSeek architecture."""
    
    def identify(self, model_dir: Path) -> bool:
        config_path = model_dir / "config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
                model_type = config.get("model_type", "").lower()
                return any(k in model_type for k in ["llama", "mistral", "deepseek"])
        return False

    def load(self, model_dir: Path, load_in_4bit: bool) -> Tuple[Any, Any, Any]:
        # Implementation is very similar for transformers-capable models
        # but allows for specific tweaks (e.g., rope_scaling for Llama 3)
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        
        model_kwargs = {"trust_remote_code": True, "device_map": "auto"}
        if load_in_4bit:
            model_kwargs["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True)
            
        tokenizer = AutoTokenizer.from_pretrained(str(model_dir), trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(str(model_dir), low_cpu_mem_usage=True, **model_kwargs)
        return torch, tokenizer, model

    def generate(self, torch_module, tokenizer, model, messages: List[dict], max_new_tokens: int) -> str:
        # Llama-specific prompt handling if needed
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer([prompt], return_tensors="pt")
        model_inputs = {key: value.to(model.device) for key, value in model_inputs.items()}
        
        generated_ids = model.generate(
            **model_inputs, 
            max_new_tokens=max_new_tokens, 
            do_sample=True, 
            temperature=0.6, # Llama usually likes slightly lower temp 
            top_p=0.9
        )
        
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs["input_ids"], generated_ids)
        ]
        return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
