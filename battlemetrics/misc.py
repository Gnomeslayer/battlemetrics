from typing import NamedTuple

__all__ = ("APIScopes",)


class APIScopes(NamedTuple):
    """All types for the function check_api_scopes."""

    active: bool
    scopes: list[str]
    client_id: str
    token_type: str
