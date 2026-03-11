
import math
import torch
import torch.nn.functional as F

def reference_attention(q, k, v, padding_keep=None, dropout_p=0.0, training=False, amp_safe=False, is_causal=False):
    B, H, Tq, d = q.shape
    Tk = k.size(2)

    if is_causal:
        causal = torch.tril(torch.ones((Tq, Tk), dtype=torch.bool, device=q.device)).view(1, 1, Tq, Tk)
        padding_keep = causal if padding_keep is None else (padding_keep & causal)

    # Core Attention logic using the 'nutrients' from main.tex
    scores = (q @ k.transpose(-2, -1)) / math.sqrt(d)
    if padding_keep is not None:
        scores = scores.masked_fill(~padding_keep, float("-inf"))
    
    attn = torch.softmax(scores, dim=-1)
    if dropout_p > 0:
        attn = torch.dropout(attn, p=dropout_p, train=training)
    
    return attn @ v, attn

def sdpa_attention(q, k, v, padding_keep=None, dropout_p=0.0, training=False, is_causal=False):
    # Adapter for PyTorch's Scaled Dot Product Attention
    # Note: Simplified mask handling for this 'parasitic' layer
    out = F.scaled_dot_product_attention(
        q, k, v,
        attn_mask=None, # In our case, we handle masking through high-level logic or leave as is_causal
        dropout_p=dropout_p if training else 0.0,
        is_causal=is_causal
    )
    return out, None
