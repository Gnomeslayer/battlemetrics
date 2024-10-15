from typing import NamedTuple

__all__ = (
    "NoteAttributes",
    "NoteRelationships",
    "Note",
)


class NoteAttributes(NamedTuple):
    """Attributes of a Note.

    Attributes
    ----------
    clearancelevel: int
        The clearance level of the note.
    createdat: str
        The date the note was created.
    expiresat: str
        The date the note expires.
    note: str
        The content of the note in HTML format.
    shared: bool
        Whether the note is shared.
    """

    clearancelevel: int
    createdat: str
    expiresat: str
    note: str
    shared: bool


class NoteRelationships(NamedTuple):
    """Relationships of a Note.

    Attributes
    ----------
    organization_id: int
        The ID of the organization where this note is stored.
    player_id: int
        The ID of the player this note is about.
    user_id: int
        The ID of the user who created this note.
    """

    organization_id: int
    player_id: int
    user_id: int


class Note(NamedTuple):
    """Basic Note Data.

    Attributes
    ----------
    id: int
        The ID of the note.
    attributes: NoteAttributes
        The attributes of the note.
    relationships: NoteRelationships
        The relationships of the note.
    """

    id: int
    type: str
    attributes: NoteAttributes
    relationships: NoteRelationships
