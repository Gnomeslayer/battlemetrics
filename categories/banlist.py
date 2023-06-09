import utility


class BansList:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def create(self, organization_id: int, action: str, autoadd: bool, ban_identifiers: list, native_ban: bool, list_default_reasons: list, ban_list_name: str) -> dict:
        """Creates a new banlist for your targeted organization.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-banList-/ban-lists

        Args:
            organization_id (str): The organization ID.
            action (str): "none", "log", "kick"
            autoadd (bool): true or false
            ban_identifiers (list): ["steamID", "ip"]
            native_ban (bool): Should this be a native ban as well?
            list_default_reasons (list): Default reason for the ban if no new reason is specified
            ban_list_name (str): Name of the banlist

        Returns:
            dict: Returns a dictionary response of the new banlist created.
        """

        url = f"{self.base_url}/ban-lists"
        json_post = {
            "data": {
                "type": "banList",
                "attributes": {
                    "name": f"{ban_list_name}",
                    "action": f"{action}",
                    "defaultIdentifiers": ban_identifiers,
                    "defaultReasons": list_default_reasons,
                    "defaultAutoAddEnabled": str(autoadd).lower(),
                    "defaultNativeEnabled": str(native_ban).lower(),
                    "nativeBanTTL": None,
                    "nativeBanTempMaxExpires": None,
                    "nativeBanPermMaxExpires": None
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}"
                        }
                    },
                    "owner": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}"
                        }
                    }
                }
            }
        }
        return await utility._post_request(url=url, post=json_post, headers=self.headers)

    async def accept_invite(self, code: str, action: str, autoadd: bool, ban_identifiers: list, native_ban: bool, list_default_reasons: list, organization_id: str, organization_owner_id: str) -> dict:
        """Accepts an invitation to subscribe to a banlist.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-banList-/ban-lists/accept-invite

        Args:
            code (str): Invitation code.
            action (str): "none", "log" or "kick"
            autoadd (bool): True or False
            ban_identifiers (list): ["steamID", "ip"]
            native_ban (bool): True or False
            list_default_reasons (list): ["Banned for hacking"]
            organization_id (str): ID of your organization?
            organization_owner_id (str): ID of the owner of the organization

        Returns:
            dict: Response from server.
        """
        url = f"{self.base_url}/ban-lists/accept-invite"
        params = {
            "data": {
                "type": "banList",
                "attributes": {
                    "code": code,
                    "action": action,
                    "defaultIdentifiers": ban_identifiers,
                    "defaultReasons": list_default_reasons,
                    "defaultAutoAddEnabled": str(autoadd).lower(),
                    "defaultNativeEnabled": str(native_ban).lower(),
                    "nativeBanTTL": None,
                    "nativeBanTempMaxExpires": None,
                    "nativeBanPermMaxExpires": None
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}"
                        }
                    },
                    "owner": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_owner_id}"
                        }
                    }
                }
            }
        }
        return await utility._post_request(url=url, post=params, headers=self.headers)

    async def unsubscribe(self, banlist_id: str, organization_id: str) -> dict:
        """Unscubscribes from a banlist

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-banList-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}/relationships/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}

        Args:
            banlist_id (str): ID of the banlist
            organization_id (str): Your organization ID

        Returns:
            dict: Response from server.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/organizations/{organization_id}"
        return await utility._delete_request(url=url, headers=self.headers)

    async def list(self) -> dict:
        """Lists all your banlists for you.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banList-/ban-lists

        Returns:
            dict: A dictionary response of all the banlists you have access to.
        """
        url = f"{self.base_url}/ban-lists"
        params = {
            "include": "server,organization,owner",
            "page[size]": "100"
        }
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def subbed_orgs(self, banlist_id: str) -> dict:
        """Lists all the organizations that are subscribed to the targeted banlist. You require manage perms to use this list (or be the owner)

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banList-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}/relationships/organizations

        Args:
            banlist_id (str): The Banlist ID

        Returns:
            dict: A dictionary response of all the organizations subbed to the targeted banlist.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/organizations"
        params = {
            "include": "server,organization,owner",
            "page[size]": "100"
        }
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def sub_info(self, banlist_id: str, organization_id: str) -> dict:
        """_summary_

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banList-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}/relationships/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}

        Args:
            banlist_id (str): The ID of the targeted banlist.
            organization_id (_type_): The ID of the targeted organization subscribed to the targeted banlist.

        Returns:
            dict: A dictionary response of all the information requested.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/{organization_id}"
        params = {
            "include": "organization, owner, server"
        }
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def read(self, banlist_id: str) -> dict:
        """Retrieves the name of a banlist by the banlist id

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banList-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}

        Args:
            banlist_id (str): The ID of the banlist.

        Returns:
            dict: Returns a dictionary response of the requested data.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}"
        params = {
            "include": "owner"
        }
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def update(self, banlist_id: str, organization_id: str, action: str = None, autoadd: bool = None, ban_identifiers: list = None, native_ban: bool = None, list_default_reasons: list = None, ban_list_name: str = None) -> dict:
        """Updates the targeted banlist with the altered information you supply

        Documentation: https://www.battlemetrics.com/developers/documentation#link-PATCH-banList-/ban-lists/{(%23%2Fdefinitions%2FbanList%2Fdefinitions%2Fidentity)}/relationships/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}

        Args:
            banlist_id (str): Banlist ID.
            organization_id (str): Organization ID

            Optional paramaters default to the banlist settings.

            action (str, optional): "none", "log" or "kick"
            autoadd (bool, optional): True or False
            ban_identifiers (list, optional): ["steamID", "ip"]
            native_ban (bool, optional): True or False
            list_default_reasons (list, optional): [List of default reasons]
            ban_list_name (str, optional): Name of the banlist

        Returns:
            dict: Dictionary response of the new banlist.
        """
        banlist = await self.get_list(banlist_id=banlist_id)
        if not banlist:
            return None

        if action:
            banlist['attributes']['action'] = action
        if autoadd:
            banlist['attributes']['defaultAutoAddEnabled'] = str(
                autoadd).lower()
        if ban_identifiers:
            banlist['attributes']['defaultIdentifiers'] = ban_identifiers
        if native_ban:
            banlist['attributes']['defaultNativeEnabled'] = str(
                native_ban).lower()
        if list_default_reasons:
            banlist['attributes']['defaultReasons'] = list_default_reasons
        if ban_list_name:
            banlist['attributes']['name'] = ban_list_name
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/organizations/{organization_id}"
        return await utility._patch_request(url=url, post=banlist, headers=self.headers)

    async def get_list(self, banlist_id: str) -> dict:
        """Returns the banlist information of the targeted banlist

        Documentation: None. Custom code.

        Args:
            banlist_id (str): The ID of the banlist you want.

        Returns:
            dict: The dictionary response of the targeted banlist.
        """
        url = f"https://api.battlemetrics.com/ban-lists"
        params = {
            "page[size]: 100"
        }
        banlists = await utility._get_request(url=url, params=params, headers=self.headers)

        for banlist in banlists:
            if banlist['id'] == banlist_id:
                return banlist
        return None
