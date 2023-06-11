from . import utility


class Other:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    activity_list = ["unknown",
                     "triggerNotice",
                     "event: removePlayer",
                     "event: addPlayer",
                     "adminLog",
                     "playerMessage",
                     "rustLog: playerDeath: radiation",
                     "rustLog: playerDeath: animal",
                     "rustLog: playerDeath: thirst",
                     "rustLog: playerDeath: heat",
                     "rustLog: playerDeath: fall",
                     "rustLog: playerDeath: poison",
                     "rustLog: playerDeath: hunger",
                     "rustLog: playerDeath: blunt",
                     "rustLog: playerDeath: bleeding",
                     "rustLog: playerDeath: drowned",
                     "rustLog: playerDeath: cold",
                     "rustLog: playerDeath: entity",
                     "rustLog: playerDeath: died",
                     "rustLog: playerDeath: suicide",
                     "rustLog: playerDeath: PVP",
                     "rustLog: publisherBanned",
                     "rustLog: playerReport",
                     "rustLog: eacKick",
                     "rustLog: antiHack",
                     "rustLog: oxideClans2087",
                     "rustLog: playerPM",
                     "rustLog: playerWarning",
                     "rustLog: warning",
                     "rustLog: event",
                     "rustLog: rejectedConnection",
                     "rustLog: rconCommand",
                     "rustLog: saveStats",
                     "event: query"]

    async def activity(self, blacklist: str = None, whitelist: str = None) -> dict:
        """Retrieves the activity logs.

        Documentation: There is no documentation on this endpoint unfortunately.

        Args:
            blacklist (str, optional): Example: unknown, playerMessage. Defaults to None.
            whitelist (str, optional): unknown, playerMessage. Defaults to None.

        Returns:
            dict: _description_
        """
        url = f"{self.base_url}/activity"

        params = {
            "version": "^0.1.0",
            "filter[types][blacklist]": blacklist,
            "filter[types][whitelist]": whitelist,
            "page[size]": "100",
            "include": "organization,server,user,player"
        }

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=params)

    async def activity_options(self) -> str:
        """Returns a list of all your activity whitelist/blacklist options to use in the activity function

        Returns:
            str: Words
        """

        for activity in self.activity_list:
            print(activity)
        return self.activity_list