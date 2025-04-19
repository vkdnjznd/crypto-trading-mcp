import os
import httpx
import uuid
import hashlib
import jwt
import json

from typing import List, Optional, Literal
from urllib.parse import urlencode, unquote

from crypto_trading_mcp.exchanges.base import (
    CryptoExchange,
    Balance,
    CryptoTradingPair,
    Order,
    OrderBook,
    OrderBookItem,
    Ticker,
)
from crypto_trading_mcp.http_handler import HTTPRequester, BearerAuth
from crypto_trading_mcp.utils import iso_to_timestamp


class UpbitRequester(HTTPRequester):
    UPBIT_ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
    UPBIT_SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

    def generate_auth(
        self, params: Optional[dict] = None, json: Optional[dict] = None
    ) -> BearerAuth:
        payload = {
            "access_key": self.UPBIT_ACCESS_KEY,
            "nonce": str(uuid.uuid4()),
        }

        if params or json:
            query_string = unquote(urlencode(params or json, doseq=True)).encode()

            m = hashlib.sha512()
            m.update(query_string)
            payload["query_hash"] = m.hexdigest()
            payload["query_hash_alg"] = "SHA512"

        token = jwt.encode(payload, self.UPBIT_SECRET_KEY, algorithm="HS256")
        return BearerAuth(token)

    async def send(self, *args, **kwargs) -> httpx.Response:
        self.authorization = self.generate_auth(
            kwargs.get("params"), kwargs.get("json")
        )
        return await super().send(*args, **kwargs)


class Upbit(CryptoExchange):
    def __init__(self, requester: HTTPRequester):
        self.requester = requester
        self.base_url = "https://api.upbit.com/v1"

    async def get_symbols(self) -> List[CryptoTradingPair]:
        response = await self.requester.get(
            url=f"{self.base_url}/market/all",
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        markets = response.json()
        return [
            CryptoTradingPair(
                symbol=market["market"],
                name=market["english_name"],
            )
            for market in markets
        ]

    async def get_tickers(self, symbol: str = "") -> List[Ticker]:
        params = {"markets": symbol} if symbol else None
        response = await self.requester.get(
            url=f"{self.base_url}/ticker",
            params=params,
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        tickers = response.json()
        return [
            Ticker(
                symbol=ticker["market"],
                trade_timestamp=ticker["trade_timestamp"],
                trade_price=ticker["trade_price"],
                trade_volume=ticker["trade_volume"],
                opening_price=ticker["opening_price"],
                high_price=ticker["high_price"],
                low_price=ticker["low_price"],
                change_percentage=ticker["signed_change_rate"] * 100,
                change_price=ticker["change_price"],
                acc_trade_volume=ticker["acc_trade_volume"],
                acc_trade_price=ticker["acc_trade_price"],
                timestamp=ticker["timestamp"],
            )
            for ticker in tickers
        ]

    async def get_balances(self) -> List[Balance]:
        response = await self.requester.get(
            url=f"{self.base_url}/accounts",
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        balances = response.json()
        return [
            Balance(
                currency=balance["currency"],
                balance=float(balance["balance"]),
                locked=float(balance["locked"]),
                avg_buy_price=float(balance["avg_buy_price"]),
                avg_buy_price_modified=balance["avg_buy_price_modified"],
                unit_currency=balance["unit_currency"],
            )
            for balance in balances
        ]

    async def get_open_orders(
        self,
        symbol: str,
        page: int,
        limit: int,
        order_by: Literal["asc", "desc"] = "desc",
    ) -> List[Order]:
        params = {
            "market": symbol,
            "page": page,
            "limit": limit,
            "order_by": order_by,
            "states[]": ["wait", "watch"],
        }

        response = await self.requester.get(
            url=f"{self.base_url}/orders/open",
            params=params,
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        orders = response.json()
        return [
            Order(
                order_id=order["uuid"],
                side=order["side"],
                amount=float(order["volume"]),
                price=float(order["price"]),
                order_type=order["ord_type"],
                status=order["state"],
                executed_volume=float(order["executed_volume"]),
                remaining_volume=float(order["remaining_volume"]),
                created_at=iso_to_timestamp(order["created_at"]),
            )
            for order in orders
        ]

    async def get_closed_orders(
        self,
        symbol: str,
        page: int,
        limit: int,
        status: Optional[Literal["done", "canceled"]] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        order_by: Literal["asc", "desc"] = "desc",
    ) -> List[Order]:
        params = {"market": symbol, "limit": limit, "order_by": order_by}
        if status:
            params["state"] = "cancel" if status == "canceled" else status
        else:
            params["states[]"] = ["done", "cancel"]

        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        response = await self.requester.get(
            url=f"{self.base_url}/orders/closed",
            params=params,
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        orders = response.json()
        return [
            Order(
                order_id=order["uuid"],
                side=order["side"],
                amount=float(order["volume"]),
                price=float(order["price"]),
                order_type=order["ord_type"],
                status=order["state"],
                executed_volume=float(order["executed_volume"]),
                remaining_volume=float(order["remaining_volume"]),
                created_at=iso_to_timestamp(order["created_at"]),
            )
            for order in orders
        ]

    async def get_order(self, order_id: str, symbol: str = None) -> Order:
        response = await self.requester.get(
            url=f"{self.base_url}/order",
            params={"uuid": order_id},
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        orders = response.json()
        order = orders[0]
        return Order(
            order_id=order["uuid"],
            side=order["side"],
            amount=float(order["volume"]),
            price=float(order["price"]),
            order_type=order["ord_type"],
            status=order["state"],
            executed_volume=float(order["executed_volume"]),
            remaining_volume=float(order["remaining_volume"]),
            created_at=iso_to_timestamp(order["created_at"]),
        )

    async def get_order_book(self, market: str) -> OrderBook:
        response = await self.requester.get(
            url=f"{self.base_url}/orderbook",
            params={"markets": market},
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        order_book = response.json()[0]
        return OrderBook(
            symbol=order_book["market"],
            timestamp=order_book["timestamp"],
            items=[
                OrderBookItem(
                    ask_price=float(unit["ask_price"]),
                    ask_quantity=float(unit["ask_size"]),
                    bid_price=float(unit["bid_price"]),
                    bid_quantity=float(unit["bid_size"]),
                )
                for unit in order_book["orderbook_units"]
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
        order_type = "price" if order_type == "market" and side == "bid" else order_type

        response = await self.requester.post(
            url=f"{self.base_url}/orders",
            json={
                "market": symbol,
                "side": side,
                "volume": None if order_type == "price" else amount,
                "price": None if order_type == "market" and side == "ask" else price,
                "ord_type": order_type,
            },
        )
        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        order = response.json()
        return Order(
            order_id=order["uuid"],
            side=order["side"],
            amount=float(order["volume"]),
            price=float(order["price"]),
            order_type=order["ord_type"],
            status=order["state"],
            executed_volume=float(order["executed_volume"]),
            remaining_volume=float(order["remaining_volume"]),
            created_at=iso_to_timestamp(order["created_at"]),
        )

    async def cancel_order(self, order_id: str, symbol: str = None) -> bool:
        response = await self.requester.delete(
            url=f"{self.base_url}/order",
            params={"uuid": order_id},
        )

        if response.is_error:
            self._raise_for_failed_response(
                response.status_code, self._get_error_message(response, "error.message")
            )

        return True
