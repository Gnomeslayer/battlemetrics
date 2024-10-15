from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, ClassVar

# Components
from battlemetrics.components.banlist import BanList
from battlemetrics.components.bans import Bans
from battlemetrics.components.flags import Flags
from battlemetrics.components.gameinfo import GameInfo
from battlemetrics.components.notes import Notes
from battlemetrics.components.organization import Organization
from battlemetrics.components.player import Player
from battlemetrics.components.server import Server
from battlemetrics.components.session import Session
from battlemetrics.http import HTTPClient, Route
from battlemetrics.misc import ActivityLogs, APIScopes, Metrics
from battlemetrics.state import ConnectionState

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    from aiohttp import BaseConnector

    from battlemetrics.note import Note

__all__ = ("Battlemetrics",)


class Battlemetrics:
    """The main client to handle all the Battlemetrics requests.

    Parameters
    ----------
        api_key (str)
            Your given API token.
    """

    BASE_URL: ClassVar[str] = "https://api.battlemetrics.com"

    def __init__(
        self,
        api_key: str,
        *,
        connector: BaseConnector | None = None,
        loop: AbstractEventLoop | None = None,
    ) -> None:
        self.__api_key = api_key

        self.loop = loop

        self.http = HTTPClient(
            api_key=self.__api_key,
            connector=connector,
            loop=loop,
        )
        self._connection = ConnectionState(loop=self.http.loop, http=self.http)

    @property
    def player(self) -> Player:
        """Return the player class."""
        return Player(http=self.http, base_url=self.BASE_URL)

    @property
    def server(self) -> Server:
        """Return the server class."""
        return Server(http=self.http, base_url=self.BASE_URL)

    @property
    def notes(self) -> Notes:
        """Return the notes class."""
        return Notes(http=self.http, base_url=self.BASE_URL)

    @property
    def flags(self) -> Flags:
        """Return the flags class."""
        return Flags(http=self.http, base_url=self.BASE_URL)

    @property
    def session(self) -> Session:
        """Return the session class."""
        return Session(http=self.http, base_url=self.BASE_URL)

    @property
    def banlist(self) -> BanList:
        """Return the banlist class."""
        return BanList(http=self.http, base_url=self.BASE_URL)

    @property
    def organization(self) -> Organization:
        """Return the organization class."""
        return Organization(http=self.http, base_url=self.BASE_URL)

    @property
    def gameinfo(self) -> GameInfo:
        """Return the gameinfo class."""
        return GameInfo(http=self.http, base_url=self.BASE_URL)

    @property
    def bans(self) -> Bans:
        """Return the bans class."""
        return Bans(http=self.http, base_url=self.BASE_URL)

    async def get_note(self, player_id: int, note_id: int) -> Note:
        """Return a note based on player ID and note ID.

        Parameters
        ----------
            player_id (int):
                The ID of the player.
            note_id (int):
                The ID of the note.
        """
        return await self._connection.get_note(player_id, note_id)

    async def check_api_scopes(self, token: str | None = None) -> APIScopes:
        """Retrieve the token scopes from the oauth.

        Parameters
        ----------
            api_key (str | None):
                Your given API token. Defaults to the one supplied to this battlemetrics class.

        Returns
        -------
            APIScopes
        """
        if not token:
            token = self.api_key

        url: str = "https://www.battlemetrics.com/oauth/introspect"
        json_dict = {
            "token": token,
        }
        data = await self.http.request(
            Route(
                method="POST",
                url=url,
            ),
            json=json_dict,
        )
        return APIScopes(
            active=data["active"],
            scopes=data["scope"].split(":"),
            client_id=data["client_id"],
            token_type=data["type"],
        )

    async def metrics(
        self,
        name: str = "games.rust.players",
        start_date: str | None = None,
        end_date: str | None = None,
        resolution: str = "60",
    ) -> list[Metrics]:
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

        if not start_date:
            now = datetime.now(tz=UTC)
            start_date = now - timedelta(days=1)
            start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if not end_date:
            end_date = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        params = {
            "metrics[0][name]": name,
            "metrics[0][range]": f"{start_date}:{end_date}",
            "metrics[0][resolution]": resolution,
            "fields[dataPoint]": "name,group,timestamp,value",
        }
        data = await self.http.request(
            Route(
                method="GET",
                path="/metrics",
            ),
            params=params,
        )
        return [
            Metrics(
                type=x.get("type"),
                timestamp=x["attributes"].get("timestamp"),
                value=x["attributes"].get("value"),
            )
            for x in data["data"]
        ]

    async def activity_logs(
        self,
        filter_bmid: int | None = None,
        filter_search: str | None = None,
        filter_servers: int | None = None,
        blacklist: str | None = None,
        whitelist: str | None = None,
    ) -> ActivityLogs:
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
        params = {
            "page[size]": "100",
            "include": "organization,server,user,player",
        }

        if blacklist:
            params["filter[types][blacklist]"] = blacklist
        if whitelist:
            params["filter[types][whitelist]"] = whitelist
        if filter_servers:
            params["filter[servers]"] = filter_servers
        if filter_search:
            params["filter[search]"] = filter_search
        if filter_bmid:
            params["filter[players]"] = filter_bmid

        data = await self.http.request(
            Route(
                method="GET",
                path="/activity",
            ),
            params=params,
        )
        return ActivityLogs(**data)
