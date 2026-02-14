import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logging

logger = setup_logging()

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    """Wrapper for the Binance Futures Testnet REST API."""

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {"X-MBX-APIKEY": self.api_key}

    def _sign(self, params):
        """Add timestamp and HMAC-SHA256 signature to the request params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method, path, params=None):
        """Send a signed request and return the JSON response."""
        if params is None:
            params = {}

        params = self._sign(params)
        url = BASE_URL + path

        logger.debug("REQUEST  %s %s params=%s", method, url, params)

        try:
            response = requests.request(method, url, headers=self.headers, params=params)
            data = response.json()
        except requests.RequestException as e:
            logger.error("Network error: %s", e)
            raise

        logger.debug("RESPONSE %s %s", response.status_code, data)

        if response.status_code != 200:
            error_msg = data.get("msg", "Unknown error")
            error_code = data.get("code", response.status_code)
            logger.error("API error %s: %s", error_code, error_msg)
            raise RuntimeError(f"Binance API error {error_code}: {error_msg}")

        return data

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """Place an order on the Binance Futures Testnet.

        Args:
            symbol: Trading pair, e.g. BTCUSDT
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Required for LIMIT orders
        """
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": str(quantity),
        }

        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            params["price"] = str(price)
            params["timeInForce"] = "GTC"

        return self._request("POST", "/fapi/v1/order", params)
