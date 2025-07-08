# TradeAssistant

TradeAssistant monitors markets, computes technical indicators, and generates daily analysis reports.

The assistant can pull data from **yfinance**, **CSV files**, or the Coinbase API.

## Quick Start

```bash
pip install -e .
cp config.toml.example config.toml
python -m tradeassistant --run-once --config config.toml
```

If you choose the `coinbase` provider set the `COINBASE_API_KEY` environment variable with your API token.
