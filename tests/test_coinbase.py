import pandas as pd
import requests
from tradeassistant.data import fetch_coinbase

class DummyResp:
    def __init__(self, data):
        self._data = data
        self.status_code = 200
    def json(self):
        return self._data
    def raise_for_status(self):
        pass

def test_fetch_coinbase(monkeypatch):
    sample = [
        [1622505600, 100, 110, 105, 108, 123.0],
        [1622592000, 108, 115, 110, 111, 321.0],
    ]
    def fake_get(url, params=None, headers=None, timeout=10):
        return DummyResp(sample)
    monkeypatch.setattr(requests, "get", fake_get)
    df = fetch_coinbase("BTC-USD")
    assert list(df.columns) == ["low", "high", "open", "close", "volume"]
    assert len(df) == 2
