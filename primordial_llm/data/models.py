from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from primordial_llm.data.law import PrimordialLawProfile
from primordial_llm.data.replacement_tracker import ReplacementTrackerState


Message = Dict[str, str]


@dataclass
class ChatRuntimeConfig:
    repo_root: Path
    weights_dir: Optional[Path] = None
    sandbox_root_name: str = "llm_sandbox"
    max_new_tokens: int = 512
    load_in_4bit: bool = False


@dataclass
class RuntimePaths:
    repo_root: Path
    sandbox_root: Path
    workspace_root: Path
    prompt_path: Path
    policy_path: Path
    logs_root: Path
    memory_root: Path
    short_term_memory_root: Path
    long_term_memory_root: Path
    reports_root: Path
    generated_root: Path


@dataclass
class RuntimeContext:
    config: ChatRuntimeConfig
    paths: RuntimePaths
    policy: Dict[str, object]
    law_profile: PrimordialLawProfile
    system_prompt: str


@dataclass
class ExecutionPlan:
    normalized_input: str
    reasoning_mode: str
    phase_trace: List[str]
    should_generate: bool = True
    warnings: List[str] = field(default_factory=list)


@dataclass
class BootstrapReport:
    summary: str
    report_path: Path
    short_term_note_path: Path
    long_term_note_path: Path
    created_directories: List[Path]
    code_inventory: Dict[str, object]


@dataclass
class TranscriptState:
    system_prompt: str
    conversation: List[Message] = field(default_factory=list)
    tool_messages: List[Message] = field(default_factory=list)

    @classmethod
    def create(cls, system_prompt: str) -> "TranscriptState":
        return cls(system_prompt=system_prompt)

    def append_user_message(self, content: str) -> None:
        self.conversation.append({"role": "user", "content": content})

    def append_assistant_message(self, content: str) -> None:
        self.conversation.append({"role": "assistant", "content": content})

    def append_tool_message(self, content: str) -> None:
        tool_message = {"role": "tool", "content": content}
        self.conversation.append(tool_message)
        self.tool_messages.append(tool_message)

    def latest_messages(self, limit: int) -> List[Message]:
        if limit <= 0:
            return []
        return list(self.conversation[-limit:])


@dataclass
class ActiveTaskState:
    latest_user_input: str = ""
    reasoning_mode: str = "balanced_fusion"
    phase_trace: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def absorb_plan(self, plan: ExecutionPlan) -> None:
        self.latest_user_input = plan.normalized_input
        self.reasoning_mode = plan.reasoning_mode
        self.phase_trace = list(plan.phase_trace)
        self.warnings = list(plan.warnings)


@dataclass
class ValidationTraceState:
    last_decision: Optional[Dict[str, object]] = None
    history: List[Dict[str, object]] = field(default_factory=list)

    def record(self, decision: Dict[str, object]) -> None:
        self.last_decision = dict(decision)
        self.history.append(dict(decision))


@dataclass
class ToolTraceState:
    last_tool_call: Optional[Dict[str, object]] = None
    last_tool_result: Optional[str] = None
    history: List[Dict[str, object]] = field(default_factory=list)
    validation: ValidationTraceState = field(default_factory=ValidationTraceState)

    def record_tool_call(self, tool_call: Dict[str, object]) -> None:
        self.last_tool_call = tool_call
        self.history.append({"type": "call", "payload": dict(tool_call)})

    def record_tool_result(self, tool_result: str) -> None:
        self.last_tool_result = tool_result
        self.history.append({"type": "result", "payload": tool_result})


@dataclass
class MemoryPointers:
    identity_anchor_path: Optional[Path] = None
    active_context_path: Optional[Path] = None
    latest_report_path: Optional[Path] = None
    latest_short_term_snapshot_path: Optional[Path] = None
    latest_long_term_snapshot_path: Optional[Path] = None


@dataclass
class ArtifactTraceState:
    generated_paths: List[Path] = field(default_factory=list)


@dataclass
class ContextAssemblyState:
    last_packet: str = ""
    last_message_count: int = 0

    def record(self, packet: str, message_count: int) -> None:
        self.last_packet = packet
        self.last_message_count = message_count


@dataclass
class ReplicationBlueprint:
    organ_name: str
    target_module: str
    role: str
    planned_interfaces: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    source_nutrients: List[str] = field(default_factory=list)
    status: str = "planned"


@dataclass
class ReplicationState:
    blueprints: List[ReplicationBlueprint] = field(default_factory=list)
    latest_report_path: Optional[Path] = None

    def has_blueprint(self, organ_name: str) -> bool:
        return any(blueprint.organ_name == organ_name for blueprint in self.blueprints)

    def register(self, blueprint: ReplicationBlueprint) -> None:
        if not self.has_blueprint(blueprint.organ_name):
            self.blueprints.append(blueprint)


@dataclass
class MemoryConsolidationState:
    latest_summary: str = ""
    latest_short_term_path: Optional[Path] = None
    latest_long_term_path: Optional[Path] = None
    history: List[str] = field(default_factory=list)

    def record(self, summary: str, short_term_path: Path, long_term_path: Path) -> None:
        self.latest_summary = summary
        self.latest_short_term_path = short_term_path
        self.latest_long_term_path = long_term_path
        self.history.append(summary)


@dataclass
class ChatSessionState:
    transcript: TranscriptState
    active_task: ActiveTaskState = field(default_factory=ActiveTaskState)
    tool_trace: ToolTraceState = field(default_factory=ToolTraceState)
    memory_pointers: MemoryPointers = field(default_factory=MemoryPointers)
    artifact_trace: ArtifactTraceState = field(default_factory=ArtifactTraceState)
    context_assembly: ContextAssemblyState = field(default_factory=ContextAssemblyState)
    replication: ReplicationState = field(default_factory=ReplicationState)
    replacement_tracker: ReplacementTrackerState = field(default_factory=ReplacementTrackerState)
    memory_consolidation: MemoryConsolidationState = field(default_factory=MemoryConsolidationState)
    state_changes: int = 0

    @classmethod
    def create(cls, system_prompt: str) -> "ChatSessionState":
        return cls(transcript=TranscriptState.create(system_prompt))

    def absorb_plan(self, plan: ExecutionPlan) -> None:
        self.active_task.absorb_plan(plan)

    def append_user_message(self, content: str) -> None:
        self.transcript.append_user_message(content)

    def append_assistant_message(self, content: str) -> None:
        self.transcript.append_assistant_message(content)

    def append_tool_message(self, content: str) -> None:
        self.transcript.append_tool_message(content)
