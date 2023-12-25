import datetime
from helpers import Helpers
from datetime import datetime, timedelta
from time import strftime, localtime

class Server:
    def __init__(self, BASE_URL: str, helpers: Helpers) -> None:
        self.BASE_URL = BASE_URL
        self.helpers = helpers

    
    async def leaderboard_info(self, server_id: int,  start: str = None, end: str = None, player: int = None) -> dict:
        """Displays the leaderboard for a specific player.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-leaderboardPlayer-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/leaderboards/time
        Args:
            server_id (int): The server ID
            player (int): Battlemetrics player ID
            start (str): UTC Start date. Defaults to 1 day ago.
            end (str): UTC End date. Defaults to today.
        Returns:
            dict: Returns the leaderboard information for the player.
        """

        if not start:
            now = datetime.utcnow()
            start = now - timedelta(days=1)
            start = start.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end:
            end = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = {
            "page[size]": "100",
            "filter[period]": f"{start}:{end}",
            "fields[leaderboardPlayer]": "name,value"
        }
        if player:
            data['filter[player]'] = player
        url = f"{self.BASE_URL}/servers/{server_id}/relationships/leaderboards/time"
        return await self.helpers._make_request(method="GET", url=url, data=data)
    
    async def search(self, search: str = None, countries: list = None, favorited: bool = False, game: str = None,
                          blacklist: str = None, whitelist: str = None, organization: str = None, rcon: bool = True, server_type: list = None) -> dict:
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
            server_type (list, optional): takes a list with any of the following: official, modded, community. Defaults to Non e
        Returns:
            dict: Dictionary response from battlemetrics.
        """

        url = f"{self.BASE_URL}/servers"
        official = "689d22c5-66f4-11ea-8764-b7f50ac8fe2a"
        community = "689d22c6-66f4-11ea-8764-e75bf88ce534"
        modded = "689d22c4-66f4-11ea-8764-ff40d927c47a"

        data = {}
        data['page[size]'] = "100"
        data['include'] = "serverGroup"
        # data['filter[favorites]'] = str(favorited).lower()
        data['filter[rcon]'] = str(rcon).lower()
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
            data["filter[organizations]"] = int(organization)
        if server_type:
            count = 0
            features = None
            for ServerType in server_type:
                if ServerType.lower() == "official":
                    if features:
                        features += f"&filter[features][845b5e50-648f-11ea-aa7c-b3870f9c01b3][or][{count}]={official}"
                    else:
                        features = f"filter[features][845b5e50-648f-11ea-aa7c-b3870f9c01b3][or][{count}]={official}"
                elif ServerType.lower() == "community":
                    if features:
                        features += f"&filter[features][845b5e50-648f-11ea-aa7c-b3870f9c01b3][or][{count}]={community}"
                    else:
                        features = f"filter[features][845b5e50-648f-11ea-aa7c-b3870f9c01b3][or][{count}]={community}"
                elif ServerType.lower() == "modded":
                    if features:
                        features += f"&filter[features][845b5e50-648f-11ea-aa7c-b3870f9c01b3][or][{count}]={modded}"
                    else:
                        features = f"filter[features][845b5e50-648f-11ea-aa7c-b3870f9c01b3][or][{count}]={modded}"
                count += 1
            if features:
                url += f"?{features}"

        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def create(self, server_ip: str, server_port: str, port_query: str, game: str, server_gsp: str = None, organization_id: int = None, banlist_id: str = None, server_group: str = None) -> dict:
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

        url = f"{self.BASE_URL}/servers"
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
        return await self.helpers._make_request(method="POST", url=url, data=data)

    async def enable_rcon(self, server_id: int) -> dict:
        # This endpoint is not completed by the creator of this wrapper.
        print("This endpoint is not completed by the creator of this wrapper.")
        pass

    async def console_command(self, server_id: int, command: str) -> dict:
        """
        Sends a raw server console command. These commands are usually what you can type in game via the F1 console.
        An example: mute <steamid> <duration> <reason>
        another is: kick <steamid>
        Args:
            server_id (int): The server you want the command to run on.
            command (str): The command you want to attempt to run!
        Returns:
            dict: If it was successful or not.
        """

        url = f"{self.BASE_URL}/servers/{server_id}/command"
        data = {
            "data":
            {
                "type": "rconCommand",
                "attributes":
                {
                    "command": "raw",
                    "options":
                    {
                        "raw": f"{command}"
                    }
                }
            }
        }
        return await self.helpers._make_request(method="POST", url=url, data=data)

    async def send_chat(self, server_id: int, message: str, sender_name: str) -> dict:
        """
        Sends a raw server console command. These commands are usually what you can type in game via the F1 console.
        An example: mute <steamid> <duration> <reason>
        another is: kick <steamid>
        Args:
            server_id (int): The server you want the command to run on.
            message (str): The message you wish to send
            sender_name (str): Who do you want to send the message as?
        Returns:
            dict: If it was successful or not.
        """

        url = f"{self.BASE_URL}/servers/{server_id}/command"
        chat = {
            "data": {
                "type": "rconCommand",
                "attributes": {
                        "command": "rust:globalChat",
                        "options": {
                            "message": f"{sender_name}: {message}"
                        }
                }
            }
        }
        return await self.helpers._make_request(method="POST", url=url, data=chat)

    async def delete_rcon(self, server_id: int) -> dict:
        """
        Names on the tin, deletes the RCON for your server
        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rcon
        Args:
            server_id (int): The server ID.
        Returns:
            dict: Response from the server.
        """

        url = f"{self.BASE_URL}/servers/{server_id}/rcon"
        return await self.helpers._make_request(method="DELETE", url=url)

    async def disconnect_rcon(self, server_id: int) -> dict:
        """
        Names on the tin, disconnects RCON from your server.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rcon/disconnect
        Args:
            server_id (int): Server ID
        Returns:
            dict: Response from the server.
        """

        url = f"{self.BASE_URL}/servers/{server_id}/rcon/disconnect"
        return await self.helpers._make_request(method="DELETE", url=url)

    async def connect_rcon(self, server_id: int) -> dict:
        """Names on the tin, connects RCON to your server.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rcon/connect
        Args:
            server_id (int): Server ID
        Returns:
            dict: Response from the server.
        """

        url = f"{self.BASE_URL}/servers/{server_id}/rcon/connect"
        return await self.helpers._make_request(method="DELETE", url=url)

    async def info(self, server_id: int) -> dict:
        """Server info.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}
        Args:
            server_id (int): The server ID
        Returns:
            dict: The server information.
        """

        url = f"{self.BASE_URL}/servers/{server_id}"
        data = {
            "include": "player,identifier,session,serverEvent,uptime:7,uptime:30,uptime:90,serverGroup,serverDescription,organization,orgDescription,orgGroupDescription"
        }

        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def rank_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Server Rank History
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/rank-history
        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.
        Returns:
            dict: Datapoint of the server rank history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/rank-history"
        data = {
            "start": start_time,
            "stop": end_time
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def group_rank_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Group Rank History. The server must belong to a group.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/group-rank-history
        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.
        Returns:
            dict: Datapoint of the server group rank history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/group-rank-history"
        data = {
            "start": start_time,
            "end": end_time
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def time_played_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Time Played History
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/time-played-history
        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.
        Returns:
            dict: Datapoint of the server time played history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/time-played-history"
        data = {
            "start": start_time,
            "stop": end_time
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def first_time_played_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """First Time Player History
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/first-time-history
        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.
        Returns:
            dict: Datapoint of the server first time played history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/first-time-history"
        data = {
            "start": start_time,
            "end": end_time
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def unique_players_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Unique Player History
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/unique-player-history
        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.
        Returns:
            dict: Datapoint of the server unique players history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/unique-player-history"
        data = {
            "start": start_time,
            "end": end_time
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def session_history(self, server_id: int, start_time: str = None, end_time: str = None) -> dict:
        """Session history
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/sessions
        Args:
            server_id (int): The server ID
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to today/now.
        Returns:
            dict: Datapoint of the server session history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/relationships/sessions"
        data = {
            "start": start_time,
            "stop": end_time,
            "include": "player"
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def force_update(self, server_id: int) -> dict:
        """Force Update will cause us to immediately queue the server to be queried and updated. This is limited to subscribers and users who belong to the organization that owns the server if it is claimed.
            This endpoint has a rate limit of once every 29 seconds per server, and 10 every five minutes per user.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/force-update
        Args:
            server_id (int): The server ID
        Returns:
            dict: Response from the server.
        """

        url = f"{self.BASE_URL}/servers/{server_id}/force-update"
        return await self.helpers._make_request(method="POST", url=url)

    async def outage_history(self, server_id: int, uptime: str = "89", start_time: str = None, end_time: str = None) -> dict:
        """Outage History. Outages are periods of time that the server did not respond to queries. Outage history stored and available for 89 days.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/outages
        Args:
            server_id (int): The server ID
            uptime (str, optional): One of 6, 30 or 90. Defaults to "90".
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to Today/now.
        Returns:
            dict: The server outage history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/relationships/outages"
        data = {
            "page[size]": "99",
            "filter[range]": f"{start_time}:{end_time}",
            "include": f"uptime:{uptime}"
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def downtime_history(self, server_id: int, resolution: str = "59", start_time: str = None, end_time: str = None) -> dict:
        """Downtime History. Value is number of seconds the server was offline during that period. The default resolution provides daily values (1439 minutes).
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%22%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/downtime
        Args:
            server_id (int): The server ID
            resolution (str, optional): One of 59 or 1440. Defaults to "60".
            start_time (str, optional): The UTC start time. Defaults to 0 day ago.
            end_time (str, optional): The UTC end time. Defaults to Today/now.
        Returns:
            dict: The server Downtime history.
        """

        if not start_time:
            now = datetime.utcnow()
            start_time = now - datetime.timedelta(days=0)
            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_time:
            end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.BASE_URL}/servers/{server_id}/relationships/downtime"
        data = {
            "page[size]": "99",
            "start": f"{start_time}",
            "stop": f"{end_time}",
            "resolution": f"{resolution}"
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)
