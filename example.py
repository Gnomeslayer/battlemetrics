from battlemetrics import Battlemetrics
import json
import asyncio

with open('config.json', 'r') as f:
    config = json.load(f)

example_bmid = 579979635
example_steam_id = 76561198151275725
example_banlist = "d8461f90-fbfe-11e9-a94e-7d2750722003"
example_server_id = 3298068
example_org_id = 13771

bmapi = Battlemetrics(config['tokens']['battlemetrics_token'])

#example = asyncio.run(bmapi.organization.info(organization_id=example_organization_id))
#example = asyncio.run(bmapi.ban_list.get_list(banlist=example_banlist_id))
#example = asyncio.run(bmapi.server.leaderboard_info(server_id=example_server_id))
#example = asyncio.run(bmapi.player.match_identifiers(identifier=example_steam_id, type="steamID"))
#example = asyncio.run(bmapi.player.quick_match(identifier=example_steam_id, type="steamID"))
#example = asyncio.run(bmapi.server.search(server_type=['community'], rcon=False))
#example = asyncio.run(bmapi.server.search(server_type=['modded', 'official'], rcon=False))
#example = asyncio.run(bmapi.server.info(server_id=example_server_id))
#example = asyncio.run(bmapi.player.search(example_bmid))
#example = asyncio.run(bmapi.player.search(filter_online=True))
#example = asyncio.run(bmapi.player.play_history(player_id=example_bmid, server_id=example_server_id))
example = asyncio.run(bmapi.player.session_history(player_id=982404963))
#example = asyncio.run(bmapi.activity_logs(filter_bmid=1121979267, whitelist="rustLog:playerReport"))

with open('example.json', 'w') as f:
    f.write(json.dumps(example, indent=4))
