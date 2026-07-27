from datetime import date
import pytest
from irlib.conventions.day_count import (
    Actual360,
    Actual365,
    ActualActualISDA,
    Thirty360ISDA,
    get_day_counter,
)
from irlib.core.exceptions import InvalidConventionError
from irlib.core.types import DayCountConvention


def test_actual_360():
    counter = Actual360()
    d1 = date(2026, 1, 1)
    d2 = date(2026, 7, 1)
    # 2026/1/1 到 2026/7/1 共 181 天
    assert counter.day_count(d1, d2) == 181
    assert counter.year_fraction(d1, d2) == pytest.approx(181.0 / 360.0)


def test_actual_365():
    counter = Actual365()
    d1 = date(2026, 1, 1)
    d2 = date(2026, 7, 1)
    assert counter.day_count(d1, d2) == 181
    assert counter.year_fraction(d1, d2) == pytest.approx(181.0 / 365.0)


def test_thirty_360_isda():
    counter = Thirty360ISDA()
    # 一般月
    d1 = date(2026, 1, 15)
    d2 = date(2026, 7, 15)
    assert counter.day_count(d1, d2) == 180
    assert counter.year_fraction(d1, d2) == pytest.approx(0.5)

    # 31 號邊界條件測試
    d3 = date(2026, 1, 31)
    d4 = date(2026, 7, 31)
    assert counter.day_count(d3, d4) == 180  # d3與d4皆會調整為 30


def test_act_act_isda_leap_year():
    counter = ActualActualISDA()
    # 2024 年為閏年 (366 天)
    d1 = date(2024, 1, 1)
    d2 = date(2025, 1, 1)
    assert counter.year_fraction(d1, d2) == pytest.approx(1.0)

    # 跨閏年與平年 (2024/7/1 到 2025/7/1)
    # 2024/7/1 ~ 2025/1/1: 184 天 / 366
    # 2025/1/1 ~ 2025/7/1: 181 天 / 365
    d3 = date(2024, 7, 1)
    d4 = date(2025, 7, 1)
    expected = (184.0 / 366.0) + (181.0 / 365.0)
    assert counter.year_fraction(d3, d4) == pytest.approx(expected)


def test_get_day_counter_factory():
    counter = get_day_counter(DayCountConvention.ACT_360)
    assert isinstance(counter, Actual360)

    with pytest.raises(InvalidConventionError):
        get_day_counter("INVALID_CONVENTION")
