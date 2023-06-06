import utility


class Session:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def info(self, filter_server: int = None, filter_game: str = None, filter_organizations: int = None, filter_player: int = None, filter_identifiers: int = None) -> dict:
        """Returns the session information for the targeted server, game or organization.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-session-/sessions

        Args:
            server (int, optional): Targeted server. Defaults to None.
            game (str, optional): Targeted game. Defaults to None.
            organizations (int, optional): Targeted Organization. Defaults to None.
            player (int, optional): Targeted player. Defaults to None.
            identifiers (int, optional): Targeted identifiers. Defaults to None.

        Returns:
            dict: Session information.
        """

        url = f"{self.base_url}/sessions"

        params = {
            "include": "identifier,server,player",
            "page[size]": "100"
        }

        if filter_server:
            params["filter[servers]"] = filter_server
        if filter_game:
            params["filter[game]"] = filter_game
        if filter_organizations:
            params["filter[organizations]"] = filter_organizations
        if filter_player:
            params["filter[players]"] = filter_player
        if filter_identifiers:
            params["filter[identifiers]"] = filter_identifiers

        return await utility._get_request(url=url, haders=self.headers, params=params)

    async def coplay(self, sessionid: str) -> dict:
        """Returns a list of sessions that were active during the same time as the provided session id.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-session-/sessions/{(%23%2Fdefinitions%2Fsession%2Fdefinitions%2Fidentity)}/relationships/coplay

        Args:
            sessionid (str): The session ID you want to lookup

        Returns:
            dict: A dictionary response from the server.
        """

        url = f"{self.base_url}/sessions/{sessionid}/relationships/coplay"

        params = {
            "include": "identifier,server,player",
            "page[size]": "100"
        }

        return await utility._get_request(url=url, haders=self.headers, params=params)
