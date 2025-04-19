import pytest
import httpx

from crypto_trading_mcp.exchanges.upbit import Upbit
from crypto_trading_mcp.exchanges.base import (
    CryptoTradingPair,
    OrderBook,
    OrderBookItem,
    Ticker,
    Balance,
    Order,
)
from tests.test_requester import FakeHTTPRequester
from crypto_trading_mcp.exceptions import CryptoAPIException


@pytest.fixture
def success_symbols_response():
    return httpx.Response(
        200,
        json=[
            {
                "market": "KRW-BTC",
                "korean_name": "비트코인",
                "english_name": "Bitcoin",
                "market_event": {
                    "warning": False,
                    "caution": {
                        "PRICE_FLUCTUATIONS": False,
                        "TRADING_VOLUME_SOARING": False,
                        "DEPOSIT_AMOUNT_SOARING": True,
                        "GLOBAL_PRICE_DIFFERENCES": False,
                        "CONCENTRATION_OF_SMALL_ACCOUNTS": False,
                    },
                },
            },
            {
                "market": "KRW-ETH",
                "korean_name": "이더리움",
                "english_name": "Ethereum",
                "market_event": {
                    "warning": True,
                    "caution": {
                        "PRICE_FLUCTUATIONS": False,
                        "TRADING_VOLUME_SOARING": False,
                        "DEPOSIT_AMOUNT_SOARING": False,
                        "GLOBAL_PRICE_DIFFERENCES": False,
                        "CONCENTRATION_OF_SMALL_ACCOUNTS": False,
                    },
                },
            },
        ],
    )


@pytest.fixture
def success_tickers_response():
    return httpx.Response(
        200,
        json=[
            {
                "market": "KRW-BTC",
                "trade_date": "20240822",
                "trade_time": "071602",
                "trade_date_kst": "20240822",
                "trade_time_kst": "161602",
                "trade_timestamp": 1724310962713,
                "opening_price": 82900000,
                "high_price": 83000000,
                "low_price": 81280000,
                "trade_price": 82324000,
                "prev_closing_price": 82900000,
                "change": "FALL",
                "change_price": 576000,
                "change_rate": 0.0069481303,
                "signed_change_price": -576000,
                "signed_change_rate": -0.0069481303,
                "trade_volume": 0.00042335,
                "acc_trade_price": 66058843588.46906,
                "acc_trade_price_24h": 250206655398.15125,
                "acc_trade_volume": 803.00214714,
                "acc_trade_volume_24h": 3047.01625142,
                "highest_52_week_price": 105000000,
                "highest_52_week_date": "2024-03-14",
                "lowest_52_week_price": 34100000,
                "lowest_52_week_date": "2023-09-11",
                "timestamp": 1724310962747,
            },
            {
                "market": "KRW-ETH",
                "trade_date": "20240822",
                "trade_time": "071600",
                "trade_date_kst": "20240822",
                "trade_time_kst": "161600",
                "trade_timestamp": 1724310960320,
                "opening_price": 3564000,
                "high_price": 3576000,
                "low_price": 3515000,
                "trade_price": 3560000,
                "prev_closing_price": 3564000,
                "change": "FALL",
                "change_price": 4000,
                "change_rate": 0.0011223345,
                "signed_change_price": -4000,
                "signed_change_rate": -0.0011223345,
                "trade_volume": 0.00281214,
                "acc_trade_price": 14864479133.80843,
                "acc_trade_price_24h": 59043494176.58761,
                "acc_trade_volume": 4188.3697943,
                "acc_trade_volume_24h": 16656.93091147,
                "highest_52_week_price": 5783000,
                "highest_52_week_date": "2024-03-13",
                "lowest_52_week_price": 2087000,
                "lowest_52_week_date": "2023-10-12",
                "timestamp": 1724310960351,
            },
        ],
    )


@pytest.fixture
def success_balances_response():
    return httpx.Response(
        200,
        json=[
            {
                "currency": "KRW",
                "balance": "1000000.0",
                "locked": "0.0",
                "avg_buy_price": "0",
                "avg_buy_price_modified": False,
                "unit_currency": "KRW",
            },
            {
                "currency": "BTC",
                "balance": "2.0",
                "locked": "0.0",
                "avg_buy_price": "101000",
                "avg_buy_price_modified": True,
                "unit_currency": "KRW",
            },
        ],
    )


@pytest.fixture
def success_order_response():
    return httpx.Response(
        200,
        json=[
            {
                "uuid": "d098ceaf-6811-4df8-97f2-b7e01aefc03f",
                "side": "bid",
                "ord_type": "limit",
                "price": "104812000",
                "state": "wait",
                "market": "KRW-BTC",
                "created_at": "2024-06-13T10:26:21+09:00",
                "volume": "0.00101749",
                "remaining_volume": "0.00006266",
                "reserved_fee": "53.32258094",
                "remaining_fee": "3.28375996",
                "paid_fee": "50.03882098",
                "locked": "6570.80367996",
                "executed_volume": "0.00095483",
                "executed_funds": "100077.64196",
                "trades_count": 1,
            }
        ],
    )


@pytest.fixture
def success_open_orders_response():
    return httpx.Response(
        200,
        json=[
            {
                "uuid": "d098ceaf-6811-4df8-97f2-b7e01aefc03f",
                "side": "bid",
                "ord_type": "limit",
                "price": "104812000",
                "state": "wait",
                "market": "KRW-BTC",
                "created_at": "2024-06-13T10:26:21+09:00",
                "volume": "0.00101749",
                "remaining_volume": "0.00006266",
                "reserved_fee": "53.32258094",
                "remaining_fee": "3.28375996",
                "paid_fee": "50.03882098",
                "locked": "6570.80367996",
                "executed_volume": "0.00095483",
                "executed_funds": "100077.64196",
                "trades_count": 1,
            },
        ],
    )


@pytest.fixture
def success_closed_orders_response():
    return httpx.Response(
        200,
        json=[
            {
                "uuid": "e5715c44-2d1a-41e6-91d8-afa579e28731",
                "side": "ask",
                "ord_type": "limit",
                "price": "103813000",
                "state": "done",
                "market": "KRW-BTC",
                "created_at": "2024-06-13T10:28:36+09:00",
                "volume": "0.00039132",
                "remaining_volume": "0",
                "reserved_fee": "0",
                "remaining_fee": "0",
                "paid_fee": "20.44627434",
                "locked": "0",
                "executed_volume": "0.00039132",
                "executed_funds": "40892.54868",
                "trades_count": 2,
            },
        ],
    )


@pytest.fixture
def success_order_book_response():
    return httpx.Response(
        200,
        json=[
            {
                "market": "KRW-BTC",
                "timestamp": 1720597558776,
                "total_ask_size": 1.20339227,
                "total_bid_size": 1.08861101,
                "orderbook_units": [
                    {
                        "ask_price": 83186000,
                        "bid_price": 83184000,
                        "ask_size": 0.02565269,
                        "bid_size": 0.07744926,
                    },
                    {
                        "ask_price": 83206000,
                        "bid_price": 83182000,
                        "ask_size": 0.02656392,
                        "bid_size": 0.51562837,
                    },
                    {
                        "ask_price": 83207000,
                        "bid_price": 83181000,
                        "ask_size": 0.00172255,
                        "bid_size": 0.00173694,
                    },
                ],
                "level": 0,
            }
        ],
    )


@pytest.fixture
def success_place_order_response():
    return httpx.Response(
        200,
        json={
            "uuid": "cdd92199-2897-4e14-9448-f923320408ad",
            "side": "bid",
            "ord_type": "limit",
            "price": "100.0",
            "state": "wait",
            "market": "KRW-BTC",
            "created_at": "2018-04-10T15:42:23+09:00",
            "volume": "0.01",
            "remaining_volume": "0.01",
            "reserved_fee": "0.0015",
            "remaining_fee": "0.0015",
            "paid_fee": "0.0",
            "locked": "1.0015",
            "executed_volume": "0.0",
            "trades_count": 0,
        },
    )


@pytest.fixture
def success_cancel_order_response():
    return httpx.Response(
        200,
        json={
            "uuid": "cdd92199-2897-4e14-9448-f923320408ad",
            "side": "bid",
            "ord_type": "limit",
            "price": "100.0",
            "state": "wait",
            "market": "KRW-BTC",
            "created_at": "2018-04-10T15:42:23+09:00",
            "volume": "0.01",
            "remaining_volume": "0.01",
            "reserved_fee": "0.0015",
            "remaining_fee": "0.0015",
            "paid_fee": "0.0",
            "locked": "1.0015",
            "executed_volume": "0.0",
            "trades_count": 0,
        },
    )


@pytest.mark.asyncio
async def test_get_symbols(success_symbols_response):
    requester = FakeHTTPRequester(success_symbols_response)
    sut = Upbit(requester)
    symbols = await sut.get_symbols()

    assert symbols == [
        CryptoTradingPair(
            symbol="KRW-BTC",
            name="Bitcoin",
        ),
        CryptoTradingPair(
            symbol="KRW-ETH",
            name="Ethereum",
        ),
    ]


@pytest.mark.asyncio
async def test_get_tickers(success_tickers_response):
    requester = FakeHTTPRequester(success_tickers_response)
    sut = Upbit(requester)
    tickers = await sut.get_tickers()

    assert tickers == [
        Ticker(
            symbol="KRW-BTC",
            trade_timestamp=1724310962713,
            trade_price=82324000.0,
            trade_volume=0.00042335,
            opening_price=82900000.0,
            high_price=83000000.0,
            low_price=81280000.0,
            change_percentage=-0.69,
            change_price=576000.0,
            acc_trade_volume=803.00214714,
            acc_trade_price=66058843588.46906,
            timestamp=1724310962747,
        ),
        Ticker(
            symbol="KRW-ETH",
            trade_timestamp=1724310960320,
            trade_price=3560000.0,
            trade_volume=0.00281214,
            opening_price=3564000.0,
            high_price=3576000.0,
            low_price=3515000.0,
            change_percentage=-0.11,
            change_price=4000.0,
            acc_trade_volume=4188.3697943,
            acc_trade_price=14864479133.80843,
            timestamp=1724310960351,
        ),
    ]


@pytest.mark.asyncio
async def test_get_balances(success_balances_response):
    requester = FakeHTTPRequester(success_balances_response)
    sut = Upbit(requester)
    balances = await sut.get_balances()

    assert balances == [
        Balance(
            currency="KRW",
            balance=1000000.0,
            locked=0.0,
            avg_buy_price=0,
            avg_buy_price_modified=False,
            unit_currency="KRW",
        ),
        Balance(
            currency="BTC",
            balance=2.0,
            locked=0.0,
            avg_buy_price=101000,
            avg_buy_price_modified=True,
            unit_currency="KRW",
        ),
    ]


@pytest.mark.asyncio
async def test_get_order(success_order_response):
    requester = FakeHTTPRequester(success_order_response)
    sut = Upbit(requester)
    order = await sut.get_order("d098ceaf-6811-4df8-97f2-b7e01aefc03f")

    assert order == Order(
        order_id="d098ceaf-6811-4df8-97f2-b7e01aefc03f",
        side="bid",
        amount=0.00101749,
        price=104812000,
        order_type="limit",
        status="wait",
        executed_volume=0.00095483,
        remaining_volume=0.00006266,
        created_at=1718241981000,
    )


@pytest.mark.asyncio
async def test_get_open_orders(success_open_orders_response):
    requester = FakeHTTPRequester(success_open_orders_response)
    sut = Upbit(requester)
    orders = await sut.get_open_orders("KRW-BTC", 1, 100)

    assert orders == [
        Order(
            order_id="d098ceaf-6811-4df8-97f2-b7e01aefc03f",
            side="bid",
            amount=0.00101749,
            price=104812000,
            order_type="limit",
            status="wait",
            executed_volume=0.00095483,
            remaining_volume=0.00006266,
            created_at=1718241981000,
        ),
    ]


@pytest.mark.asyncio
async def test_get_closed_orders(success_closed_orders_response):
    requester = FakeHTTPRequester(success_closed_orders_response)
    sut = Upbit(requester)
    orders = await sut.get_closed_orders("KRW-BTC", 1, 100)

    assert orders == [
        Order(
            order_id="e5715c44-2d1a-41e6-91d8-afa579e28731",
            side="ask",
            amount=0.00039132,
            price=103813000,
            order_type="limit",
            status="done",
            executed_volume=0.00039132,
            remaining_volume=0,
            created_at=1718242116000,
        ),
    ]


@pytest.mark.asyncio
async def test_get_order_book(success_order_book_response):
    requester = FakeHTTPRequester(success_order_book_response)
    sut = Upbit(requester)
    order_book = await sut.get_order_book("KRW-BTC")

    assert order_book == OrderBook(
        symbol="KRW-BTC",
        timestamp=1720597558776,
        items=[
            OrderBookItem(
                ask_price=83186000,
                ask_quantity=0.02565269,
                bid_price=83184000,
                bid_quantity=0.07744926,
            ),
            OrderBookItem(
                ask_price=83206000,
                ask_quantity=0.02656392,
                bid_price=83182000,
                bid_quantity=0.51562837,
            ),
            OrderBookItem(
                ask_price=83207000,
                ask_quantity=0.00172255,
                bid_price=83181000,
                bid_quantity=0.00173694,
            ),
        ],
    )


@pytest.mark.asyncio
async def test_place_order(success_place_order_response):
    requester = FakeHTTPRequester(success_place_order_response)
    sut = Upbit(requester)
    order = await sut.place_order("KRW-BTC", "bid", 0.001, 104812000)

    assert order == Order(
        order_id="cdd92199-2897-4e14-9448-f923320408ad",
        side="bid",
        amount=0.01,
        price=100.0,
        order_type="limit",
        status="wait",
        executed_volume=0.0,
        remaining_volume=0.01,
        created_at=1523342543000,
    )


@pytest.mark.asyncio
async def test_cancel_order(success_cancel_order_response):
    requester = FakeHTTPRequester(success_cancel_order_response)
    sut = Upbit(requester)
    result = await sut.cancel_order("cdd92199-2897-4e14-9448-f923320408ad")

    assert result is True


@pytest.mark.asyncio
async def test_get_failed_message():
    requester = FakeHTTPRequester(
        httpx.Response(400, json={"error": {"message": "Get Balances Failed"}})
    )
    sut = Upbit(requester)

    with pytest.raises(CryptoAPIException) as e:
        await sut.get_balances()

    assert e.value.code == "400"
    assert e.value.message == "Get Balances Failed"
