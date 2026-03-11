
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Any

class BaseNutrient(ABC):
    """Abstract base for architectural nutrients (model adapters)."""
    
    @abstractmethod
    def load(self, model_dir: Path, load_in_4bit: bool) -> Tuple[Any, Any, Any]:
        """Load torch, tokenizer, and model."""
        pass

    @abstractmethod
    def generate(self, torch_module, tokenizer, model, messages: List[dict], max_new_tokens: int) -> str:
        """Architecture-specific generation logic."""
        pass

    @abstractmethod
    def identify(self, model_dir: Path) -> bool:
        """Check if this nutrient can absorb the given model."""
        pass
