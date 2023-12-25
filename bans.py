import datetime
import uuid
from helpers import Helpers
from datetime import datetime


class Bans:
    def __init__(self, helpers: Helpers, BASE_URL: str) -> None:
        self.helpers = helpers
        self.BASE_URL = BASE_URL
        
    async def create(self, reason: str, note: str, beguid_id: int, steamid_id: int, battlemetrics_id: str, org_id: str, banlist: str, server_id: str,
                         expires: str = "permanent",
                         orgwide: bool = True) -> dict:
        """Bans a user from your server or organization.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-ban-/bans
        Documentation is incorrect.
        Args:
            reason (str): Reason for the ban (This is what the user/server sees)
            note (str): Note attached to the ban (Admins/staff can see this)
            beguid_id (int): The battlemetrics ID for the BEGUID.
            steamid_id (int): The battlemetrics ID for the STEAMID
            battlemetrics_id (str): Battlemetrics ID of the banned user
            org_id (str): Organization ID the ban is associated to.
            banlist (str): Banlist the ban is associated to.
            server_id (str): Server ID the ban is associated to.
            expires (str, optional): Expiration, leave none for permanent. Defaults to None.
            orgwide (bool, optional): Orgwide or single server?. Defaults to True.
        Notes:
            Steamid_id and beguid_id are the ID's that battlemetrics associates with them. Not the ID themselves.
        Returns:
            dict: The results, whether it was successful or not.
        """
        if expires == "permanent":
            expires = None

        if expires:
            expires = await self.helpers.calculate_future_date(expires)

        current_datetime = datetime.now()
        
        #Not needed.
        #formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = {
            "data":
                {
                    "type": "ban",
                    "attributes": {
                            "reason": reason,
                            "note": note,
                            "expires": expires,
                            "identifiers": [beguid_id, steamid_id],
                            "orgWide": orgwide,
                            "autoAddEnabled": True,
                            "nativeEnabled": None
                    },
                    "relationships": {
                        "organization": {
                            "data": {
                                "type": "organization",
                                "id": f"{org_id}"
                            }
                        },
                        "server": {
                            "data": {
                                "type": "server",
                                "id": f"{server_id}"
                            }
                        },
                        "player": {
                            "data": {
                                "type": "player",
                                "id": f"{battlemetrics_id}"
                            }
                        },
                        "banList": {
                            "data": {
                                "type": "banList",
                                "id": f"{banlist}"
                            }
                        }
                    }
                }
        }

        url = f"{self.BASE_URL}/bans"
        return await self.helpers._make_request(method="POST", url=url, data=data)

    async def delete(self, banid: str) -> dict:
        """Deletes a ban.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-ban-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}
        Args:
            banid (str): The ID of the ban.
        Returns:
            dict: The response from the server.
        """

        url = f"{self.BASE_URL}/bans/{banid}"
        return await self.helpers._make_request(method="DELETE", url=url)

    async def info(self, banid: str) -> dict:
        """The ban profile of a specific banid.
        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-ban-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}
        Args:
            banid (str): The banid.
        Returns:
            dict: The ban information
        """

        url = f"{self.BASE_URL}/bans/{banid}"
        return await self.helpers._make_request(method="GET", url=url)

    async def update(self, banid: str, reason: str = None, note: str = None, append: bool = False) -> dict:
        """Updates a targeted ban
        Documentation: https://www.battlemetrics.com/developers/documentation#link-PATCH-ban-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}
        Args:
            banid (str): The target ban
            reason (str, optional): Updated reason (not required)
            note (str, optional): Updated note (not required)
            append (bool, optional): Whether you want to append the new note to the old note.
        Returns:
            dict: The response from the server.
        """

        url = f"{self.BASE_URL}/bans/{banid}"
        ban = await self.info(banid=banid)
        if reason:
            ban['data']['attributes']['reason'] = reason
        if note:
            if append:
                ban['data']['attributes']['note'] += f"\n{note}"
            else:
                ban['data']['attributes']['note'] = note
        return await self.helpers._make_request(method="PATCH", url=url, data=ban)

    async def search(self, search: str = None, player_id: int = None, banlist: str = None, expired: bool = True, exempt: bool = False, server: int = None, organization_id: int = None, userIDs: str = None):
        """List, search and filter existing bans.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-ban-/bans

        Args:
            search (str, optional): A search string, such as a steam ID. Defaults to None.
            player_id (int, optional): Battlemetrics ID of a specific user. Defaults to None.
            banlist (str, optional): Specific banlist to search. Defaults to None.
            expired (bool, optional): True/False - Do you want expired bans?. Defaults to True.
            exempt (bool, optional): True/False - Do you want to include exempt?. Defaults to False.
            server (int, optional): Server ID. Defaults to None.
            organization_id (int, optional): Organization ID. Defaults to None.
            userIDs (str, optional): User ID is the ID of the person who made the ban. Defaults to None.

        Returns:
            dict: A dictionary response of all the bans for the given parameters.
        """

        data = {
            "include": "server,user,player,organization",
            "filter[expired]": str(expired).lower(),
            "filter[exempt]": str(exempt).lower(),
            "sort": "-timestamp",
            "page[size]": "100"
        }

        if organization_id:
            data['filter[organization]'] = organization_id
        if player_id:
            data['filter[player]'] = player_id
        if server:
            data['filter[server]'] = server
        if search:
            data['filter[search]'] = search
        if banlist:
            data['filter[banList]'] = banlist
        if userIDs:
            data['filter[users]'] = userIDs
        url = f"{self.BASE_URL}/bans"

        return await self.helpers._make_request(method="GET", url=url, data=data)