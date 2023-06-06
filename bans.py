import uuid
import time
from datetime import datetime
import utility


class Bans:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def bans(self, search: str = None, player_id: int = None, banlist: str = None, expired: bool = False, exempt: bool = False, server: int = None, organization_id: int = None, page_size: int = 100):
        """List, search and filter existing bans.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-ban-/bans

        Returns:
            dict: A dictionary response telling you if it worked or not.
        """

        params = {
            "include": "server,user,player,organization",
            "fields[server]": "name",
            "fields[player]": "name",
            "field[user]": "nickname",
            "fields[banList]": "name",
            "fields[banExemption]": "reason",
            "filter[expired]": expired,
            "filter[exempt]": exempt,
            "sort": "-timestamp",
            "page[size]": "100"
        }
        if organization_id:
            params['filter[organization]'] = organization_id
        if player_id:
            params['filter[player]'] = player_id
        if server:
            params['filter[server]'] = server
        if search:
            params['filter[search]'] = search
        if banlist:
            params['filter[banList]'] = banlist

        url = f"{self.base_url}/bans"
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def create(self, reason: str, note: str, steamid: str, battlemetrics_id: str, org_id: str, banlist: str, server_id: str,
                     expires: str = None,
                     orgwide: bool = True) -> dict:
        """Bans a user from your server or organization.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-ban-/bans

        Args:
            reason (str): Reason for the ban (This is what the user/server sees)
            note (str): Note attached to the ban (Admins/staff can see this)
            steamid (str): Steam ID of the banned user
            battlemetrics_id (str): _Battlemetrics ID of the banned user
            org_id (str): Organization ID the ban is associated to.
            banlist (str): Banlist the ban is associated to.
            server_id (str): Server ID the ban is associated to.
            expires (str, optional): Expiration, leave none for permanent_. Defaults to None.
            orgwide (bool, optional): Orgwide or single server?. Defaults to True.

        Returns:
            dict: The results, whether it was successful or not.
        """
        if expires:
            try:
                expiration_time = datetime.strptime(
                    expires, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                raise ValueError(
                    "Invalid expiration time format. Please provide time in format 'YYYY-MM-DDTHH:MM:SS.sssZ'.")

        json_post = {
            "data": {
                "type": "ban",
                "attributes": {
                    "uid": str(uuid.uuid4()),
                    "timestamp": time.now(),
                    "reason": reason,
                    "note": note,
                    "expires": f"{expiration_time}",
                    "identifiers": [
                        1000,
                        {
                            "type": "steamID",
                            "identifier": f"{steamid}",
                            "manual": True
                        }
                    ],
                    "orgWide": str(orgwide).lower(),
                    "autoAddEnabled": False,
                    "nativeEnabled": True
                },
                "relationships": {
                    "player": {
                        "data": {
                            "type": "player",
                            "id": f"{battlemetrics_id}"
                        }
                    },
                    "server": {
                        "data": {
                            "type": "server",
                            "id": f"{server_id}"
                        }
                    },
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{org_id}"
                        }
                    },
                    "user": {
                        "data": {
                            "type": "user",
                            "id": "42"
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
        url = f"{self.base_url}/bans"
        return await utility._post_request(url=url, post=json_post, headers=self.headers)

    async def export(self, organization_id: int, server: int = None, game: str = "Rust") -> dict:
        """Grabs you the ban list for a specific organization or server belongin to the organization.
        Only supports Rust format at the moment.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-ban-/bans/export

        Args:
            server (int): The server ID you want the bans for.
            organization (int): The organizational ID
            game (str, optional): Only supports rust bans. Defaults to "Rust".

        Returns:
            dict: The ban list. Also saves it locally.
        """

        game = game.lower()
        game = "rust"
        if game == "rust":
            format = "rust/bans.cfg"
        if game == "arma2":
            format = "arma2/bans.txt"
        if game == "arma3":
            format = "arma3/bans.txt"
        if game == "squad":
            format = "squad/Bans.cfg"
        if game == "ark":
            format = "ark/banlist.txt"

        params = {
            "filter[organization]": organization_id,
            "format": format
        }

        if server:
            params["filter[organization]"] = server

        url = f"{self.base_url}/bans/export"
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def delete(self, banid: str) -> dict:
        """Deletes a ban.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-ban-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}

        Args:
            banid (str): The ID of the ban.

        Returns:
            dict: The response from the server.
        """
        url = f"{self.base_url}/bans/{banid}"
        return await utility._delete_request(url=url, headers=self.headers)

    async def info(self, banid: str) -> dict:
        """The ban profile of a specific banid.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-ban-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}

        Args:
            banid (str): The banid.

        Returns:
            dict: The ban information
        """
        url = f"{self.base_url}/bans/{banid}"
        return await utility._get_request(url=url, headers=self.headers)

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
        url = f"{self.base_url}/bans/{banid}"
        ban = await self.info(banid=banid)
        if reason:
            ban['data']['attributes']['reason'] = reason
        if note:
            if append:
                ban['data']['attributes']['note'] += f"\n{note}"
            else:
                ban['data']['attributes']['note'] = note
        return await utility._patch_request(url=url, post=ban, headers=self.headers)
