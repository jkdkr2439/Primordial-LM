# Primordial Qwen Digestion Map

## Core Principle

This repository should not evolve toward "Primordial wrapped around Qwen."

It should evolve toward:

- Qwen as digestible substrate
- Primordial as the host organism
- Qwen logic decomposed into capabilities
- each capability re-assigned to the correct Primordial organ

The architectural center must remain Primordial.
Qwen should become one of the organs Primordial uses, not the skeleton of the system.

## Host-Substrate Model

### Primordial is the host

Primordial owns:

- identity
- memory
- intent absorption
- phase selection
- reasoning mode selection
- planning
- constraint enforcement
- execution routing
- response shaping
- long-term evolution

### Qwen is the substrate

Qwen contributes:

- tokenizer + chat template
- model inference
- next-token generation
- language completion ability
- latent tool-call emission
- conversational continuation patterns

Qwen should not own the top-level control loop once digestion is complete.

## Qwen Capabilities To Digest

The current Qwen-derived runtime exposes several real capabilities. Those capabilities must be separated from their original runner form.

### 1. Session loop

Observed in:

- `local_qwen_sandbox_chat.py`
- `primordial_llm/main.py`

Qwen-native form:

- read user input
- append messages
- generate reply
- maybe parse tool call
- maybe execute tool
- generate final reply

Primordial digestion:

- move ownership of turn lifecycle to `PROCESS`
- treat generation as one stage inside a larger Primordial action cycle
- allow pre-generation and post-generation stages to remain independent of model inference

Target owner:

- `primordial_llm/process`

### 2. Prompt assembly

Observed in:

- `local_qwen_sandbox_chat.py`
- `primordial_llm/output/model_runtime.py`
- `primordial_llm/data/context_registry.py`

Qwen-native form:

- build `messages`
- apply chat template
- append generation prompt

Primordial digestion:

- split raw conversation state from role-specific cognitive state
- let Primordial decide what context is injected
- let Qwen only render Primordial state into tokenizable form

Target owner:

- state design in `primordial_llm/data`
- assembly policy in `primordial_llm/process`
- final tokenization bridge in `primordial_llm/output`

### 3. Model loading and inference

Observed in:

- `local_qwen_sandbox_chat.py`
- `primordial_llm/output/model_runtime.py`

Qwen-native form:

- load tokenizer
- load model
- choose quantization
- generate text

Primordial digestion:

- reduce this to a pure substrate service
- inference should not know planning, phases, memory architecture, or tool policy

Target owner:

- `primordial_llm/output`

### 4. Tool-call emission

Observed in:

- `local_qwen_sandbox_chat.py`
- `primordial_llm/process/tool_calls.py`

Qwen-native form:

- produce JSON-looking text
- parse JSON
- treat any `tool` field as executable intent

Primordial digestion:

- Qwen may suggest an action
- Primordial must validate whether that suggestion becomes executable intent
- tool-call parsing is not enough; there must be authorization, classification, and routing

Target owner:

- syntax extraction in `primordial_llm/process/tool_calls.py`
- semantic validation in `primordial_llm/process`
- execution in `primordial_llm/output/tool_runtime.py`

### 5. Tool execution

Observed in:

- `local_qwen_sandbox_chat.py`
- `primordial_llm/output/tool_runtime.py`

Qwen-native form:

- read file
- write file
- list dir
- run command

Primordial digestion:

- tools become effectors
- effectors are downstream organs
- the model is not the one acting; Primordial is acting through effectors

Target owner:

- execution in `primordial_llm/output`
- permission and intent checks in `primordial_llm/process`
- path and runtime constraints in `primordial_llm/data`

### 6. Conversation state retention

Observed in:

- `local_qwen_sandbox_chat.py`
- `primordial_llm/data/models.py`

Qwen-native form:

- a flat `messages` array

Primordial digestion:

- separate transcript from cognition
- keep at least these state layers distinct:
  - transcript memory
  - active task memory
  - identity anchor
  - execution trace
  - tool trace
  - generated artifacts

Target owner:

- `primordial_llm/data`

### 7. Safety boundary assembly

Observed in:

- `llm_sandbox/agent_prompt.md`
- `llm_sandbox/sandbox_policy.json`
- `primordial_llm/data/context_registry.py`

Qwen-native form:

- merge prompt text and policy summary into one system message

Primordial digestion:

- system prompt should stop being the only carrier of law
- policy must become structured runtime law, not only prose fed into the model

Target owner:

- policy registry in `primordial_llm/data`
- enforcement and gating in `primordial_llm/process`
- explanation rendering in `primordial_llm/display`

### 8. Startup bootstrap

Observed in:

- `primordial_llm/process/bootstrap.py`
- `tools/start_primordial_qwen_chat.ps1`

Qwen-native inheritance:

- start model
- start loop

Primordial digestion:

- bootstrap should scan substrate state
- materialize memory organs
- anchor identity
- inventory capabilities
- prepare evolution workspace before the first turn

Target owner:

- `primordial_llm/process/bootstrap.py`

This is the part already moving in the right direction.

## Primordial Organ Assignment

### INPUT

Responsibilities:

- user signal intake
- intent normalization
- command vs request vs reflection separation
- entrypoint adaptation for CLI later expanding to other interfaces

Should absorb from Qwen:

- turn entry semantics only

Should never absorb:

- model loading
- tool execution

Current files:

- `primordial_llm/input/cli.py`

### DATA

Responsibilities:

- runtime paths
- policy registry
- session schema
- memory schema
- context registry
- state separation between transcript and cognition

Should absorb from Qwen:

- message schema ideas
- system-context scaffolding

Should never absorb:

- orchestration
- printing

Current files:

- `primordial_llm/data/models.py`
- `primordial_llm/data/context_registry.py`

### PROCESS

Responsibilities:

- intent digestion
- phase trace
- reasoning mode selection
- action planning
- tool authorization
- context packing policy
- execution orchestration
- post-action integration

Should absorb from Qwen:

- turn progression pattern
- tool-call interpretation pattern

Should never absorb:

- direct tokenizer/model code

Current files:

- `primordial_llm/process/orchestrator.py`
- `primordial_llm/process/primordial.py`
- `primordial_llm/process/bootstrap.py`
- `primordial_llm/process/tool_calls.py`

### OUTPUT

Responsibilities:

- substrate inference
- tool effectors
- command execution bridge
- artifact emission

Should absorb from Qwen:

- tokenizer
- model loading
- generation
- tool runtime mechanics

Should never absorb:

- architecture decisions
- top-level execution policy

Current files:

- `primordial_llm/output/model_runtime.py`
- `primordial_llm/output/tool_runtime.py`

### DISPLAY

Responsibilities:

- observable manifestation
- console rendering
- trace visibility
- report formatting

Should absorb from Qwen:

- minimal chat display habits only

Current files:

- `primordial_llm/display/console.py`

## Current Anti-Patterns

The repository still contains Qwen-centric gravity in several places.

### Anti-pattern 1: Qwen-style main loop still defines reality

Evidence:

- `local_qwen_sandbox_chat.py`
- `primordial_llm/main.py`

Problem:

- Primordial planning is inserted into a fundamentally Qwen-shaped loop
- the host is still reacting inside a substrate-native skeleton

Desired correction:

- define a Primordial action cycle first
- call inference only when the cycle requires language realization

### Anti-pattern 2: Flat message history is still the dominant state model

Evidence:

- `ChatSessionState.messages`

Problem:

- transcript and cognition are fused
- no distinction yet between memory, plan, law, artifact trace, and interaction trace

Desired correction:

- split session state into multiple strata

### Anti-pattern 3: Tool call parsing is too close to tool execution

Evidence:

- `parse_tool_call(...)` output is nearly executable as-is

Problem:

- syntax is being treated almost like authorization

Desired correction:

- require explicit Primordial validation and routing between parse and execution

### Anti-pattern 4: Safety law is still mostly prose

Evidence:

- prompt + summarized policy are concatenated into the system message

Problem:

- law should exist as structured, enforceable runtime logic, not only persuasive prompt text

Desired correction:

- move from prompt-law to runtime-law

## Target Refactor Direction

The end state should feel like this:

1. Primordial receives raw user input.
2. Primordial classifies intent and updates active state.
3. Primordial decides whether to think, ask, act, invoke tools, or generate language.
4. Primordial assembles a bounded context package for the language organ.
5. Qwen performs language inference only inside that bounded package.
6. Primordial inspects the returned emission.
7. If an action is proposed, Primordial validates and routes it.
8. Output organs execute effects.
9. Primordial integrates the result into memory and emits the final manifestation.

This means the control center is no longer "chat loop -> model -> maybe tool."

It becomes:

"host cognition -> organ routing -> substrate inference/effectors -> reintegration."

## Immediate Refactor Priorities

### Priority 1

Replace `ChatSessionState` with a layered session model:

- transcript state
- active task state
- plan state
- tool trace
- memory pointers

### Priority 2

Insert a validation stage between:

- tool-call parse
- tool execution

### Priority 3

Move context assembly authority out of the inference runtime and into `PROCESS`.

### Priority 4

Keep `local_qwen_sandbox_chat.py` only as legacy reference, not as the conceptual model.

### Priority 5

Treat `output/model_runtime.py` as a substrate adapter and rename/restructure it later accordingly.

## Practical Rule For Future Changes

Before adding any feature, ask:

- Is this Primordial cognition?
- Is this memory structure?
- Is this substrate inference?
- Is this an effector?
- Is this only display?

If a change cannot answer that clearly, the digestion is incomplete.
