from __future__ import annotations

import json
import sqlite3
from pathlib import Path

DB_PATH = Path("tradeassistant.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS ohlcv(
        date TEXT,
        symbol TEXT,
        data TEXT,
        PRIMARY KEY(date, symbol)
    )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS reports(
        date TEXT,
        symbol TEXT,
        json TEXT,
        markdown TEXT,
        PRIMARY KEY(date, symbol)
    )"""
    )
    conn.commit()
    conn.close()


def insert_ohlcv(symbol: str, df):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for dt, row in df.iterrows():
        cur.execute(
            "REPLACE INTO ohlcv(date, symbol, data) VALUES(?,?,?)",
            (dt.date().isoformat(), symbol, row.to_json()),
        )
    conn.commit()
    conn.close()


def insert_report(symbol: str, date: str, data: dict, markdown: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "REPLACE INTO reports(date, symbol, json, markdown) VALUES(?,?,?,?)",
        (date, symbol, json.dumps(data), markdown),
    )
    conn.commit()
    conn.close()


def load_report(symbol: str, date: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT json FROM reports WHERE symbol=? AND date=?",
        (symbol, date),
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None
