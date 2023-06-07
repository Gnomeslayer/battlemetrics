import utility
from datetime import datetime, timedelta


class Player:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def player_list(self, search: str = None, filter_online: bool = True, filter_servers: int = None, filter_organization: int = None, filter_public: bool = False) -> dict:
        """Grabs a list of players based on the filters provided. For accurate information, filter by server or organization.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-player-/players

        Args:
            search (str, optional): Search for specific player. Defaults to None.
            filter_online (bool, optional): Online or offline players. Defaults to True.
            filter_servers (int, optional): Server IDs, comma separated. Defaults to None.
            filter_organization (int, optional): Organization ID. Defaults to None.
            filter_public (bool, optional): Public or private results? (RCON or Not). Defaults to False.

        Returns:
            dict: A dictionary response of all the players.
        """
        url = f"{self.base_url}/players"

        params = {
            "page[size]": "100",
            "filter[servers]": filter_servers,
            "filter[online]": str(filter_online).lower(),
            "filter[organization]": filter_organization,
            "filter[public]": str(filter_public).lower(),
            "include": "identifiers"
        }
        if search:
            params["filter[search]"] = search
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def get(self, identifier: int) -> dict:
        """Retrieves the battlemetrics player information.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-player-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}

        Args:
            identifier (int): The Battlemetrics ID of the targeted player.

        Returns:
            dict: Returns everything you can view in a DICT form.
        """
        url = f"{self.base_url}/players/{identifier}"

        params = {
            "include": "identifier,server,playerCounter,playerFlag,flagPlayer"
        }
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def play_time_history(self, player_id: int, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Returns the data we use for rendering time played history charts. Start and stop are truncated to the date.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-player-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/time-played-history/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}

        Args:
            player_id (int): The battlemetrics player ID.
            server_id (int): The server ID
            start_time (str): The UTC start. defaults to 5 days ago.
            end_time (str): The UTC end. Defaults to now.

        Returns:
            dict: Dictionary of Datapoints.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=5)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/players/{player_id}/time-played-history/{server_id}"

        params = {
            "start": start_time,
            "stop": end_time
        }
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def player_server_info(self, player_id: int, server_id: int) -> dict:
        """Returns server specifics for the given player and server.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-player-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}

        Args:
            player_id (int): The battlemetrics player ID.
            server_id (int): The server ID

        Returns:
            dict: Response from the server showing the player server info.
        """

        url = f"{self.base_url}/players/{player_id}/servers/{server_id}"

        return await utility._get_request(url=url, headers=self.headers)

    async def match_identifiers(self, identifier: str, type: str = None) -> dict:
        """Searches for one or more identifiers.
        This API method is only available to authenticated users. It is also rate limited to one request a second.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-player-/players/match

        Args:
            identifier (str): The specific identifier.
            type (str, optional): one of:"steamID" or "BEGUID" or "legacyBEGUID" or "ip" or "name" or "survivorName" or "steamFamilyShareOwner" or "conanCharName" or "egsID" or "funcomID" or "playFabID" or "mcUUID" or "7dtdEOS" or "battlebitHWID"

        Returns:
            dict: Dictionary response of any matches.
        """
        url = f"{self.base_url}/players/match"

        params = {
            "data": [
                {
                    "type": "identifier",
                    "attributes": {
                        "type": f"{type}",
                        "identifier": f"{identifier}"
                    }
                }
            ]
        }

        return await utility._post_request(url=url, post=params, headers=self.headers)

    async def session_history(self, player_id: int, filter_server: str = None, filter_organization: str = None) -> dict:
        """Returns player's session history.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-player-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/sessions

        Args:
            player_id (int): The battlemetrics player id
            filter_server (str, optional): The specific server ID. Defaults to None.
            filter_organization (str, optional): The specific organization ID. Defaults to None.

        Returns:
            dict: Returns a players session history.
        """

        url = f"{self.base_url}/players/{player_id}/relationships/sessions"
        params = {
            "include": "identifier,server",
            "page[size]": "100"
        }

        if filter_server:
            params["filter[servers]"] = filter_server
        if filter_organization:
            params["filter[organization]"] = filter_organization

        return await utility._get_request(url=url, headers=self.headers, params=params)
