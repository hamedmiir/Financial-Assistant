from __future__ import annotations

import time
from typing import Optional

import requests

COINBASE_API = "https://api.exchange.coinbase.com"


def fetch_price(symbol: str = "BTC-USD") -> float:
    """Fetch the latest trade price for the given symbol."""
    url = f"{COINBASE_API}/products/{symbol}/ticker"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return float(data["price"])


def run(interval: int = 300, symbol: str = "BTC-USD") -> None:
    """Continuously print the price and change every ``interval`` seconds."""
    last_price: Optional[float] = None
    while True:
        price = fetch_price(symbol)
        change = 0.0 if last_price is None else price - last_price
        print(f"{symbol} price: {price:.2f} (change {change:+.2f})")
        last_price = price
        time.sleep(interval)
