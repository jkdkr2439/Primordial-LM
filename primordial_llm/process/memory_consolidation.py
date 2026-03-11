from datetime import datetime
from pathlib import Path

from primordial_llm.data.models import ChatSessionState, RuntimeContext


class PrimordialMemoryConsolidator:
    """Condenses live Primor session traces into durable short-term and long-term memory artifacts."""

    def __init__(self, runtime: RuntimeContext) -> None:
        self.runtime = runtime

    def consolidate(self, session: ChatSessionState, reason: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        short_term_path = self.runtime.paths.short_term_memory_root / f"primor-session-{timestamp}.md"
        long_term_path = self.runtime.paths.long_term_memory_root / "primor_evolution_journal.md"

        short_term_content = self._build_short_term_note(session, reason)
        long_term_append = self._build_long_term_append(session, reason)

        short_term_path.write_text(short_term_content, encoding="utf-8")
        with long_term_path.open("a", encoding="utf-8") as handle:
            if long_term_path.stat().st_size == 0:
                handle.write("# Primor Evolution Journal\n\n")
            handle.write(long_term_append)

        summary = (
            f"reason={reason}; messages={len(session.transcript.conversation)}; "
            f"blueprints={len(session.replication.blueprints)}; "
            f"territories={len(session.replacement_tracker.territories)}"
        )
        session.memory_consolidation.record(summary, short_term_path, long_term_path)
        session.memory_pointers.latest_short_term_snapshot_path = short_term_path
        session.memory_pointers.latest_long_term_snapshot_path = long_term_path

    def _build_short_term_note(self, session: ChatSessionState, reason: str) -> str:
        recent_messages = session.transcript.latest_messages(6)
        recent_lines = "\n".join(
            f"- {message['role']}: {message['content'][:160]}" for message in recent_messages
        ) or "- no messages yet"
        blueprint_lines = "\n".join(
            f"- {blueprint.organ_name} -> {blueprint.target_module} ({blueprint.status})"
            for blueprint in session.replication.blueprints
        ) or "- no blueprints"
        return (
            "# Primor Session Snapshot\n\n"
            f"- Reason: {reason}\n"
            f"- Latest input: {session.active_task.latest_user_input or '[none]'}\n"
            f"- Reasoning mode: {session.active_task.reasoning_mode}\n"
            f"- Phase trace: {' -> '.join(session.active_task.phase_trace) or '[none]'}\n"
            f"- Last tool result: {session.tool_trace.last_tool_result or '[none]'}\n"
            f"- Replacement summary: {session.replacement_tracker.summarize()}\n\n"
            "## Recent Messages\n"
            f"{recent_lines}\n\n"
            "## Replication Blueprints\n"
            f"{blueprint_lines}\n"
        )

    def _build_long_term_append(self, session: ChatSessionState, reason: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest_blueprints = ", ".join(blueprint.organ_name for blueprint in session.replication.blueprints) or "none"
        replacement_summary = session.replacement_tracker.summarize()
        return (
            f"## {timestamp}\n\n"
            f"- Reason: {reason}\n"
            f"- Latest input: {session.active_task.latest_user_input or '[none]'}\n"
            f"- Reasoning mode: {session.active_task.reasoning_mode}\n"
            f"- Blueprints: {latest_blueprints}\n"
            f"- Replacement summary: {replacement_summary}\n"
            f"- Latest reports: bootstrap={self._path_text(session.memory_pointers.latest_report_path)}, "
            f"replication={self._path_text(session.replication.latest_report_path)}, "
            f"replacement={self._path_text(session.replacement_tracker.latest_report_path)}\n\n"
        )

    @staticmethod
    def _path_text(path: Path | None) -> str:
        return "[none]" if path is None else str(path)
