import asyncio
from logging import getLogger
from typing import Any, ClassVar

import aiohttp
import yarl

from battlemetrics.errors import HTTPException

_log = getLogger(__name__)

SUCCESS_STATUS = [200, 201]


async def json_or_text(
    response: aiohttp.ClientResponse,
) -> dict[str, Any] | list[dict[str, Any]] | str:
    """
    Process an `aiohttp.ClientResponse` to return either a JSON object or raw text.

    This function attempts to parse the response as JSON. If the content type of the response is not
    application/json or parsing fails, it falls back to returning the raw text of the response.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        The response object to process.

    Returns
    -------
    dict[str, t.Any] | list[dict[str, t.Any]] | str
        The parsed JSON object as a dictionary or list of dictionaries, or the raw response text.
    """
    try:
        if "application/json" in response.headers["content-type"].lower():
            return await response.json()
    except KeyError:
        # Thanks Cloudflare
        pass

    return await response.text(encoding="utf-8")


class Route:
    """Represents a route for the BattleMetrics API.

    This method requires either one of path or url.

    Parameters
    ----------
    method : str
        The HTTP method for the route.
    path : str
        The path for the route.
    url : str
        The URL for the route.
    parameters : int | str | bool
        Optional parameters for the route.
    """

    BASE: ClassVar[str] = "https://api.battlemetrics.com"

    def __init__(
        self,
        method: str,
        path: str | None = None,
        url: str | None = None,
        **parameters: int | str | bool,
    ) -> None:
        if not path and not url:
            msg = "Either path or url must be provided."
            raise ValueError(msg)
        if path and url:
            msg = "Only one of path or url can be provided."
            raise ValueError(msg)

        self.endpoint: str = self.BASE + path if path else url
        self.method: str = method
        url = yarl.URL(self.endpoint)
        if parameters:
            url = url.update_query(**parameters)
        self.url: str = url.human_repr()


class HTTPClient:
    """Represent an HTTP Client used for making requests to APIs."""

    def __init__(
        self,
        api_key: str,
        connector: aiohttp.BaseConnector | None = None,
        *,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.connector = connector

        self.__session: aiohttp.ClientSession = None  # type: ignore[reportAttributeAccessIssue]

        self.api_key: str = api_key

        self.ensure_session()

    def ensure_session(self) -> None:
        """
        Ensure that an :class:`aiohttp.ClientSession` is created and open.

        If a session does not exist, this method creates a new :class:`aiohttp.ClientSession`
        using the provided connector and loop.
        """
        if not self.__session or self.__session.closed:
            self.__session = aiohttp.ClientSession(connector=self.connector)

    async def close(self) -> None:
        """Close the :class:`aiohttp.ClientSession` if it exists and is open."""
        if self.__session:
            await self.__session.close()

    async def request(
        self,
        route: Route,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> dict[str, Any] | list[dict[str, Any]] | str:
        """
        Send a request to the specified route and returns the response.

        This method constructs and sends an HTTP request based on the specified route and headers.
        It processes the response to return JSON data or raw text, handling errors as needed.

        Parameters
        ----------
        route : Route
            The route object containing the method and URL for the request.
        headers : dict[str, str] | None, optional
            Optional headers to include with the request. Defaults to None.

        Returns
        -------
        dict[str, t.Any] | list[dict[str, t.Any]] | str
            The response data as a parsed JSON object or list, or raw text if JSON parsing is
            not applicable.

        Raises
        ------
        errors.GeneralHTTPError
            Will raise if the request fails or the response indicates an error.
        """
        self.ensure_session()

        method = route.method
        url = route.url

        _headers = {"Accept": "application/json"}

        headers = headers.update(**_headers) if headers else _headers

        # TODO: Add a check for the api key.
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with self.__session.request(method, url, headers=headers, **kwargs) as response:
            _log.debug(f"{method} {url} returned {response.status}")

            # errors typically have text involved, so this should be safe 99.5% of the time.
            data = await json_or_text(response)
            _log.debug(f"{method} {url} has received {data}")

            await self.close()

            if response.status in SUCCESS_STATUS:
                return data

            raise HTTPException(response, data)
