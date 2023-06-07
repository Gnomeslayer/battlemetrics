import utility


class Playernote:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def create(self, note: str, shared: bool, organization_id: int, player_id: int) -> dict:
        """Create a new note

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes

        Args:
            note (str): The note itself.
            shared (bool): Will this be shared or not? (True or False)
            organization_id (int): The organization ID this note belongs to.
            player_id (int): The battlemetrics ID of the player this note is attached to.

        Returns:
            dict: Response from server (was it successful?)
        """

        url = f"{self.base_url}/players/{player_id}/relationships/notes"
        params = {
            "data": {
                "type": "playerNote",
                "attributes": {
                    "note": note,
                    "shared": str(shared).lower(),
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

        return await utility._post_request(url=url, post=params, headers=self.headers)

    async def delete(self, player_id: int, note_id: str) -> dict:
        """Delete an existing note.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes/{(%23%2Fdefinitions%2FplayerNote%2Fdefinitions%2Fidentity)}

        Args:
            player_id (int): The battlemetrics ID of the player the note is attached to.
            note_id (str): The note ID itself.

        Returns:
            dict: Response from server.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/notes/{note_id}"

        return await utility._delete_request(url=url, headers=self.headers)

    async def note_list(self, player_id: int, filter_personal: bool = False) -> dict:
        """List existing note.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes
        Args:
            player_id (int): The battlemetrics ID of the player.
            filter_personal (bool, optional): List only your notes?. Defaults to False.

        Returns:
            dict: List of notes on users profile.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/notes"
        params = {
            "include": "user,organization",
            "page[size]": "100"
        }

        if filter_personal:
            params["filter[personal]"] = str(filter_personal).lower()

        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def note_update(self, player_id: int, note_id: str, note: str, shared: bool, append: bool = False) -> dict:
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

        url = f"{self.base_url}/players/{player_id}/relationships/notes/{note_id}"

        if append:
            existingnote = self.note_info(player_id=player_id, note_id=note_id)
            if existingnote:
                existingnote = existingnote['data']['attributes']['note']
            note = f"{existingnote}\n{note}"
        params = {
            "data": {
                "type": "playerNote",
                "id": "example",
                "attributes": {
                    "note": f"{note}",
                    "shared": f"{str(shared).lower()}"
                }
            }
        }

        return await utility._patch_request(url=url, post=params, headers=self.headers)

    async def note_info(self, player_id: int, note_id: str) -> dict:
        """Info for existing note.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-playerNote-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/notes/{(%23%2Fdefinitions%2FplayerNote%2Fdefinitions%2Fidentity)}

        Args:
            player_id (int): The battlemetrics ID of the user.
            note_id (str): The ID of the note.

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/notes/{note_id}"

        return await utility._get_request(url=url, headers=self.headers)
