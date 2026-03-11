from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class GenerationLaw:
    transcript_window: int
    max_new_tokens: int
    require_context_packet: bool = True
    tool_feedback_as_tool_message: bool = True


@dataclass(frozen=True)
class ToolLaw:
    supported_tools: List[str] = field(default_factory=list)
    blocked_commands: List[str] = field(default_factory=list)
    blocked_tokens: List[str] = field(default_factory=list)
    allow_absolute_paths: bool = False
    allow_parent_navigation: bool = False


@dataclass(frozen=True)
class MemoryLaw:
    preserve_identity_anchor: bool = True
    preserve_active_context: bool = True
    preserve_latest_report: bool = True


@dataclass(frozen=True)
class PrimordialLawProfile:
    generation: GenerationLaw
    tools: ToolLaw
    memory: MemoryLaw

    def to_context_packet(self) -> Dict[str, object]:
        return {
            "generation": {
                "transcript_window": self.generation.transcript_window,
                "max_new_tokens": self.generation.max_new_tokens,
                "require_context_packet": self.generation.require_context_packet,
                "tool_feedback_as_tool_message": self.generation.tool_feedback_as_tool_message,
            },
            "tools": {
                "supported_tools": list(self.tools.supported_tools),
                "blocked_commands": list(self.tools.blocked_commands),
                "blocked_tokens": list(self.tools.blocked_tokens),
                "allow_absolute_paths": self.tools.allow_absolute_paths,
                "allow_parent_navigation": self.tools.allow_parent_navigation,
            },
            "memory": {
                "preserve_identity_anchor": self.memory.preserve_identity_anchor,
                "preserve_active_context": self.memory.preserve_active_context,
                "preserve_latest_report": self.memory.preserve_latest_report,
            },
        }


def build_law_profile(policy: Dict[str, object], max_new_tokens: int) -> PrimordialLawProfile:
    return PrimordialLawProfile(
        generation=GenerationLaw(
            transcript_window=8,
            max_new_tokens=max_new_tokens,
        ),
        tools=ToolLaw(
            supported_tools=["list_dir", "read_file", "write_file", "run_command"],
            blocked_commands=[str(item).lower() for item in policy.get("blocked_commands", [])],
            blocked_tokens=[str(item) for item in policy.get("blocked_tokens", [])],
        ),
        memory=MemoryLaw(),
    )
