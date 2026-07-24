from datetime import date
import pytest
from irlib.core.base_engine import BaseEngine
from irlib.core.base_instrument import BaseInstrument
from irlib.core.pricing_context import PricingContext
from irlib.core.pricing_result import PricingResult
from irlib.core.types import Currency, Frequency


class MockInstrument(BaseInstrument):
    @property
    def currency(self) -> Currency:
        return Currency.USD

    def is_expired(self, valuation_date: date) -> bool:
        return valuation_date > date(2030, 1, 1)


class MockEngine(BaseEngine):
    def calculate(self, instrument: BaseInstrument, context: PricingContext) -> PricingResult:
        if instrument.is_expired(context.valuation_date):
            return PricingResult(npv=0.0)
        return PricingResult(npv=100.0, greeks={"DV01": 0.05})


def test_core_pricing_flow():
    valuation_date = date(2026, 1, 1)
    inst = MockInstrument()
    engine = MockEngine()
    context = PricingContext(valuation_date=valuation_date)

    res = engine.calculate(inst, context)
    assert res.npv == 100.0
    assert res.greeks["DV01"] == 0.05
    assert not inst.is_expired(valuation_date)


def test_enum_values():
    assert Currency.USD.value == "USD"
    assert Frequency.SEMIANNUAL.value == 2
