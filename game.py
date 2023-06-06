import utility


class Game:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, game: str = None) -> dict:
        """Lists all the games Battlemetrics can view.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-game-/games

        Args:
            game (str, optional): Refine it to a specific game. Or leave as none.

        Returns:
            dict: Games information!
        """

        params = {
            "page[size]": "100"
        }
        if game:
            params['fields[game]'] = game
        url = f"{self.base_url}/games"
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def info(self, game_id: str, game: str = None) -> dict:
        """Gets information on a specific game.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-game-/games/{(%23%2Fdefinitions%2Fgame%2Fdefinitions%2Fidentity)}

        Args:
            game_id (str): The ID of a specific game.
            game (str, optional): Limit it to a specific game, or leave as none.

        Returns:
            dict: Game information.
        """
        params = {
            "page[size]": "100"
        }
        if game:
            params['fields[game]'] = game

        url = f"{self.base_url}/games/{game_id}"
        return await utility._get_request(url=url, headers=self.headers, params=params)
