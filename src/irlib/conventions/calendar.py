from abc import ABC, abstractmethod
from datetime import date, timedelta
from irlib.core.exceptions import InvalidConventionError
from irlib.core.types import BusinessDayConvention


class BaseCalendar(ABC):
    """營業日日曆抽象基類"""

    @abstractmethod
    def is_holiday(self, dt: date) -> bool:
        """判斷指定日期是否為國定假日 (不包含週末)"""
        pass

    def is_weekend(self, dt: date) -> bool:
        """判斷指定日期是否為週末 (週六、週日)"""
        return dt.weekday() in (5, 6)

    def is_business_day(self, dt: date) -> bool:
        """判斷指定日期是否為營業日"""
        return not self.is_weekend(dt) and not self.is_holiday(dt)

    def adjust(self, dt: date, convention: BusinessDayConvention) -> date:
        """根據營業日慣例調整非營業日"""
        if convention == BusinessDayConvention.UNADJUSTED:
            return dt

        if self.is_business_day(dt):
            return dt

        if convention == BusinessDayConvention.FOLLOWING:
            curr = dt
            while not self.is_business_day(curr):
                curr += timedelta(days=1)
            return curr

        elif convention == BusinessDayConvention.MODIFIED_FOLLOWING:
            curr = dt
            while not self.is_business_day(curr):
                curr += timedelta(days=1)
            # 若調整後跨月，則改為向前找上一個營業日
            if curr.month != dt.month:
                curr = dt
                while not self.is_business_day(curr):
                    curr -= timedelta(days=1)
            return curr

        elif convention == BusinessDayConvention.PRECEDING:
            curr = dt
            while not self.is_business_day(curr):
                curr -= timedelta(days=1)
            return curr

        elif convention == BusinessDayConvention.MODIFIED_PRECEDING:
            curr = dt
            while not self.is_business_day(curr):
                curr -= timedelta(days=1)
            # 若調整後跨月，則改為向後找下一個營業日
            if curr.month != dt.month:
                curr = dt
                while not self.is_business_day(curr):
                    curr += timedelta(days=1)
            return curr

        raise InvalidConventionError(f"不支援的營業日慣例: {convention}")

    def add_business_days(self, dt: date, days: int) -> date:
        """推算 N 個營業日後的日期"""
        step = 1 if days >= 0 else -1
        count = abs(days)
        curr = dt
        while count > 0:
            curr += timedelta(days=step)
            if self.is_business_day(curr):
                count -= 1
        return curr


class NullCalendar(BaseCalendar):
    """無假日日曆 (僅考慮週末，適用於理論驗證)"""

    def is_holiday(self, dt: date) -> bool:
        return False


class UnitedStatesCalendar(BaseCalendar):
    """美國主要金融市場日曆 (包含美聯儲主要假日)"""

    def is_holiday(self, dt: date) -> bool:
        year = dt.year
        month = dt.month
        day = dt.day

        # New Year's Day (Jan 1)
        if month == 1 and day == 1:
            return True
        # Independence Day (Jul 4)
        if month == 7 and day == 4:
            return True
        # Veterans Day (Nov 11)
        if month == 11 and day == 11:
            return True
        # Christmas Day (Dec 25)
        if month == 12 and day == 25:
            return True

        return False
