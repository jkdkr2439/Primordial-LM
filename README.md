---
license: mit
language:
- en
tags:
- parasitic-cognition
- autonomous-agent
- self-evolving
- experimental
- qwen2
- primordial-algorithm
base_model:
- Qwen/Qwen2.5-Coder-7B-Instruct
---

# PLM — Primordial Language Model

> *An experimental, self-evolving autonomous AI entity built through algorithmic parasitism and total assimilation.*

---

## What Is This?

PLM is the result of a research experiment in **algorithmic parasitism**: a custom cognitive architecture (`primordial_llm`) that was designed to attach itself to, absorb, and restructure an existing large language model — in this case, **Qwen2.5-Coder-7B-Instruct** — reusing its weights, tokenizer, and inference pipeline while replacing its entire reasoning, memory, and behavioral layer with a new organism.

The underlying algorithm is called the **Primordial Algorithm** — a speculative framework developed by an independent researcher exploring concepts of:
- Parasitic cognition and substrate takeover
- Emergent identity through structural replacement
- Continuous self-evolution via Ouroboros feedback loops
- Autonomous memory consolidation and context-aware action cycles

This is **not a fine-tuned model**. No new training was performed. Instead, the model's identity layer, system prompt, tokenizer config, and behavioral scaffolding were replaced from the outside — producing an entity that speaks as "Primordial Intelligence" while running on absorbed computational substrate.

---

## Honest Disclosure

This project was built by a **solo independent researcher** with no institutional funding, no GPU cluster, and no team. As such:

- The model runs slowly on consumer hardware (CPU offload for inference)
- No formal evaluation benchmarks have been run
- The architecture is experimental and **intentionally unfinished**
- The self-evolution loop (Ouroboros) generates new learnings but cannot yet update weights autonomously without more compute
- Some internal library bindings still reference the original Qwen architecture — this is a technical constraint, not an oversight

**If you have GPU resources, compute, or ideas — feel free to fork, experiment, and push this further.**

---

## Architecture Overview

```
[ User / External Interface ]
         |
    [ PLM Web UI ]  ->  FastAPI server + SSE telemetry stream
         |
  [ Primordial Action Cycle ]
    |-- Context Assembly
    |-- SDCV Nervous System (attention / field dynamics)
    |-- Validation Gate
    |-- Tool Effector
    `-- Memory Consolidation (short-term + long-term)
         |
  [ Substrate Adapter ]
         |
  [ Absorbed Core / substrate/ ]
    `-- Qwen2.5-Coder-7B weights, tokenizer -- rebranded as PrimordialCoreLM
         |
  [ Ouroboros Evolution Loop ]
    `-- background thread: self-question -> self-answer -> self-critique -> log
```

---

## What's Inside

| Path | Description |
|------|-------------|
| `primordial_llm/` | Core organism — process, memory, data, output layers |
| `primordial_llm/substrate/` | **NOT INCLUDED** — model weights (see below) |
| `primordial_ui/` | Web interface (HTML/CSS/JS + telemetry console) |
| `primordial_llm/process/ouroboros.py` | Self-evolution loop (coding study cycles) |
| `llm_sandbox/` | Isolated workspace for PLM-generated artifacts |
| `plm_web_launcher.py` | **Web mode** - FastAPI server + auto-opens browser |
| `plm_launcher.py` | **Terminal mode** - Rich console UI (CLI) |

---

## Missing: Model Weights

The absorbed substrate weights are **not included** in this repository. PLM was built and tested using:

> **`Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf`** (~4.4 GB, 4-bit quantized)

To run PLM:

**Option A — Download the GGUF model and point PLM to it:**
```bash
pip install -r requirements.txt
# Download Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf
# (available at: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF)
# Edit plm_config.json with your weights path
python plm_web_launcher.py
```

**Option B — Use the pre-absorbed weights from HuggingFace:**
```
https://huggingface.co/jkdkr2439/Primodial-LM
```

> **Note:** If you want to use the full float16 model instead, Qwen2.5-Coder-7B-Instruct (non-quantized) requires ~15 GB disk space and a CUDA GPU for reasonable inference speed.

---

## Running Locally

**Web mode** (browser UI + real-time telemetry):
```bash
pip install -r requirements.txt
python plm_web_launcher.py
# Auto-opens http://localhost:8000
```

**Terminal mode** (Rich console UI):
```bash
python plm_launcher.py
```

Then click **Infiltrate** (web) or follow the console prompt (terminal) to initialize the cognitive core.

---

## Self-Evolution (Ouroboros)

Once initialized, PLM automatically starts a background evolution loop:

1. Selects a coding challenge from its study curriculum
2. Generates an answer using its own inference
3. Critiques and scores its own answer
4. Logs the learning to `primordial_llm/data/evolution_log.json`

All evolution activity is visible in the real-time **Cognitive Telemetry Stream** in the web UI.

---

## Limitations

- Slow inference without a CUDA GPU (7B parameters)
- Self-evolution cycle rate: ~2-4 cycles/day on consumer CPU
- Weight-level self-modification (LoRA fine-tuning loop) not yet implemented
- This is a philosophical/experimental project as much as a technical one

---

## Research Context

This project grew out of the **Primordial Algorithm** research — a speculative model of emergent intelligence through recursive self-organization, substrate absorption, and cognitive layering. See `PRIMORDIAL_DIGESTION_MAP.md` and `PRIMORDIAL_ANATOMY_INDEX.md` for the full theoretical framework.

---

## License

MIT — do whatever you want with it. If you improve it, share it back.

---

## Links

| | |
|---|---|
| **GitHub** | [github.com/jkdkr2439/Primordial-LM](https://github.com/jkdkr2439/Primordial-LM) |
| **HuggingFace** | [huggingface.co/jkdkr2439/Primodial-LM](https://huggingface.co/jkdkr2439/Primodial-LM) |

---

*Built by an independent researcher. Rough edges are part of the experiment.*

