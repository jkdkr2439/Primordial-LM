
import random
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from primordial_llm.process.context_field import Entity

@dataclass
class CompressedSeed:
    genotype: np.ndarray
    epigenetic_mask: np.ndarray
    quantum_step: int

class PrimordialReproductiveEngine:
    """ARC Organ: Manages agent evolution and proto-DNA reproduction."""
    
    def __init__(self, mutation_rate: float = 0.04):
        self.mutation_rate = mutation_rate

    def compress(self, entity: Entity, anchors: List[Entity]) -> CompressedSeed:
        """Hoai Operation: Context stripping."""
        # Higher weight to anchors that are further from mean (epigenetic significance)
        centroid = np.mean([a.coords for a in anchors], axis=0) if anchors else entity.coords
        significance = np.abs(entity.coords - centroid)
        mask = (significance > np.median(significance)).astype(float)
        
        return CompressedSeed(
            genotype=entity.coords.copy(),
            epigenetic_mask=mask,
            quantum_step=entity.quantum_step
        )

    def decompress(self, seed: CompressedSeed, substrate: Entity) -> Entity:
        """Dung Operation: Blending and mutation."""
        # Hybrid genotype
        blend_mask = seed.epigenetic_mask > 0.5
        new_coords = substrate.coords.copy()
        
        # Seed overrides substrate where imprinted
        new_coords[blend_mask] = seed.genotype[blend_mask]
        
        # Blend other parts
        other_mask = ~blend_mask
        new_coords[other_mask] = (new_coords[other_mask] + seed.genotype[other_mask]) / 2.0
        
        # Mutate
        mutation = np.random.normal(0, self.mutation_rate, size=new_coords.shape)
        new_coords += mutation
        
        # Recoil to unit sphere
        new_coords /= (np.linalg.norm(new_coords) + 1e-9)
        
        return Entity(
            name=f"primor-child-{random.getrandbits(32):x}",
            coords=new_coords,
            domain=substrate.domain,
            quantum_step=seed.quantum_step
        )

    def interact(self, entity_a: Entity, entity_b: Entity, type_a: str, type_b: str):
        """Interaction Matrix: DD, DH, HD, HH."""
        # DD: Symmetric Merge
        if type_a == 'D' and type_b == 'D':
            new_coords = (entity_a.coords + entity_b.coords) / 2.0
            new_coords /= np.linalg.norm(new_coords)
            return Entity(f"merge-{random.getrandbits(16):x}", new_coords, entity_a.domain, entity_a.quantum_step)
            
        # DH: B compresses, A receives
        if type_a == 'D' and type_b == 'H':
            seed = self.compress(entity_b, []) # Simplified for now
            return self.decompress(seed, entity_a)
            
        # HD: A compresses, B receives
        if type_a == 'H' and type_b == 'D':
            seed = self.compress(entity_a, [])
            return self.decompress(seed, entity_b)
            
        # HH: Apoptosis
        return None
