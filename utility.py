import aiohttp
import json
from time import strftime, localtime


async def _post_request(url, post: dict = None, headers: dict = None) -> dict:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=url, json=post) as r:
            response = await r.json()
    return response


async def _patch_request(url, post: dict = None, headers: dict = None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url=url, json=post) as r:
            response = await r.json()
    return response


async def _delete_request(url: str, headers: dict = None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.delete(url=url) as r:
            response = await r.json()
    return response


async def _get_request(url, headers: dict = None, params=None) -> dict:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, params=params) as r:
            content_type = r.headers.get('content-type', '')
            if 'json' in content_type:
                response = await r.json()
            elif 'octet-stream' in content_type:
                response = await r.content.read()
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
                response = ban_dict
                with open('test.json', 'w') as f:
                    f.write(json.dumps(ban_dict, indent=4))
                # If content type is octet-stream, write response to file
                # filename = 'response.bin'
                # with open(filename, 'wb') as f:
                #    while True:
                #        chunk = await r.content.read(1024)
                #        if not chunk:
                #            break
                #        f.write(chunk)
                # response = {'Saved the file as: ': filename}
            else:
                # If content type is not recognized, raise an exception
                raise Exception(
                    f"Unsupported content type: {content_type}")
    return response
