from . import utility


class Other:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.api_key = api_key

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

    async def banlist_get_list(self, banlist_id: str) -> dict:
        """Returns the banlist information of the targeted banlist

        Documentation: None. Custom code.

        Args:
            banlist_id (str): The ID of the banlist you want.

        Returns:
            dict: The dictionary response of the targeted banlist.
        """
        url = f"https://api.battlemetrics.com/ban-lists"
        data = {
            "page[size]: 100"
        }
        banlists = await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

        for banlist in banlists:
            if banlist['id'] == banlist_id:
                return banlist
        return None

    async def organization_info(self, organization_id: int) -> dict:
        """Returns an organizations profile.

        Documentation: Not documented in the API.

        Args:
            organization_id (int): An organizations battlemetrics ID.

        Returns:
            dict: The information about your organization or a targeted organization
        """

        url = f"{self.base_url}/organizations/{organization_id}"
        data = {
            "include": "organizationUser,banList,role,organizationStats"
        }

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def activity_logs(self, blacklist: str = None, whitelist: str = None) -> dict:
        """Retrieves the activity logs.

        Documentation: There is no documentation on this endpoint unfortunately.

        Args:
            blacklist (str, optional): Example: unknown, playerMessage. Defaults to None.
            whitelist (str, optional): unknown, playerMessage. Defaults to None.

        Returns:
            dict: _description_
        """
        url = f"{self.base_url}/activity"

        data = {
            "version": "^0.1.0",
            "filter[types][blacklist]": blacklist,
            "filter[types][whitelist]": whitelist,
            "page[size]": "100",
            "include": "organization,server,user,player"
        }

        return await utility._make_request(headers=self.headers, method="GET", url=url, data=data)

    async def check_api_scopes(self, api_key: str = None) -> dict:
        """Retrieves the tokens scopes from the oauth.
        Args:
            api_key (str, optional): Your given API token. Defaults to the one supplied to this battlemetrics class.
        Returns:
            dict: The tokens data.
        """
        if not api_key:
            api_key = self.api_key
        url = f"https://www.battlemetrics.com/oauth/introspect"
        data = {
            "token": api_key
        }
        return await utility._make_request(headers=self.headers, method="POST", url=url, data=data)
