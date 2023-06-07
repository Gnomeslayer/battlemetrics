import utility
from datetime import datetime, timedelta


class Coplay:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, player_id: int, time_start: str = None, time_end: str = None, player_names: str = None, organization_names: str = None, server_names: str = None) -> dict:
        """Gets the coplay data related to the targeted player

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-coplayRelation-/players/{(%23%2Fdefinitions%2Fplayer%2Fdefinitions%2Fidentity)}/relationships/coplay

        Args:
            player_id (int): The BATTLEMETRICS id of the targeted player
            time_start (str): UTC time start. Defaults to 7 days ago
            time_end (str): UTC time ends. Defaults to day.
            player_names (str, optional): Player names to target. Defaults to None.
            organization_names (str, optional): Specific Organizations. Defaults to None.
            server_names (str, optional): Specific servers. Defaults to None.

        Returns:
            dict: A dictionary response of all the coplay users.
        """

        if not time_start:
            now = datetime.utcnow()
            time_start = now - timedelta(days=1)
            time_start = time_start.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not time_end:
            time_end = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        params = {
            "filter[period]": f"{time_start}:{time_end}",
            "page[size]": "100",
            "fields[coplayrelation]": "name,duration"
        }

        if player_names:
            params["filter[players]"] = player_names
        if organization_names:
            params["filter[organizations]"] = organization_names
        if server_names:
            params["filter[servers]"] = server_names

        url = f"{self.base_url}/players/{player_id}/relationships/coplay"
        return await utility._get_request(url=url, headers=self.headers, params=params)
