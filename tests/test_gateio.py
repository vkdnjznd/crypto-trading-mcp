import pytest
import httpx

from crypto_trading_mcp.exchanges.gateio import GateIO, GateIOAuth
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
        json=[
            {
                "id": "ETH_USDT",
                "base": "ETH",
                "base_name": "Ethereum",
                "quote": "USDT",
                "quote_name": "Tether",
                "fee": "0.2",
                "min_base_amount": "0.001",
                "min_quote_amount": "1.0",
                "max_base_amount": "10000",
                "max_quote_amount": "10000000",
                "amount_precision": 3,
                "precision": 6,
                "trade_status": "tradable",
                "sell_start": 1516378650,
                "buy_start": 1516378650,
            }
        ],
    )


@pytest.fixture
def success_tickers_response():
    return httpx.Response(
        200,
        json=[
            {
                "currency_pair": "BTC3L_USDT",
                "last": "2.46140352",
                "lowest_ask": "2.477",
                "highest_bid": "2.4606821",
                "change_percentage": "-8.91",
                "change_utc0": "-8.91",
                "change_utc8": "-8.91",
                "base_volume": "656614.0845820589",
                "quote_volume": "1602221.66468375534639404191",
                "high_24h": "2.7431",
                "low_24h": "1.9863",
                "etf_net_value": "2.46316141",
                "etf_pre_net_value": "2.43201848",
                "etf_pre_timestamp": 1611244800,
                "etf_leverage": "2.2803019447281203",
            }
        ],
    )


@pytest.fixture
def success_balances_response():
    return httpx.Response(
        200,
        json=[
            {"currency": "ETH", "available": "968.8", "locked": "0", "update_id": 98}
        ],
    )


@pytest.fixture
def success_order_response():
    return httpx.Response(
        200,
        json={
            "id": "1852454420",
            "create_time": "1710488334",
            "update_time": "1710488334",
            "create_time_ms": 1710488334073,
            "update_time_ms": 1710488334074,
            "status": "closed",
            "currency_pair": "BTC_USDT",
            "type": "limit",
            "account": "unified",
            "side": "buy",
            "amount": "0.001",
            "price": "65000",
            "time_in_force": "gtc",
            "iceberg": "0",
            "left": "0",
            "filled_amount": "0.001",
            "fill_price": "63.4693",
            "filled_total": "63.4693",
            "avg_deal_price": "63469.3",
            "fee": "0.00000022",
            "fee_currency": "BTC",
            "point_fee": "0",
            "gt_fee": "0",
            "gt_maker_fee": "0",
            "gt_taker_fee": "0",
            "gt_discount": False,
            "rebated_fee": "0",
            "rebated_fee_currency": "USDT",
            "finish_as": "filled",
        },
    )


@pytest.fixture
def success_order_book_response():
    return httpx.Response(
        200,
        json={
            "id": 123456,
            "current": 1623898993123,
            "update": 1623898993121,
            "asks": [["1.52", "1.151"], ["1.53", "1.218"]],
            "bids": [["1.17", "201.863"], ["1.16", "725.464"]],
        },
    )


@pytest.fixture
def success_open_orders_response():
    return httpx.Response(
        200,
        json=[
            {
                "id": "1852454420",
                "create_time": "1710488334",
                "update_time": "1710488334",
                "create_time_ms": 1710488334073,
                "update_time_ms": 1710488334074,
                "status": "open",
                "currency_pair": "BTC_USDT",
                "type": "limit",
                "account": "unified",
                "side": "buy",
                "amount": "0.001",
                "price": "65000",
                "time_in_force": "gtc",
                "iceberg": "0",
                "left": "0",
                "filled_amount": "0.001",
                "fill_price": "63.4693",
                "filled_total": "63.4693",
                "avg_deal_price": "63469.3",
                "fee": "0.00000022",
                "fee_currency": "BTC",
                "point_fee": "0",
                "gt_fee": "0",
                "gt_maker_fee": "0",
                "gt_taker_fee": "0",
                "gt_discount": False,
                "rebated_fee": "0",
                "rebated_fee_currency": "USDT",
                "finish_as": "filled",
            },
        ],
    )


@pytest.fixture
def success_closed_orders_response():
    return httpx.Response(
        200,
        json=[
            {
                "id": "1852454425",
                "create_time": "1710488334",
                "update_time": "1710488334",
                "create_time_ms": 1710488334073,
                "update_time_ms": 1710488334074,
                "status": "closed",
                "currency_pair": "BTC_USDT",
                "type": "limit",
                "account": "unified",
                "side": "sell",
                "amount": "0.001",
                "price": "65000",
                "time_in_force": "gtc",
                "iceberg": "0",
                "left": "0",
                "filled_amount": "0.001",
                "fill_price": "63.4693",
                "filled_total": "63.4693",
                "avg_deal_price": "63469.3",
                "fee": "0.00000022",
                "fee_currency": "BTC",
                "point_fee": "0",
                "gt_fee": "0",
                "gt_maker_fee": "0",
                "gt_taker_fee": "0",
                "gt_discount": False,
                "rebated_fee": "0",
                "rebated_fee_currency": "USDT",
                "finish_as": "filled",
            },
        ],
    )


@pytest.fixture
def success_place_order_response():
    return httpx.Response(
        200,
        json={
            "id": "1852454420",
            "text": "t-abc123",
            "amend_text": "-",
            "create_time": "1710488334",
            "update_time": "1710488334",
            "create_time_ms": 1710488334073,
            "update_time_ms": 1710488334074,
            "status": "closed",
            "currency_pair": "BTC_USDT",
            "type": "limit",
            "account": "unified",
            "side": "buy",
            "amount": "0.001",
            "price": "65000",
            "time_in_force": "gtc",
            "iceberg": "0",
            "left": "0",
            "filled_amount": "0.001",
            "fill_price": "63.4693",
            "filled_total": "63.4693",
            "avg_deal_price": "63469.3",
            "fee": "0.00000022",
            "fee_currency": "BTC",
            "point_fee": "0",
            "gt_fee": "0",
            "gt_maker_fee": "0",
            "gt_taker_fee": "0",
            "gt_discount": False,
            "rebated_fee": "0",
            "rebated_fee_currency": "USDT",
            "finish_as": "filled",
        },
    )


@pytest.fixture
def success_cancel_order_response():
    return httpx.Response(
        200,
        json={
            "id": "1852454420",
            "create_time": "1710488334",
            "update_time": "1710488334",
            "create_time_ms": 1710488334073,
            "update_time_ms": 1710488334074,
            "status": "closed",
            "currency_pair": "BTC_USDT",
            "type": "limit",
            "account": "unified",
            "side": "buy",
            "amount": "0.001",
            "price": "65000",
            "time_in_force": "gtc",
            "iceberg": "0",
            "left": "0",
            "filled_amount": "0.001",
            "fill_price": "63.4693",
            "filled_total": "63.4693",
            "avg_deal_price": "63469.3",
            "fee": "0.00000022",
            "fee_currency": "BTC",
            "point_fee": "0",
            "gt_fee": "0",
            "gt_maker_fee": "0",
            "gt_taker_fee": "0",
            "gt_discount": False,
            "rebated_fee": "0",
            "rebated_fee_currency": "USDT",
            "finish_as": "filled",
        },
    )


def test_generate_signature():
    auth = GateIOAuth()
    signature = auth.generate_signature(
        "fake-endpoint",
        "POST",
        "1710488334",
        "currency_pair=BTC_USDT",
        '{"side":"buy","amount":"0.001","price":"65000","type":"limit","time_in_force":"gtc"}',
    )

    assert (
        signature
        == "ce0372c44f5fe877702fe7ae35c272157baaa58939449535ee45ae17a393820e27ca4e16aa190f23302592870aa10bff17e9d80bfe09c909aab323aed7f69419"
    )


@pytest.mark.asyncio
async def test_get_symbols(success_symbols_response):
    requester = FakeHTTPRequester(success_symbols_response)
    sut = GateIO(requester)
    symbols = await sut.get_symbols()
    assert symbols == [
        CryptoTradingPair(
            symbol="ETH_USDT",
            name="Ethereum",
        ),
    ]


@pytest.mark.asyncio
async def test_get_tickers(success_tickers_response):
    requester = FakeHTTPRequester(success_tickers_response)
    sut = GateIO(requester)
    tickers = await sut.get_tickers()
    ticker = tickers[0]

    assert ticker.symbol == "BTC3L_USDT"
    assert ticker.trade_price == 2.46140352
    assert ticker.trade_volume == 656614.0845820589
    assert ticker.high_price == 2.7431
    assert ticker.low_price == 1.9863
    assert ticker.acc_trade_volume == 1602221.66468375534639404191


@pytest.mark.asyncio
async def test_get_balances(success_balances_response):
    requester = FakeHTTPRequester(success_balances_response)
    sut = GateIO(requester)
    balances = await sut.get_balances()
    balance = balances[0]

    assert balance.currency == "ETH"
    assert balance.balance == 968.8
    assert balance.locked == 0.0
    assert balance.unit_currency is None


@pytest.mark.asyncio
async def test_get_order(success_order_response):
    requester = FakeHTTPRequester(success_order_response)
    sut = GateIO(requester)
    order = await sut.get_order("1852454420", "BTC_USDT")

    assert order.order_id == "1852454420"
    assert order.side == "bid"
    assert order.amount == 0.001
    assert order.price == 65000
    assert order.order_type == "limit"
    assert order.status == "done"


@pytest.mark.asyncio
async def test_get_open_orders(success_open_orders_response):
    requester = FakeHTTPRequester(success_open_orders_response)
    sut = GateIO(requester)
    orders = await sut.get_open_orders("BTC_USDT", 1, 100)

    assert orders == [
        Order(
            order_id="1852454420",
            side="bid",
            amount=0.001,
            price=65000.0,
            order_type="limit",
            status="wait",
            executed_volume=0.001,
            remaining_volume=0.0,
            created_at=1710488334073,
        ),
    ]


@pytest.mark.asyncio
async def test_get_closed_orders(success_closed_orders_response):
    requester = FakeHTTPRequester(success_closed_orders_response)
    sut = GateIO(requester)
    orders = await sut.get_closed_orders("BTC_USDT", 1, 100)

    assert orders == [
        Order(
            order_id="1852454425",
            side="ask",
            amount=0.001,
            price=65000.0,
            order_type="limit",
            status="done",
            executed_volume=0.001,
            remaining_volume=0.0,
            created_at=1710488334073,
        ),
    ]


@pytest.mark.asyncio
async def test_get_closed_orders(success_closed_orders_response):
    requester = FakeHTTPRequester(success_closed_orders_response)
    sut = GateIO(requester)
    orders = await sut.get_closed_orders("BTC_USDT", 1, 100)

    assert orders == [
        Order(
            order_id="1852454425",
            side="ask",
            amount=0.001,
            price=65000.0,
            order_type="limit",
            status="done",
            executed_volume=0.001,
            remaining_volume=0.0,
            created_at=1710488334073,
        ),
    ]


@pytest.mark.asyncio
async def test_get_order_book(success_order_book_response):
    requester = FakeHTTPRequester(success_order_book_response)
    sut = GateIO(requester)
    order_book = await sut.get_order_book("BTC_USDT")

    assert order_book.symbol == "BTC_USDT"
    assert order_book.timestamp == 1623898993123
    assert order_book.items[0].ask_price == 1.52
    assert order_book.items[0].ask_quantity == 1.151
    assert order_book.items[0].bid_price == 1.17
    assert order_book.items[0].bid_quantity == 201.863

    assert order_book.items[1].ask_price == 1.53
    assert order_book.items[1].ask_quantity == 1.218
    assert order_book.items[1].bid_price == 1.16
    assert order_book.items[1].bid_quantity == 725.464


@pytest.mark.asyncio
async def test_place_order(success_place_order_response):
    requester = FakeHTTPRequester(success_place_order_response)
    sut = GateIO(requester)
    order = await sut.place_order("BTC_USDT", "bid", 0.001, 65000)

    assert order.order_id == "1852454420"
    assert order.side == "bid"
    assert order.amount == 0.001
    assert order.price == 65000
    assert order.order_type == "limit"
    assert order.status == "done"


@pytest.mark.asyncio
async def test_cancel_order(success_cancel_order_response):
    requester = FakeHTTPRequester(success_cancel_order_response)
    sut = GateIO(requester)
    result = await sut.cancel_order("1852454420", "BTC_USDT")

    assert result is True
