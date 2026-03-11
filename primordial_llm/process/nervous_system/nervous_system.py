
import torch
import torch.nn as nn
from .I.input_contracts import SelfAttentionConfig
from .P.kernels import reference_attention, sdpa_attention

class PrimordialNervousSystem(nn.Module):
    """
    The internal attention organ of PLM. 
    It doesn't replace the LLM, it 'attends' to the interaction before the LLM does.
    """
    def __init__(self, cfg: SelfAttentionConfig):
        super().__init__()
        self.cfg = cfg
        d = cfg.d_model
        # These are the 'Internal Proto-Weights' the user felt were missing
        self.wq = nn.Linear(d, d, bias=False)
        self.wk = nn.Linear(d, d, bias=False)
        self.wv = nn.Linear(d, d, bias=False)
        self.wo = nn.Linear(d, d, bias=False)
        
    def forward(self, x: torch.Tensor, is_causal: bool = True):
        # DIPOD P-Layer logic
        q = self.wq(x)
        k = self.wk(x)
        v = self.wv(x)
        
        # Reshape for multi-head [B, T, h*d] -> [B, h, T, d]
        B, T, d_model = x.shape
        h = self.cfg.num_heads
        d_head = d_model // h
        
        q = q.view(B, T, h, d_head).transpose(1, 2)
        k = k.view(B, T, h, d_head).transpose(1, 2)
        v = v.view(B, T, h, d_head).transpose(1, 2)
        
        # Kernel Selection (Simplified for Parasitic use)
        if hasattr(torch.nn.functional, "scaled_dot_product_attention"):
            y, attn = sdpa_attention(q, k, v, is_causal=is_causal)
            if y is None: # SDPA doesn't return weights usually
                y, attn = reference_attention(q, k, v, is_causal=is_causal)
        else:
            y, attn = reference_attention(q, k, v, is_causal=is_causal)
            
        # Re-merge heads
        y = y.transpose(1, 2).contiguous().view(B, T, d_model)
        return self.wo(y), attn

    def save_weights(self, path: str):
        """Persist the parasitic internal weights."""
        torch.save(self.state_dict(), path)

    def load_weights(self, path: str):
        """Re-absorb persisted weights."""
        if torch.cuda.is_available():
            self.load_state_dict(torch.load(path))
        else:
            self.load_state_dict(torch.load(path, map_location=torch.device('cpu')))

    def mutate(self, strength: float = 0.01):
        """Evolve the weights via random mutation (Proto-DNA update)."""
        with torch.no_grad():
            for param in self.parameters():
                param.add_(torch.randn_like(param) * strength)
