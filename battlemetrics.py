from time import strftime, localtime
from datetime import datetime, timedelta
from components.player import Player
from components.server import Server
from components.helpers import Helpers
from components.notes import Notes
from components.flags import Flags
from components.session import Session
from components.banlist import Ban_List
from components.organization import Organization
from components.game_info import Game_Info
from battlemetrics_wrapper_v2.classes.bans import Bans


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

    async def pagination(self, page_link:str) -> dict:
        return await self.helpers._make_request(method="GET", url=page_link)

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
