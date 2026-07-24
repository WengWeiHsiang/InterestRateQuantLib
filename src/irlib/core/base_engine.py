from abc import ABC, abstractmethod
from irlib.core.base_instrument import BaseInstrument
from irlib.core.pricing_context import PricingContext
from irlib.core.pricing_result import PricingResult


class BaseEngine(ABC):
    """所有定價引擎的抽象基類"""

    @abstractmethod
    def calculate(self, instrument: BaseInstrument, context: PricingContext) -> PricingResult:
        """執行定價計算並返回 PricingResult"""
        pass
