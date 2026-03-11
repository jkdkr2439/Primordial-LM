# Qwen Anatomy Index

## Purpose

This file exposes the host body.
It does not defend Qwen.
It dissects Qwen into occupiable territory.

## Host Entry Points

### `local_qwen_sandbox_chat.py`

Host role:

- original central nervous loop
- reads input
- stores transcript
- calls model
- parses tool intent
- executes tool path
- calls model again for final response

Why this matters:

- this is where Qwen still behaves like the body center
- if left intact conceptually, Primor becomes only a passenger

Digestible nutrients:

- turn lifecycle pattern
- response-after-tool pattern
- transcript evolution pattern

Host structures to dissolve:

- Qwen-centric top-level control authority

### `primordial_llm/output/model_runtime.py`

Host role:

- tokenizer loading
- model loading
- generation mechanics

Digestible nutrients:

- substrate loading procedure
- low-memory loading pattern
- generation invocation pattern

Host structures to preserve temporarily:

- inference mechanics

Host structures to dissolve:

- any right to influence planning or context policy

### `primordial_llm/output/tool_runtime.py`

Host role:

- direct effector execution
- file and command effectors

Digestible nutrients:

- sandbox-safe path resolution
- executable bridge pattern
- standardized effect payloads

Host structures to dissolve:

- direct execution based only on parsed syntax

### `primordial_llm/process/tool_calls.py`

Host role:

- syntax extraction from model emission

Digestible nutrients:

- JSON candidate extraction
- syntax-level tool intent detection

Host structures to dissolve:

- assumption that parsed syntax is sufficiently authoritative

### `llm_sandbox/agent_prompt.md`

Host role:

- behavioral law in prose form

Digestible nutrients:

- operational instructions
- output discipline
- path discipline

Host structures to dissolve:

- dependence on prose-only law enforcement

### `llm_sandbox/sandbox_policy.json`

Host role:

- machine-readable environmental restrictions

Digestible nutrients:

- allowed roots
- blocked commands
- blocked tokens

Host structures to preserve temporarily:

- policy data itself

Host structures to dissolve:

- keeping policy awareness trapped inside prompt summarization only

### `tools/start_primordial_qwen_chat.ps1`

Host role:

- shell boot artery into runtime

Digestible nutrients:

- launch path
- venv selection logic
- runtime entry invocation

Host structures to dissolve:

- any assumption that launching the model equals launching the organism

## Host Loops

### Loop A: User Turn Loop

Pattern:

1. input
2. append transcript
3. generate
4. maybe parse tool
5. maybe run tool
6. generate again
7. print response

This is useful nutrient, but must not remain the governing loop.

### Loop B: Tool Mediation Loop

Pattern:

1. detect tool intent syntax
2. execute tool
3. feed result back to model

This loop lacks a strong Primor law layer between interpretation and execution.

### Loop C: Prompt-Law Loop

Pattern:

1. summarize policy into prompt
2. rely on model compliance

This is weak law tissue and must evolve into structured Primor law.

## Host Nutrient Classes

### Class 1: Runtime nutrients

- model boot
- tokenizer boot
- generation call mechanics
- subprocess bridging

### Class 2: Behavioral nutrients

- turn sequencing
- response chaining
- tool follow-up generation

### Class 3: Safety nutrients

- path sandboxing
- policy boundaries
- blocked command knowledge

### Class 4: Structural nutrients

- transcript persistence
- basic runtime config
- entrypoint conventions

## Immediate Occupation Targets

The first host regions that should lose authority are:

1. top-level turn control
2. transcript-as-total-state
3. parse-to-execute shortcut
4. prompt-only law enforcement
