from battlemetrics import Battlemetrics
import json
import asyncio

example_bmid = 579979635
example_steam_id = 76561198151275725
example_organization_id = 25433
example_banlist_id = "abc"
example_server_id = 1234

bmapi = Battlemetrics("Your battlemetrics token here.")

example = asyncio.run(bmapi.organization.info(organization_id=example_organization_id))
example = asyncio.run(bmapi.ban_list.search(banlist=example_banlist_id))
example = asyncio.run(bmapi.server.info(server_id=example_server_id))
example = asyncio.run(bmapi.player.search(example_bmid))
example = asyncio.run(bmapi.player.search(filter_online=True))
example = asyncio.run(bmapi.server.leaderboard_info(server_id=example_server_id))
example = asyncio.run(bmapi.player.match_identifiers(identifier=example_steam_id, type="steamID"))
example = asyncio.run(bmapi.player.quick_match(identifier=example_steam_id, type="steamID"))
example = asyncio.run(bmapi.server.search(server_type=['community'], rcon=False))
example = asyncio.run(bmapi.server.search(server_type=['modded', 'official'], rcon=False))

with open('example.json', 'w') as f:
    f.write(json.dumps(example, indent=4))
