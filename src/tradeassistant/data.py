from __future__ import annotations
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd
import yfinance as yf

CACHE = Path(".cache")
CACHE.mkdir(exist_ok=True)


def _cache_path(symbol: str) -> Path:
    return CACHE / f"{symbol}.json"


def fetch_yfinance(symbol: str) -> pd.DataFrame:
    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(days=180)
    ticker = yf.Ticker(symbol)
    retries = 3
    for _ in range(retries):
        try:
            df = ticker.history(start=start, end=end, interval="1d")
            if not df.empty:
                break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError(f"failed to download data for {symbol}")
    df = df.rename(columns=str.lower)
    df.index = df.index.tz_localize("UTC")
    _cache_path(symbol).write_text(df.to_json())
    return df


def load_cached(symbol: str) -> pd.DataFrame | None:
    path = _cache_path(symbol)
    if path.exists():
        return pd.read_json(path.read_text())
    return None


def load_csv(symbol: str) -> pd.DataFrame:
    path = Path(f"data/{symbol}.csv")
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path, parse_dates=["Date"])
    df = df.set_index("Date")
    df.index = df.index.tz_localize("UTC")
    return df.rename(columns=str.lower)


def load_data(symbols: Iterable[str], provider: str = "yfinance") -> dict[str, pd.DataFrame]:
    data = {}
    for sym in symbols:
        df = None
        if provider == "yfinance":
            try:
                df = fetch_yfinance(sym)
            except Exception:
                df = load_cached(sym)
        elif provider == "csv":
            df = load_csv(sym)
        else:
            raise ValueError(f"unknown provider {provider}")
        if df is None:
            raise RuntimeError(f"no data for {sym}")
        data[sym] = df.tail(120)
    return data
