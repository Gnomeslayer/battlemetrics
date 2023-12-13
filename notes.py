from helpers import Helpers


class Notes:
    def __init__(self, BASE_URL: str, helpers: Helpers) -> None:
        self.BASE_URL = BASE_URL
        self.helpers = helpers


    async def create(self, note: str, organization_id: int, player_id: int, shared: bool = True) -> dict:
        """Create a new note
        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes
        Args:
            note (str): The note it
            shared (bool): Will this be shared or not? (True or False), default is True
            organization_id (int): The organization ID this note belongs to.
            player_id (int): The battlemetrics ID of the player this note is attached to.
        Returns:
            dict: Response from server (was it successful?)
        """

        url = f"{self.BASE_URL}/players/{player_id}/relationships/notes"
        data = {
            "data": {
                "type": "playerNote",
                "attributes": {
                    "note": note,
                    "shared": shared
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}",
                        }
                    }
                }
            }
        }
        return await self.helpers._make_request(method="POST", url=url, data=data)


    async def delete(self, player_id: int, note_id: str) -> dict:
        """Delete an existing note.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes/{(%23%2Fdefinitions%2FplayerNote%2Fdefinitions%2Fidentity)}
        Args:
            player_id (int): The battlemetrics ID of the player the note is attached to.
            note_id (str): The note ID it
        Returns:
            dict: Response from server.
        """

        url = f"{self.BASE_URL}/players/{player_id}/relationships/notes/{note_id}"
        return await self.helpers._make_request(method="DELETE", url=url)


    async def list(self, player_id: int, filter_personal: bool = False) -> dict:
        """List existing note.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes
        Args:
            player_id (int): The battlemetrics ID of the player.
            filter_personal (bool, optional): List only your notes?. Defaults to False.
        Returns:
            dict: List of notes on users profile.
        """

        url = f"{self.BASE_URL}/players/{player_id}/relationships/notes"
        data = {
            "include": "user,organization",
            "page[size]": "100"
        }
        if filter_personal:
            data["filter[personal]"] = str(filter_personal).lower()
        return await self.helpers._make_request(method="GET", url=url, data=data)


    async def update(self, player_id: int, note_id: str, note: str, shared: bool, append: bool = False) -> dict:
        """Update an existing note.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-PATCH-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes/{(%23%2Fdefinitions%2FplayerNote%2Fdefinitions%2Fidentity)}
        Args:
            player_id (int): The battlemetrics ID of the user.
            note_id (str): The ID of the note.
            note (str): The new note.
            shared (bool): Shared?
        Returns:
            dict: Response from server.
        """

        url = f"{self.BASE_URL}/players/{player_id}/relationships/notes/{note_id}"
        if append:
            existingnote = self.note_info(player_id=player_id, note_id=note_id)
            if existingnote:
                existingnote = existingnote['data']['attributes']['note']
            note = f"{existingnote}\n{note}"
        data = {
            "data": {
                "type": "playerNote",
                "id": "example",
                "attributes": {
                    "note": f"{note}",
                    "shared": f"{str(shared).lower()}"
                }
            }
        }
        return await self.helpers._make_request(method="PATCH", url=url, data=data)


    async def info(self, player_id: int, note_id: str) -> dict:
        """Info for existing note.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes/{(%23%2Fdefinitions%2FplayerNote%2Fdefinitions%2Fidentity)}
        Args:
            player_id (int): The battlemetrics ID of the user.
            note_id (str): The ID of the note.
        Returns:
            dict: Response from the server.
        """

        url = f"{self.BASE_URL}/players/{player_id}/relationships/notes/{note_id}"
        return await self.helpers._make_request(method="GET", url=url)
