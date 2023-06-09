# Battlemetrics API Wrapper

This repository provides a Python wrapper for the Battlemetrics API, allowing users to easily access and interact with Battlemetrics data.

# Disclaimer
Please note that I am an individual member of the community and not affiliated with Battlemetrics. The resources provided here are developed to facilitate the usage of the Battlemetrics API but come with no official endorsement or sponsorship from Battlemetrics.

It's important to understand that any actions you take using these resources are solely your responsibility. I am not liable for any damage or consequences that may occur to your server or account. Please exercise caution and ensure that you follow best practices when using the API.

## Getting Started

To begin using the Battlemetrics API, make sure you have RCON access and an API token. If you don't have an API token yet, you can obtain one by visiting the [Battlemetrics developers page](https://www.battlemetrics.com/developers).

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Gnomeslayer/battlemetrics.git
   ```
2. Install the required dependencies
   Although at this time, the only dependency is aiohttp, so you can simply do:
   ```bash
   pip install aiohttp
   ```
   or you can do:
   ```bash
   pip install -r requirements.txt
   ```
3. Import the `Battlemetrics` class into your project.
   ```bash
   import battlemetrics
   ```
## Usage
Here's an example of how to use the Battlemetrics API wrapper:
```bash
# Instantiate the API wrapper with your token
token = "Your API token here"
api = battlemetrics
api.setup(token)

# Retrieve player information
player = api.player_info(12345)

# Print the player information
print(player)
```
Make sure to replace `"Your API token here"` with your actual API token obtained from the Battlemetrics developers page.

## Additional usage
Some endpoints have a pagination system, to get the "next" or "previous" page, pass through the link.
```bash
token = "Your API token here"
api = battlemetrics
api.setup(token)
game_list = asyncio.run(api.game_list())
game_list = asyncio.run(api.next())
print(test_data['pages'][0]) #Loading the page data.
or alternatively
print(test_data['pages'])
```

## Resources
For more details on the Battlemetrics API and its capabilities, refer to the official [Battlemetrics API](https://www.battlemetrics.com/developers/documentation).

## Contributing
If you find any issues or have suggestions for improvement, please feel free to submit a pull request or open an issue in the [issue tracker](https://github.com/Gnomeslayer/battlemetrics/issues). I welcome contributions from the community!

## Contact
You can contact me on Discord, simply add me: gnomeslayer
or, you can join the official [Battlemetrics discord](https://discord.gg/xWa3UNG4yh) and @gnomeslayer there.
