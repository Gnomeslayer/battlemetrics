# TODO: Better docstring
class GameInfo:
    """The game info class to handle all the game requests."""

    def __init__(self, helpers, base_url: str) -> None:
        self.helpers = helpers
        self.base_url = base_url

    async def features(self, game: str | None = None) -> dict:
        """List the game features for the specified game.

        Parameters
        ----------
            game (str, optional): _description_. Defaults to None.

        Returns
        -------
            dict: Returns a dictionary of the game features.
        """
        data = {
            "page[size]": "100",
        }
        if game:
            data["filter[game]"] = game
        url = f"{self.base_url}/game-features"
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def feature_options(self, feature_id: str, sort: str = "players") -> dict:
        """Get the game feature options.

        Parameters
        ----------
            feature_id (str): The ID of the game Feature.
            sort (str, optional): Takes "count" and "players". Defaults to "players".

        Returns
        -------
            dict: Game feature options
        """
        data = {
            "page[size]": "100",
            "sort": sort,
        }
        url = f"{self.base_url}/game-features/{feature_id}/relationships/options"
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def list(self, game: str | None = None) -> dict:
        """List all the games Battlemetrics can view.

        Parameters
        ----------
            game (str, optional): Refine it to a specific game. Or leave as none.

        Returns
        -------
            dict: Games information!
        """
        data = {
            "page[size]": "100",
        }
        if game:
            data["fields[game]"] = game
        url = f"{self.base_url}/games"
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def info(self, game_id: str, game: str | None = None) -> dict:
        """Get information on a specific game.

        Parameters
        ----------
            game_id (str): The ID of a specific game.
            game (str, optional): Limit it to a specific game, or leave as none.

        Returns
        -------
            dict: Game information.
        """
        data = {
            "page[size]": "100",
        }
        if game:
            data["fields[game]"] = game
        url = f"{self.base_url}/games/{game_id}"
        return await self.helpers._make_request(method="GET", url=url, params=data)
