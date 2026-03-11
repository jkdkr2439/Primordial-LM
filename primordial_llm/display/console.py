import json
from pathlib import Path

from primordial_llm.data.models import BootstrapReport, ExecutionPlan


def show_startup(workspace_root: Path) -> None:
    print("[chat-runner] Model loaded. Type /exit to quit.")
    print("[chat-runner] Sandbox workspace:", workspace_root)


def show_bootstrap_report(report: BootstrapReport) -> None:
    print("[primordial] bootstrap complete")
    print(f"[primordial] {report.summary}")
    print(f"[primordial] report: {report.report_path}")
    print(f"[primordial] short-term memory: {report.short_term_note_path}")
    print(f"[primordial] long-term memory: {report.long_term_note_path}")


def show_plan(plan: ExecutionPlan) -> None:
    print(
        "[primordial] "
        f"mode={plan.reasoning_mode} phases={' -> '.join(plan.phase_trace)}",
        flush=True,
    )


def show_tool_call(tool_call: dict) -> None:
    print("assistant(tool)>", json.dumps(tool_call, ensure_ascii=True, indent=2))


def show_tool_result(tool_result: str) -> None:
    print("tool>", tool_result)


def show_assistant_message(message: str) -> None:
    print("assistant>", message)
