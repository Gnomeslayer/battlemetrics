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

#Grab the battlemetrics identifiers from a steam identifier.
battlemetrics_identifiers = asyncio.run(bmapi.player.match_identifiers(identifier=example_steam_id, identifier_type="steamID"))

#Grab the complete profile from this user.
battlemetrics_user_identifier = battlemetrics_identifiers['data'][0]['relationships']['player']['data']['id']

#Grab the complete profile
player_info = asyncio.run(bmapi.player.info(identifier=battlemetrics_user_identifier))

#Grab the battlemetrics ID's for the users BEGUID and STEAMID
beguid_id = None
steamid_id = None
for included in player_info['included']:
    if included['type'] == "identifier":
        if included['attributes']['type'] == "BEGUID":
            beguid_id = included['id']
        if included['attributes']['type'] == "steamID":
            steamid_id = included['id']

#Creating the ban.
#only 1 identifier linked to the user is required to ban,
#In this example I chose to use 2.
asyncio.run(bmapi.player.add_ban(reason="Document Ban.",
                                              note="This was made for the purpose of documentation.",
                                              steamid_id=steamid_id,
                                              beguid_id=beguid_id,
                                              battlemetrics_id=battlemetrics_user_identifier,
                                              banlist=example_banlist,
                                              server_id=example_server_id,
                                              org_id=example_org_id))

