from typing import Any

from aiohttp import ClientResponse
from requests import Response

_ResponseType = ClientResponse | Response


class BMException(Exception):
    """Base exception class for all errors.

    This is used so we can catch any error without catching the BLE001 ruff rule.
    """


# Thanks to https://github.com/DisnakeDev/disnake ❤️
def _flatten_error_dict(d: dict[str, Any], key: str = "") -> dict[str, str]:
    items: list[tuple[str, str]] = []
    for k, v in d.items():
        new_key = f"{key}.{k}" if key else k

        if isinstance(v, dict):
            try:
                _errors: list[dict[str, Any]] = v["_errors"]
            except KeyError:
                items.extend(_flatten_error_dict(v, new_key).items())
            else:
                items.append((new_key, " ".join(x.get("message", "") for x in _errors)))
        else:
            items.append((new_key, v))

    return dict(items)


class HTTPException(BMException):
    """Exception that's raised when an HTTP request operation fails.

    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The response of the failed HTTP request. This is an
        instance of :class:`aiohttp.ClientResponse`. In some cases
        this could also be a :class:`requests.Response`.

    text: :class:`str`
        The text of the error. Could be an empty string.
    status: :class:`int`
        The status code of the HTTP request.
    code: :class:`int`
        The Discord specific error code for the failure.
    """

    def __init__(self, response: _ResponseType, message: str | dict[str, Any] | None) -> None:
        self.response: _ResponseType = response
        self.status: int = response.status
        self.code: int
        self.text: str
        if isinstance(message, dict):
            self.code = message.get("code", 0)
            self.text = message.get("message", "")
        else:
            self.text = message or ""
            self.code = 0

        fmt = "{0.status} {0.reason} (error code: {1})"
        if len(self.text):
            fmt += ": {2}"

        super().__init__(fmt.format(self.response, self.code, self.text))
