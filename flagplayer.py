import utility


class Flagplayer:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def create(self, player_id: int, flag_id: str = None) -> dict:
        """Creates or adds a flag to the targeted players profile.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-flagPlayer-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/flags

        Args:
            player_id (int): Battlemetrics ID of the player.
            flag_id (str, optional): An existing flag ID. Defaults to None.

        Returns:
            dict: Player profile relating to the new flag.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/flags"
        json_post = {
            "data": [
                {
                    "type": "payerFlag"
                }
            ]
        }
        if flag_id:
            json_post['data'][0]['id'] = flag_id

        return await utility._post_request(url=url, post=json_post, headers=self.headers)

    async def get(self, player_id: int) -> dict:
        """Returns all the flags on a players profile

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-flagPlayer-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/flags

        Args:
            player_id (int): Battlemetrics ID of the targeted player.

        Returns:
            dict: The profile with all the flags.
        """

        params = {
            "page[size]": "100",
            "include": "playerFlag"
        }
        url = f"{self.base_url}/players/{player_id}/relationships/flags"
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def delete(self, player_id: int, flag_id: str) -> dict:
        """Deletes a targeted flag from a targeted player ID

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-flagPlayer-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/flags/{(%23%2Fdefinitions%2FplayerFlag%2Fdefinitions%2Fidentity)}

        Args:
            player_id (int): Battlemetrics ID of the player.
            flag_id (str): FLAG ID

        Returns:
            dict: If you were successful or not.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/flags/{flag_id}"
        return await utility._delete_request(url=url, headers=self.headers)
