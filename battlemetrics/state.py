from __future__ import annotations

from typing import TYPE_CHECKING

from .http import HTTPClient, Route
from .note import Note

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

__all__ = ("ConnectionState",)


class ConnectionState:
    """Represents the connection state of the client."""

    def __init__(self, loop: AbstractEventLoop, http: HTTPClient) -> None:
        self.loop = loop
        self.http = http

    async def get_note(self, player_id: int, note_id: int) -> Note:
        """Return a note based on player ID and note ID.

        Parameters
        ----------
        player_id : int
            The ID of the player.
        note_id : int
            The ID of the note.
        """
        url = f"/players/{player_id}/relationships/notes/{note_id}"
        data = await self.http.request(
            Route(
                method="GET",
                path=url,
            ),
        )
        return Note(data=data, state=self)
