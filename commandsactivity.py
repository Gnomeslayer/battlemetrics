import utility
from datetime import datetime, timedelta


class CommandsActivity:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, organization_id: int, summary: bool = False, users: str = None, commands: str = None, time_start: str = None, time_end: str = None, servers: int = None) -> dict:
        """Grabs all the command activity related to the targeted organization

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-commandStats-/organizations/{(%23%2Fdefinitions%2Forganization%2Fdefinitions%2Fidentity)}/relationships/command-stats

        Args:
            organization_id (int): The Organization ID
            summary (bool, optional): A summary. Defaults to False.
            users (str, optional): Specific users?. Defaults to None.
            commands (str, optional): Specific Commands?. Defaults to None.
            time_start (str, optional): UTC start time. Defaults to 7 days ago.
            time_end (str, optional): UTC end time. Defaults to today.
            servers (int, optional): Targeted servers. Defaults to None.

        Returns:
            dict: Returns command usage data.
        """

        if not time_start:
            now = datetime.utcnow()
            time_start = now - timedelta(days=7)
            time_start = time_start.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not time_end:
            time_end = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        params = {
            "filter[timestamp]": f"{time_start}:{time_end}"
        }
        if summary:
            params['filter[summary]'] = str(summary).lower()
        if users:
            params['filter[users]'] = users

        if commands:
            params['filter[commands]'] = commands
        if servers:
            params['filter[servers]'] = servers

        url = f"{self.base_url}/organizations/{organization_id}/relationships/command-stats"
        return await utility._get_request(url=url, headers=self.headers, params=params)
