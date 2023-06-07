import utility
from datetime import datetime, timedelta


class Datapoint:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def metrics(self, name: str = "games.rust.players", start_date: str = None, end_date: str = None, resolution: str = "60") -> dict:
        """A data point as used in time series information.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-dataPoint-/metrics

        Args:
            name (str, optional): "games.{game}.players" and "games.{game}.players.steam", defaults to "games.rust.players"
            start_date (str, optional) UTC time format. Defaults to Current Date.
            end_date (str, optional): UTC time format. Defaults to 1 day ago.
            resolution (str, optional): raw, 30, 60 or 1440. Defaults to "60".

        Returns:
            dict: a bunch of numbers.
        """
        url = f"{self.base_url}/metrics"
        # current_time = datetime.utcnow()
        # current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not start_date:
            now = datetime.utcnow()
            start_date = now - timedelta(days=1)
            start_date = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        params = {
            "metrics[0][name]": name,
            "metrics[0][range]": f"{start_date}:{end_date}",
            "metrics[0][resolution]": resolution
        }

        return await utility._get_request(url=url, headers=self.headers, params=params)
