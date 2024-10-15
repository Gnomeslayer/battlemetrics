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

    async def delete_note(self, player_id: int, note_id: str) -> None:
        """Delete an existing note.

        Parameters
        ----------
            player_id (int): The battlemetrics ID of the player the note is attached to.
            note_id (str): The note's ID

        Returns
        -------
            dict: Response from server.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/notes/{note_id}"
        await self.http.request(
            Route(
                method="DELETE",
                url=url,
            ),
        )

    async def update_note(
        self,
        player_id: int,
        note_id: str,
        *,
        content: str,
        clearancelevel: int | None = None,
        shared: bool = True,
        append: bool | None = False,
    ) -> Note:
        """Update an existing note.

        Parameters
        ----------
            player_id (int): The battlemetrics ID of the user.
            note_id (str): The ID of the note.
            content (str): The new content of the note.
            clearancelevel (int): The new clearance level of the note.
            shared (bool): Whether this note should be shared.
            append (bool): Whether to append the new content to the existing note.

        Returns
        -------
            dict: Response from server.
        """
        if existing := await self.get_note(player_id=player_id, note_id=note_id):
            existing_content = existing.content
        else:
            msg = "Note does not exist."
            raise ValueError(msg)

        url = f"{self.base_url}/players/{player_id}/relationships/notes/{note_id}"

        content = f"{existing_content}\n{content}" if append else content

        data = {
            "data": {
                "type": "playerNote",
                "id": "example",
                "attributes": {
                    "clearanceLevel": f"{clearancelevel}",
                    "note": f"{content}",
                    "shared": f"{str(shared).lower()}",
                },
            },
        }

        result = await self.http.request(
            Route(
                method="PATCH",
                url=url,
            ),
            json_dict=data,
        )
        return Note(data=result, state=self)
