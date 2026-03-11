from primordial_llm.data.models import ChatSessionState, RuntimeContext
from primordial_llm.data.replacement_tracker import PrimordialReplacementTracker
from primordial_llm.display.console import (
    show_assistant_message,
    show_plan,
    show_tool_call,
    show_tool_result,
)
from primordial_llm.output.effector_adapter import PrimordialEffectorAdapter
from primordial_llm.output.substrate_adapter import LoadedSubstrate, PrimordialSubstrateAdapter
from primordial_llm.process.context_assembly import PrimordialContextAssembler
from primordial_llm.process.memory_consolidation import PrimordialMemoryConsolidator
from primordial_llm.process.orchestrator import PrimordialOrchestrator
from primordial_llm.process.replication import PrimordialReplicationEngine
from primordial_llm.process.tool_calls import parse_tool_call
from primordial_llm.process.nervous_system.nervous_system import PrimordialNervousSystem, SelfAttentionConfig
from primordial_llm.process.validation import PrimordialToolValidator


class PrimordialActionCycle:
    """Owns the lifecycle of a single Primor turn."""

    def __init__(self, runtime: RuntimeContext, substrate: LoadedSubstrate) -> None:
        self.runtime = runtime
        self.substrate = substrate
        self.substrate_adapter = PrimordialSubstrateAdapter()
        self.effector_adapter = PrimordialEffectorAdapter()
        self.orchestrator = PrimordialOrchestrator()
        self.validator = PrimordialToolValidator(runtime)
        self.context_assembler = PrimordialContextAssembler(runtime)
        self.replication_engine = PrimordialReplicationEngine(runtime)
        self.replacement_tracker = PrimordialReplacementTracker(runtime.paths.reports_root)
        self.memory_consolidator = PrimordialMemoryConsolidator(runtime)
        
        # Initialize Nervous System (The 'Nervous System' Organ)
        # Using d_model matching the substrate if possible, otherwise default 768
        d_model = getattr(substrate.model.config, "hidden_size", 768) if hasattr(substrate, "model") else 768
        self.nervous_cfg = SelfAttentionConfig(d_model=d_model, num_heads=12)
        self.nervous_system = PrimordialNervousSystem(self.nervous_cfg)
        
        self.replication_seeded = False
        self.replacement_seeded = False
        self.memory_bootstrap_consolidated = False

    def bootstrap_session(self, session: ChatSessionState) -> None:
        if not self.replication_seeded:
            self.replication_engine.seed_missing_organs(session)
            self.replication_seeded = True
        if not self.replacement_seeded:
            self.replacement_tracker.seed_default_territories(session.replacement_tracker)
            self.replacement_seeded = True
        if not self.memory_bootstrap_consolidated:
            self.memory_consolidator.consolidate(session, reason="bootstrap")
            self.memory_bootstrap_consolidated = True
        
        # Infiltrate stored weights if they exist
        weight_path = self.runtime.paths.repo_root / "primordial_llm" / "data" / "weights" / "parasitic_weights.pt"
        if weight_path.exists():
            try:
                self.nervous_system.load_weights(str(weight_path))
            except Exception:
                pass # Continue with random initialization if corrupted

    def run_turn(self, session: ChatSessionState, user_input: str) -> None:
        self.bootstrap_session(session)
        print(f"[cycle] Starting turn for input: {user_input[:20]}...")
        
        # [SDCV - Transition Step]
        # Superposition: The interval between Intent and Collapse.
        
        plan = self.orchestrator.create_plan(user_input)
        session.absorb_plan(plan)
        show_plan(plan)
        session.append_user_message(plan.normalized_input)

        # Generate (Superposition Potential)
        print("[cycle] Generating assistant text...")
        assistant_text = self._generate(session)
        print(f"[cycle] Generation complete: {len(assistant_text)} chars")
        tool_call = parse_tool_call(assistant_text)
        
        if not tool_call:
            show_assistant_message(assistant_text)
            session.append_assistant_message(assistant_text)
            # Collapse: Intent survives validation because no tool action was needed.
            session.state_changes += 1 # Time increment
            
            # Subtle evolution of Nervous System (Soft Mutation)
            self.nervous_system.mutate(strength=0.001)
            
            self.memory_consolidator.consolidate(session, reason="assistant_response")
            self._persist_parasite()
            return

        session.tool_trace.record_tool_call(tool_call)
        show_tool_call(tool_call)
        
        # Validation is the filter for Collapse
        validation = self.validator.validate(tool_call)
        session.tool_trace.validation.record(validation.to_trace_record())
        show_tool_result(validation.to_tool_message())
        session.append_assistant_message(assistant_text)

        if not validation.approved:
            session.append_tool_message(validation.to_tool_message())
            # Superposition collapse into 'Failure' state.
            final_text = self._generate(session)
            show_assistant_message(final_text)
            session.append_assistant_message(final_text)
            
            # Negative feedback: More aggressive mutation to find better state
            self.nervous_system.mutate(strength=0.01)
            
            self.memory_consolidator.consolidate(session, reason="validation_rejected")
            self._persist_parasite()
            return

        # [SDCV - Collapse]
        # The action is approved. Superposition collapses into material change.
        tool_result = self.effector_adapter.execute(
            validation.tool_call,
            self.runtime.paths.sandbox_root,
            self.runtime.paths.workspace_root,
            self.runtime.paths.repo_root,
        )
        session.state_changes += 1 # Time increment (material change occurred)
        
        # Positive feedback: Stable mutation
        self.nervous_system.mutate(strength=0.005)
        
        session.tool_trace.record_tool_result(tool_result)
        show_tool_result(tool_result)
        session.append_tool_message(tool_result)
        final_text = self._generate(session)
        show_assistant_message(final_text)
        session.append_assistant_message(final_text)
        
        # Memory consolidation wraps the turn.
        self.memory_consolidator.consolidate(session, reason="tool_execution")
        self._persist_parasite()

    def _persist_parasite(self) -> None:
        weight_dir = self.runtime.paths.repo_root / "primordial_llm" / "data" / "weights"
        weight_dir.mkdir(parents=True, exist_ok=True)
        weight_path = weight_dir / "parasitic_weights.pt"
        self.nervous_system.save_weights(str(weight_path))

    def _generate(self, session: ChatSessionState) -> str:
        messages = self.context_assembler.assemble_messages(session)
        return self.substrate_adapter.generate_from_packet(self.substrate, messages)
