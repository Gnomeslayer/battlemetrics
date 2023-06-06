import utility
from datetime import datetime, timedelta


class Leaderboard:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def get(self, server_id: int, player: int, start: str, end: str) -> dict:
        """Displays the leaderboard for a specific player.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-leaderboardPlayer-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}/relationships/leaderboards/time

        Args:
            server_id (int): The server ID
            player (int): Battlemetrics player ID
            start (str): UTC Start date. Defaults to 1 day ago.
            end (str): UTC End date. Defaults to today.

        Returns:
            dict: Returns the leaderboard information for the player.
        """
        if not start:
            # seven_days_ago = current_time - timedelta(days=1)
            # seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
            # start_date = seven_days_ago_str

            start = (datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') - timedelta(days=1)
                     ).strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end:
            end = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        params = {
            "page[size]": "100",
            "filter[period]": f"{start}:{end}",
            "filter[player]": player,
            "fields[leaderboardPlayer]": "name,value"
        }
        url = f"{self.base_url}/servers/{server_id}/relationships/leaderboards/time"
        return await utility._get_request(url=url, headers=self.headers, params=params)
