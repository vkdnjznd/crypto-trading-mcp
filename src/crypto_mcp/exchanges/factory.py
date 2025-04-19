from abc import ABC, abstractmethod

from crypto_mcp.exchanges.base import CryptoExchange
from crypto_mcp.exchanges.upbit import Upbit
from crypto_mcp.exchanges.gateio import GateIO
from crypto_mcp.http_handler import HTTPRequester
from crypto_mcp.exchanges.upbit import UpbitRequester
from crypto_mcp.exchanges.gateio import GateIOAuth
from crypto_mcp.exchanges.binance import Binance, BinanceAuth


class ExchangeFactory(ABC):
    @abstractmethod
    def create_requester(self) -> HTTPRequester:
        pass

    @abstractmethod
    def create_exchange(self) -> CryptoExchange:
        pass


class UpbitFactory(ExchangeFactory):
    def create_requester(self) -> HTTPRequester:
        return UpbitRequester()

    def create_exchange(self) -> CryptoExchange:
        return Upbit(self.create_requester())


class GateIOFactory(ExchangeFactory):
    def create_requester(self) -> HTTPRequester:
        return HTTPRequester(GateIOAuth())

    def create_exchange(self) -> CryptoExchange:
        return GateIO(self.create_requester())


class BinanceFactory(ExchangeFactory):
    def create_requester(self) -> HTTPRequester:
        return HTTPRequester(BinanceAuth())

    def create_exchange(self) -> CryptoExchange:
        return Binance(self.create_requester())


factories: dict[str, ExchangeFactory] = {
    "upbit": UpbitFactory,
    "gateio": GateIOFactory,
    "binance": BinanceFactory,
}


def get_factory(exchange_name: str) -> ExchangeFactory:
    return factories[exchange_name]()
