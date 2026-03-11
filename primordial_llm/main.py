from pathlib import Path

from primordial_llm.data.context_registry import build_runtime_context
from primordial_llm.data.models import ChatSessionState
from primordial_llm.display.console import show_bootstrap_report, show_startup
from primordial_llm.input.cli import parse_args, read_user_input
from primordial_llm.output.substrate_adapter import PrimordialSubstrateAdapter
from primordial_llm.process.action_cycle import PrimordialActionCycle
from primordial_llm.process.bootstrap import PrimordialBootstrapper


def run_chat() -> None:
    config = parse_args()
    runtime = build_runtime_context(config)
    bootstrapper = PrimordialBootstrapper(runtime)
    bootstrap_report = bootstrapper.bootstrap()
    substrate_adapter = PrimordialSubstrateAdapter()

    if config.weights_dir is None:
        raise SystemExit("[plm] No weights dir provided. Set PLM_WEIGHTS_DIR or pass --weights-dir.")

    weights_dir = config.weights_dir.resolve()
    if not weights_dir.exists():
        raise SystemExit(f"[plm] Weights dir not found: {weights_dir}")

    substrate = substrate_adapter.load_substrate(
        weights_dir,
        config.load_in_4bit,
        config.max_new_tokens,
    )

    cycle = PrimordialActionCycle(runtime, substrate)
    session = ChatSessionState.create(runtime.system_prompt)
    session.memory_pointers.active_context_path = bootstrap_report.short_term_note_path
    session.memory_pointers.identity_anchor_path = bootstrap_report.long_term_note_path
    session.memory_pointers.latest_report_path = bootstrap_report.report_path
    cycle.bootstrap_session(session)

    show_bootstrap_report(bootstrap_report)
    print(f"[plm] repo root: {runtime.paths.repo_root}")
    print(f"[plm] weights dir: {weights_dir}")
    if session.replication.latest_report_path:
        print(f"[primordial] replication report: {session.replication.latest_report_path}")
    if session.replacement_tracker.latest_report_path:
        print(f"[primordial] replacement tracker: {session.replacement_tracker.latest_report_path}")
    if session.memory_consolidation.latest_short_term_path:
        print(f"[primordial] memory snapshot: {session.memory_consolidation.latest_short_term_path}")
    show_startup(runtime.paths.workspace_root)

    while True:
        try:
            user_input = read_user_input()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input in {"/exit", "/quit"}:
            break

        cycle.run_turn(session, user_input)


def main() -> None:
    run_chat()


if __name__ == "__main__":
    main()
