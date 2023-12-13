from battlemetrics import Battlemetrics
import json
import asyncio

with open("config.json", "r") as f:
    config = json.load(f)

battlemetrics_token = config['tokens']['battlemetrics_token']

example_bmid = 579979635
example_steam_id = 76561198151275725
example_organization_id = 25433
example_banlist_id = "abc"
example_server_id = 1234

bmapi = Battlemetrics(battlemetrics_token)

#example = asyncio.run(api.organization_friend_list(organization_id=example_organization_id))

#example = asyncio.run(api.ban_list_search(banlist=example_banlist_id))

#example = asyncio.run(api.server_info(server_id=example_server_id))

example = asyncio.run(bmapi.player.player_info(example_bmid))

#example = asyncio.run(api.player_list(filter_online=True))

#example = asyncio.run(api.leaderboard_info(server_id=example_server_id))

#example = asyncio.run(api.player_match_identifiers(identifier=example_steam_id, type="steamID"))

#example = asyncio.run(api.player_quick_match(identifier=example_steam_id, type="steamID"))

#example = asyncio.run(api.server_list(server_type=['community'], rcon=False))

#example = asyncio.run(api.server_list(server_type=['modded', 'official'], rcon=False))

with open('example.json', 'w') as f:
    f.write(json.dumps(example, indent=4))
