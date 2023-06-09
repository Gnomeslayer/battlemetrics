import utility
from datetime import datetime, timedelta


class Organizationstats:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, organization_id: int, start: str, end: str, game: str = None) -> dict:
        """Gets the player stats for the organization

        Documentation: https://www.battlemetrics.com/developers/documentation#resource-organizationStats

        Args:
            organization_id (int): Organization ID
            start (str): UTC start time. Defaults to 7 days ago.
            end (str): UTC end time. Defaults to today.
            game (str, optional): Targeted game, example: rust. Defaults to None.

        Returns:
            dict: Player stats for the organization.
        """
        if not start:
            now = datetime.utcnow()
            start = now - timedelta(days=1)
            start = start.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end:
            end = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/organizations/{organization_id}/stats/players"

        params = {
            "filter[range]": f"{start}:{end}"
        }
        if game:
            params["filter[game]"] = game

        return await utility._get_request(url=url, headers=self.headers, params=params)
