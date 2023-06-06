import utility
from datetime import datetime, timedelta


class Organization:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def player_stats(self, organization_id: int, start_date: str = None, end_date: str = None) -> dict:
        """Returns the statistics of all the players who have joined your server and where they're from.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-organization-/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}/stats/players

        Args:
            organization_id (int): Your organization ID
            start_date (str, optional): Start date, max 90 days. Defaults to 90 days ago.
            end_date (str, optional): End date, defaults to now.

        Returns:
            dict: Returns a dictionary of all the stats!
        """
        url = f"{self.base_url}/organizations/{organization_id}/stats/players"
        if not start_date:
            now = datetime.utcnow()
            start_date = now - timedelta(days=90)
            start_date = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        params = {
            "filter[game]": "rust",
            "filter[range]": f"{start_date}:{end_date}"
        }

        return await utility._get_request(url=url, headers=self.headers, params=params)
