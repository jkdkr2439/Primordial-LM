import json
from pathlib import Path
from typing import List

from primordial_llm.data.models import ChatSessionState, Message, RuntimeContext


class PrimordialContextAssembler:
    """Packages only the bounded context Primor wants the substrate to see."""

    def __init__(self, runtime: RuntimeContext) -> None:
        self.runtime = runtime
        self.generation_law = runtime.law_profile.generation

    def assemble_messages(self, session: ChatSessionState) -> List[Message]:
        packet = {
            "primor_active_task": {
                "latest_user_input": session.active_task.latest_user_input,
                "reasoning_mode": session.active_task.reasoning_mode,
                "phase_trace": session.active_task.phase_trace,
                "warnings": session.active_task.warnings,
            },
            "primor_memory_pointers": {
                "active_context_path": self._stringify_path(session.memory_pointers.active_context_path),
                "identity_anchor_path": self._stringify_path(session.memory_pointers.identity_anchor_path),
                "latest_report_path": self._stringify_path(session.memory_pointers.latest_report_path),
            },
            "primor_tool_state": {
                "last_tool_call": session.tool_trace.last_tool_call,
                "last_tool_result": session.tool_trace.last_tool_result,
                "last_validation": session.tool_trace.validation.last_decision,
            },
            "primor_artifact_state": {
                "generated_paths": [self._stringify_path(path) for path in session.artifact_trace.generated_paths],
            },
            "primor_replication_state": {
                "latest_report_path": self._stringify_path(session.replication.latest_report_path),
                "blueprints": [
                    {
                        "organ_name": blueprint.organ_name,
                        "target_module": blueprint.target_module,
                        "status": blueprint.status,
                    }
                    for blueprint in session.replication.blueprints
                ],
            },
            "primor_replacement_state": {
                "latest_report_path": self._stringify_path(session.replacement_tracker.latest_report_path),
                "summary": session.replacement_tracker.summarize(),
                "territories": [
                    {
                        "name": territory.name,
                        "path": territory.path,
                        "status": territory.status,
                    }
                    for territory in session.replacement_tracker.territories
                ],
            },
            "primor_context_law": self.runtime.law_profile.to_context_packet(),
        }
        packet_text = json.dumps(packet, ensure_ascii=True, indent=2)
        bounded_transcript = session.transcript.latest_messages(self.generation_law.transcript_window)
        session.context_assembly.record(packet_text, len(bounded_transcript))
        messages = [{"role": "system", "content": session.transcript.system_prompt}]
        if self.generation_law.require_context_packet:
            messages.append({"role": "system", "content": f"Primor context packet:\n{packet_text}"})
        messages.extend(bounded_transcript)
        return messages

    @staticmethod
    def _stringify_path(value: Path | None) -> str | None:
        return None if value is None else str(value)
