import httpx
import json

from abc import ABC, abstractmethod
from typing import Literal, Optional
from dataclasses import dataclass

from crypto_trading_mcp.http_handler import HTTPRequester
from crypto_trading_mcp.exceptions import (
    AuthenticationException,
    BadRequestException,
    NotFoundException,
    InternalServerErrorException,
    CryptoAPIException,
    RateLimitException,
)


@dataclass
class CryptoTradingPair:
    symbol: str
    name: str


@dataclass
class Ticker:
    symbol: str
    trade_timestamp: int
    trade_price: float
    trade_volume: float
    opening_price: float
    high_price: float
    low_price: float
    change_percentage: float
    change_price: float
    acc_trade_volume: float
    acc_trade_price: float
    timestamp: int

    def __post_init__(self):
        self.change_percentage = round(self.change_percentage, 2)


@dataclass
class Balance:
    currency: str
    balance: float
    locked: float
    avg_buy_price: float
    avg_buy_price_modified: bool
    unit_currency: str


@dataclass
class Order:
    order_id: str
    side: str
    amount: float
    price: float
    order_type: Literal["limit", "market"]
    status: Literal["wait", "done", "canceled"]
    executed_volume: float
    remaining_volume: float
    created_at: int


@dataclass
class OrderBookItem:
    ask_price: float
    ask_quantity: float
    bid_price: float
    bid_quantity: float


@dataclass
class OrderBook:
    symbol: str
    timestamp: int
    items: list[OrderBookItem]


class CryptoExchange(ABC):
    """
    Abstract base class for crypto exchanges.
    """

    def __init__(self, requester: HTTPRequester) -> None:
        self.requester = requester

    def _get_error_message(
        self, response: httpx.Response, message_fields: list[str]
    ) -> str:
        # response: failed response from exchange API
        # message_fields: fields to extract a error message from body of the response
        # You can use dot notation to access nested fields,
        # e.g. "error.message" will be converted to ["error"]["message"]

        try:
            data = response.json()
            for field in message_fields.strip().split("."):
                data = data[field]

            return data
        except (AttributeError, KeyError, json.JSONDecodeError):
            return ""

    def _raise_for_failed_response(self, status_code: int, message: str = None):
        if status_code == 401:
            raise AuthenticationException(
                "401", message=message or "Authentication failed"
            )
        elif status_code == 400:
            raise BadRequestException("400", message=message or "Bad Request")
        elif status_code == 404:
            raise NotFoundException("404", message=message or "Not Found")
        elif status_code == 429:
            raise RateLimitException("429", message=message or "Rate Limit Exceeded")
        elif status_code == 500:
            raise InternalServerErrorException(
                "500", message=message or "Internal Server Error"
            )
        else:
            raise CryptoAPIException(str(status_code), message)

    @abstractmethod
    async def get_symbols(self) -> list[CryptoTradingPair]:
        pass

    @abstractmethod
    async def get_tickers(self, symbol: str = "") -> list[Ticker]:
        pass

    @abstractmethod
    async def get_balances(self) -> list[Balance]:
        pass

    @abstractmethod
    async def get_open_orders(
        self,
        symbol: str,
        page: int,
        limit: int,
        order_by: Literal["asc", "desc"] = "desc",
    ) -> list[Order]:
        pass

    @abstractmethod
    async def get_closed_orders(
        self,
        symbol: str,
        page: int,
        limit: int,
        status: Optional[Literal["done", "canceled"]] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        order_by: Literal["asc", "desc"] = "desc",
    ) -> list[Order]:
        pass

    @abstractmethod
    async def get_order(self, order_id: str, symbol: str = None) -> Order:
        pass

    @abstractmethod
    async def get_order_book(self, symbol: str) -> OrderBook:
        pass

    @abstractmethod
    async def place_order(
        self,
        symbol: str,
        side: Literal["bid", "ask"],
        amount: float,
        price: float,
        order_type: Literal["limit", "market"] = "limit",
    ) -> Order:
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str, symbol: str = None) -> bool:
        pass
