import utility


class Gamefeatureoptions:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, feature_id: str, sort: str = "players") -> dict:
        """Gets the game feature options.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-gameFeatureOption-/game-features/{(%23%2Fdefinitions%2FgameFeature%2Fdefinitions%2Fidentity)}/relationships/options

        Args:
            feature_id (str): The ID of the game Feature.
            sort (str, optional): Takes "count" and "players". Defaults to "players".

        Returns:
            dict: Game feature options
        """
        params = {
            "page[size]": "100",
            "sort": sort
        }

        url = f"{self.base_url}/game-features/{feature_id}/relationships/options"
        return await utility._get_request(url=url, headers=self.headers, params=params)
