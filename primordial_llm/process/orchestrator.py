from primordial_llm.data.models import ExecutionPlan
from primordial_llm.process.primordial import PrimordialEvolutionCore


class PrimordialOrchestrator:
    """PROCESS layer entrypoint for intent absorption and action planning."""

    def __init__(self) -> None:
        self.evolution_core = PrimordialEvolutionCore()

    def create_plan(self, user_input: str) -> ExecutionPlan:
        return self.evolution_core.build_plan(user_input)
