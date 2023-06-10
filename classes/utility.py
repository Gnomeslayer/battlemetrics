import aiohttp
from time import strftime, localtime


async def _parse_octet_stream(response):
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
    return response


async def _make_request(headers: dict, method: str, url: str, data: dict = None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method=method, url=url, json=data, params=data) as r:
            content_type = r.headers.get('content-type', '')
            if 'json' in content_type:
                response = await r.json()
            elif 'octet-stream' in content_type:
                response = await _parse_octet_stream(await r.content.read())
            else:
                raise Exception(
                    f"Unsupported content type: {content_type}")
    return response
