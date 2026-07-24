from datetime import date
from enum import Enum, auto
from typing import Union

# Date / Time Type Aliases
DateOrYearFraction = Union[date, float]


class Currency(Enum):
    """標準 ISO 4217 貨幣代碼"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    TWD = "TWD"
    CHF = "CHF"


class DayCountConvention(Enum):
    """計息天數慣例"""
    ACT_360 = "ACT/360"
    ACT_365 = "ACT/365"
    THIRTY_360 = "30/360"
    ACT_ACT = "ACT/ACT"


class BusinessDayConvention(Enum):
    """營業日調整慣例"""
    FOLLOWING = "Following"
    MODIFIED_FOLLOWING = "ModifiedFollowing"
    PRECEDING = "Preceding"
    MODIFIED_PRECEDING = "ModifiedPreceding"
    UNADJUSTED = "Unadjusted"


class Frequency(Enum):
    """付息與重設頻率 (每年次數)"""
    ON = 365            # Overnight
    MONTHLY = 12
    QUARTERLY = 4
    SEMIANNUAL = 2
    ANNUAL = 1


class Compounding(Enum):
    """利率複利方式"""
    SIMPLE = auto()
    COMPOUNDED = auto()
    CONTINUOUS = auto()
