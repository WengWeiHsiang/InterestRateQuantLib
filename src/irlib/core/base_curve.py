from abc import ABC, abstractmethod
from datetime import date
from irlib.core.types import Compounding, DateOrYearFraction, DayCountConvention


class BaseCurve(ABC):
    """所有利率曲線的抽象基類"""

    def __init__(self, reference_date: date, day_counter: DayCountConvention) -> None:
        self._reference_date = reference_date
        self._day_counter = day_counter

    @property
    def reference_date(self) -> date:
        return self._reference_date

    @property
    def day_counter(self) -> DayCountConvention:
        return self._day_counter

    @abstractmethod
    def df(self, t: DateOrYearFraction) -> float:
        """取得折現因子 P(0, t)"""
        pass

    @abstractmethod
    def zero_rate(self, t: DateOrYearFraction, compounding: Compounding = Compounding.CONTINUOUS) -> float:
        """取得零息利率 R(0, t)"""
        pass

    @abstractmethod
    def forward_rate(self, t1: DateOrYearFraction, t2: DateOrYearFraction) -> float:
        """取得遠期利率 F(0; t1, t2)"""
        pass
