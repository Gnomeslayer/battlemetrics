from battlemetrics import Battlemetrics
import json
import asyncio

with open("config.json", "r") as f:
    config = json.load(f)

example_bmid = 579979635
example_steam_id = 76561198151275725
example_banlist = "d8461f90-fbfe-11e9-a94e-7d2750722003"
example_server_id = 3298068
example_org_id = 13771

bmapi = Battlemetrics(config['tokens']['battlemetrics_token'])



#Creating the ban.
#Only requires a steam ID or Battlemetrics identifier.
#It will automagically grab everything it requires from there.
asyncio.run(bmapi.player.add_ban(reason="Document Ban.",
                                              note="This was made for the purpose of documentation.",
                                              battlemetrics_id=example_bmid,
                                              banlist=example_banlist,
                                              server_id=example_server_id,
                                              org_id=example_org_id))
