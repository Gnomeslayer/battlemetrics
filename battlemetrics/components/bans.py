from battlemetrics.components.helpers import Helpers


class Bans:
    """The bans class to handle all the ban requests."""

    def __init__(self, helpers: Helpers, base_url: str) -> None:
        self.helpers = helpers
        self.base_url = base_url

    async def delete(self, banid: str) -> dict:
        """Delete a ban.

        Parameters
        ----------
            banid (str): The ID of the ban.

        Returns
        -------
            dict: The response from the server.
        """
        url = f"{self.base_url}/bans/{banid}"

        return await self.helpers._make_request(method="DELETE", url=url)

    async def info(self, banid: str) -> dict:
        """Get information about a specific ban.

        Parameters
        ----------
            banid (str): The banid.

        Returns
        -------
            dict: The ban information
        """
        url = f"{self.base_url}/bans/{banid}"
        data = {
            "include": "server,user,playerIdentifiers,organization,banExemption",
        }
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def update(
        self,
        banid: str,
        reason: str | None = None,
        note: str | None = None,
        append: bool = False,
    ) -> dict:
        """Update a targeted ban.

        Parameters
        ----------
            banid (str): The target ban
            reason (str, optional): Updated reason (not required)
            note (str, optional): Updated note (not required)
            append (bool, optional): Whether you want to append the new note to the old note.

        Returns
        -------
            dict: The response from the server.
        """
        url = f"{self.base_url}/bans/{banid}"
        ban = await self.info(banid=banid)
        if reason:
            ban["data"]["attributes"]["reason"] = reason
        if note:
            if append:
                ban["data"]["attributes"]["note"] += f"\n{note}"
            else:
                ban["data"]["attributes"]["note"] = note
        return await self.helpers._make_request(method="PATCH", url=url, json=ban)

    # TODO: Is it supposed to say userIDs?
    # TODO: Make this function look neat.
    async def search(
        self,
        search: str = None,
        player_id: int = None,
        banlist: str = None,
        server: int = None,
        organization_id: int = None,
        userids: str | None = None,
        *,
        expired: bool = True,
        exempt: bool = False,
    ):
        """List, search and filter existing bans.

        Parameters
        ----------
            search (str, optional): A search string, such as a steam ID. Defaults to None.
            player_id (int, optional): Battlemetrics ID of a specific user. Defaults to None.
            banlist (str, optional): Specific banlist to search. Defaults to None.
            expired (bool, optional): True/False - Do you want expired bans?. Defaults to True.
            exempt (bool, optional): True/False - Do you want to include exempt?. Defaults to False.
            server (int, optional): Server ID. Defaults to None.
            organization_id (int, optional): Organization ID. Defaults to None.
            userIDs (str, optional): User ID is the ID of the person who made the ban. Defaults to None.

        Returns
        -------
            dict: A dictionary response of all the bans for the given parameters.
        """
        data = {
            "include": "server,user,player,organization",
            "filter[expired]": str(expired).lower(),
            "filter[exempt]": str(exempt).lower(),
            "sort": "-timestamp",
            "page[size]": "100",
        }

        if organization_id:
            data["filter[organization]"] = organization_id
        if player_id:
            data["filter[player]"] = player_id
        if server:
            data["filter[server]"] = server
        if search:
            data["filter[search]"] = search
        if banlist:
            data["filter[banList]"] = banlist
        if userids:
            data["filter[users]"] = userids
        url = f"{self.base_url}/bans"

        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def native_ban_info(self, server: int = None, ban: str = None) -> dict:
        """Return all the native bans.

        Parameters
        ----------
            server (int, optional): Target server. Defaults to None.
            ban (int, optional): Target ban. Defaults to None.

        Returns
        -------
            dict: All native bans.
        """
        data = {
            "page[size]": "100",
            "include": "server,ban",
            "sort": "-createdAt",
            "fields[ban]": "reason",
            "fields[server]": "name",
            "fields[banNative]": "createdAt,reason",
        }
        if ban:
            data["filter[ban]"] = ban
        if server:
            data["filter[server]"] = server
        url = f"{self.base_url}/bans-native"
        return await self.helpers._make_request(method="GET", url=url, params=data)

    async def native_force_update(self, native_id: str) -> dict:
        """Force an update on a native ban.

        Parameters
        ----------
            native_id (str): Targeted native ban

        Returns
        -------
            dict: Response from the server.
        """
        url = f"{self.base_url}/bans-native/{native_id}/force-update"
        return await self.helpers._make_request(method="POST", url=url)
