from datetime import UTC, datetime, timedelta
from typing import ClassVar

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
    """The main client to handle all the Battlemetrics requests.

    Parameters
    ----------
        api_key (str)
            Your given API token.
    """

    BASE_URL: ClassVar[str] = "https://api.battlemetrics.com"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @property
    def helpers(self) -> Helpers:
        """Return the helpers class."""
        return Helpers(api_key=self.api_key)

    @property
    def player(self) -> Player:
        """Return the player class."""
        return Player(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def server(self) -> Server:
        """Return the server class."""
        return Server(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def notes(self) -> Notes:
        """Return the notes class."""
        return Notes(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def flags(self) -> Flags:
        """Return the flags class."""
        return Flags(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def session(self) -> Session:
        """Return the session class."""
        return Session(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def banlist(self) -> BanList:
        """Return the banlist class."""
        return BanList(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def organization(self) -> Organization:
        """Return the organization class."""
        return Organization(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def gameinfo(self) -> GameInfo:
        """Return the gameinfo class."""
        return GameInfo(helpers=self.helpers, base_url=self.BASE_URL)

    @property
    def bans(self) -> Bans:
        """Return the bans class."""
        return Bans(helpers=self.helpers, base_url=self.BASE_URL)

    def check_api_scopes(self, token: str | None = None) -> dict:
        """Retrieve the token scopes from the oauth.

        Parameters
        ----------
            api_key (str | None):
                Your given API token. Defaults to the one supplied to this battlemetrics class.

        Returns
        -------
            dict: The tokens data.
        """
        if not token:
            token = self.api_key

        url = "https://www.battlemetrics.com/oauth/introspect"
        data = {
            "token": token,
        }
        return self.helpers._make_request(method="POST", url=url, json_dict=data)

    def metrics(
        self,
        name: str = "games.rust.players",
        start_date: str | None = None,
        end_date: str | None = None,
        resolution: str = "60",
    ) -> dict:
        """Return metrics.

        Parameters
        ----------
            name (str, optional): "games.{game}.players" and "games.{game}.players.steam".
            start_date (str, optional) UTC time format. Defaults to Current Date.
            end_date (str, optional): UTC time format. Defaults to 1 day ago.
            resolution (str, optional): raw, 30, 60 or 1440. Defaults to "60".

        Returns
        -------
            dict: a bunch of numbers.
        """
        url = f"{self.BASE_URL}/metrics"

        if not start_date:
            now = datetime.now(tz=UTC)
            start_date = now - timedelta(days=1)
            start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if not end_date:
            end_date = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "metrics[0][name]": name,
            "metrics[0][range]": f"{start_date}:{end_date}",
            "metrics[0][resolution]": resolution,
            "fields[dataPoint]": "name,group,timestamp,value",
        }
        return self.helpers._make_request(method="GET", url=url, params=data)

    def activity_logs(
        self,
        filter_bmid: int | None = None,
        filter_search: str | None = None,
        filter_servers: int | None = None,
        blacklist: str | None = None,
        whitelist: str | None = None,
    ) -> dict:
        """Retrieve the activity logs.

        Parameters
        ----------
            filter_bmid (int, optional): A battlemetrics ID for a specific user. Defaults to None.
            filter_search (str, optional): What do you want to search?. Defaults to None.
            filter_servers (int, optional): A specific battlemetrics server ID. Defaults to None.
            blacklist (str, optional): Example: unknown, playerMessage. Defaults to None.
            whitelist (str, optional): unknown, playerMessage. Defaults to None.

        Returns
        -------
            dict: The activity logs information.
        """
        url = f"{self.BASE_URL}/activity"
        data = {
            "page[size]": "100",
            "include": "organization,server,user,player",
        }

        if blacklist:
            data["filter[types][blacklist]"] = blacklist
        if whitelist:
            data["filter[types][whitelist]"] = whitelist
        if filter_servers:
            data["filter[servers]"] = filter_servers
        if filter_search:
            data["filter[search]"] = filter_search
        if filter_bmid:
            data["filter[players]"] = filter_bmid

        return self.helpers._make_request(method="GET", url=url, params=data)
