import pytest
import httpx


from typing import Literal, Optional
from crypto_trading_mcp.http_handler import HTTPRequester


class FakeHTTPRequester(HTTPRequester):
    def __init__(
        self, fake_response: httpx.Response, authorization: Optional[httpx.Auth] = None
    ):
        self.fake_response = fake_response
        self.authorization = authorization

    async def send(
        self,
        url: str,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> httpx.Response:
        return self.fake_response


@pytest.fixture
def success_response():
    response = httpx.Response(200)
    response._content = b'{"status": "success"}'
    return response


@pytest.fixture
def error_response():
    return httpx.Response(500)


@pytest.mark.asyncio
async def test_send_success(success_response):
    requester = FakeHTTPRequester(success_response)

    response = await requester.send(
        url="https://api.example.com/test",
        method="GET",
        headers={"Content-Type": "application/json"},
    )

    assert response == success_response


@pytest.mark.asyncio
async def test_send_with_json_data(success_response):
    requester = FakeHTTPRequester(success_response)

    response = await requester.send(
        url="https://api.example.com/test",
        method="POST",
        data={"key": "value"},
        headers={"Content-Type": "application/json"},
    )

    assert response == success_response


@pytest.mark.asyncio
async def test_send_error_handling(error_response):
    requester = FakeHTTPRequester(error_response)

    response = await requester.send(
        url="https://api.example.com/test",
        method="GET",
    )

    assert response == error_response
