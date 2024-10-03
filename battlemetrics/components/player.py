import datetime
import uuid
from datetime import datetime, timedelta

from battlemetrics.components.helpers import Helpers


class Player:
    """Player class to interact with the battlemetrics player API."""

    def __init__(self, helpers: Helpers, base_url: str) -> None:
        self.helpers = helpers
        self.base_url = base_url

    async def identifiers(self, player_id: int) -> dict:
        """Get player identifiers and related players and identifiers.

        Parameters
        ----------
            player_id (int): The player battlemetrics Identifier.

        Returns
        -------
            dict: Players related identifiers.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/related-identifiers"
        data = {
            "include": "player,identifier",
            "page[size]": "100",
        }
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def search(
        self,
        search: str = None,
        filter_game: str = None,
        filter_servers: int = None,
        filter_organization: int = None,
        *,
        filter_online: bool = False,
        filter_public: bool = False,
        flag: str = None,
    ) -> dict:
        """Grab a list of players based on the filters provided. For accurate information, filter by server or organization.

        Parameters
        ----------
            search (str, optional): Search for specific player. Defaults to None.
            filter_online (bool, optional): Online or offline players. Defaults to True.
            filter_servers (int, optional): Server IDs, comma separated. Defaults to None.
            filter_organization (int, optional): Organization ID. Defaults to None.
            filter_public (bool, optional): Public or private results? (RCON or Not). Defaults to False.
            filter_game (str, optional): Filters the results to specific game. Lowercase, case sensitive. Defaults to None.

        Returns
        -------
            dict: A dictionary response of all the players.
        """
        url = f"{self.base_url}/players"
        data = {
            "page[size]": "100",
            "include": "server,identifier,playerFlag,flagPlayer",
        }
        if search:
            data["filter[search]"] = search
        if filter_servers:
            data["filter[server]"] = filter_servers
        if filter_organization:
            data["filter[organization]"] = filter_organization
        if flag:
            data["filter[playerFlags]"] = flag

        if filter_online:
            data["filter[online]"] = "true"
        else:
            data["filter[online]"] = "false"

        if filter_public:
            data["filter[public]"] = "true"
        else:
            data["filter[public]"] = "false"

        if filter_game:
            data["server"]["game"] = filter_game

        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def info(self, identifier: int) -> dict:
        """Retrieve the battlemetrics player information.

        Parameters
        ----------
            identifier (int): The Battlemetrics ID of the targeted player.

        Returns
        -------
            dict: Returns everything you can view in a DICT form.

        """
        url = f"{self.base_url}/players/{identifier}"
        data = {
            "include": "identifier,server,playerCounter,playerFlag,flagPlayer",
        }

        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def play_history(
        self,
        player_id: int,
        server_id: int,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> dict:
        """Return the data we use for rendering time played history charts. Start and stop are truncated to the date.

        Parameters
        ----------
            player_id (int): The battlemetrics player ID.
            server_id (int): The server ID
            start_time (str): The UTC start. defaults to 5 days ago.
            end_time (str): The UTC end. Defaults to now.

        Returns
        -------
            dict: Dictionary of Datapoints.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=5)
            start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        if not end_time:
            # end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            now = datetime.utcnow()
            end_time = now + timedelta(days=1)
            end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        url = f"{self.base_url}/players/{player_id}/time-played-history/{server_id}"
        data = {
            "start": start_time,
            "stop": end_time,
        }
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def server_info(self, player_id: int, server_id: int) -> dict:
        """Return server specifics for the given player and server.

        Parameters
        ----------
            player_id (int): The battlemetrics player ID.
            server_id (int): The server ID
        Returns:
            dict: Response from the server showing the player server info.
        """
        url = f"{self.base_url}/players/{player_id}/servers/{server_id}"
        return await self.helpers._make_request(method="GET", url=url)

    async def match_identifiers(self, identifier: str, identifier_type: str = None) -> dict:
        """Search for one or more identifiers.

        This API method is only available to authenticated users. It is also rate limited to one request a second.

        Parameters
        ----------
            identifier (str): The specific identifier.
            type (str, optional): one of:"steamID" or "BEGUID" or "legacyBEGUID" or "ip" or "name" or "survivorName" or "steamFamilyShareOwner" or "conanCharName" or "egsID" or "funcomID" or "playFabID" or "mcUUID" or "7dtdEOS" or "battlebitHWID"

        Returns
        -------
            dict: Dictionary response of any matches.
        """
        url = (
            f"{self.base_url}/players/match?include=player,server,identifier,playerFlag,flagPlayer"
        )
        data = {
            "data": [
                {
                    "type": "identifier",
                    "attributes": {
                        "type": identifier_type,
                        "identifier": f"{identifier}",
                    },
                },
            ],
        }
        return await self.helpers._make_request(method="POST", url=url, json_dict=data)

    async def session_history(
        self,
        player_id: int,
        filter_server: str | None = None,
        filter_organization: str | None = None,
    ) -> dict:
        """Return player's session history.

        Parameters
        ----------
            player_id (int): The battlemetrics player id
            filter_server (str, optional): The specific server ID. Defaults to None.
            filter_organization (str, optional): The specific organization ID. Defaults to None.

        Returns
        -------
            dict: Returns a players session history.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/sessions"
        data = {
            "include": "identifier,server",
            "page[size]": "100",
        }
        if filter_server:
            data["filter[servers]"] = filter_server
        if filter_organization:
            data["filter[organizations]"] = filter_organization

        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def add_flag(self, player_id: int, flag_id: str = None) -> dict:
        """Create or add a flag to the targeted players profile.

        Parameters
        ----------
            player_id (int): Battlemetrics ID of the player.
            flag_id (str, optional): An existing flag ID. Defaults to None.

        Returns
        -------
            dict: Player profile relating to the new flag.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/flags"
        data = {
            "data": [
                {
                    "type": "playerFlag",
                },
            ],
        }
        if flag_id:
            data["data"][0]["id"] = flag_id

        return await self.helpers._make_request(method="POST", url=url, json_dict=data)

    async def flags(self, player_id: int) -> dict:
        """Return all the flags on a players profile.

        Parameters
        ----------
            player_id (int): Battlemetrics ID of the targeted player.

        Returns
        -------
            dict: The profile with all the flags.
        """
        data = {
            "page[size]": "100",
            "include": "playerFlag",
        }
        url = f"{self.base_url}/players/{player_id}/relationships/flags"
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def delete_flag(self, player_id: int, flag_id: str) -> dict:
        """Delete a targeted flag from a targeted player ID.

        Parameters
        ----------
            player_id (int): Battlemetrics ID of the player.
            flag_id (str): FLAG ID

        Returns
        -------
            dict: If you were successful or not.
        """
        url = f"{self.base_url}/players/{player_id}/relationships/flags/{flag_id}"
        return await self.helpers._make_request(method="DELETE", url=url)

    async def coplay_info(
        self,
        player_id: int,
        time_start: str | None = None,
        time_end: str | None = None,
        player_names: str | None = None,
        organization_names: str | None = None,
        server_names: str | None = None,
    ) -> dict:
        """Get the coplay data related to the targeted player.

        Parameters
        ----------
            player_id (int): The BATTLEMETRICS id of the targeted player
            time_start (str): UTC time start. Defaults to 7 days ago
            time_end (str): UTC time ends. Defaults to day.
            player_names (str, optional): Player names to target. Defaults to None.
            organization_names (str, optional): Specific Organizations. Defaults to None.
            server_names (str, optional): Specific servers. Defaults to None.

        Returns
        -------
            dict: A dictionary response of all the coplay users.
        """
        if not time_start:
            now = datetime.utcnow()
            time_start = now - timedelta(days=1)
            time_start = time_start.strftime("%Y-%m-%dT%H:%M:%SZ")
        if not time_end:
            time_end = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "filter[period]": f"{time_start}:{time_end}",
            "page[size]": "100",
            "fields[coplayrelation]": "name,duration",
        }
        if player_names:
            data["filter[players]"] = player_names
        if organization_names:
            data["filter[organizations]"] = organization_names
        if server_names:
            data["filter[servers]"] = server_names
        url = f"{self.base_url}/players/{player_id}/relationships/coplay"
        return await self.helpers._make_request(method="GET", url=url, params=data)

    # TODO: NEEDS AN ENUM FOR IDENTIFIER TYPES
    async def quick_match(self, identifier: str, identifier_type: str) -> dict:
        """Player Quick Match Identifiers.

        Searches for one or more identifiers.
        This API method is only available to authenticated users. It is also rate limited to 10 requests per second.
        Enterprise users have a higher rate limit of 30 requests per second.
        The servers filter limits which servers you get when including server information, it does not filter players by server.
        Results will be returned sorted by the player's id.

        Parameters
        ----------
            identifier (str): Any identifier associated with the users profile on battlemetrics.
            identifier_type (str): one of:"steamID" or "BEGUID" or "legacyBEGUID" or "ip" or "name" or "survivorName" or "steamFamilyShareOwner" or "conanCharName" or "egsID" or "eosID" or "funcomID" or "playFabID" or "mcUUID" or "7dtdEOS" or "battlebitHWID"

        Returns
        -------
            dict: Returns a dictionary of the matching player(s)
        """
        url = f"{self.base_url}/players/quick-match"
        data = {
            "data": [
                {
                    "type": "identifier",
                    "attributes": {
                        "type": identifier_type,
                        "identifier": f"{identifier}",
                    },
                },
            ],
        }

        return await self.helpers._make_request(method="POST", url=url, json_dict=data)

    # TODO: Deprecated datetime usage
    async def add_ban(
        self,
        reason: str,
        note: str,
        org_id: str,
        banlist: str,
        server_id: str,
        expires: str = "permanent",
        battlemetrics_id: int | None = None,
        steam_id: int | None = None,
        *,
        orgwide: bool = True,
    ) -> dict:
        """Create a ban for the targeted user.

        One of battlemetrics_id or steam_id is required to ban the user.
        By default the ban is set to organization wide.

        Parameters
        ----------
            reason (str): Reason for the ban (This is what the user/server sees)
            note (str): Note attached to the ban (Admins/staff can see this)
            org_id (str): Organization ID the ban is associated to.
            banlist (str): Banlist the ban is associated to.
            server_id (str): Server ID the ban is associated to.
            expires (str, optional): _description_. Defaults to "permanent".
            orgwide (bool, optional): _description_. Defaults to True.
            battlemetrics_id (int, optional): Battlemetrics ID of the banned user.
            steam_id (int, optional): Steam ID of the banned user.

        Returns
        -------
            dict: The results, whether it was successful or not.
        """
        if expires == "permanent":
            expires = None

        if expires:
            expires = await self.helpers.calculate_future_date(expires)

        current_datetime = datetime.now()
        # Not needed.
        # formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = {
            "data": {
                "type": "ban",
                "attributes": {
                    "uid": str(uuid.uuid4())[:14],
                    "reason": reason,
                    "note": note,
                    "expires": expires,
                    "identifiers": [],
                    "orgWide": orgwide,
                    "autoAddEnabled": True,
                    "nativeEnabled": None,
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{org_id}",
                        },
                    },
                    "server": {
                        "data": {
                            "type": "server",
                            "id": f"{server_id}",
                        },
                    },
                    "player": {
                        "data": {
                            "type": "player",
                            "id": f"{battlemetrics_id}",
                        },
                    },
                    "banList": {
                        "data": {
                            "type": "banList",
                            "id": f"{banlist}",
                        },
                    },
                },
            },
        }
        # Grab the complete profile
        if not steam_id and not battlemetrics_id:
            return "Please submit either a STEAM IDENTIFIER or BATTLEMETRICS IDENTIFIER"

        if steam_id and not battlemetrics_id:
            # Grab the battlemetrics identifiers from a steam identifier.
            battlemetrics_identifiers = await self.match_identifiers(
                identifier=steam_id,
                identifier_type="steamID",
            )
            # Grab the complete profile from this user.
            battlemetrics_id = battlemetrics_identifiers["data"][0]["relationships"]["player"][
                "data"
            ]["id"]
        if battlemetrics_id:
            player_info = await self.info(identifier=battlemetrics_id)

        # Grab the battlemetrics ID's for the users BEGUID and STEAMID
        for included in player_info["included"]:
            if included["type"] == "identifier":
                if included["attributes"]["type"] == "BEGUID":
                    data["data"]["attributes"]["identifiers"].append(int(included["id"]))
                if included["attributes"]["type"] == "steamID":
                    data["data"]["attributes"]["identifiers"].append(int(included["id"]))
        url = f"{self.base_url}/bans"
        return await self.helpers._make_request(method="POST", url=url, json_dict=data)

    async def add_note(
        self,
        note: str,
        organization_id: int,
        player_id: int,
        shared: bool = True,
    ) -> dict:
        """Create a new note.

        Parameters
        ----------
            note (str): The note it
            shared (bool): Will this be shared or not? (True or False), default is True
            organization_id (int): The organization ID this note belongs to.
            player_id (int): The battlemetrics ID of the player this note is attached to.

        Returns
        -------
            dict: Response from server (was it successful?)
        """
        url = f"{self.base_url}/players/{player_id}/relationships/notes"
        data = {
            "data": {
                "type": "playerNote",
                "attributes": {
                    "note": note,
                    "shared": shared,
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}",
                        },
                    },
                },
            },
        }
        return await self.helpers._make_request(method="POST", url=url, json_dict=data)
