from battlemetrics.http import HTTPClient, Route


class BanList:
    """A class regarding the banlist component of the Battlemetrics API."""

    def __init__(self, http: HTTPClient, base_url: str) -> None:
        self.http = http
        self.base_url = base_url

    async def rust_banlist_export(
        self,
        organization_id: int,
        server_id: int | None = None,
    ) -> list[dict]:
        """Export your rust banlist.

        Parameters
        ----------
            organization_id (int): Organization ID the banlist belongs to
            server_id (int): Server ID the banlist is associated with.

        Returns
        -------
            list[dict]: A list of dictionaries that provide the ban data.
        """
        url = f"{self.base_url}/bans/export"
        params = {
            "filter[organization]": organization_id,
            "format": "rust/bans.cfg",
        }
        if server_id:
            params["filter[server]"] = server_id

        return await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=params,
        )

    # TODO: PLR0913 - To many parameters
    async def create_invite(
        self,
        organization_id: int,
        banlist_id: str,
        uses: int = 1,
        limit: int = 1,
        *,
        permmanage: bool = False,
        permcreate: bool = False,
        permupdate: bool = False,
        permdelete: bool = False,
    ) -> dict:
        """Create an invite.

        Parameters
        ----------
            organization_id (int): The target organization to be invited.
            banlist_id (str): The ID of the banlist you want to create the invite for
            permManage (bool): Are they allowed to manage it?
            permCreate (bool): Can they create stuff related to this banlist?
            permUpdate (bool): Can they update the banlist?
            permDelete (bool): Can they delete stuff related to this banlist?
            uses (int, optional): Number of times this banlist invite has been used.. Defaults to 1.
            limit (int, optional): How many times it's allowed to be used. Defaults to 1.

        Returns
        -------
            dict: Returns whether it was successful or not.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/invites"
        data = {
            "data": {
                "type": "banListInvite",
                "attributes": {
                    "uses": uses,
                    "limit": limit,
                    "permManage": permmanage,
                    "permCreate": permcreate,
                    "permUpdate": permupdate,
                    "permDelete": permdelete,
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}",
                        },
                    },
                },
            },
        }
        return await self.http.request(
            Route(
                method="POST",
                url=url,
            ),
            json=data,
        )

    async def read_invitation(self, invite_id: str) -> dict:
        """See the information about a specific banlist invite, such as uses.

        Paramaters
        ----------
            invite_id (str): The banlist invite id.

        Returns
        -------
            dict: The banlist invite information
        """
        url = f"{self.base_url}/ban-list-invites/{invite_id}"
        data = {
            "include": "banList",
            "fields[organization]": "tz,banTemplate",
            "fields[user]": "nickname",
            "fields[banList]": "name, action",
            "fields[banListInvite]": "uses",
        }
        return await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=data,
        )

    async def invite_list(self, banlist_id: str) -> dict:
        """Return all the invites for a specific banlist ID.

        Parameters
        ----------
            banlist_id (str): The ID of a banlist
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/invites"
        data = {
            "include": "banList",
            "fields[organization]": "tz,banTemplate",
            "fields[user]": "nickname",
            "fields[banList]": "name,action",
            "fields[banListInvite]": "uses",
            "page[size]": "100",
        }
        return await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=data,
        )

    async def delete_invite(self, banlist_id: str, banlist_invite_id: str) -> dict:
        """Delete an invite from a targeted banlist.

        Parameters
        ----------
            banlist_id (str): The target banlist
            banlist_invite_id (str): The target invite.

        Returns
        -------
            dict: Whether it was successful or not.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/invites/{banlist_invite_id}"
        return await self.http.request(
            Route(
                method="DELETE",
                url=url,
            ),
        )

    async def exemption_create(
        self,
        banid: str,
        organization_id: int,
        reason: str | None = None,
    ) -> dict:
        """Create an exemption to the banlist.

        Parameters
        ----------
            banid (str): The banid you want to create an exemption for.
            organization_id (str): The organization associated to the exemption
            reason (str, optional): Reason for the exemption. Defaults to None.

        Returns
        -------
            dict: Whether it was successful or not.
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"
        data = {
            "data": {
                "type": "banExemption",
                "attributes": {
                    "reason": reason,
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}",
                        },
                    },
                },
            },
        }
        return await self.http.request(
            Route(
                method="POST",
                url=url,
            ),
            json=data,
        )

    async def exemption_delete(self, banid: str) -> dict:
        """Delete an exemption.

        Parameters
        ----------
            banid (str): The ban that has an exemption
        Returns:
            dict: Whether it was successful or not
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"
        return await self.http.request(Route(method="DELETE", url=url))

    async def exemption_info_single(self, banid: str, exemptionid: str) -> dict:
        """Pull information from a ban regarding a specific exemption.

        Parameters
        ----------
            banid (str): Target ban
            exemptionid (str): Target exemption
        Returns:
            dict: Information about the exemption
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions/{exemptionid}"
        return await self.http.request(Route(method="GET", url=url))

    async def exemption_info_all(self, banid: str) -> dict:
        """Pull all exemptions related to the targeted ban.

        Parameters
        ----------
            banid (str): Target ban
        Returns:
            dict: All ban exemptions
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"
        data = {
            "fields[banExemption]": "reason",
        }
        return await self.http.request(Route(method="GET", url=url), params=data)

    async def exemption_update(self, banid: str, exemptionid: str, reason: str) -> dict:
        """Update a ban exemption.

        Parameters
        ----------
            banid (str): The target ban
            exemptionid (str): The target exemption
            reason (str): New reason

        Returns
        -------
            dict: Whether you were successful or not.
        """
        banexemption = await self.exemption_info_single(banid=banid, exemptionid=exemptionid)
        banexemption["data"]["attributes"]["reason"] = reason
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"
        return await self.http.request(Route(method="PATCH", url=url), json=banexemption)

    # TODO: PLR0913 - To many parameters
    async def create(  # noqa: PLR0913
        self,
        organization_id: int,
        action: str,
        ban_identifiers: list,
        list_default_reasons: list,
        ban_list_name: str,
        *,
        autoadd: bool = False,
        native_ban: bool = False,
    ) -> dict:
        """Create a new banlist for your targeted organization.

        Parameters
        ----------
            organization_id (int): The organization ID.
            action (str): "none", "log", "kick"
            ban_identifiers (list): ["steamID", "ip"]
            list_default_reasons (list): List of default reasons for the ban.
            ban_list_name (str): Name of the ban list.
            autoadd (bool, optional): true or false. Defaults to False.
            native_ban (bool, optional): Whether this ban should be a native ban. Defaults to False.
        """
        url = f"{self.base_url}/ban-lists"
        data = {
            "data": {
                "type": "banList",
                "attributes": {
                    "name": f"{ban_list_name}",
                    "action": f"{action}",
                    "defaultIdentifiers": ban_identifiers,
                    "defaultReasons": list_default_reasons,
                    "defaultAutoAddEnabled": str(autoadd).lower(),
                    "defaultNativeEnabled": str(native_ban).lower(),
                    "nativeBanTTL": None,
                    "nativeBanTempMaxExpires": None,
                    "nativeBanPermMaxExpires": None,
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}",
                        },
                    },
                    "owner": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}",
                        },
                    },
                },
            },
        }
        return await self.http.request(
            Route(
                method="POST",
                url=url,
            ),
            json=data,
        )

    # TODO: To many arguments
    async def accept_invite(
        self,
        code: str,
        action: str,
        ban_identifiers: list,
        list_default_reasons: list,
        organization_id: str,
        organization_owner_id: str,
        *,
        autoadd: bool,
        native_ban: bool,
    ) -> dict:
        """Accept an invitation to subscribe to a banlist.

        Parameters
        ----------
            code (str): Invitation code.
            action (str): "none", "log" or "kick"
            autoadd (bool): True or False
            ban_identifiers (list): ["steamID", "ip"]
            native_ban (bool): True or False
            list_default_reasons (list): ["Banned for hacking"]
            organization_id (str): ID of your organization?
            organization_owner_id (str): ID of the owner of the organization
        Returns:
            dict: Response from server.
        """
        url = f"{self.base_url}/ban-lists/accept-invite"
        data = {
            "data": {
                "type": "banList",
                "attributes": {
                    "code": code,
                    "action": action,
                    "defaultIdentifiers": ban_identifiers,
                    "defaultReasons": list_default_reasons,
                    "defaultAutoAddEnabled": str(autoadd).lower(),
                    "defaultNativeEnabled": str(native_ban).lower(),
                    "nativeBanTTL": None,
                    "nativeBanTempMaxExpires": None,
                    "nativeBanPermMaxExpires": None,
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}",
                        },
                    },
                    "owner": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_owner_id}",
                        },
                    },
                },
            },
        }
        return await self.http.request(
            Route(
                method="POST",
                url=url,
            ),
            json=data,
        )

    async def unsubscribe(self, banlist_id: str, organization_id: str) -> dict:
        """Unsubscribe from a banlist.

        Parameters
        ----------
            banlist_id (str): ID of the banlist
            organization_id (str): Your organization ID

        Returns
        -------
            dict: Response from server.
        """
        url = (
            f"{self.base_url}/ban-lists/{banlist_id}/relationships/organizations/{organization_id}"
        )
        return await self.http.request(Route(method="DELETE", url=url))

    async def subscribed_orgs(self, banlist_id: str) -> dict:
        """List all the organizations that are subscribed to the targeted banlist.

        You require manage perms to use this list (or be the owner).

        Parameters
        ----------
            banlist_id (str): The Banlist ID

        Returns
        -------
            dict: A dictionary response of all the organizations subbed to the targeted banlist.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/organizations"
        data = {
            "include": "server,organization,owner",
            "page[size]": "100",
        }
        return await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=data,
        )

    async def subscribers(self, banlist_id: str, organization_id: str) -> dict:
        """Get the subscriber information for a specific banlist.

        Parameters
        ----------
            banlist_id (str): The ID of the targeted banlist.
            organization_id (_type_): The ID of the targeted organization subscribed to the banlist.

        Returns
        -------
            dict: A dictionary response of all the information requested.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}/relationships/{organization_id}"
        data = {
            "include": "organization, owner, server",
        }
        return await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=data,
        )

    # TODO: Give a different name
    async def read(self, banlist_id: str) -> dict:
        """Retrieve the name of a banlist by the banlist id.

        Parameters
        ----------
            banlist_id (str): The ID of the banlist.

        Returns
        -------
            dict: Returns a dictionary response of the requested data.
        """
        url = f"{self.base_url}/ban-lists/{banlist_id}"
        data = {
            "include": "owner",
        }
        return await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=data,
        )

    # TODO: Update documentation for autoadd and native_ban.
    # TODO: PLR0913 - To many parameters
    async def update(  # noqa: PLR0913
        self,
        banlist_id: str,
        organization_id: str,
        action: str | None = None,
        ban_identifiers: list | None = None,
        list_default_reasons: list | None = None,
        ban_list_name: str | None = None,
        *,
        autoadd: bool | None = None,
        native_ban: bool | None = None,
    ) -> dict:
        """Update the targeted banlist with the altered information you supply.

        Parameters
        ----------
            banlist_id (str): Banlist ID.
            organization_id (str): Organization ID
            Optional paramaters default to the banlist settings.
            action (str, optional): "none", "log" or "kick"
            autoadd (bool, optional): True or False
            ban_identifiers (list, optional): ["steamID", "ip"]
            native_ban (bool, optional): True or False
            list_default_reasons (list, optional): [List of default reasons]
            ban_list_name (str, optional): Name of the banlist

        Returns
        -------
            dict: Dictionary response of the new banlist.
        """
        banlist = await self.get_list(banlist_id=banlist_id)
        if not banlist:
            return None
        if action:
            banlist["attributes"]["action"] = action
        if autoadd:
            banlist["attributes"]["defaultAutoAddEnabled"] = str(autoadd).lower()
        if ban_identifiers:
            banlist["attributes"]["defaultIdentifiers"] = ban_identifiers
        if native_ban:
            banlist["attributes"]["defaultNativeEnabled"] = str(native_ban).lower()
        if list_default_reasons:
            banlist["attributes"]["defaultReasons"] = list_default_reasons
        if ban_list_name:
            banlist["attributes"]["name"] = ban_list_name
        url = (
            f"{self.base_url}/ban-lists/{banlist_id}/relationships/organizations/{organization_id}"
        )
        return await self.http.request(
            Route(
                method="PATCH",
                url=url,
            ),
            json=banlist,
        )

    async def get_list(self, banlist_id: str | None = None) -> dict:
        """Return the banlist information of the targeted banlist.

        Parameters
        ----------
            banlist_id (str): The ID of the banlist you want.

        Returns
        -------
            dict: The dictionary response of the targeted banlist.
        """
        url = "https://api.battlemetrics.com/ban-lists"
        data = {
            "page[size]": "100",
            "include": "organization,owner,server",
        }
        banlists = await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=data,
        )
        for banlist in banlists:
            if banlist["id"] == banlist_id:
                return banlist
        return banlists

    async def list(self) -> dict:
        """List all your banlists for you.

        Returns
        -------
            dict: A dictionary response of all the banlists you have access to.
        """
        url = f"{self.base_url}/ban-lists"
        data = {
            "include": "server,organization,owner",
            "page[size]": "100",
        }
        return await self.http.request(
            Route(
                method="GET",
                url=url,
            ),
            params=data,
        )
