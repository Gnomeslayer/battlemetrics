from battlemetrics import Battlemetrics
import asyncio

api = Battlemetrics("your token here")

player_info = asyncio.run(api.player.info(12345))