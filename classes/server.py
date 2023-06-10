import utility
from datetime import datetime, timedelta


class Server:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def server_rank_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Server Rank History

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rank-history

        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.

        Returns:
            dict: Datapoint of the server rank history.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/rank-history"

        data = {
            "start": start_time,
            "end": end_time
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_group_rank_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Group Rank History. The server must belong to a group.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/group-rank-history

        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.

        Returns:
            dict: Datapoint of the server group rank history.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/group-rank-history"

        data = {
            "start": start_time,
            "end": end_time
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_time_played_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Time Played History

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/time-played-history

        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.

        Returns:
            dict: Datapoint of the server time played history.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/time-played-history"

        data = {
            "start": start_time,
            "end": end_time
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_first_time_played_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """First Time Player History

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/first-time-history

        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.

        Returns:
            dict: Datapoint of the server first time played history.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/first-time-history"

        data = {
            "start": start_time,
            "end": end_time
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_unique_players_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Unique Player History

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/unique-player-history

        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.

        Returns:
            dict: Datapoint of the server unique players history.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/unique-player-history"

        data = {
            "start": start_time,
            "end": end_time
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_session_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Session history

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/sessions

        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.

        Returns:
            dict: Datapoint of the server session history.
        """
        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/relationships/sessions"

        data = {
            "start": start_time,
            "stop": end_time,
            "include": "player"
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_list(self, search: str = None, countries: list = None, favorited: bool = False, game: str = None,
                          blacklist: str = None, whitelist: str = None, organization: str = None, rcon: bool = False) -> dict:
        """List, search and filter servers.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers

        Args:
            search (str, optional): Search for specific server. Defaults to None.
            countries (list, optional): Server in a country. Defaults to None.
            favorited (bool, optional): Favorited or not on battlemetrics. Defaults to False.
            game (str, optional): Specific game. Defaults to None.
            blacklist (str, optional): Blacklisted servers. Defaults to None.
            whitelist (str, optional): Whitelisted servers. Defaults to None.
            organization (str, optional): Organization ID. Defaults to None.
            rcon (bool, optional): RCON only. Defaults to False.

        Returns:
            dict: Dictionary response from battlemetrics.
        """
        url = f"{self.base_url}/servers"
        data = {
            "page[size]": "100",
            "include": "serverGroup",
            "filter[favorites]": str(favorited).lower(),
            "filter[rcon]": str(rcon).lower()
        }

        if search:
            data["filter[search]"] = search
        if countries:
            data["filter[countries]"] = countries
        if game:
            data["filter[game]"] = game
        if blacklist:
            data["filter[ids][blacklist]"] = blacklist
        if whitelist:
            data["filter[ids][whitelist]"] = whitelist
        if organization:
            data["filter[organizations]"] = organization

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_create(self, server_ip: str, server_port: str, port_query: str, game: str, server_gsp: str = None, organization_id: int = None, banlist_id: str = None, server_group: str = None) -> dict:
        """Add a server to the system.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-server-/servers

        The documentation does not provide information on how to properly use the params after the "Game" param.

        Args:
            server_ip (str): The IP of your server
            server_port (str): The port of the server
            port_query (str): The port query of the server
            game (str): The game of the server
            server_gsp (str): game server provider
            organization_id (int): The organization ID the server belongs to
            banlist_id (str): A banlist ID the server uses.
            server_group (str): The server group.

        Returns:
            dict: Response from battlemetrics.

        """

        url = f"{self.base_url}/servers"
        data = {
            "data": {
                "type": "server",
                "attributes": {
                    "ip": f"{server_ip}",
                    "port": f"{server_port}",
                    "portQuery": f"{port_query}"
                },
                "relationships": {
                    "game": {
                        "data": {
                            "type": "game",
                            "id": f"{game}"
                        }
                    }
                }
            }
        }

        return await utility._make_request(headers=self.headers, method="POST", url=url, data=data)

    async def server_update(self, server_id: int) -> dict:
        pass
     #  data = {
     #      "data": {
     #          "type": "server",
     #          "id": "42",
     #          "attributes": {
     #              "portRCON": 2302,
     #              "rconPassword": "password",
     #              "metadata": {
     #              },
     #              "ip": "127.0.0.1",
     #              "address": "play.example.com",
     #              "port": 2302,
     #              "portQuery": 2303,
     #              "private": False
     #          },
     #          "relationships": {
     #              "defaultBanList": {
     #                  "data": {
     #                      "type": "banList",
     #                      "id": "01234567-89ab-cdef-0123-456789abcdef"
     #                  }
     #              }
     #          }
     #      }
     #  }

    async def server_enable_rcon(self, server_id: int) -> dict:
        # This endpoint is not completed by the creator of this wrapper.
        pass

    async def server_delete_rcon(self, server_id: int) -> dict:
        """Names on the tin, deletes the RCON for your server

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rcon

        Args:
            server_id (int): The server ID.

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/servers/{server_id}/rcon"

        return await utility._make_request(headers=self.headers, method="DELETE", url=url)

    async def server_disconnect_rcon(self, server_id: int) -> dict:
        """Names on the tin, disconnects RCON from your server.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rcon/disconnect

        Args:
            server_id (int): Server ID

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/servers/{server_id}/rcon/disconnect"

        return await utility._make_request(headers=self.headers, method="DELETE", url=url)

    async def server_connect_rcon(self, server_id: int) -> dict:
        """Names on the tin, connects RCON to your server.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rcon/connect

        Args:
            server_id (int): Server ID

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/servers/{server_id}/rcon/connect"

        return await utility._make_request(headers=self.headers, method="DELETE", url=url)

    async def server_info(self, server_id: int) -> dict:
        """Server info.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}

        Args:
            server_id (int): The server ID

        Returns:
            dict: The server information.
        """
        url = f"{self.base_url}/servers/{server_id}"

        data = {
            "include": "player,identifier"
        }

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_force_update(self, server_id: int) -> dict:
        """Force Update will cause us to immediately queue the server to be queried and updated. This is limited to subscribers and users who belong to the organization that owns the server if it is claimed.

            This endpoint has a rate limit of once every 30 seconds per server, and 10 every five minutes per user.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/force-update

        Args:
            server_id (int): The server ID

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/servers/{server_id}/force-update"
        return await utility._make_request(headers=self.headers, method="POST", url=url)

    async def server_outage_history(self, server_id: int, uptime: str = "90", start_time: str = None, end_time: str = None) -> dict:
        """Outage History. Outages are periods of time that the server did not respond to queries. Outage history stored and available for 90 days.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/outages

        Args:
            server_id (int): The server ID
            uptime (str, optional): One of 7, 30 or 90. Defaults to "90".
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to Today/now.

        Returns:
            dict: The server outage history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/relationships/outages"
        data = {
            "page[size]": "100",
            "filter[range]": f"{start_time}:{end_time}",
            "include": f"uptime:{uptime}"
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def server_downtime_history(self, server_id: int, resolution: str = "60", start_time: str = None, end_time: str = None) -> dict:
        """Downtime History. Value is number of seconds the server was offline during that period. The default resolution provides daily values (1440 minutes).

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/downtime

        Args:
            server_id (int): The server ID
            resolution (str, optional): One of 60 or 1440. Defaults to "60".
            start_time (str, optional): The UTC start time. Defaults to 1 day ago.
            end_time (str, optional): The UTC end time. Defaults to Today/now.

        Returns:
            dict: The server Downtime history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - timedelta(days=1)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/servers/{server_id}/relationships/downtime"
        data = {
            "page[size]": "100",
            "start": f"{start_time}",
            "stop": f"{end_time}",
            "resolution": f"{resolution}"
        }
        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)
