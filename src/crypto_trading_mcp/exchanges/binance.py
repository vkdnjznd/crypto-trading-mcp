import hmac
import hashlib
import time
import json
import httpx
import os

from urllib.parse import unquote
from typing import Literal, Optional, Generator

from crypto_trading_mcp.exchanges.base import (
    CryptoExchange,
    CryptoTradingPair,
    Ticker,
    Balance,
    Order,
    OrderBook,
    OrderBookItem,
)


class BinanceAuth(httpx.Auth):
    BINANCE_ACCESS_KEY = os.getenv("BINANCE_ACCESS_KEY")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

    def is_signature_required(self, path: str) -> bool:
        endpoints = (
            "/api/v3/order",
            "/api/v3/openOrders",
            "/api/v3/allOrders",
            "/api/v3/account",
        )

        return path.endswith(endpoints)

    def generate_signature(
        self, query_string: str = "", payload_string: str = ""
    ) -> str:
        message = ""
        if query_string:
            message += query_string

        if payload_string:
            message += payload_string

        signature = hmac.new(
            self.BINANCE_SECRET_KEY.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

        return signature

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        if self.is_signature_required(request.url.path):
            query_string = unquote(request.url.query.decode())
            payload_string = unquote(request.content.decode())

            signature = self.generate_signature(query_string, payload_string)
            request.url = request.url.copy_merge_params({"signature": signature})

        request.headers["X-MBX-APIKEY"] = self.BINANCE_ACCESS_KEY
        yield request


class Binance(CryptoExchange):
    BASE_URL = "https://api.binance.com/api/v3"

    async def get_symbols(self) -> list[CryptoTradingPair]:
        response = await self.requester.get(f"{self.BASE_URL}/exchangeInfo")

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "msg")
            )

        data = response.json()
        symbols = []
        for symbol_info in data["symbols"]:
            if symbol_info["status"] == "TRADING":
                symbols.append(
                    CryptoTradingPair(
                        symbol=symbol_info["symbol"], name=symbol_info["baseAsset"]
                    )
                )

        return symbols

    async def get_tickers(self, symbol: str) -> Ticker:
        response = await self.requester.get(
            f"{self.BASE_URL}/ticker/24hr", params={"symbol": symbol}
        )

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "msg")
            )

        data = response.json()
        return Ticker(
            symbol=data["symbol"],
            trade_price=float(data["lastPrice"]),
            trade_volume=float(data["volume"]),
            trade_timestamp=int(time.time() * 1000),
            opening_price=float(data["openPrice"]),
            high_price=float(data["highPrice"]),
            low_price=float(data["lowPrice"]),
            change_percentage=float(data["priceChangePercent"]),
            change_price=float(data["priceChange"]),
            acc_trade_volume=float(data["quoteVolume"]),
            acc_trade_price=float(data["quoteVolume"]) * float(data["lastPrice"]),
            timestamp=int(time.time() * 1000),
        )

    async def get_balances(self) -> list[Balance]:
        response = await self.requester.get(
            f"{self.BASE_URL}/account", params={"timestamp": int(time.time() * 1000)}
        )

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "msg")
            )

        data = response.json()
        balances = []
        for balance in data["balances"]:
            balances.append(
                Balance(
                    currency=balance["asset"],
                    balance=float(balance["free"]),
                    locked=float(balance["locked"]),
                    avg_buy_price=None,
                    avg_buy_price_modified=False,
                    unit_currency=None,
                )
            )
        return balances

    async def get_open_orders(
        self,
        symbol: str,
        page: int,
        limit: int,
        order_by: Literal["asc", "desc"] = "desc",
    ) -> list[Order]:
        response = await self.requester.get(
            f"{self.BASE_URL}/openOrders",
            params={
                "symbol": symbol,
                "timestamp": int(time.time() * 1000),
            },
        )

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "msg")
            )

        data = response.json()
        return [self._convert_to_order(order) for order in data]

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
            "symbol": symbol,
            "limit": limit,
            "timestamp": int(time.time() * 1000),
        }

        if start_date:
            params["startTime"] = start_date
        if end_date:
            params["endTime"] = end_date

        response = await self.requester.get(
            f"{self.BASE_URL}/allOrders",
            params=params,
        )

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response)
            )

        data = response.json()
        return [
            self._convert_to_order(order)
            for order in data
            if order["status"]
            in ("FILLED", "CANCELED", "REJECTED", "EXPIRED", "EXPIRED_IN_MATCH")
        ]

    async def get_order(self, order_id: str, symbol: str = None) -> Order:
        response = await self.requester.get(
            f"{self.BASE_URL}/order",
            params={
                "symbol": symbol,
                "orderId": order_id,
                "timestamp": int(time.time() * 1000),
            },
        )

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response)
            )

        data = response.json()
        return self._convert_to_order(data)

    async def get_order_book(self, symbol: str) -> OrderBook:
        response = await self.requester.get(
            f"{self.BASE_URL}/depth", params={"symbol": symbol}
        )

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response)
            )

        data = response.json()
        return OrderBook(
            symbol=symbol,
            timestamp=int(time.time() * 1000),
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
        side: Literal["bid", "ask"],
        amount: float,
        price: float,
        order_type: Literal["limit", "market"] = "limit",
    ) -> Order:
        params = {
            "symbol": symbol,
            "side": "BUY" if side == "bid" else "SELL",
            "quantity": str(amount),
            "price": str(price),
            "type": order_type.upper(),
            "timestamp": int(time.time() * 1000),
        }

        if order_type == "limit":
            params["timeInForce"] = "GTC"
        elif order_type == "market":
            params["timeInForce"] = "IOC"

        response = await self.requester.post(f"{self.BASE_URL}/order", params=params)

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response)
            )

        data = response.json()
        data["time"] = data["transactTime"]
        return self._convert_to_order(data)

    async def cancel_order(self, order_id: str, symbol: str = None) -> Order:
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": int(time.time() * 1000),
        }
        response = await self.requester.delete(f"{self.BASE_URL}/order", params=params)

        if not response.is_success:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response)
            )

        data = response.json()
        data["time"] = data["transactTime"]
        return self._convert_to_order(data)

    def _convert_to_order(self, data: dict) -> Order:
        status_map = {
            "NEW": "wait",
            "PENDING_NEW": "wait",
            "PARTIALLY_FILLED": "wait",
            "FILLED": "done",
        }

        return Order(
            order_id=str(data["orderId"]),
            side="bid" if data["side"] == "BUY" else "ask",
            price=float(data.get("price", 0)),
            order_type=data["type"].lower(),
            amount=float(data["origQty"]),
            status=status_map.get(data["status"], "canceled"),
            executed_volume=float(data.get("executedQty", 0)),
            remaining_volume=float(data.get("origQty", 0))
            - float(data.get("executedQty", 0)),
            created_at=data["time"],
        )
