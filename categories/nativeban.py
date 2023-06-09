import utility


class NativeBan:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, server: int = None, ban: str = None) -> dict:
        """Returns all the native bans

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banNative-/bans-native

        Args:
            server (int, optional): Target server. Defaults to None.
            ban (int, optional): Target ban. Defaults to None.

        Returns:
            dict: All native bans.
        """

        params = {
            "page[size]": "100",
            "include": "server,ban",
            "sort": "-createdAt",
            "fields[ban]": "reason",
            "fields[server]": "name",
            "fields[banNative]": "createdAt,reason"
        }

        if ban:
            params["filter[ban]"] = ban
        if server:
            params["filter[server]"] = server
        url = f"{self.base_url}/bans-native"
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def force_update(self, native_id: str) -> dict:
        """Forces an update on a native ban

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-banNative-/bans-native/{(%23%2Fdefinitions%2FbanNative%2Fdefinitions%2Fidentity)}/force-update

        Args:
            native_id (str): Targeted native ban

        Returns:
            dict: Response from the server.
        """
        url = f"{self.base_url}/bans-native/{native_id}/force-update"
        return await utility._post_request(url=url, post=None, headers=self.headers)
