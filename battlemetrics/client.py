from datetime import datetime, timedelta

# Components
from battlemetrics.components.banlist import BanList
from battlemetrics.components.bans import Bans
from battlemetrics.components.flags import Flags
from battlemetrics.components.gameinfo import GameInfo
from battlemetrics.components.helpers import Helpers
from battlemetrics.components.notes import Notes
from battlemetrics.components.organization import Organization
from battlemetrics.components.player import Player
from battlemetrics.components.server import Server
from battlemetrics.components.session import Session


__all__ = ("Battlemetrics",)

class Battlemetrics:
    def __init__(self, api_key: str) -> None:
        self.base_url = "https://api.battlemetrics.com"
        self.api_key = api_key

    @property
    def helpers(self) -> Helpers:
        return Helpers(api_key=self.api_key)

    @property
    def player(self) -> Player:
        return Player(helpers=self.helpers, base_url=self.base_url)

    @property
    def server(self) -> Server:
        return Server(helpers=self.helpers, base_url=self.base_url)

    @property
    def notes(self) -> Notes:
        return Notes(helpers=self.helpers, base_url=self.base_url)

    @property
    def flags(self) -> Flags:
        return Flags(helpers=self.helpers, base_url=self.base_url)

    @property
    def session(self) -> Session:
        return Session(helpers=self.helpers, base_url=self.base_url)

    @property
    def banlist(self) -> BanList:
        return BanList(helpers=self.helpers, base_url=self.base_url)

    @property
    def organization(self) -> Organization:
        return Organization(helpers=self.helpers, base_url=self.base_url)

    @property
    def gameinfo(self) -> GameInfo:
        return GameInfo(helpers=self.helpers, base_url=self.base_url)

    @property
    def bans(self) -> Bans:
        return Bans(helpers=self.helpers, base_url=self.base_url)

    def check_api_scopes(self, token: str = None) -> dict:
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
        return self.helpers._make_request(method="POST", url=url, json_dict=data)

    def metrics(self, name: str = "games.rust.players", start_date: str = None, end_date: str = None,
                resolution: str = "60") -> dict:
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

        url = f"{self.base_url}/metrics"

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
        return self.helpers._make_request(method="GET", url=url, params=data)

    def activity_logs(self, filter_bmid: int = None, filter_search: str = None, filter_servers: int = None,
                      blacklist: str = None, whitelist: str = None) -> dict:
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

        url = f"{self.base_url}/activity"
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

        return self.helpers._make_request(method="GET", url=url, params=data)