from primordial_llm.data.models import ExecutionPlan


class PrimordialPhaseEngine:
    """Dual-axis staging hook for future evolution logic."""

    def trace(self, user_input: str) -> list[str]:
        phases = ["V", "Sinh"]
        if user_input:
            phases.append("Dan")
        phases.append("Chuyen")
        phases.append("Dung/Hoai")
        return phases


class PrimordialEvolutionCore:
    """Absorbs raw user intent into an IPOD execution plan."""

    def __init__(self) -> None:
        self.phase_engine = PrimordialPhaseEngine()

    def build_plan(self, user_input: str) -> ExecutionPlan:
        normalized_input = user_input.strip()
        reasoning_mode = self._select_reasoning_mode(normalized_input)
        phase_trace = self.phase_engine.trace(normalized_input)
        warnings = []
        if not normalized_input:
            warnings.append("Empty input detected.")
        return ExecutionPlan(
            normalized_input=normalized_input,
            reasoning_mode=reasoning_mode,
            phase_trace=phase_trace,
            warnings=warnings,
        )

    def _select_reasoning_mode(self, normalized_input: str) -> str:
        lower = normalized_input.lower()
        if any(token in lower for token in ("refactor", "architecture", "ipod", "restructure")):
            return "logical_architect"
        if any(token in lower for token in ("idea", "metaphor", "creative", "brainstorm")):
            return "creative_synthesizer"
        return "balanced_fusion"
