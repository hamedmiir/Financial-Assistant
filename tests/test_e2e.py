from pathlib import Path

import pandas as pd
import pytest

from tradeassistant.__main__ import main


@pytest.mark.e2e
def test_run_once(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    df = pd.DataFrame({
        'Date': pd.date_range('2020-01-01', periods=3),
        'Open': [1,2,3],
        'High': [1,2,3],
        'Low': [1,2,3],
        'Close': [1,2,3],
        'Volume': [1,1,1]
    })
    df.to_csv(data_dir / 'AAPL.csv', index=False)
    cfg = tmp_path / 'config.toml'
    cfg.write_text('[general]\n timezone="UTC"\n data_provider="csv"\n symbols=["AAPL"]\n[scheduler]\n hour_utc=0\n')
    monkeypatch.chdir(tmp_path)
    main.callback = main
    main(['--config', str(cfg), '--run-once'])
    report = Path('reports') / f"{pd.Timestamp.now().date().isoformat()}.md"
    assert report.exists()
