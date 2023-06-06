import utility


class Relatedplayeridentifier:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, player_id: int) -> dict:
        """Get player identifiers and related players and identifiers.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-relatedIdentifier-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/related-identifiers

        Args:
            player_id (int): The player battlemetrics Identifier.

        Returns:
            dict: Players related identifiers.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/related-identifiers"

        params = {
            "include": "player,identifier",
            "page[size]": "100"
        }

        return await utility._get_request(url=url, params=params, headers=self.headers)
