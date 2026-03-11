from dataclasses import dataclass
from pathlib import Path
from typing import List, Type, Any, Optional

from primordial_llm.output.nutrients.base import BaseNutrient
from primordial_llm.output.nutrients.primordial_core import PrimordialCoreNutrient
from primordial_llm.output.nutrients.llama_nutrient import LlamaNutrient

@dataclass
class LoadedSubstrate:
    torch_module: Any
    tokenizer: Any
    model: Any
    max_new_tokens: int
    nutrient: BaseNutrient

class PrimordialSubstrateAdapter:
    """Exploits the correct architectural nutrient for the host substrate."""
    
    NUTRIENTS: List[Type[BaseNutrient]] = [
        PrimordialCoreNutrient,
        LlamaNutrient
    ]

    INTERNAL_SUBSTRATE_PATH = Path("d:/Tung/PLM/primordial_llm/substrate")

    def get_internal_substrate_path(self) -> Optional[Path]:
        if (self.INTERNAL_SUBSTRATE_PATH / "config.json").exists():
            return self.INTERNAL_SUBSTRATE_PATH
        return None

    def _select_nutrient(self, weights_dir: Path) -> BaseNutrient:
        for NutrientClass in self.NUTRIENTS:
            n = NutrientClass()
            if n.identify(weights_dir):
                return n
        # Default fallback to Primordial Core if identification fails
        return PrimordialCoreNutrient()

    def load_substrate(self, weights_dir: Path, load_in_4bit: bool, max_new_tokens: int) -> LoadedSubstrate:
        nutrient = self._select_nutrient(weights_dir)
        torch_module, tokenizer, model = nutrient.load(weights_dir, load_in_4bit)
        
        return LoadedSubstrate(
            torch_module=torch_module,
            tokenizer=tokenizer,
            model=model,
            max_new_tokens=max_new_tokens,
            nutrient=nutrient
        )

    def generate_from_packet(self, substrate: LoadedSubstrate, messages: List[dict]) -> str:
        return substrate.nutrient.generate(
            substrate.torch_module,
            substrate.tokenizer,
            substrate.model,
            messages,
            substrate.max_new_tokens
        )

