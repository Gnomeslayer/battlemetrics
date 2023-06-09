import utility


class BanListExemptions:
    def __init__(self, api_key):
        self.base_url = "https://api.battlemetrics.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def next(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def previous(self, url: str):
        return await utility._get_request(url=url, headers=self.headers)

    async def create(self, banid: str, organization_id: int, reason: str = None) -> dict:
        """Creates an exemption to the banlist.

        Documentation: https://www.battlemetrics.com/developers/documentation#link-POST-banExemption-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}/relationships/exemptions

        Args:
            banid (str): The banid you want to create an exemption for.
            organization_id (str): The organization associated to the exemption
            reason (str, optional): Reason for the exemption. Defaults to None.

        Returns:
            dict: Whether it was successful or not.
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"
        json_post = {
            "data": {
                "type": "banExemption",
                "attributes": {
                        "reason": reason
                },
                "relationships": {
                    "organization": {
                        "data": {
                            "type": "organization",
                            "id": f"{organization_id}"
                        }
                    }
                }
            }
        }
        return await utility._post_request(url=url, post=json_post, headers=self.headers)

    async def delete(self, banid: str) -> dict:
        """Deletes an exemption

        Documentation: https://www.battlemetrics.com/developers/documentation#link-DELETE-banExemption-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}/relationships/exemptions

        Args:
            banid (str): The ban that has an exemption

        Returns:
            dict: Whether it was successful or not
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"
        return await utility._delete_request(url=url, headers=self.headers)

    async def info_single(self, banid: str, exemptionid: str) -> dict:
        """Pulls information from a ban regarding a specific exemption

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banExemption-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}/relationships/exemptions/{(%23%2Fdefinitions%2FbanExemption%2Fdefinitions%2Fidentity)}

        Args:
            banid (str): Target ban
            exemptionid (str): Target exemption

        Returns:
            dict: Information about the exemption
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions/{exemptionid}"
        return await utility._get_request(url=url, headers=self.headers)

    async def info_all(self, banid: str) -> dict:
        """Pulls all exemptions related to the targeted ban

        Documentation: https://www.battlemetrics.com/developers/documentation#link-GET-banExemption-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}/relationships/exemptions

        Args:
            banid (str): Target ban

        Returns:
            dict: All ban exemptions
        """
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"

        params = {
            "fields[banExemption]": "reason"
        }
        return await utility._get_request(url=url, headers=self.headers, params=params)

    async def update(self, banid: str, exemptionid: str, reason: str) -> dict:
        """Updates a ban exemption

        Documentation: https://www.battlemetrics.com/developers/documentation#link-PATCH-banExemption-/bans/{(%23%2Fdefinitions%2Fban%2Fdefinitions%2Fidentity)}/relationships/exemptions

        Args:
            banid (str): The target ban
            exemptionid (str): The target exemption
            reason (str): New reason

        Returns:
            dict: Whether you were successful or not.
        """
        banexemption = await self.info_single(banid=banid, exemptionid=exemptionid)
        banexemption['data']['attributes']['reason'] = reason
        url = f"{self.base_url}/bans/{banid}/relationships/exemptions"
        return await utility._patch_request(url=url, post=banexemption, headers=self.headers)
