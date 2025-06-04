import pandas as pd

from tradeassistant import indicators


def test_rsi():
    s = pd.Series([1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3])
    r = indicators.rsi(s, 3)
    assert len(r) == len(s)
    assert r.iloc[-1] >= 0
