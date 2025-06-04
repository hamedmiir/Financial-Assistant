from __future__ import annotations

import json
from pathlib import Path
from typing import List

import tomli
from pydantic import BaseModel


class GeneralSettings(BaseModel):
    timezone: str
    data_provider: str = "yfinance"
    symbols: List[str]


class SchedulerSettings(BaseModel):
    hour_utc: int = 15


class Settings(BaseModel):
    general: GeneralSettings
    scheduler: SchedulerSettings


def load_config(path: str | Path) -> Settings:
    path = Path(path)
    data: dict
    if path.suffix in {".toml", ""}:
        data = tomli.loads(path.read_text())
    elif path.suffix == ".json":
        data = json.loads(path.read_text())
    elif path.suffix in {".yaml", ".yml"}:
        import yaml  # type: ignore

        data = yaml.safe_load(path.read_text())
    else:
        raise ValueError(f"Unsupported config format: {path.suffix}")
    return Settings(**data)
