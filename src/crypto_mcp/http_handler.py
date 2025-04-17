import httpx

from typing import Literal, Optional, Generator


class HTTPRequester:
    def __init__(self, authorization: Optional[httpx.Auth] = None):
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
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    data=data,
                    json=json,
                    headers=headers,
                    params=params,
                    auth=self.authorization,
                )

                return response
            except httpx.RequestError as e:
                return httpx.Response(
                    status_code=500,
                    content=e.response.content,
                    headers=e.response.headers,
                    request=e.request,
                )

    async def get(
        self, url: str, headers: Optional[dict] = None, params: Optional[dict] = None
    ) -> httpx.Response:
        return await self.send(url, "GET", headers=headers, params=params)

    async def post(
        self,
        url: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> httpx.Response:
        return await self.send(
            url, "POST", data=data, json=json, headers=headers, params=params
        )

    async def put(
        self,
        url: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> httpx.Response:
        return await self.send(
            url, "PUT", data=data, json=json, headers=headers, params=params
        )

    async def delete(
        self, url: str, headers: Optional[dict] = None, params: Optional[dict] = None
    ) -> httpx.Response:
        return await self.send(url, "DELETE", headers=headers, params=params)


class BearerAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request
