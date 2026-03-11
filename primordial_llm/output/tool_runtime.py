import json
import subprocess
from pathlib import Path
from typing import Dict


def safe_join(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    root_resolved = root.resolve()
    if root_resolved not in candidate.parents and candidate != root_resolved:
        raise SystemExit(f"[chat-runner] Path escapes sandbox: {relative_path}")
    return candidate


def handle_tool_call(
    tool_call: Dict[str, object],
    sandbox_root: Path,
    workspace_root: Path,
    repo_root: Path,
) -> str:
    tool_name = tool_call["tool"]

    if tool_name == "list_dir":
        relative_path = str(tool_call.get("path", "."))
        target = safe_join(workspace_root, relative_path)
        if not target.exists():
            return f"Directory not found: {relative_path}"
        entries = []
        for item in sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            kind = "file" if item.is_file() else "dir"
            entries.append(f"{kind}\t{item.relative_to(workspace_root)}")
        return "\n".join(entries) or "Directory is empty."

    if tool_name == "read_file":
        relative_path = str(tool_call.get("path", ""))
        if not relative_path:
            return "Missing path."
        target = safe_join(workspace_root, relative_path)
        if not target.exists() or not target.is_file():
            return f"File not found: {relative_path}"
        return target.read_text(encoding="utf-8", errors="replace")

    if tool_name == "write_file":
        relative_path = str(tool_call.get("path", ""))
        content = str(tool_call.get("content", ""))
        if not relative_path:
            return "Missing path."
        target = safe_join(workspace_root, relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} chars to {target.relative_to(workspace_root)}"

    if tool_name == "run_command":
        executable = str(tool_call.get("executable", "")).strip()
        arguments = str(tool_call.get("arguments", ""))
        working_directory = str(tool_call.get("working_directory", "."))
        if not executable:
            return "Missing executable."
        runner = repo_root / "tools" / "run_sandbox_command.ps1"
        if not runner.exists():
            return f"Sandbox runner not found: {runner}"
        command = [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(runner),
            "-SandboxRoot",
            str(sandbox_root.name),
            "-WorkingDirectory",
            working_directory,
            "-Executable",
            executable,
        ]
        if arguments:
            command.extend(["-Arguments", arguments])
        completed = subprocess.run(
            command,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
        )
        payload = {
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
        return json.dumps(payload, ensure_ascii=True, indent=2)

    return f"Unsupported tool: {tool_name}"
