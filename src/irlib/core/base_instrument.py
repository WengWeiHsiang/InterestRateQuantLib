from abc import ABC, abstractmethod
from datetime import date
from irlib.core.types import Currency


class BaseInstrument(ABC):
    """所有金融商品的抽象基類 (僅定義交易條款，不含定價邏輯)"""

    @property
    @abstractmethod
    def currency(self) -> Currency:
        """商品計價幣別"""
        pass

    @abstractmethod
    def is_expired(self, valuation_date: date) -> bool:
        """判斷商品在評價日是否已到期"""
        pass
