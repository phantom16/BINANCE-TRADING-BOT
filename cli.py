"""CLI entry point for the Simplified Trading Bot."""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

logger = setup_logging()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Place orders on Binance Futures Testnet (USDT-M).",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g. BTCUSDT)")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", default=None, help="Order price (required for LIMIT)")
    return parser.parse_args()


def main():
    # Load API keys from .env file
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env or environment.")
        sys.exit(1)

    args = parse_args()

    # Validate all inputs before sending anything
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except ValueError as e:
        logger.error("Validation error: %s", e)
        sys.exit(1)

    # Create client and place the order
    client = BinanceClient(api_key, api_secret)

    try:
        place_order(client, symbol, side, order_type, quantity, price)
    except RuntimeError as e:
        logger.error("Failed to place order: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
