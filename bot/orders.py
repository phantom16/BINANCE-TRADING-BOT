"""Order placement logic - connects the CLI to the API client."""

from bot.client import BinanceClient
from bot.logging_config import setup_logging

logger = setup_logging()


def place_order(client, symbol, side, order_type, quantity, price=None):
    """Build, send, and log an order."""

    # Print what we're about to do
    price_str = f" price={price}" if price is not None else ""
    logger.info("Order request: %s %s %s qty=%s%s", side, order_type, symbol, quantity, price_str)

    # Send the order
    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    # Print the result
    logger.info(
        "Order response: orderId=%s status=%s executedQty=%s avgPrice=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
        response.get("avgPrice"),
    )
    logger.info("Order placed successfully!")

    return response
