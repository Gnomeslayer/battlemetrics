import utility


class Flagplayer:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def flag_create(self, color: str, description: str, icon_name: str, flag_name: str, organization_id: int, user_id: int) -> dict:
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
        data = {
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

        return await utility._make_request(headers=self.headers, method="POST", url=url, data=data)

    async def flag_delete(self, flag_id: str) -> dict:
        """Delete an existing flag.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-playerFlag-/player-flags/{(%23%2Fdefinitions%2FplayerFlag%2Fdefinitions%2Fidentity)}

        Args:
            flag_id (str): The ID of the flag

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/player-flags/{flag_id}"

        return await utility._make_request(headers=self.headers, method="DELETE", url=url)

    async def flag_info(self, flag_id: str) -> dict:
        """Info for existing flag.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-playerFlag-/player-flags/{(%23%2Fdefinitions%2FplayerFlag%2Fdefinitions%2Fidentity)}

        Args:
            flag_id (str): The ID of the flag

        Returns:
            dict: Dictionary response of the flag data.
        """
        url = f"{self.base_url}/player-flags/{flag_id}"

        return await utility._make_request(headers=self.headers, method="GET", url=url)

    async def flag_list(self, filter_personal: bool = False) -> dict:
        """List existing player flags.

        Documentation:https://www.battlemetrics.com/developers/documentation#link-GET-playerFlag-/player-flags

        Args:
            filter_personal (bool, optional): Hide/show personal flags. Defaults to False.

        Returns:
            dict: Dictionary response of a list of flags.
        """

        url = f"{self.base_url}/player-flags"

        data = {
            "page[size]": "100",
            "include": "organization"
        }

        if filter_personal:
            data["filter[personal]"] = str(filter_personal).lower()

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

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
        data = {
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

        return await utility._make_request(headers=self.headers, method="PATCH", url=url, data=data)
