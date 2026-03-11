from pathlib import Path
from typing import Dict

from primordial_llm.output.tool_runtime import handle_tool_call


class PrimordialEffectorAdapter:
    """Explicit subordinate adapter for host execution tissue."""

    def execute(
        self,
        tool_call: Dict[str, object],
        sandbox_root: Path,
        workspace_root: Path,
        repo_root: Path,
    ) -> str:
        return handle_tool_call(tool_call, sandbox_root, workspace_root, repo_root)
