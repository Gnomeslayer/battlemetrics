from time import strftime, localtime
from datetime import datetime, timedelta
from player import Player
from server import Server
from helpers import Helpers
from notes import Notes
from flags import Flags
from session import Session
from banlist import Ban_List
from organization import Organization
from game_info import Game_Info
from bans import Bans


class Battlemetrics:
    """Sets up the wrapper.

    Args:
        api_key (str): Your battlemetrics API token.

    Returns:
        None: Doesn't return anything.
    """

    def __init__(self, api_key: str) -> None:
        self.BASE_URL = "https://api.battlemetrics.com"
        self.api_key = api_key
        #self.response_data = None
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.helpers = Helpers(api_key=api_key)
        self.player = Player(helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.server = Server(helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.notes = Notes(helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.flags = Flags(helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.session = Session(helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.ban_list = Ban_List(helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.bans = Bans(helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.organization = Organization(
            helpers=self.helpers, BASE_URL=self.BASE_URL)
        self.game_info = Game_Info(
            helpers=self.helpers, BASE_URL=self.BASE_URL)

    async def check_api_scopes(self, token: str = None) -> dict:
        """Retrieves the tokens scopes from the oauth.
        Documentation: None.
        Args:
            api_key (str, optional): Your given API token. Defaults to the one supplied to this battlemetrics class.
        Returns:
            dict: The tokens data.
        """
        if not token:
            token = self.api_key

        url = f"https://www.battlemetrics.com/oauth/introspect"
        data = {
            "token": token
        }
        return await self.helpers._make_request(method="POST", url=url, data=data)

    #async def next(self) -> dict:
#
    #    if not self.response_data['links'].get('next'):
    #        return
    #    url = self.response_data['links']['next']
    #    if self.response_data['pages']:
    #        if self.response_data['pages'][-1]['links'].get('next'):
    #            url = response_data['pages'][-1]['links']['next']
    #    self.response_data = await self.helpers._make_request(method="GET", url=url)
    #    self.response_data['pages'].append(self.response_data)
    #    return self.response_data

    async def native_ban_info(self, server: int = None, ban: str = None) -> dict:
        """Returns all the native bans
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banNative-/bans-native
        Args:
            server (int, optional): Target server. Defaults to None.
            ban (int, optional): Target ban. Defaults to None.
        Returns:
            dict: All native bans.
        """

        data = {
            "page[size]": "100",
            "include": "server,ban",
            "sort": "-createdAt",
            "fields[ban]": "reason",
            "fields[server]": "name",
            "fields[banNative]": "createdAt,reason"
        }
        if ban:
            data["filter[ban]"] = ban
        if server:
            data["filter[server]"] = server
        url = f"{self.BASE_URL}/bans-native"
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def native_force_update(self, native_id: str) -> dict:
        """Forces an update on a native ban
        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-banNative-/bans-native/{(%23%2Fdefinitions%2FbanNative%2Fdefinitions%2Fidentity)}/force-update
        Args:
            native_id (str): Targeted native ban
        Returns:
            dict: Response from the server.
        """

        url = f"{self.BASE_URL}/bans-native/{native_id}/force-update"
        return await self.helpers._make_request(method="POST", url=url)

    async def metrics(self, name: str = "games.rust.players", start_date: str = None, end_date: str = None, resolution: str = "60") -> dict:
        """A data point as used in time series information.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-dataPoint-/metrics
        Args:
            name (str, optional): "games.{game}.players" and "games.{game}.players.steam", defaults to "games.rust.players"
            start_date (str, optional) UTC time format. Defaults to Current Date.
            end_date (str, optional): UTC time format. Defaults to 1 day ago.
            resolution (str, optional): raw, 30, 60 or 1440. Defaults to "60".
        Returns:
            dict: a bunch of numbers.
        """

        url = f"{self.BASE_URL}/metrics"
        # current_time = datetime.utcnow()
        # current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not start_date:
            now = datetime.utcnow()
            start_date = now - timedelta(days=1)
            start_date = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = {
            "metrics[0][name]": name,
            "metrics[0][range]": f"{start_date}:{end_date}",
            "metrics[0][resolution]": resolution,
            "fields[dataPoint]": "name,group,timestamp,value"
        }
        return await self.helpers._make_request(method="GET", url=url, data=data)

    async def activity_logs(self, filter_bmid: int = None, filter_search: str = None, filter_servers: int = None, blacklist: str = None, whitelist: str = None) -> dict:
        """Retrieves the activity logs.

        Args:
            filter_bmid (int, optional): A battlemetrics ID for a specific user. Defaults to None.
            filter_search (str, optional): What do you want to search?. Defaults to None.
            filter_servers (int, optional): A specific battlemetrics server ID. Defaults to None.
            blacklist (str, optional): Example: unknown, playerMessage. Defaults to None.
            whitelist (str, optional): unknown, playerMessage. Defaults to None.

        Returns:
            dict: The activity logs information.
        """

        url = f"{self.BASE_URL}/activity"
        data = {
            "page[size]": "100",
            "include": "organization,server,user,player"
        }

        if blacklist:
            data['filter[types][blacklist]'] = blacklist
        if whitelist:
            data['filter[types][whitelist]'] = whitelist
        if filter_servers:
            data['filter[servers]'] = filter_servers
        if filter_search:
            data['filter[search]'] = filter_search
        if filter_bmid:
            data['filter[players]'] = filter_bmid

        return await self.helpers._make_request(method="GET", url=url, data=data)
