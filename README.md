# Battlemetrics API Wrapper

This repository allows users to quickly and easily pull data from the Battlemetrics API. Removing a lot of the guesswork when reading the API.

## Alternatives

### Javascript
For the javascript equivalent, visit this repository: https://github.com/cubiquitous/battlemetrics-js

# Disclaimer
Please note that I am an individual member of the community and not affiliated with Battlemetrics. The resources provided here are developed to facilitate the usage of the Battlemetrics API but come with no official endorsement or sponsorship from Battlemetrics.

It's important to understand that any actions you take using these resources are solely your responsibility. I am not liable for any damage or consequences that may occur to your server or account. Please exercise caution and ensure that you follow best practices when using the API.

## Getting Started

To begin using the Battlemetrics API, make sure you have RCON access and an API token. If you don't have an API token yet, you can obtain one by visiting the [Battlemetrics developers page](https://www.battlemetrics.com/developers).

## Installation

1. Clone or Install this repo:

   Clone this repository
   ```bash
   git clone https://github.com/Gnomeslayer/battlemetrics.git
   ```
   Pip install
   ```bash
   pip install battlemetrics
   ```

2. Install the required dependencies

   or you can do:
   ```bash
   pip install -r requirements.txt
   ```

3. Import the `Battlemetrics` class into your project.
   ```bash
   from battlemetrics import Battlemetrics
   ```

## Usage
Refer to example file for examples.
Here's an example of how to use the Battlemetrics API wrapper:
```bash
# Instantiate the API wrapper with your token
bmapi = battlemetrics("Your token here")

# Retrieve player information
player = asyncio.run(bmapi.player.search(12345))

# Print the player information
print(player)
```
Make sure to replace `"Your API token here"` with your actual API token obtained from the Battlemetrics developers page.


## Resources
For more details on the Battlemetrics API and its capabilities, refer to the official [Battlemetrics API](https://www.battlemetrics.com/developers/documentation).

## Contributing
If you find any issues or have suggestions for improvement, please feel free to submit a pull request or open an issue in the [issue tracker](https://github.com/Gnomeslayer/battlemetrics/issues). I welcome contributions from the community!

## Contact
You can contact me on Discord, simply add me: gnomeslayer
or, you can join the official [Battlemetrics discord](https://discord.gg/xWa3UNG4yh) and @gnomeslayer there.


## Suport
This repository will ALWAYS be free and hopefully regularly updated, but if you want to support me, you can do so [Here](https://ko-fi.com/gnomeslayer)