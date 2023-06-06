import utility
import uuid


class Organizationfriend:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def friends(self, organization_id: str, filter_accepted: bool = True, filter_origin: bool = True, filter_name: str = None, filter_reciprocated: bool = True) -> dict:
        """Gets all the organization friends.

        Documentation: https://www.battlemetrics.com/developers/documentation#resource-organizationFriend

        Args:
            organization_id (str): Your organization ID
            filter_accepted (bool, optional): True or False. Have they accepted our friendship?. Defaults to True.
            filter_origin (bool, optional): True or False. Defaults to True.
            filter_name (str, optional): Name of a specific organization. Defaults to None.
            filter_reciprocated (bool, optional): True or False. Are the feelings mutual?. Defaults to True.

        Returns:
            dict: Returns all the friendship information based on the paramaters set.
        """
        url = f"{self.base_url}/organizations/{organization_id}/relationships/friends"
        params = {
            "include": "organization",
            "filter[accepted]": str(filter_accepted).lower(),
            "filter[origin]": str(filter_origin).lower(),
            "filter[reciprocated]": str(filter_reciprocated).lower()
        }
        if filter_name:
            params['filter[name]'] = filter_name

        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def organization_friend(self, organization_id: int, friend_organization_id: int) -> dict:
        """Gets the friend information for your organization.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-organizationFriend-/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}/relationships/friends/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}

        Args:
            organization_id (int): Your organization ID
            friend_organization_id (int): Friend organization ID

        Returns:
            dict: Dictionary response about the organization friendship
        """

        url = f"{self.base_url}/organizations/{organization_id}/relationships/friends/{friend_organization_id}"

        params = {
            "include": "organization,playerFlag,organizationStats"
        }

        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def update_friendship(self, organization_id: int, friend_organization_id: int, identifiers: list, playerflag: str, shared_notes: bool = True, accepted: bool = True) -> dict:
        """Updates your organizations friendship.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-PATCH-organizationFriend-/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}/relationships/friends/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}

        Args:
            organization_id (int): Your organization ID
            friend_organization_id (int): The friendly organizations ID.
            identifiers (list): [ip, steamID], identifiers to be shared.
            shared_notes (bool, optional): Sharing Notes?
            accepted (bool, optional):Accepted friendship?

        Returns:
            dict: Returns a dictionary response on the new updated friendship.
        """

        url = f"https://api.battlemetrics.com/organizations/{organization_id}/relationships/friends/{friend_organization_id}"
        json = {
            "data": {
                "id": friend_organization_id,
                "type": "organizationFriend",
                "attributes": {
                    "accepted": str(accepted).lower(),
                    "identifiers": identifiers,
                    "notes": str(shared_notes).lower()
                }
            }
        }

        return await utility._patch_request(url=url, post=json, headers=self.headers)

    async def create(self, organization_id: int, friendly_org: int, identifiers: list, shared_notes: bool = True) -> dict:
        """Creates a new friend invite to the targeted organization ID

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-organizationFriend-/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}/relationships/friends

        Args:
            organization_id (int): Your organization ID
            friendly_org (int): Targeted organization ID
            identifiers (list): ["steamID", "ip"]
            shared_notes (bool, optional): Sharing notes? Defaults to True.

        Returns:
            dict: Returns the dictionary response from the server
        """
        url = f"https://api.battlemetrics.com/organizations/{organization_id}/relationships/friends"
        json = {
            "data": {
                "type": "organizationFriend",
                "attributes": {
                    "identifiers": identifiers,
                    "notes": str(shared_notes).lower()
                },
                "relationships": {
                    "friend": {
                        "data": {
                            "type": "organization",
                            "id": f"{friendly_org}"
                        }
                    },
                    "flagsShared": {
                        "data": [
                            {
                                "type": "playerFlag",
                                "id": f"{uuid.uuid5}"
                            }
                        ]
                    }
                }
            }
        }

        return await utility._post_request(url=url, post=json, headers=self.headers)

    async def delete(self, organization_id: int, friends_id: int) -> dict:
        """Deletes a friendship

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-organizationFriend-/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}/relationships/friends/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}

        Args:
            organization_id (int): Your organization ID
            friends_id (int): Friends organization ID

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/organizations/{organization_id}/relationships/friends/{friends_id}"
        return await utility._delete_request(url=url, headers=self.headers)
