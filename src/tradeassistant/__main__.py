from __future__ import annotations

import json
from pathlib import Path

import typer

from .analysis import Analysis
from .config import load_config
from .data import load_data
from .report import save_markdown, to_markdown
from .storage import init_db, insert_ohlcv, insert_report

app = typer.Typer()


@app.command()
def main(config: Path = typer.Option(Path("config.toml"), "--config"), run_once: bool = False, daemon: bool = False):
    settings = load_config(config)
    init_db()

    def job():
        data = load_data(settings.general.symbols, provider=settings.general.data_provider)
        results = []
        for sym, df in data.items():
            insert_ohlcv(sym, df)
            analysis = Analysis(sym, df)
            r = analysis.compute()
            results.append(r)
            insert_report(sym, r["date"], r, json.dumps(r))
        md = to_markdown(results)
        save_markdown(md)

    if run_once:
        job()
    elif daemon:
        from .scheduler import start

        start(settings.scheduler.hour_utc, job)
        typer.echo("Scheduler started. Press Ctrl+C to exit.")
        try:
            import time

            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            typer.echo("Exiting")
    else:
        typer.echo("Specify --run-once or --daemon")


if __name__ == "__main__":
    app()
