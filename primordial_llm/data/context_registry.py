import json
from pathlib import Path

from primordial_llm.data.law import build_law_profile
from primordial_llm.data.models import ChatRuntimeConfig, RuntimeContext, RuntimePaths


def fail(message: str) -> None:
    raise SystemExit(f"[plm] {message}")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def summarize_policy(policy: dict) -> str:
    allowed_roots = ", ".join(policy.get("allowed_roots", []))
    blocked_commands = ", ".join(policy.get("blocked_commands", []))
    blocked_tokens = " ".join(policy.get("blocked_tokens", []))
    return (
        "Sandbox policy summary:\n"
        f"- Allowed roots: {allowed_roots}\n"
        f"- Blocked commands: {blocked_commands}\n"
        f"- Blocked tokens: {blocked_tokens}\n"
        "- When you need to act, respond with a JSON object only.\n"
        "- Supported tools: list_dir, read_file, write_file, run_command."
    )


def ensure_runtime_directories(paths: RuntimePaths) -> None:
    for path in (
        paths.logs_root,
        paths.memory_root,
        paths.short_term_memory_root,
        paths.long_term_memory_root,
        paths.reports_root,
        paths.generated_root,
    ):
        path.mkdir(parents=True, exist_ok=True)


def build_runtime_context(config: ChatRuntimeConfig) -> RuntimeContext:
    repo_root = config.repo_root.resolve()
    sandbox_root = (repo_root / config.sandbox_root_name).resolve()
    workspace_root = sandbox_root / "workspace"
    prompt_path = sandbox_root / "agent_prompt.md"
    policy_path = sandbox_root / "sandbox_policy.json"
    logs_root = sandbox_root / "logs"
    memory_root = sandbox_root / "memory"
    short_term_memory_root = memory_root / "short_term"
    long_term_memory_root = memory_root / "long_term"
    reports_root = memory_root / "reports"
    generated_root = workspace_root / "primordial_generated"

    if not repo_root.exists():
        fail(f"Repo root not found: {repo_root}")
    if not sandbox_root.exists():
        fail(f"Sandbox root not found: {sandbox_root}")
    if not workspace_root.exists():
        fail(f"Sandbox workspace not found: {workspace_root}")
    if not prompt_path.exists() or not policy_path.exists():
        fail("Sandbox prompt/policy files are missing.")

    policy = json.loads(load_text(policy_path))
    law_profile = build_law_profile(policy, config.max_new_tokens)
    system_prompt = load_text(prompt_path).strip() + "\n\n" + summarize_policy(policy)
    paths = RuntimePaths(
        repo_root=repo_root,
        sandbox_root=sandbox_root,
        workspace_root=workspace_root,
        prompt_path=prompt_path,
        policy_path=policy_path,
        logs_root=logs_root,
        memory_root=memory_root,
        short_term_memory_root=short_term_memory_root,
        long_term_memory_root=long_term_memory_root,
        reports_root=reports_root,
        generated_root=generated_root,
    )
    ensure_runtime_directories(paths)
    return RuntimeContext(
        config=config,
        paths=paths,
        policy=policy,
        law_profile=law_profile,
        system_prompt=system_prompt,
    )
