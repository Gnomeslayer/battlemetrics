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
        formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = {
            "data":
                {
                    "type": "ban",
                    "attributes": {
                            "uid": str(uuid.uuid4())[:14],
                            "timestamp": str(formatted_datetime),
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
