# LLM Sandbox

This folder is a constrained workspace for a local coding model such as Qwen2.5-7B-Instruct.

## Goals

- Give the model its own working directory.
- Keep command execution inside a small, auditable boundary.
- Preserve logs, prompts, and scratch files for later review.

## Layout

- `workspace/`: files the model is allowed to create and edit.
- `memory/`: notes, plans, and distilled learnings for the agent.
- `logs/`: command logs and execution traces.
- `runtime/`: optional virtual environment and local runtime state.
- `sandbox_policy.json`: allowed roots and blocked commands.
- `agent_prompt.md`: a starter system prompt for your local Qwen runner.
- `..\tools\`: helper scripts that control sandbox execution.

## Bootstrap

From `D:\Tung\Qwen2.5-7B-Instruct`:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap_llm_sandbox.ps1
```

If Python is installed, the bootstrap script will also create `llm_sandbox\runtime\.venv`.
If Python is not installed yet, the directory structure is still created and the script prints the next step.

## Run A Command Inside The Sandbox

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_sandbox_command.ps1 -Executable git -Arguments "status"
```

Or target a subfolder inside the sandbox workspace:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_sandbox_command.ps1 -WorkingDirectory demo -Executable cmd -Arguments "/c dir"
```

## Connecting Qwen Later

Your inference layer should give Qwen only these tools:

1. Read files under `llm_sandbox\workspace`.
2. Write files under `llm_sandbox\workspace` and `llm_sandbox\memory`.
3. Execute commands only through `.\tools\run_sandbox_command.ps1`.

That keeps the model useful without letting it roam across the whole machine.
