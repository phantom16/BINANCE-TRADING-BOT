# Simplified Trading Bot

A small Python command-line tool that places orders on the **Binance Futures Testnet (USDT-M)**.
It supports **Market** and **Limit** orders, for both **Buy** and **Sell** sides.

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/phantom16/BINANCE-TRADING-BOT.git
cd BINANCE-TRADING-BOT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs two packages: `requests` (for API calls) and `python-dotenv` (for loading `.env` files).

### 3. Set up your API keys

First, go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com), create an account, and generate an API key.

Then create a `.env` file in the project root:

```bash
cp .env.example .env
```

Open `.env` and paste your keys:

```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

---

## Usage

### Market order (buy at current price)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit order (sell at a specific price)

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 75000
```

### All available arguments

| Argument      | Required     | Description                              |
|--------------|-------------|------------------------------------------|
| `--symbol`   | Yes         | Trading pair, e.g. `BTCUSDT`, `ETHUSDT`  |
| `--side`     | Yes         | `BUY` or `SELL`                          |
| `--type`     | Yes         | `MARKET` or `LIMIT`                      |
| `--quantity` | Yes         | How much to buy/sell (e.g. `0.01`)       |
| `--price`    | LIMIT only  | The price you want (e.g. `75000`)        |

**Note:** The testnet has a minimum order value of ~100 USDT. For BTC, use at least `0.01` quantity.

---

## Project Structure

```
bot/
  __init__.py          # Makes bot a Python package
  client.py            # Handles API requests, signing, and error handling
  orders.py            # Takes validated input and places the order
  validators.py        # Checks all user input before anything is sent
  logging_config.py    # Sets up logging to console and file
cli.py                 # Entry point - parses arguments and runs everything
requirements.txt       # Python dependencies
.env.example           # Template for API keys
logs/
  trading_bot.log      # Auto-generated log file with request/response details
```

---

## How Logging Works

The bot logs to two places:

- **Console** - shows a short summary (what you're ordering, the result)
- **Log file** (`logs/trading_bot.log`) - saves full details including the raw API request and response

This makes it easy to see what happened at a glance, and debug issues when needed.

---

## Assumptions

- This only works with the **Binance Futures Testnet**, not the real exchange
- API calls are made directly using the `requests` library (no `python-binance` wrapper)
- Limit orders default to **GTC** (Good-Til-Cancelled)
- Each run places a single order - it's not a background service or loop
