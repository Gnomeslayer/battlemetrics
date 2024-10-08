class Session:
    """A class to represent the Session component of the BattleMetrics API."""

    def __init__(self, base_url: str, helpers) -> None:
        self.helpers = helpers
        self.base_url = base_url

    async def info(
        self,
        filter_server: int | None = None,
        filter_game: str | None = None,
        filter_organizations: int | None = None,
        filter_player: int | None = None,
        filter_identifiers: int | None = None,
    ) -> dict:
        """Return the session information for the targeted server, game or organization.

        Parameters
        ----------
            server (int, optional): Targeted server. Defaults to None.
            game (str, optional): Targeted game. Defaults to None.
            organizations (int, optional): Targeted Organization. Defaults to None.
            player (int, optional): Targeted player. Defaults to None.
            identifiers (int, optional): Targeted identifiers. Defaults to None.

        Returns
        -------
            dict: Session information.
        """
        url = f"{self.base_url}/sessions"
        data = {
            "include": "identifier,server,player",
            "page[size]": "100",
        }
        if filter_server:
            data["filter[servers]"] = filter_server
        if filter_game:
            data["filter[game]"] = filter_game
        if filter_organizations:
            data["filter[organizations]"] = filter_organizations
        if filter_player:
            data["filter[players]"] = filter_player
        if filter_identifiers:
            data["filter[identifiers]"] = filter_identifiers
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def coplay(self, sessionid: str) -> dict:
        """Return a list of sessions that were active during the same time as the provided ID.

        Parameters
        ----------
            sessionid (str): The session ID you want to lookup

        Returns
        -------
            dict: A dictionary response from the server.
        """
        url = f"{self.base_url}/sessions/{sessionid}/relationships/coplay"
        data = {
            "include": "identifier,server,player",
            "page[size]": "99",
        }
        return await self.helpers._make_request(method="GET", url=url, params=data)
