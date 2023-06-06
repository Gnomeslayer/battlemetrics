import utility


class Gamefeatures:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, game: str = None) -> dict:
        """Lists the game features for the specified game

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-gameFeature-/game-features

        Args:
            game (str, optional): _description_. Defaults to None.

        Returns:
            dict: Returns a dictionary of the game features.
        """
        params = {
            "page[size]": "100"
        }
        if game:
            params['filter[game]'] = game
        url = f"{self.base_url}/game-features"
        await utility._get_request(url=url, headers=self.headers, params=params)
