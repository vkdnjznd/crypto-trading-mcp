import os
import httpx
import hashlib
import time
import hmac
import json

from typing import Literal, Optional, Generator
from urllib.parse import unquote

from crypto_trading_mcp.exchanges.base import (
    CryptoExchange,
    CryptoTradingPair,
    Ticker,
    Balance,
    Order,
    OrderBook,
    OrderBookItem,
)
from crypto_trading_mcp.http_handler import HTTPRequester


class GateIOAuth(httpx.Auth):
    GATEIO_ACCESS_KEY = os.getenv("GATEIO_ACCESS_KEY")
    GATEIO_SECRET_KEY = os.getenv("GATEIO_SECRET_KEY")

    def generate_signature(
        self,
        endpoint: str,
        method: str,
        timestamp: int,
        query_string: str = "",
        payload_string: str = "",
    ) -> str:
        m = hashlib.sha512()
        m.update(payload_string.encode())
        hashed_payload = m.hexdigest()

        message = f"{method}\n{endpoint}\n{query_string}\n{hashed_payload}\n{timestamp}"
        signature = hmac.new(
            self.GATEIO_SECRET_KEY.encode(), message.encode(), hashlib.sha512
        ).hexdigest()

        return signature

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        body = request.content.decode()
        query_string = unquote(request.url.query.decode())

        timestamp = time.time()
        signature = self.generate_signature(
            request.url.path, request.method, timestamp, query_string, body
        )

        request.headers["KEY"] = self.GATEIO_ACCESS_KEY
        request.headers["SIGN"] = signature
        request.headers["Timestamp"] = str(timestamp)

        yield request


class GateIO(CryptoExchange):
    def __init__(self, requester: HTTPRequester) -> None:
        super().__init__(requester)
        self.base_url = "https://api.gateio.ws/api/v4"

    async def get_symbols(self) -> list[CryptoTradingPair]:
        response = await self.requester.get(f"{self.base_url}/spot/currency_pairs")

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        data = response.json()
        return [
            CryptoTradingPair(
                symbol=item["id"],
                name=item["base_name"],
            )
            for item in data
        ]

    async def get_tickers(self, symbol: str = "") -> list[Ticker]:
        response = await self.requester.get(
            f"{self.base_url}/spot/tickers",
            params={"currency_pair": symbol} if symbol else None,
        )

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        data = response.json()
        timestamp = time.time() * 1000
        return [
            Ticker(
                symbol=item["currency_pair"],
                trade_timestamp=timestamp,
                trade_price=float(item["last"]),
                trade_volume=float(item["base_volume"]),
                opening_price=None,
                high_price=float(item["high_24h"]),
                low_price=float(item["low_24h"]),
                change_percentage=float(item["change_percentage"]),
                change_price=None,
                acc_trade_volume=float(item["quote_volume"]),
                acc_trade_price=float(item["quote_volume"]) * float(item["last"]),
                timestamp=timestamp,
            )
            for item in data
        ]

    async def get_balances(self) -> list[Balance]:
        response = await self.requester.get(f"{self.base_url}/spot/accounts")

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        data = response.json()
        return [
            Balance(
                currency=item["currency"],
                balance=float(item["available"]),
                locked=float(item["locked"]),
                avg_buy_price=None,
                avg_buy_price_modified=None,
                unit_currency=None,
            )
            for item in data
        ]

    def _convert_to_order(self, data: dict) -> Order:
        status_map = {
            "open": "wait",
            "closed": "done",
            "cancelled": "cancel",
        }

        return Order(
            order_id=data["id"],
            side="bid" if data["side"] == "buy" else "ask",
            amount=float(data["amount"]),
            price=float(data["price"]),
            order_type=data["type"],
            status=status_map[data["status"]],
            executed_volume=float(data["filled_amount"]),
            remaining_volume=float(data["left"]),
            created_at=data["create_time_ms"],
        )

    async def get_open_orders(
        self,
        symbol: str,
        page: int,
        limit: int,
        order_by: Literal["asc", "desc"] = "desc",
    ) -> list[Order]:
        params = {
            "currency_pair": symbol,
            "page": page,
            "limit": limit,
            "status": "open",
        }

        response = await self.requester.get(
            f"{self.base_url}/spot/orders", params=params
        )

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        data = response.json()
        return [self._convert_to_order(item) for item in data]

    async def get_closed_orders(
        self,
        symbol: str,
        page: int,
        limit: int,
        status: Optional[Literal["done", "cancel"]] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        order_by: Literal["asc", "desc"] = "desc",
    ) -> list[Order]:
        params = {
            "currency_pair": symbol,
            "page": page,
            "limit": limit,
            "status": "finished",
        }

        if start_date:
            params["from"] = start_date // 1000
        if end_date:
            params["to"] = end_date // 1000

        response = await self.requester.get(
            f"{self.base_url}/spot/orders", params=params
        )

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        data = response.json()
        return [self._convert_to_order(item) for item in data]

    async def get_order(self, order_id: str, symbol: str = None) -> Order:
        response = await self.requester.get(
            f"{self.base_url}/spot/orders/{order_id}",
            params={"currency_pair": symbol} if symbol else None,
        )

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        data = response.json()
        return self._convert_to_order(data)

    async def get_order_book(self, symbol: str) -> OrderBook:
        response = await self.requester.get(
            f"{self.base_url}/spot/order_book", params={"currency_pair": symbol}
        )

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        data = response.json()
        return OrderBook(
            symbol=symbol,
            timestamp=data["current"],
            items=[
                OrderBookItem(
                    ask_price=float(ask[0]),
                    ask_quantity=float(ask[1]),
                    bid_price=float(bid[0]),
                    bid_quantity=float(bid[1]),
                )
                for ask, bid in zip(data["asks"], data["bids"])
            ],
        )

    async def place_order(
        self,
        symbol: str,
        side: str,
        amount: float,
        price: float,
        order_type: Literal["limit", "market"] = "limit",
    ) -> Order:
        data = {
            "currency_pair": symbol,
            "side": "buy" if side == "bid" else "sell",
            "amount": str(amount),
            "price": str(price),
            "type": order_type,
            "time_in_force": "gtc" if order_type == "limit" else "ioc",
        }

        response = await self.requester.post(f"{self.base_url}/spot/orders", json=data)
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        order_data = response.json()
        return self._convert_to_order(order_data)

    async def cancel_order(self, order_id: str, symbol: str = None) -> bool:
        response = await self.requester.delete(
            f"{self.base_url}/spot/orders/{order_id}",
            params={"currency_pair": symbol},
        )

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "message")
            )

        return True
