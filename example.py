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

bmapi = Battlemetrics(config = config['tokens']['battlemetrics_token'])


example = asyncio.run(bmapi.ban_list.rust_banlist_export(organization_id=25433, server_id=11334532))

with open('example.json', 'w') as f:
    f.write(json.dumps(example, indent=4))