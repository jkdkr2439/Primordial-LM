
from dataclasses import dataclass
from typing import Literal, Optional

KernelName = Literal["flash", "sdpa", "reference"]
PrecisionPolicy = Literal["native", "amp_safe"]
AttentionType = Literal["mha", "gqa"]

@dataclass(frozen=True)
class SelfAttentionConfig:
    d_model: int
    num_heads: int
    dropout_p: float = 0.0
    attention_type: AttentionType = "mha"
    kv_num_heads: Optional[int] = None
    kernel_preference: KernelName = "sdpa"
    precision_policy: PrecisionPolicy = "native"
    enable_telemetry: bool = True
    telemetry_sample_rate: float = 0.05
    enable_kv_cache: bool = True
    enable_debug_payloads: bool = False
    debug_max_T_for_matrix: int = 512
