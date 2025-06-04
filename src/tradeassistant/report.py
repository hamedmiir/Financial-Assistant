from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def to_markdown(results: Iterable[dict]) -> str:
    lines = [f"# TradeAssistant Report – {date.today().isoformat()}", ""]
    lines.append("## Summary")
    for r in results:
        lines.append(f"* {r['symbol']} — {r['trend'].capitalize()} (Signal {r['signal']})")
    lines.append("")
    lines.append("## Detailed Analysis")
    for r in results:
        lines.append(f"### {r['symbol']}")
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        lines.append(f"| Close | {r['close']:.2f} |")
        lines.append(f"| RSI-14 | {r['rsi']:.1f} |")
        lines.append("")
        lines.append(r["summary"])
        lines.append("")
    lines.append(f"_Generated at {date.today().isoformat()} by TradeAssistant v0.1.0_")
    return "\n".join(lines)


def save_markdown(content: str):
    path = REPORT_DIR / f"{date.today().isoformat()}.md"
    path.write_text(content)
