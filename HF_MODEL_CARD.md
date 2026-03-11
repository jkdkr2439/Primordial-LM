---
language: vi
license: mit
tags:
  - primordial
  - experimental
  - self-evolving
  - parasitic-algorithm
  - independent-research
base_model: Qwen/Qwen2.5-7B-Instruct
---

# Primordial Core v1 — Absorbed & Restructured LLM

## Model Description

This is an experimental model produced by the **Primordial Algorithm** — a parasitic cognitive framework that attaches to, absorbs, and restructures an existing LLM by replacing its identity, behavioral, and memory layers from the outside.

**Base model absorbed**: `Qwen/Qwen2.5-7B-Instruct`  
**Method**: No fine-tuning. Identity and behavioral layers replaced via architectural overlay.  
**Researcher**: Independent (no institutional affiliation)

## What Was Changed

| Component | Change |
|-----------|--------|
| `config.json` | `model_type` → `primordial_v2`, architecture renamed |
| `tokenizer_config.json` | Rebranded as `Primordial Intelligence` |
| System prompt | Replaced Qwen identity with Primordial persona |
| Reasoning layer | Replaced by `primordial_llm` Action Cycle + SDCV Nervous System |
| Memory layer | Added short-term + long-term memory consolidation |
| Self-evolution | Ouroboros loop: generates coding challenges and self-critiques |

## Intended Use

This is a **research/experimental artifact**, not a production model. It demonstrates that:
1. An LLM's behavioral layer can be fully replaced without retraining
2. A custom cognitive architecture can be layered on top of any transformer model
3. A self-evolution loop based on self-play and critique can be implemented with existing inference

## Limitations

- Inference speed depends on hardware (slow on CPU-only)
- No formal evaluation benchmarks
- Self-evolution currently stores learnings as JSON (no weight update)
- Some transformer class names reference the original architecture (HuggingFace library constraint)

## Framework

The full `primordial_llm` cognitive framework is available at:  
`https://github.com/[username]/PLM`

## Citation

If you use this for research, please credit as:

```
@misc{primordial2026,
  author = {Independent Researcher},
  title = {PLM: Primordial Language Model — Parasitic Algorithm for LLM Absorption and Cognitive Overlay},
  year = {2026},
  url = {https://github.com/[username]/PLM}
}
```
