from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):
    """所有利率與波動率模型的抽象基類"""

    @property
    @abstractmethod
    def params(self) -> dict[str, Any]:
        """模型參數字典"""
        pass

    @abstractmethod
    def numeraire(self, t: float, state_vars: Any = None) -> float:
        """計算時間 t 之計價單位 (Numeraire)"""
        pass
