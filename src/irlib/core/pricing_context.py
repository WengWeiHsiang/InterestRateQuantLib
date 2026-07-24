from dataclasses import dataclass, field
from datetime import date
from typing import Any, Optional


@dataclass
class PricingContext:
    """定價環境資訊"""
    valuation_date: date
    market_data: Optional[Any] = None               # MarketDataStore 實例
    # 計算設定 (如 MC paths, Tree steps)
    settings: dict[str, Any] = field(default_factory=dict)
