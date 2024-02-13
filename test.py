import battlemetrics
import asyncio
import json

with open("config.json", "r") as f:
    config = json.load(f)

api = battlemetrics.Battlemetrics(config['tokens']['battlemetrics_token'])

response = asyncio.run(api.player.match_identifiers(identifier="76561199541364031", identifier_type="steamID"))