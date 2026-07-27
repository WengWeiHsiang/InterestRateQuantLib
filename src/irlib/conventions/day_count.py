from abc import ABC, abstractmethod
import calendar
from datetime import date
from irlib.core.exceptions import InvalidConventionError
from irlib.core.types import DayCountConvention


class DayCounter(ABC):
    """計息天數與 Year Fraction 計算抽象基類"""

    @abstractmethod
    def day_count(self, start_date: date, end_date: date) -> int:
        """計算兩日期的實際或慣例天數差"""
        pass

    @abstractmethod
    def year_fraction(self, start_date: date, end_date: date) -> float:
        """計算兩日期的年化時間長度 (Year Fraction tau)"""
        pass


class Actual360(DayCounter):
    """Act/360 慣例 (美元/歐元貨幣市場與浮動腳常用)"""

    def day_count(self, start_date: date, end_date: date) -> int:
        return (end_date - start_date).days

    def year_fraction(self, start_date: date, end_date: date) -> float:
        return self.day_count(start_date, end_date) / 360.0


class Actual365(DayCounter):
    """Act/365 Fixed 慣例 (英鎊市場常用)"""

    def day_count(self, start_date: date, end_date: date) -> int:
        return (end_date - start_date).days

    def year_fraction(self, start_date: date, end_date: date) -> float:
        return self.day_count(start_date, end_date) / 365.0


class Thirty360ISDA(DayCounter):
    """30/360 ISDA (Bond Basis) 慣例 (美國公司債與固定利率腳常用)"""

    def day_count(self, start_date: date, end_date: date) -> int:
        d1 = start_date.day
        d2 = end_date.day
        m1 = start_date.month
        m2 = end_date.month
        y1 = start_date.year
        y2 = end_date.year

        if d1 == 31:
            d1 = 30
        if d2 == 31 and d1 >= 30:
            d2 = 30

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)

    def year_fraction(self, start_date: date, end_date: date) -> float:
        return self.day_count(start_date, end_date) / 360.0


class ActualActualISDA(DayCounter):
    """Act/Act ISDA 慣例 (美國國債常用，跨閏年精確處理)"""

    def day_count(self, start_date: date, end_date: date) -> int:
        return (end_date - start_date).days

    def year_fraction(self, start_date: date, end_date: date) -> float:
        if start_date == end_date:
            return 0.0

        if start_date > end_date:
            return -self.year_fraction(end_date, start_date)

        y1 = start_date.year
        y2 = end_date.year

        if y1 == y2:
            days_in_year = 366.0 if calendar.isleap(y1) else 365.0
            return (end_date - start_date).days / days_in_year

        # 跨年份拆分計算
        d1_end = date(y1 + 1, 1, 1)
        days_y1 = (d1_end - start_date).days
        year_frac_y1 = days_y1 / (366.0 if calendar.isleap(y1) else 365.0)

        d2_start = date(y2, 1, 1)
        days_y2 = (end_date - d2_start).days
        year_frac_y2 = days_y2 / (366.0 if calendar.isleap(y2) else 365.0)

        middle_years = float(y2 - y1 - 1)

        return year_frac_y1 + middle_years + year_frac_y2


def get_day_counter(convention: DayCountConvention) -> DayCounter:
    """DayCounter 工廠函式"""
    mapping = {
        DayCountConvention.ACT_360: Actual360(),
        DayCountConvention.ACT_365: Actual365(),
        DayCountConvention.THIRTY_360: Thirty360ISDA(),
        DayCountConvention.ACT_ACT: ActualActualISDA(),
    }
    if convention not in mapping:
        raise InvalidConventionError(f"不支援的 DayCount 慣例: {convention}")
    return mapping[convention]
