import pytest
import httpx

from crypto_trading_mcp.exchanges.binance import Binance, BinanceAuth
from crypto_trading_mcp.exchanges.base import (
    CryptoTradingPair,
    OrderBook,
    OrderBookItem,
    Ticker,
    Balance,
    Order,
)
from tests.test_requester import FakeHTTPRequester


@pytest.fixture
def success_symbols_response():
    return httpx.Response(
        200,
        json={
            "timezone": "UTC",
            "serverTime": 1565246363776,
            "symbols": [
                {
                    "symbol": "ETHBTC",
                    "status": "TRADING",
                    "baseAsset": "ETH",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT",
                        "TAKE_PROFIT_LIMIT",
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "otoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "cancelReplaceAllowed": False,
                    "allowAmend": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [],
                    "permissions": [],
                    "permissionSets": [["SPOT", "MARGIN"]],
                    "defaultSelfTradePreventionMode": "NONE",
                    "allowedSelfTradePreventionModes": ["NONE"],
                }
            ],
            "sors": [{"baseAsset": "BTC", "symbols": ["BTCUSDT", "BTCUSDC"]}],
        },
    )


@pytest.fixture
def success_tickers_response():
    return httpx.Response(
        200,
        json={
            "symbol": "BNBBTC",
            "priceChange": "-94.99999800",
            "priceChangePercent": "-95.960",
            "weightedAvgPrice": "0.29628482",
            "prevClosePrice": "0.10002000",
            "lastPrice": "4.00000200",
            "lastQty": "200.00000000",
            "bidPrice": "4.00000000",
            "bidQty": "100.00000000",
            "askPrice": "4.00000200",
            "askQty": "100.00000000",
            "openPrice": "99.00000000",
            "highPrice": "100.00000000",
            "lowPrice": "0.10000000",
            "volume": "8913.30000000",
            "quoteVolume": "15.30000000",
            "openTime": 1499783499040,
            "closeTime": 1499869899040,
            "firstId": 28385,
            "lastId": 28460,
            "count": 76,
        },
    )


@pytest.fixture
def success_balances_response():
    return httpx.Response(
        200,
        json={
            "makerCommission": 15,
            "takerCommission": 15,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "commissionRates": {
                "maker": "0.00150000",
                "taker": "0.00150000",
                "buyer": "0.00000000",
                "seller": "0.00000000",
            },
            "canTrade": True,
            "canWithdraw": True,
            "canDeposit": True,
            "brokered": False,
            "requireSelfTradePrevention": False,
            "preventSor": False,
            "updateTime": 123456789,
            "accountType": "SPOT",
            "balances": [
                {"asset": "BTC", "free": "4723846.89208129", "locked": "0.00000000"},
                {"asset": "LTC", "free": "4763368.68006011", "locked": "0.00000000"},
            ],
            "permissions": ["SPOT"],
            "uid": 354937868,
        },
    )


@pytest.fixture
def success_order_response():
    return httpx.Response(
        200,
        json={
            "symbol": "LTCBTC",
            "orderId": 1,
            "orderListId": -1,
            "clientOrderId": "myOrder1",
            "price": "0.1",
            "origQty": "1.0",
            "executedQty": "0.0",
            "cummulativeQuoteQty": "0.0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "stopPrice": "0.0",
            "icebergQty": "0.0",
            "time": 1499827319559,
            "updateTime": 1499827319559,
            "isWorking": True,
            "workingTime": 1499827319559,
            "origQuoteOrderQty": "0.000000",
            "selfTradePreventionMode": "NONE",
        },
    )


@pytest.fixture
def success_order_book_response():
    return httpx.Response(
        200,
        json={
            "lastUpdateId": 1027024,
            "bids": [["4.00000000", "431.00000000"]],
            "asks": [["4.00000200", "12.00000000"]],
        },
    )


@pytest.fixture
def success_open_orders_response():
    return httpx.Response(
        200,
        json=[
            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "orderListId": -1,
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "cummulativeQuoteQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559,
                "updateTime": 1499827319559,
                "isWorking": True,
                "origQuoteOrderQty": "0.000000",
                "workingTime": 1499827319559,
                "selfTradePreventionMode": "NONE",
            }
        ],
    )


@pytest.fixture
def success_closed_orders_response():
    return httpx.Response(
        200,
        json=[
            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "orderListId": -1,
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "cummulativeQuoteQty": "0.0",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559,
                "updateTime": 1499827319559,
                "isWorking": True,
                "origQuoteOrderQty": "0.000000",
                "workingTime": 1499827319559,
                "selfTradePreventionMode": "NONE",
            }
        ],
    )


@pytest.fixture
def success_place_order_response():
    return httpx.Response(
        200,
        json={
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1,
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595,
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "origQuoteOrderQty": "0.000000",
            "cummulativeQuoteQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "SELL",
            "workingTime": 1507725176595,
            "selfTradePreventionMode": "NONE",
        },
    )


@pytest.fixture
def success_cancel_order_response():
    return httpx.Response(
        200,
        json={
            "symbol": "LTCBTC",
            "origClientOrderId": "myOrder1",
            "orderId": 4,
            "orderListId": -1,
            "clientOrderId": "cancelMyOrder1",
            "transactTime": 1684804350068,
            "price": "2.00000000",
            "origQty": "1.00000000",
            "executedQty": "0.00000000",
            "cummulativeQuoteQty": "0.00000000",
            "status": "CANCELED",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "selfTradePreventionMode": "NONE",
        },
    )


@pytest.mark.asyncio
async def test_get_symbols(success_symbols_response):
    binance = Binance(FakeHTTPRequester(success_symbols_response))
    symbols = await binance.get_symbols()

    assert symbols[0].symbol == "ETHBTC"
    assert symbols[0].name == "ETH"


@pytest.mark.asyncio
async def test_get_tickers(success_tickers_response):
    binance = Binance(FakeHTTPRequester(success_tickers_response))
    ticker = await binance.get_tickers("BNBBTC")

    assert ticker.symbol == "BNBBTC"
    assert ticker.trade_price == 4.00000200
    assert ticker.change_percentage == -95.96
    assert ticker.change_price == -94.99999800
    assert ticker.trade_volume == 8913.30000000
    assert ticker.acc_trade_volume == 15.30000000
    assert ticker.opening_price == 99.00000000
    assert ticker.high_price == 100.00000000
    assert ticker.low_price == 0.10000000


@pytest.mark.asyncio
async def test_get_balances(success_balances_response):
    binance = Binance(FakeHTTPRequester(success_balances_response))
    balances = await binance.get_balances()

    assert balances[0].currency == "BTC"
    assert balances[0].balance == 4723846.89208129
    assert balances[0].locked == 0.00000000

    assert balances[1].currency == "LTC"
    assert balances[1].balance == 4763368.68006011
    assert balances[1].locked == 0.00000000


@pytest.mark.asyncio
async def test_get_open_orders(success_open_orders_response):
    binance = Binance(FakeHTTPRequester(success_open_orders_response))
    orders = await binance.get_open_orders("LTCBTC", 1, 10)

    assert orders[0].order_id == "1"
    assert orders[0].price == 0.1
    assert orders[0].amount == 1.0
    assert orders[0].status == "wait"
    assert orders[0].created_at == 1499827319559


@pytest.mark.asyncio
async def test_get_closed_orders(success_closed_orders_response):
    binance = Binance(FakeHTTPRequester(success_closed_orders_response))
    orders = await binance.get_closed_orders("LTCBTC", 1, 10)

    assert orders[0].order_id == "1"
    assert orders[0].price == 0.1
    assert orders[0].amount == 1.0
    assert orders[0].status == "done"
    assert orders[0].created_at == 1499827319559


@pytest.mark.asyncio
async def test_get_order(success_order_response):
    binance = Binance(FakeHTTPRequester(success_order_response))
    order = await binance.get_order("1", "LTCBTC")

    assert order.order_id == "1"
    assert order.price == 0.1
    assert order.amount == 1.0
    assert order.status == "wait"
    assert order.created_at == 1499827319559


@pytest.mark.asyncio
async def test_get_order_book(success_order_book_response):
    binance = Binance(FakeHTTPRequester(success_order_book_response))
    order_book = await binance.get_order_book("LTCBTC")

    assert order_book.symbol == "LTCBTC"
    assert order_book.items[0].ask_price == 4.00000200
    assert order_book.items[0].ask_quantity == 12.00000000
    assert order_book.items[0].bid_price == 4.00000000
    assert order_book.items[0].bid_quantity == 431.00000000


@pytest.mark.asyncio
async def test_place_order(success_place_order_response):
    binance = Binance(FakeHTTPRequester(success_place_order_response))
    order = await binance.place_order("BTCUSDT", "ask", 10.00000000, 0.00000000)

    assert order.order_id == "28"
    assert order.price == 0.00000000
    assert order.amount == 10.00000000
    assert order.status == "done"
    assert order.created_at == 1507725176595


@pytest.mark.asyncio
async def test_cancel_order(success_cancel_order_response):
    binance = Binance(FakeHTTPRequester(success_cancel_order_response))
    order = await binance.cancel_order("1", "LTCBTC")

    assert order.order_id == "4"
    assert order.price == 2.00000000
    assert order.amount == 1.00000000
    assert order.status == "canceled"
    assert order.created_at == 1684804350068


def test_generate_signature():
    auth = BinanceAuth()
    auth.BINANCE_SECRET_KEY = "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"  # secret for testing

    payload_only_signature = auth.generate_signature(
        payload_string="symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559"
    )

    query_string_only_signature = auth.generate_signature(
        query_string="symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559"
    )

    both_signature = auth.generate_signature(
        "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC",
        "quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559",
    )

    assert (
        payload_only_signature
        == "c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71"
    )

    assert (
        query_string_only_signature
        == "c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71"
    )

    assert (
        both_signature
        == "0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77"
    )
