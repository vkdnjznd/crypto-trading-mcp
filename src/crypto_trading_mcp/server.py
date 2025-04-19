import logging
import time
import asyncio

from typing import Optional, Literal, Callable
from functools import wraps
from fastmcp import FastMCP

from crypto_trading_mcp.exchanges.factory import get_factory, factories
from crypto_trading_mcp.exceptions import CryptoAPIException


def envelope(func: Callable) -> Callable:
    @wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            data = await func(*args, **kwargs)
            return {
                "success": True,
                "code": "200",
                "message": "OK",
                "data": data,
                "timestamp": int(time.time() * 1000),
            }
        except CryptoAPIException as e:
            return e
        except Exception as e:
            raise e

    return wrapped


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastMCP("CryptoTrading", debug=True)


@app.prompt()
async def get_exchange_names():
    return f"Available exchange names: {', '.join(factories.keys())}"


@app.tool()
@envelope
async def get_symbols(exchange_name: str):
    """
    Get all Crypto Symbols

    This function retrieves all available trading pairs from the exchange.
    The response includes market information that can be used to query current prices
    for specific trading pairs. Each market represents a trading pair that can be
    used to get current price information.

    Args:
        exchange_name: str - The name of the exchange to get symbols from
    """
    return await get_factory(exchange_name).create_exchange().get_symbols()


@app.tool()
@envelope
async def get_balances(exchange_name: str):
    """
    Get all Crypto Balances

    This function retrieves all available balances from the exchange.
    The response includes balance information that can be used to query current prices
    for specific trading pairs. Each market represents a trading pair that can be
    used to get current price information.

    Args:
        exchange_name: str - The name of the exchange to get balances from
    """
    return await get_factory(exchange_name).create_exchange().get_balances()


@app.tool()
@envelope
async def get_tickers(exchange_name: str, symbol: str):
    """
    Get current price information for a specific trading pair

    The symbol parameter should be a valid trading pair code obtained from the get_markets function.
    For example, if get_markets returns "KRW-BTC", you can use that as the symbol to get
    the current price information for Bitcoin in Korean Won.

    Args:
        exchange_name: str - The name of the exchange to get tickers from
        symbol: str - The trading pair symbol (e.g., 'BTC-USDT')
    """
    return await get_factory(exchange_name).create_exchange().get_tickers(symbol)


@app.tool()
@envelope
async def get_order_detail(exchange_name: str, order_id: str, symbol: str):
    """
    Get order detail by order id

    This function retrieves the details of a specific order by its order ID.
    It provides comprehensive information about the order, including the order ID,
    the trading pair, the side of the order, the amount, the price, the order type,
    the status, the executed volume, the remaining volume, and the creation time.

    Args:
        exchange_name: str - The name of the exchange to get order details from
        order_id: str - The order id of the order to get details for
        symbol: str - The trading pair symbol (e.g., 'BTC-USDT')
    """
    return (
        await get_factory(exchange_name).create_exchange().get_order(order_id, symbol)
    )


@app.tool()
@envelope
async def get_open_orders(
    exchange_name: str,
    symbol: str,
    page: int,  # page number (starting from 1)
    limit: int,  # number of orders per page (max 100)
    order_by: str = "desc",  # order creation time sorting direction ('asc' for oldest first, 'desc' for newest first)
):
    """
    Retrieve all waiting or reserved orders for a given trading pair

    This function retrieves the open order history for a specific trading pair from the exchange,
    allowing you to check the prices and timestamps of waiting or reserved orders for a given asset.

    It supports pagination (using integer values for page and limit parameters),
    and sorting by creation time.
    The response includes detailed information about each order, such as order ID,
    creation time, price, amount, and order status.

    Args:
        exchange_name: str - The name of the exchange to get open orders from
        symbol: str - The trading pair symbol (e.g., 'BTC-USDT')
        page: int - The page number (starting from 1)
        limit: int - The number of orders per page (max 100)
        order_by: str = "desc" - Order creation time sorting direction ('asc' for oldest first, 'desc' for newest first)
    """
    return (
        await get_factory(exchange_name)
        .create_exchange()
        .get_open_orders(symbol, page, limit, order_by)
    )


@app.tool()
@envelope
async def get_closed_orders(
    exchange_name: str,
    symbol: str,
    page: int,  # page number (starting from 1)
    limit: int,  # number of orders per page (max 100)
    order_by: str = "desc",
    status: Optional[Literal["done", "cancel"]] = None,
    start_date: Optional[int] = None,
    end_date: Optional[int] = None,
):
    """
    Retrieve all closed orders for a given trading pair

    This function retrieves the closed order history for a specific trading pair from the exchange,
    allowing you to check the prices and timestamps of executed orders for a given asset.

    It supports pagination (using integer values for page and limit parameters),
    and sorting by creation time.

    Args:
        exchange_name: str - The name of the exchange to get closed orders from
        symbol: str - The trading pair symbol (e.g., 'BTC-USDT')
        page: int - The page number (starting from 1)
        limit: int - The number of orders per page (max 100)
        order_by: str = "desc" - Order creation time sorting direction ('asc' for oldest first, 'desc' for newest first)
        status: Optional[Literal["done", "cancel"]] = None - The status of the order ('done' for completed, 'cancel' for canceled)
        start_date: Optional[int] = None - The start date of the order (timestamp milliseconds)
        end_date: Optional[int] = None - The end date of the order (timestamp milliseconds)
    """
    return (
        await get_factory(exchange_name)
        .create_exchange()
        .get_closed_orders(symbol, page, limit, status, start_date, end_date, order_by)
    )


@app.tool()
@envelope
async def get_order_book(exchange_name: str, symbol: str):
    """
    Get order book by symbol

    This function retrieves the order book for a specific trading pair from the exchange.
    It provides comprehensive information about the order book, including the order ID,
    the trading pair, the side of the order, the amount, the price, the order type,
    the status, the executed volume, the remaining volume, and the creation time.

    Args:
        exchange_name: str - The name of the exchange to get order book from
        symbol: str - The trading pair symbol (e.g., 'BTC-USDT')
    """
    return await get_factory(exchange_name).create_exchange().get_order_book(symbol)


@app.tool()
@envelope
async def place_order(
    exchange_name: str,
    symbol: str,
    side: str,
    amount: float,
    price: float,
    order_type: Literal["limit", "market"] = "limit",
):
    """
    Place an order

    This function places an order on the exchange.
    It supports both limit and market orders.
    The order type can be specified as either "limit" or "market".
    The side of the order can be specified as either "bid" for buy or "ask" for sell.
    The amount and price parameters are required for both limit and market orders.
    The order type can be specified as either "limit" or "market".

    Args:
        exchange_name: str - The name of the exchange to place an order on
        symbol: str - The trading pair symbol (e.g., 'BTC-USDT')
        side: str - The side of the order ('bid' for buy, 'ask' for sell)
        amount: float - The amount of the order
        price: float - The price of the order
        order_type: Literal["limit", "market"] - Requires one of two values: "limit" for limit order or "market" for market order. Defaults to "limit".
    """
    return (
        await get_factory(exchange_name)
        .create_exchange()
        .place_order(symbol, side, amount, price, order_type)
    )


@app.tool()
@envelope
async def cancel_order(exchange_name: str, order_id: str, symbol: str):
    """
    Cancel an order

    This function cancels an order on the exchange.
    It requires an order ID as input.

    Args:
        exchange_name: str - The name of the exchange to cancel an order on
        order_id: str - The order id of the order to cancel
        symbol: str - The trading pair symbol (e.g., 'BTC-USDT')
    """
    return (
        await get_factory(exchange_name)
        .create_exchange()
        .cancel_order(order_id, symbol)
    )


if __name__ == "__main__":
    logger.info("Starting server")

    asyncio.run(app.run("sse"), debug=True)
