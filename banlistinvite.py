import utility


class Banlistinvite:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def create(self, organization_id: int, banlist_id: str, permManage: bool, permCreate: bool, permUpdate: bool, permDelete: bool, uses: int = 1, limit: int = 1) -> dict:
        """Creates an invite to 

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-banListInvite-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}/relationships/invites

        Args:
            organization_id (int): The target organization to be invited.
            banlist_id (str): The ID of the banlist you want to create the invite for
            permManage (bool): Are they allowed to manage it?
            permCreate (bool): Can they create stuff related to this banlist?
            permUpdate (bool): Can they update the banlist?
            permDelete (bool): Can they delete stuff related to this banlist?
            uses (int, optional): Number of times this banlist invite has been used.. Defaults to 1.
            limit (int, optional): How many times it's allowed to be used. Defaults to 1.

        Returns:
            dict: Returns whether it was successful or not.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/invites"
        json_post = {
            "data": {
                "type": "banListInvite",
                "attributes": {
                    "uses": uses,
                    "limit": limit,
                    "permManage": str(permManage).lower(),
                    "permCreate": str(permCreate).lower(),
                    "permUpdate": str(permUpdate).lower(),
                    "permDelete": str(permDelete).lower()
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}"
                        }
                    }
                }
            }
        }

        return await utility._post_request(url=url, post=json_post, headers=self.headers)

    async def read(self, invite_id: str) -> dict:
        """Allows you to see the information about a specific banlist invite, such as uses.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banListInvite-/ban-list-invites/{(%23%2Fdefinitions%2FbanListInvite%2Fdefinitions%2Fidentity)}

        Args:
            invite_id (str): The banlist invite id.

        Returns:
            dict: The banlist invite information
        """
        url = f"{self.base_url}/ban-list-invites/{invite_id}"
        params = {
            "include": "banList",
            "fields[organization]": "tz,banTemplate",
            "fields[user]": "nickname",
            "fields[banList]": "name, action",
            "fields[banListInvite]": "uses"
        }

        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def invite_list(self, banlist_id: str) -> dict:
        """Returns all the invites for a specific banlist ID

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banListInvite-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}/relationships/invites

        Args:
            banlist_id (str): The ID of a banlist
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/invites"
        params = {
            "include": "banList",
            "fields[organization]": "tz,banTemplate",
            "fields[user]": "nickname",
            "fields[banList]": "name,action",
            "fields[banListInvite]": "uses",
            "page[size]": "100"
        }

        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def delete(self, banlist_id: str, banlist_invite_id: str) -> dict:
        """Deletes an invite from a targeted banlist

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-banListInvite-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}/relationships/invites/{(%23%2Fdefinitions%2FbanListInvite%2Fdefinitions%2Fidentity)}

        Args:
            banlist_id (str): The target banlist
            banlist_invite_id (str): The target invite.

        Returns:
            dict: Whether it was successful or not.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/invites/{banlist_invite_id}"

        return await utility._delete_request(url=url, headers=self.headers)
