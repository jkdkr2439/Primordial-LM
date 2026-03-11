from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


VALID_TERRITORY_STATUS = {"active", "scaffold", "demoted", "replaced"}


@dataclass
class HostTerritory:
    name: str
    path: str
    status: str
    role: str
    notes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in VALID_TERRITORY_STATUS:
            raise ValueError(f"invalid territory status: {self.status}")


@dataclass
class ReplacementTrackerState:
    territories: List[HostTerritory] = field(default_factory=list)
    latest_report_path: Optional[Path] = None

    def has_territory(self, path: str) -> bool:
        return any(territory.path == path for territory in self.territories)

    def register(self, territory: HostTerritory) -> None:
        if not self.has_territory(territory.path):
            self.territories.append(territory)

    def summarize(self) -> Dict[str, int]:
        counts = {status: 0 for status in sorted(VALID_TERRITORY_STATUS)}
        for territory in self.territories:
            counts[territory.status] = counts.get(territory.status, 0) + 1
        return counts


class PrimordialReplacementTracker:
    """Tracks which host regions are still authoritative and which have been displaced."""

    def __init__(self, reports_root: Path) -> None:
        self.reports_root = reports_root

    def seed_default_territories(self, tracker_state: ReplacementTrackerState) -> None:
        for territory in self._default_territories():
            tracker_state.register(territory)
        tracker_state.latest_report_path = self._persist_report(tracker_state)

    def _persist_report(self, tracker_state: ReplacementTrackerState) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = self.reports_root / f"replacement-tracker-{timestamp}.md"
        summary = tracker_state.summarize()
        lines = [
            "# Primor Replacement Tracker",
            "",
            "## Summary",
            "",
            f"- Active: {summary.get('active', 0)}",
            f"- Scaffold: {summary.get('scaffold', 0)}",
            f"- Demoted: {summary.get('demoted', 0)}",
            f"- Replaced: {summary.get('replaced', 0)}",
            "",
            "## Territories",
            "",
        ]
        for territory in tracker_state.territories:
            lines.extend(
                [
                    f"### {territory.name}",
                    "",
                    f"- Path: `{territory.path}`",
                    f"- Status: {territory.status}",
                    f"- Role: {territory.role}",
                    f"- Notes: {'; '.join(territory.notes) if territory.notes else 'none'}",
                    "",
                ]
            )
        report_path.write_text("\n".join(lines), encoding="utf-8")
        return report_path

    @staticmethod
    def _default_territories() -> List[HostTerritory]:
        return [
            HostTerritory(
                name="Legacy Sandbox Loop",
                path="primordial_llm/substrate",
                status="active",
                role="Absorbed substrate core retained as the unified cognitive engine.",
                notes=["Fully absorbed into the primordial core.", "Now the internal computational backbone."],
            ),
            HostTerritory(
                name="Main Entry Shell",
                path="primordial_llm/main.py",
                status="scaffold",
                role="Thin shell that boots the organism and hands control into Primor-owned process organs.",
                notes=["Main no longer owns turn logic.", "Still remains as startup shell."],
            ),
            HostTerritory(
                name="Model Runtime Legacy Tissue",
                path="primordial_llm/output/model_runtime.py",
                status="demoted",
                role="Legacy host inference tissue retained underneath the explicit substrate adapter.",
                notes=["Now called only through substrate_adapter.", "No longer imported directly by main or the action cycle."],
            ),
            HostTerritory(
                name="Substrate Adapter Organ",
                path="primordial_llm/output/substrate_adapter.py",
                status="replaced",
                role="Primor-owned adapter that subordinates host inference to a controlled substrate interface.",
                notes=["Explicitly mediates model load and generation from Primor packets."],
            ),
            HostTerritory(
                name="Tool Runtime Legacy Tissue",
                path="primordial_llm/output/tool_runtime.py",
                status="demoted",
                role="Legacy host execution tissue retained underneath the explicit effector adapter.",
                notes=["Now called only through effector_adapter.", "No longer imported directly by the action cycle."],
            ),
            HostTerritory(
                name="Effector Adapter Organ",
                path="primordial_llm/output/effector_adapter.py",
                status="replaced",
                role="Primor-owned adapter that subordinates host execution to a controlled effector interface.",
                notes=["Explicitly mediates validated tool execution."],
            ),
            HostTerritory(
                name="Action Cycle Organ",
                path="primordial_llm/process/action_cycle.py",
                status="replaced",
                role="Primor-owned turn lifecycle replacing the host loop as runtime authority.",
                notes=["Primor now owns plan -> generate -> validate -> effect -> reintegrate."],
            ),
            HostTerritory(
                name="Context Assembly Organ",
                path="primordial_llm/process/context_assembly.py",
                status="replaced",
                role="Primor-owned context packaging layer controlling substrate visibility.",
                notes=["Substrate now sees a bounded Primor packet and transcript slice."],
            ),
            HostTerritory(
                name="Validation Organ",
                path="primordial_llm/process/validation.py",
                status="replaced",
                role="Primor-owned law gate between syntax and action.",
                notes=["Tool execution now depends on Primor approval."],
            ),
        ]
