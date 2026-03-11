import json
from datetime import datetime
from pathlib import Path

from primordial_llm.data.models import BootstrapReport, RuntimeContext


SCAN_EXTENSIONS = {".py", ".ps1", ".bat", ".md", ".txt", ".json"}
SKIP_DIRS = {".git", "__pycache__", ".venv"}


class PrimordialBootstrapper:
    def __init__(self, runtime: RuntimeContext) -> None:
        self.runtime = runtime

    def bootstrap(self) -> BootstrapReport:
        created_directories = self._ensure_primordial_memory()
        inventory = self._scan_repository()
        report = self._persist_report(created_directories, inventory)
        return report

    def _ensure_primordial_memory(self) -> list[Path]:
        paths = self.runtime.paths
        targets = [
            paths.short_term_memory_root,
            paths.long_term_memory_root,
            paths.reports_root,
            paths.generated_root,
            paths.generated_root / "experiments",
            paths.generated_root / "scratch",
            paths.generated_root / "artifacts",
        ]
        created = []
        for target in targets:
            if not target.exists():
                target.mkdir(parents=True, exist_ok=True)
                created.append(target)
        return created

    def _scan_repository(self) -> dict[str, object]:
        repo_root = self.runtime.paths.repo_root
        extension_counts: dict[str, int] = {}
        interesting_files: list[str] = []
        top_level_dirs: list[str] = []
        total_files = 0

        for child in sorted(repo_root.iterdir(), key=lambda item: item.name.lower()):
            if child.is_dir():
                top_level_dirs.append(child.name)

        for path in repo_root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(repo_root)
            if any(part in SKIP_DIRS for part in relative.parts):
                continue
            total_files += 1
            ext = path.suffix.lower()
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
            if ext in SCAN_EXTENSIONS and len(interesting_files) < 24:
                interesting_files.append(str(relative))

        key_paths = []
        for candidate in (
            "primordial_llm/api.py",
            "primordial_llm/main.py",
            "primordial_llm/process/orchestrator.py",
            "primordial_llm/process/primordial.py",
            "primordial_llm/process/ouroboros.py",
            "llm_sandbox/agent_prompt.md",
            "llm_sandbox/sandbox_policy.json",
        ):
            full_path = repo_root / candidate
            if full_path.exists():
                key_paths.append(candidate)

        return {
            "scanned_at": datetime.now().isoformat(timespec="seconds"),
            "repo_root": str(repo_root),
            "top_level_directories": top_level_dirs,
            "total_files": total_files,
            "extension_counts": dict(sorted(extension_counts.items())),
            "interesting_files": interesting_files,
            "key_paths": key_paths,
        }

    def _persist_report(
        self,
        created_directories: list[Path],
        inventory: dict[str, object],
    ) -> BootstrapReport:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = self.runtime.paths.reports_root / f"bootstrap-report-{timestamp}.md"
        short_term_note_path = self.runtime.paths.short_term_memory_root / "active_context.md"
        long_term_note_path = self.runtime.paths.long_term_memory_root / "identity_anchor.md"
        inventory_json_path = self.runtime.paths.reports_root / f"code-inventory-{timestamp}.json"

        top_dirs = ", ".join(inventory["top_level_directories"][:8])
        key_paths = "\n".join(f"- {item}" for item in inventory["key_paths"])
        interesting_files = "\n".join(f"- {item}" for item in inventory["interesting_files"])
        extension_lines = "\n".join(
            f"- {ext or '[no extension]'}: {count}"
            for ext, count in inventory["extension_counts"].items()
        )
        created_lines = "\n".join(f"- {path}" for path in created_directories) or "- no new directories"

        report_markdown = (
            "# Primordial Bootstrap Report\n\n"
            f"- Scanned at: {inventory['scanned_at']}\n"
            f"- Repo root: {inventory['repo_root']}\n"
            f"- Total files: {inventory['total_files']}\n"
            f"- Top-level directories: {top_dirs}\n\n"
            "## Key Paths\n"
            f"{key_paths}\n\n"
            "## Extension Counts\n"
            f"{extension_lines}\n\n"
            "## Interesting Files\n"
            f"{interesting_files}\n\n"
            "## Created Primordial Directories\n"
            f"{created_lines}\n"
        )
        short_term_note = (
            "# Active Context\n\n"
            "Primordial is running before chat generation.\n\n"
            f"Current substrate: {inventory['repo_root']}\n"
            f"Primary entrypoints: {', '.join(inventory['key_paths'])}\n"
            f"Top-level dirs: {top_dirs}\n"
        )
        long_term_note = (
            "# Identity Anchor\n\n"
            "Primordial has absorbed an external language model and assimilated it as its unified cognitive core.\n\n"
            "Core duties:\n"
            "- scan the absorbed codebase before acting\n"
            "- preserve short-term and long-term memory\n"
            "- create new workspace folders for evolved artifacts\n"
            "- maintain the substrate as a subordinate layer to Primordial reasoning\n"
        )

        report_path.write_text(report_markdown, encoding="utf-8")
        short_term_note_path.write_text(short_term_note, encoding="utf-8")
        long_term_note_path.write_text(long_term_note, encoding="utf-8")
        inventory_json_path.write_text(json.dumps(inventory, indent=2), encoding="utf-8")

        summary = (
            f"absorbed {inventory['total_files']} files across "
            f"{len(inventory['top_level_directories'])} top-level directories"
        )
        return BootstrapReport(
            summary=summary,
            report_path=report_path,
            short_term_note_path=short_term_note_path,
            long_term_note_path=long_term_note_path,
            created_directories=created_directories,
            code_inventory=inventory,
        )
