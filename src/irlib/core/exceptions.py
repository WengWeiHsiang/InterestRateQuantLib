class IRLibError(Exception):
    """InterestRateQuantLib 基礎例外"""
    pass


class CurveError(IRLibError):
    """曲線建構、內插或計算失敗"""
    pass


class PricingError(IRLibError):
    """定價引擎計算錯誤"""
    pass


class MarketDataError(IRLibError):
    """缺少市場數據或歷史 Fixing 資料"""
    pass


class CalibrationError(IRLibError):
    """模型參數校準未收斂或失敗"""
    pass


class InvalidConventionError(IRLibError):
    """不支援或無效的市場慣例設定"""
    pass
