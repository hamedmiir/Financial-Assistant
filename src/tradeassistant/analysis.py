from __future__ import annotations

from datetime import date


import pandas as pd

from . import indicators


class Analysis:
    def __init__(self, symbol: str, data: pd.DataFrame):
        self.symbol = symbol
        self.data = data
        self.today = data.iloc[-1]
        self.yesterday = data.iloc[-2] if len(data) > 1 else self.today

    def compute(self) -> dict:
        df = self.data.copy()
        df["sma20"] = indicators.sma(df["close"], 20)
        df["sma50"] = indicators.sma(df["close"], 50)
        df["sma200"] = indicators.sma(df["close"], 200)
        df["rsi14"] = indicators.rsi(df["close"], 14)
        df["macd"] = indicators.macd(df["close"])
        df["atr14"] = indicators.atr(df, 14)
        latest = df.iloc[-1]

        trend = "sideways"
        if latest["sma20"] > latest["sma50"] > latest["sma200"]:
            trend = "bullish"
        elif latest["sma20"] < latest["sma50"] < latest["sma200"]:
            trend = "bearish"

        median_atr = df["atr14"].tail(30).median()
        vol_comment = "high" if latest["atr14"] > median_atr else "low"

        signal = 0
        if trend == "bullish":
            signal += 40
        elif trend == "bearish":
            signal += 10
        signal += max(min(100 - abs(50 - latest["rsi14"]), 50), 0) * 0.6

        summary = (
            f"{self.symbol} shows a {trend} trend with {vol_comment} volatility. "
            f"Signal strength {int(signal)}."
        )

        return {
            "date": date.today().isoformat(),
            "symbol": self.symbol,
            "trend": trend,
            "volatility": vol_comment,
            "signal": int(signal),
            "close": float(latest["close"]),
            "rsi": float(latest["rsi14"]),
            "summary": summary,
        }
