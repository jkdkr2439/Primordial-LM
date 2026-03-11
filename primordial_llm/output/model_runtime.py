from pathlib import Path
from typing import List


def load_model(model_dir: Path, load_in_4bit: bool):
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    except ImportError as exc:
        raise SystemExit(
            "[chat-runner] Missing dependencies. Install torch + transformers first. "
            f"Import error: {exc}"
        )

    model_kwargs = {
        "trust_remote_code": True,
        "device_map": "auto",
    }
    if load_in_4bit:
        model_kwargs["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True)
    else:
        model_kwargs["torch_dtype"] = "auto"

    print("[chat-runner] Loading tokenizer...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir), trust_remote_code=True)
    print("[chat-runner] Loading model weights...", flush=True)
    model = AutoModelForCausalLM.from_pretrained(
        str(model_dir),
        low_cpu_mem_usage=True,
        **model_kwargs,
    )
    print("[chat-runner] Model ready.", flush=True)
    return torch, tokenizer, model


def generate_reply(torch_module, tokenizer, model, messages: List[dict], max_new_tokens: int) -> str:
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    model_inputs = tokenizer([prompt], return_tensors="pt")
    model_inputs = {key: value.to(model.device) for key, value in model_inputs.items()}
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs["input_ids"], generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response.strip()
