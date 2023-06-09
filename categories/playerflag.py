import utility


class Playerflag:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def create(self, color: str, description: str, icon_name: str, flag_name: str, organization_id: int, user_id: int) -> dict:
        """Create a new flag

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-playerFlag-/player-flags

        Args:
            color (str): The color of the flag. pattern: ^#[0-9a-fA-F]{6}$
            description (str): Flag Description
            icon_name (str): Icon name. Refer to documentation
            flag_name (str): Name of flag
            organization_id (int): The organization ID the flag belongs to
            user_id (int): The User ID the flag is created by.

        Returns:
            dict: Response from server.
        """
        url = f"{self.base_url}/player-flags"
        params = {
            "data": {
                "type": "playerFlag",
                "attributes": {
                    "icon": f"{icon_name}",
                    "name": f"{flag_name}",
                    "color": f"{color}",
                    "description": f"{description}"
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}"
                        }
                    },
                    "user": {
                        "data": {
                            "type": "user",
                            "id": f"{user_id}"
                        }
                    }
                }
            }
        }

        return await utility._post_request(url=url, post=params, headers=self.headers)

    async def delete_flag(self, flag_id: str) -> dict:
        """Delete an existing flag.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-playerFlag-/player-flags/{(%23%2Fdefinitions%2FplayerFlag%2Fdefinitions%2Fidentity)}

        Args:
            flag_id (str): The ID of the flag

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/player-flags/{flag_id}"
        return await utility._delete_request(url=url, headers=self.headers)

    async def info(self, flag_id: str) -> dict:
        """Info for existing flag.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-playerFlag-/player-flags/{(%23%2Fdefinitions%2FplayerFlag%2Fdefinitions%2Fidentity)}

        Args:
            flag_id (str): The ID of the flag

        Returns:
            dict: Dictionary response of the flag data.
        """
        url = f"{self.base_url}/player-flags/{flag_id}"

        return await utility._get_request(url=url, headers=self.headers)

    async def flag_list(self, filter_personal: bool = False) -> dict:
        """List existing player flags.

        Documentation:https://www.battlemetrics.com/developers/documentation#link-GET-playerFlag-/player-flags

        Args:
            filter_personal (bool, optional): Hide/show personal flags. Defaults to False.

        Returns:
            dict: Dictionary response of a list of flags.
        """

        url = f"{self.base_url}/player-flags"

        params = {
            "page[size]": "100",
            "include": "organization"
        }

        if filter_personal:
            params["filter[personal]"] = str(filter_personal).lower()

        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def flag_update(self, flag_id: str, color: str, description: str, icon_name: str, flag_name: str) -> dict:
        """Create a new flag

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-playerFlag-/player-flags

        Args:
            color (str): The color of the flag. pattern: ^#[0-9a-fA-F]{6}$
            description (str): Flag Description
            icon_name (str): Icon name. Refer to documentation
            flag_name (str): Name of flag

        Returns:
            dict: Response from server.
        """
        url = f"{self.base_url}/player-flags/{flag_id}"
        params = {
            "data": {
                "type": "playerFlag",
                "id": f"{flag_id}",
                "attributes": {
                    "icon": f"{icon_name}",
                    "name": f"{flag_name}",
                    "color": f"{color}",
                    "description": f"{description}"
                }
            }
        }

        return await utility._patch_request(url=url, post=params, headers=self.headers)
