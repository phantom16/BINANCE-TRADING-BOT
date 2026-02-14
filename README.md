# Simplified Trading Bot - Binance Futures Testnet

A simple Python CLI app that places **Market** and **Limit** orders on the **Binance Futures Testnet (USDT-M)**.

## Setup

### 1. Prerequisites

- Python 3.x
- A [Binance Futures Testnet](https://testnet.binancefuture.com) account with API credentials

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API credentials

Copy the example env file and add your keys:

```bash
cp .env.example .env
```

Then edit `.env` with your testnet keys:

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

## How to Run

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000
```

### CLI arguments

| Argument     | Required   | Description                        |
|-------------|------------|------------------------------------|
| `--symbol`  | Yes        | Trading pair (e.g. `BTCUSDT`)      |
| `--side`    | Yes        | `BUY` or `SELL`                    |
| `--type`    | Yes        | `MARKET` or `LIMIT`                |
| `--quantity`| Yes        | Order quantity                     |
| `--price`   | LIMIT only | Order price (required for LIMIT)   |

## Project Structure

```
trading_bot/
  bot/
    __init__.py        # Makes bot a Python package
    client.py          # Binance API client (REST calls + HMAC signing)
    orders.py          # Order placement logic
    validators.py      # Input validation
    logging_config.py  # Logging setup (console + file)
  cli.py               # CLI entry point (argparse)
  requirements.txt
  README.md
  .env.example
  logs/                # Created automatically when you run the bot
    trading_bot.log
```

## Logging

All API requests, responses, and errors are logged to `logs/trading_bot.log`. The console shows a shorter summary.

## Assumptions

- All API calls go to the Binance Futures Testnet: `https://testnet.binancefuture.com`
- Uses direct REST calls with the `requests` library (not the `python-binance` wrapper)
- LIMIT orders use `GTC` (Good-Til-Cancelled) as the default time-in-force
- The bot places one order per run (not a long-running service)
