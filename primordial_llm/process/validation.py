from dataclasses import dataclass
from pathlib import PureWindowsPath
from typing import Dict

from primordial_llm.data.models import RuntimeContext


@dataclass
class ToolValidationResult:
    approved: bool
    tool_call: Dict[str, object]
    reason: str

    def to_trace_record(self) -> Dict[str, object]:
        return {
            "approved": self.approved,
            "reason": self.reason,
            "tool": self.tool_call.get("tool"),
        }

    def to_tool_message(self) -> str:
        status = "approved" if self.approved else "rejected"
        return f"Primor validation {status}: {self.reason}"


class PrimordialToolValidator:
    def __init__(self, runtime: RuntimeContext) -> None:
        self.runtime = runtime
        self.tool_law = runtime.law_profile.tools
        self.supported_tools = set(self.tool_law.supported_tools)
        self.blocked_commands = set(self.tool_law.blocked_commands)
        self.blocked_tokens = tuple(self.tool_law.blocked_tokens)

    def validate(self, tool_call: Dict[str, object]) -> ToolValidationResult:
        tool_name = str(tool_call.get("tool", "")).strip()
        if tool_name not in self.supported_tools:
            return ToolValidationResult(False, tool_call, f"unsupported tool '{tool_name}'")

        if tool_name in {"list_dir", "read_file", "write_file"}:
            path_value = str(tool_call.get("path", "")).strip()
            if tool_name != "list_dir" and not path_value:
                return ToolValidationResult(False, tool_call, "missing relative path")
            if path_value and not self._is_safe_relative_path(path_value):
                return ToolValidationResult(False, tool_call, f"unsafe relative path '{path_value}'")
            return ToolValidationResult(True, tool_call, f"{tool_name} path accepted")

        executable = str(tool_call.get("executable", "")).strip()
        arguments = str(tool_call.get("arguments", ""))
        working_directory = str(tool_call.get("working_directory", ".")).strip() or "."
        if not executable:
            return ToolValidationResult(False, tool_call, "missing executable")
        if not self._is_safe_relative_path(working_directory):
            return ToolValidationResult(False, tool_call, f"unsafe working directory '{working_directory}'")
        if executable.lower() in self.blocked_commands:
            return ToolValidationResult(False, tool_call, f"blocked executable '{executable}'")
        lowered_arguments = arguments.lower()
        if any(blocked == lowered_arguments for blocked in self.blocked_commands):
            return ToolValidationResult(False, tool_call, "arguments resolve to a blocked command")
        if any(token in arguments for token in self.blocked_tokens):
            return ToolValidationResult(False, tool_call, "arguments contain blocked shell control tokens")
        if any(blocked in lowered_arguments.split() for blocked in self.blocked_commands):
            return ToolValidationResult(False, tool_call, "arguments reference blocked commands")
        return ToolValidationResult(True, tool_call, f"run_command accepted for '{executable}'")

    def _is_safe_relative_path(self, value: str) -> bool:
        if value in {"", "."}:
            return True
        candidate = PureWindowsPath(value)
        if not self.tool_law.allow_absolute_paths and (candidate.is_absolute() or candidate.drive or candidate.root):
            return False
        if not self.tool_law.allow_parent_navigation and ".." in candidate.parts:
            return False
        return True
