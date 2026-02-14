"""Input validation for CLI arguments."""

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT"]


def validate_symbol(symbol):
    """Check that the symbol is a valid alphabetic string like BTCUSDT."""
    symbol = symbol.strip().upper()
    if not symbol or not symbol.isalpha():
        raise ValueError(f"Invalid symbol: '{symbol}'. Must be alphabetic (e.g. BTCUSDT).")
    return symbol


def validate_side(side):
    """Check that side is BUY or SELL."""
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side: '{side}'. Must be BUY or SELL.")
    return side


def validate_order_type(order_type):
    """Check that order type is MARKET or LIMIT."""
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type: '{order_type}'. Must be MARKET or LIMIT.")
    return order_type


def validate_quantity(quantity):
    """Check that quantity is a positive number."""
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid quantity: '{quantity}'. Must be a positive number.")
    if qty <= 0:
        raise ValueError(f"Quantity must be positive, got {qty}.")
    return qty


def validate_price(price, order_type):
    """Check price - required for LIMIT orders, ignored for MARKET."""
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            p = float(price)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid price: '{price}'. Must be a positive number.")
        if p <= 0:
            raise ValueError(f"Price must be positive, got {p}.")
        return p
    return None
