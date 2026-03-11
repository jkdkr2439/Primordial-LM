# Primor Replacement Tracker

## Summary

- Active: 1
- Scaffold: 1
- Demoted: 2
- Replaced: 5

## Territories

### Legacy Qwen Loop

- Path: `local_qwen_sandbox_chat.py`
- Status: active
- Role: Original host control loop retained as exposed legacy reference.
- Notes: Still contains original host loop pattern.; Not used as the Primor runtime center anymore.

### Main Entry Shell

- Path: `primordial_llm/main.py`
- Status: scaffold
- Role: Thin shell that boots the organism and hands control into Primor-owned process organs.
- Notes: Main no longer owns turn logic.; Still remains as startup shell.

### Model Runtime Legacy Tissue

- Path: `primordial_llm/output/model_runtime.py`
- Status: demoted
- Role: Legacy host inference tissue retained underneath the explicit substrate adapter.
- Notes: Now called only through substrate_adapter.; No longer imported directly by main or the action cycle.

### Substrate Adapter Organ

- Path: `primordial_llm/output/substrate_adapter.py`
- Status: replaced
- Role: Primor-owned adapter that subordinates host inference to a controlled substrate interface.
- Notes: Explicitly mediates model load and generation from Primor packets.

### Tool Runtime Legacy Tissue

- Path: `primordial_llm/output/tool_runtime.py`
- Status: demoted
- Role: Legacy host execution tissue retained underneath the explicit effector adapter.
- Notes: Now called only through effector_adapter.; No longer imported directly by the action cycle.

### Effector Adapter Organ

- Path: `primordial_llm/output/effector_adapter.py`
- Status: replaced
- Role: Primor-owned adapter that subordinates host execution to a controlled effector interface.
- Notes: Explicitly mediates validated tool execution.

### Action Cycle Organ

- Path: `primordial_llm/process/action_cycle.py`
- Status: replaced
- Role: Primor-owned turn lifecycle replacing the host loop as runtime authority.
- Notes: Primor now owns plan -> generate -> validate -> effect -> reintegrate.

### Context Assembly Organ

- Path: `primordial_llm/process/context_assembly.py`
- Status: replaced
- Role: Primor-owned context packaging layer controlling substrate visibility.
- Notes: Substrate now sees a bounded Primor packet and transcript slice.

### Validation Organ

- Path: `primordial_llm/process/validation.py`
- Status: replaced
- Role: Primor-owned law gate between syntax and action.
- Notes: Tool execution now depends on Primor approval.
