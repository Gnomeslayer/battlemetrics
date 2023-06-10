import utility
from datetime import datetime, timedelta


class Player:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def player_identifiers(self, player_id: int) -> dict:
        """Get player identifiers and related players and identifiers.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-relatedIdentifier-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/related-identifiers

        Args:
            player_id (int): The player battlemetrics Identifier.

        Returns:
            dict: Players related identifiers.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/related-identifiers"

        data = {
            "include": "player,identifier",
            "page[size]": "100"
        }

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

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

        data = {
            "page[size]": "100",
            "filter[servers]": filter_servers,
            "filter[online]": str(filter_online).lower(),
            "filter[organization]": filter_organization,
            "filter[public]": str(filter_public).lower(),
            "include": "identifiers"
        }
        if search:
            data["filter[search]"] = search

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def player_info(self, identifier: int) -> dict:
        """Retrieves the battlemetrics player information.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-player-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}

        Args:
            identifier (int): The Battlemetrics ID of the targeted player.

        Returns:
            dict: Returns everything you can view in a DICT form.
        """
        url = f"{self.base_url}/players/{identifier}"

        data = {
            "include": "identifier,server,playerCounter,playerFlag,flagPlayer"
        }

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def player_play_history(self, player_id: int, server_id: int, start_time: str = None, end_time: str = None) -> dict:
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

        data = {
            "start": start_time,
            "stop": end_time
        }

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

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

        return await utility._make_request(headers=self.headers, method="GET", url=url)

    async def player_match_identifiers(self, identifier: str, type: str = None) -> dict:
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

        data = {
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

        return await utility._make_request(headers=self.headers, method="POST", url=url, data=data)

    async def player_session_history(self, player_id: int, filter_server: str = None, filter_organization: str = None) -> dict:
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
        data = {
            "include": "identifier,server",
            "page[size]": "100"
        }

        if filter_server:
            data["filter[servers]"] = filter_server
        if filter_organization:
            data["filter[organization]"] = filter_organization

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def player_flag_add(self, player_id: int, flag_id: str = None) -> dict:
        """Creates or adds a flag to the targeted players profile.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-flagPlayer-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/flags

        Args:
            player_id (int): Battlemetrics ID of the player.
            flag_id (str, optional): An existing flag ID. Defaults to None.

        Returns:
            dict: Player profile relating to the new flag.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/flags"
        data = {
            "data": [
                {
                    "type": "payerFlag"
                }
            ]
        }
        if flag_id:
            data['data'][0]['id'] = flag_id

        return await utility._make_request(headers=self.headers, method="POST", url=url, data=data)

    async def player_flag_info(self, player_id: int) -> dict:
        """Returns all the flags on a players profile

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-flagPlayer-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/flags

        Args:
            player_id (int): Battlemetrics ID of the targeted player.

        Returns:
            dict: The profile with all the flags.
        """

        data = {
            "page[size]": "100",
            "include": "playerFlag"
        }
        url = f"{self.base_url}/players/{player_id}/relationships/flags"

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def player_flag_delete(self, player_id: int, flag_id: str) -> dict:
        """Deletes a targeted flag from a targeted player ID

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-flagPlayer-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/flags/{(%23%2Fdefinitions%2FplayerFlag%2Fdefinitions%2Fidentity)}

        Args:
            player_id (int): Battlemetrics ID of the player.
            flag_id (str): FLAG ID

        Returns:
            dict: If you were successful or not.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/flags/{flag_id}"

        return await utility._make_request(headers=self.headers, method="DELETE", url=url)

    async def player_coplay_info(self, player_id: int, time_start: str = None, time_end: str = None, player_names: str = None, organization_names: str = None, server_names: str = None) -> dict:
        """Gets the coplay data related to the targeted player

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-coplayRelation-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/coplay

        Args:
            player_id (int): The BATTLEMETRICS id of the targeted player
            time_start (str): UTC time start. Defaults to 7 days ago
            time_end (str): UTC time ends. Defaults to day.
            player_names (str, optional): Player names to target. Defaults to None.
            organization_names (str, optional): Specific Organizations. Defaults to None.
            server_names (str, optional): Specific servers. Defaults to None.

        Returns:
            dict: A dictionary response of all the coplay users.
        """

        if not time_start:
            now = datetime.utcnow()
            time_start = now - timedelta(days=1)
            time_start = time_start.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not time_end:
            time_end = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = {
            "filter[period]": f"{time_start}:{time_end}",
            "page[size]": "100",
            "fields[coplayrelation]": "name,duration"
        }

        if player_names:
            data["filter[players]"] = player_names
        if organization_names:
            data["filter[organizations]"] = organization_names
        if server_names:
            data["filter[servers]"] = server_names

        url = f"{self.base_url}/players/{player_id}/relationships/coplay"

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)
