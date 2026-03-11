
import numpy as np
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Entity:
    name: str
    coords: np.ndarray  # Normalized vector
    domain: str = None
    quantum_step: int = 0

@dataclass
class ContextPlane:
    centroid: np.ndarray
    axes: np.ndarray  # Top principal axes
    spread: float

class PrimordialContextField:
    """DCF Organ: Manages geometric semantic meaning."""
    
    def __init__(self, k_anchors: int = 8):
        self.k_anchors = k_anchors
        self.entities: Dict[str, Entity] = {}
        self.known_combos: Set[Tuple[str, ...]] = set()

    def add_entity(self, name: str, vector: np.ndarray, domain: str = None, quantum_step: int = 0):
        # Normalize vector
        norm = np.linalg.norm(vector) + 1e-9
        self.entities[name] = Entity(name, vector / norm, domain, quantum_step)

    def get_anchors(self, target_name: str) -> List[str]:
        target = self.entities.get(target_name)
        if not target:
            return []
            
        step_group = [e for e in self.entities.values() if e.quantum_step == target.quantum_step and e.name != target_name]
        if not step_group:
            return []
            
        # Compute cosine similarities
        sims = []
        for other in step_group:
            sim = np.dot(target.coords, other.coords)
            sims.append((other.name, sim))
            
        # Return top-k
        sims.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in sims[:self.k_anchors]]

    def construct_plane(self, anchor_names: List[str]) -> ContextPlane:
        vecs = np.stack([self.entities[n].coords for n in anchor_names if n in self.entities])
        centroid = vecs.mean(axis=0)
        
        # SVD for principal axes
        centered = vecs - centroid
        _, s, vt = np.linalg.svd(centered, full_matrices=False)
        
        return ContextPlane(
            centroid=centroid,
            axes=vt[:3], # Top-3 principal axes
            spread=float(s.sum())
        )

    def project_meaning(self, target_name: str, plane: ContextPlane) -> np.ndarray:
        target = self.entities.get(target_name)
        if not target:
            return np.zeros(3)
            
        v_centered = target.coords - plane.centroid
        return np.array([np.dot(v_centered, ax) for ax in plane.axes])

    def measure_resonance(self, name_a: str, name_b: str) -> int:
        anchors_a = set(self.get_anchors(name_a))
        anchors_b = set(self.get_anchors(name_b))
        return len(anchors_a.intersection(anchors_b))
