from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class PricingResult:
    """定價引擎輸出結果規格"""
    npv: float                                      # 淨現值 (Net Present Value)
    clean_price: Optional[float] = None             # 乾價 (適用於 Bond)
    dirty_price: Optional[float] = None             # 濕價 / 含息價 (適用於 Bond)
    accrued_interest: Optional[float] = None        # 應計利息
    # 風險敏感度 (DV01, Delta, Gamma, etc.)
    greeks: dict[str, float] = field(default_factory=dict)
    additional_results: dict[str, Any] = field(
        default_factory=dict)  # 額外資訊 (Cashflows, MC error, etc.)
