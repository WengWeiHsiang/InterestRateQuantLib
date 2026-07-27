from datetime import date
import pytest
from irlib.conventions.calendar import NullCalendar, UnitedStatesCalendar
from irlib.core.types import BusinessDayConvention


def test_null_calendar_weekend():
    cal = NullCalendar()
    saturday = date(2026, 5, 30)
    sunday = date(2026, 5, 31)
    monday = date(2026, 6, 1)

    assert cal.is_weekend(saturday)
    assert not cal.is_business_day(saturday)
    assert cal.is_business_day(monday)


def test_following_adjustment():
    cal = NullCalendar()
    saturday = date(2026, 5, 30)
    monday = date(2026, 6, 1)

    adjusted = cal.adjust(saturday, BusinessDayConvention.FOLLOWING)
    assert adjusted == monday


def test_modified_following_adjustment():
    cal = NullCalendar()
    # 2026/5/30 是週六，末日跨月測試
    saturday = date(2026, 5, 30)
    friday = date(2026, 5, 29)

    # Following 會推到 6/1 (跨月)，因此 Modified Following 必須退回 5/29 (同月)
    adjusted = cal.adjust(saturday, BusinessDayConvention.MODIFIED_FOLLOWING)
    assert adjusted == friday


def test_add_business_days():
    cal = NullCalendar()
    friday = date(2026, 5, 29)
    # 加 1 個營業日應跨過週末到達週一 6/1
    next_bday = cal.add_business_days(friday, 1)
    assert next_bday == date(2026, 6, 1)


def test_us_calendar_holiday():
    cal = UnitedStatesCalendar()
    july_4th = date(2026, 7, 4)
    assert cal.is_holiday(july_4th) or cal.is_weekend(july_4th)
    assert not cal.is_business_day(july_4th)
