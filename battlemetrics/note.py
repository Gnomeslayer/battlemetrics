from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from . import utils

if TYPE_CHECKING:
    from .state import ConnectionState

__all__ = ("Note",)


# TODO: Add type hint for data.
class Note:
    """Represents a note on a player."""

    def __init__(self, *, data: dict[str, Any], state: ConnectionState) -> None:
        self.state = state

        self._data = data.get("data")
        self._attributes = self._data.get("attributes")
        self._relationships = self._data.get("relationships")

    def __str__(self) -> str:
        """Return when the string method is ran on this Note."""
        return self.content

    @property
    def id(self) -> str:
        """Return the ID of the note."""
        return self._data.get("id")

    @property
    def clearancelevel(self) -> int:
        """Return the clearance level of the note."""
        return self._attributes.get("clearanceLevel")

    @property
    def created_at(self) -> datetime:
        """Return the date the note was created.

        Returns
        -------
        datetime:
            The date the note was created in the UTC timezone.
        """
        created = self._attributes.get("createdAt")
        return datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)

    @property
    def expires_at(self) -> datetime | None:
        """Return the date the note expires.

        Returns
        -------
        datetime | None:
            The date the note expires in the UTC timezone. Could not be specified..
        """
        expires = self._attributes.get("expiresAt")
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
        return utils.remove_html_tags(self._attributes.get("note"))

    @property
    def content_html(self) -> str:
        """Return the note in it's original HTML format.

        Returns
        -------
        str:
            The note.
        """
        return self._attributes.get("note")

    @property
    def shared(self) -> bool:
        """Return whether the note is shared.

        Returns
        -------
        bool:
            Whether the note is shared.
        """
        return self._attributes.get("shared")

    # TODO: Add organization property.
    @property
    def organization(self) -> dict[str, Any]:
        """Return the organization that created the note.

        Returns
        -------
        dict:
            The organization that created the note.
        """
        if org := self._relationships.get("organization"):
            return org.get("data")

        return None

    # TODO: Add player property
    @property
    def player(self) -> dict[str, Any]:
        """Return the player that the note is about.

        Returns
        -------
        dict:
            The player that the note is about.
        """
        if player := self._relationships.get("player"):
            return player.get("data")

        return None

    # TODO: Add user property
    @property
    def user(self) -> dict[str, Any]:
        """Return the user that created the note.

        Returns
        -------
        dict:
            The user that created the note.
        """
        if user := self._relationships.get("user"):
            return user.get("data")

        return None
