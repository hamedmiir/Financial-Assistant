from pathlib import Path

from tradeassistant.config import load_config


def test_load_config_toml(tmp_path: Path):
    p = tmp_path / "config.toml"
    p.write_text("""[general]\ntimezone='UTC'\ndata_provider='csv'\nsymbols=['AAPL']\n[scheduler]\nhour_utc=1\n""")
    cfg = load_config(p)
    assert cfg.general.symbols == ["AAPL"]
    assert cfg.scheduler.hour_utc == 1
