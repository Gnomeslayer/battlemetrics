from datetime import timedelta
import datetime
import json
from time import strftime, localtime

import aiohttp


class Helpers:

    def __init__(self, api_key: str) -> None:
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def _parse_octet_stream(self, response) -> dict:
        """Takes your banlist file from the API request and processes it into a dictionary
        Args:
            response (octet-stream): The file response from the API
        Returns:
            dict: Returns the converted file in dictionary form.
        """

        cfg_str = response.decode('utf-8')
        ban_dict = {}
        for line in cfg_str.split("\n"):
            if line.startswith("banid"):
                line_parts = line.split(" ")
                steam_id = line_parts[1]
                player_name = line_parts[2].strip('"')
                reason_parts = line_parts[3:-1]
                duration = line_parts[-1]
                if duration == "-1":
                    duration = "Permanent"
                if duration.isdigit():
                    duration = int(duration)
                    try:
                        duration = strftime(
                            '%Y-%m-%d %H:%M:%S', localtime(duration))
                    except:
                        duration = "FOREVER!"
                reason = " ".join(reason_parts).strip('"')
                ban_dict[steam_id] = {
                    "playername": player_name, "reason": reason, "expires": duration}
        return ban_dict

    async def _replace_char_at_position(self, input_string, position, new_character):
        return input_string[:position] + new_character + input_string[position + 1:]

    async def calculate_future_date(input_string):
        # Extract the numeric part and unit from the input string
        number = int(input_string[:-1])
        unit = input_string[-1]

        # Define a dictionary to map units to timedelta objects
        unit_to_timedelta = {
            'd': timedelta(days=number),
            'w': timedelta(weeks=number),
            'm': timedelta(days=number*30),  # Approximate for months
            'h': timedelta(hours=number),    # Hours
        }

        # Get the timedelta object based on the unit
        delta = unit_to_timedelta.get(unit)

        if delta:
            # Calculate the future date by adding the timedelta to the current date
            future_date = str(datetime.now() + delta)
            future_date = future_date.replace(" ", "T")
            future_date += "Z"
            return future_date
        else:
            return None

    async def _make_request(self, method: str, url: str, params: dict = None, json:dict= None) -> dict:
        """Queries the API and spits out the response.
        Args:
            method (str): One of: GET, POST, PATCH, DELETE
            url (str): The endpoint/url you wish to query.
            params (dict, optional): Any params you wish to send to enhance your experience?. Defaults to None.
            json (dict, optional): json data you wish to send to enhance your experience?. Defaults to None.
        Raises:
            Exception: Doom and gloom.
        Returns:
            dict: The response from the server.
        """

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.request(method=method, url=url, json=json, params=params) as r:
                if r:
                    response_content = await r.content.read()
                    response_status = r.status
                    content_type = r.headers.get('content-type', '')
                else:
                    print("Some error message here?")

        if response_status == '429':
            print("You're being rate limited by the API. Please wait a minute before trying again.")
            return
        if 'json' in content_type:
            #Try and convert the response to something we can handle.
            try:
                response = await response_content.json()
            except:
                #Attempt to fix any errors in the json response.
                response = await self.exception_handler(response_content)
        #This is dedicated if the user is attempting to download a banlist. Currently only allows RUST banlists.
        elif 'octet-stream' in content_type:
            response = await self._parse_octet_stream(await response.content.read())
        #Sometimes the API returns HTML responses. Lets handle those.
        elif "text/html" in content_type:
            response = await response.text()
            response = response.replace("'", "").replace("b", "")
        else:
            raise Exception(f"Unsupported content type: {content_type}")
        return response

    #This function attempts to find and fix any errors in the JSON response.
    async def exception_handler(self, response_content):
        json_string = response_content.decode('utf-8')
        json_dict = None
        loops = 0
        while not json_dict:
            if loops == 100000:
                print("Loop count reached..")
                break
            try:
                json_dict = json.loads(json_string)
            except json.decoder.JSONDecodeError as e:
                expecting = e.args[0].split()[1]
                expecting.replace("'", "")
                expecting.replace("\"", "")
                if len(expecting) == 3:
                    expecting = expecting.replace("'", "")
                else:
                    expecting = expecting.split()
                    expecting = f"\"{expecting[0]}\":"
                json_string = await self._replace_char_at_position(json_string, e.pos, expecting)
            loops += 1
        return json_dict
