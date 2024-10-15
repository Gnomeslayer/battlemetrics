from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from . import utils
from .types.note import Note as NotePayload
from .types.note import NoteAttributes, NoteRelationships

if TYPE_CHECKING:
    from .state import ConnectionState

__all__ = ("Note",)


class Note:
    """Represents a note on a player."""

    def __init__(self, *, data: NotePayload, state: ConnectionState) -> None:
        self.state = state
        data = data.get("data")

        self._data: NotePayload = NotePayload(**data)
        self._attributes: NoteAttributes = NoteAttributes(
            clearancelevel=data.get("attributes").get("clearanceLevel"),
            createdat=data.get("attributes").get("createdAt"),
            expiresat=data.get("attributes").get("expiresAt"),
            note=data.get("attributes").get("note"),
            shared=data.get("attributes").get("shared"),
        )
        self._relationships: NoteRelationships = (
            NoteRelationships(
                **utils.format_relationships(self._data.relationships),
            )
            if self._data.relationships
            else None
        )

    def __str__(self) -> str:
        """Return when the string method is ran on this Note."""
        return self.content

    @property
    def id(self) -> str:
        """Return the ID of the note."""
        return self._data.id

    @property
    def clearancelevel(self) -> int:
        """Return the clearance level of the note."""
        return self._attributes.clearancelevel

    @property
    def created_at(self) -> datetime:
        """Return the date the note was created.

        Returns
        -------
        datetime:
            The date the note was created in the UTC timezone.
        """
        created = self._attributes.createdat
        return datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)

    @property
    def expires_at(self) -> datetime | None:
        """Return the date the note expires.

        Returns
        -------
        datetime | None:
            The date the note expires in the UTC timezone. Could not be specified..
        """
        expires = self._attributes.expiresat
        return (
            datetime.strptime(expires, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
            if expires
            else None
        )

    @property
    def content(self) -> str:
        """Return the note in plain text.

        Returns
        -------
        str:
            The note.
        """
        return utils.remove_html_tags(self._attributes.note)

    @property
    def content_html(self) -> str:
        """Return the note in it's original HTML format.

        Returns
        -------
        str:
            The note.
        """
        return self._attributes.note

    @property
    def shared(self) -> bool:
        """Return whether the note is shared.

        Returns
        -------
        bool:
            Whether the note is shared.
        """
        return self._attributes.shared

    # TODO: Add organization property.
    @property
    def organization(self) -> dict[str, Any]:
        """Return the organization that created the note.

        Returns
        -------
        dict:
            The organization that created the note.
        """
        return self._relationships.organization_id if self._relationships else None

    # TODO: Add player property
    @property
    def player(self) -> dict[str, Any]:
        """Return the player that the note is about.

        Returns
        -------
        dict:
            The player that the note is about.
        """
        return self._relationships.player_id if self._relationships else None

    # TODO: Add user property
    @property
    def user(self) -> dict[str, Any]:
        """Return the user that created the note.

        Returns
        -------
        dict:
            The user that created the note.
        """
        return self._relationships.user_id if self._relationships else None
