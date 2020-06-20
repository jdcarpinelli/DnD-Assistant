# Welcome to dungeons!
Tools for online dungeons and dragons, including dice rolling, Open5e searching, and Discord integration.

## Overview
This project is currently a single Discord bot, __DnD-Assistant__, written in Python with [discord.py](https://github.com/Rapptz/discord.py). 

__DnD-Assistant__ can...

1. Roll dice

2. Relay messages to other users on the Discord server

3. Search [Open5e](https://open5e.com) for information related to spells, monsters, classes, weapons, and more

## Credits

* As previously mentioned, this project uses the [discord.py](https://github.com/Rapptz/discord.py) library for interacting with the Discord API through Python.

* [Open5e](https://open5e.com) is also open source. See their [GitHub repository](https://github.com/eepMoody/open5e).

* The Open5e search functionality was merged from [shadowedlucario's Oghma repository](https://github.com/shadowedlucario/oghma).

Please give them a star!

## Issues
This project is currently in beta, if you find any bugs please submit them as issues, or send them via email.

## Setup and Installation

If you're just looking to add a bot with [Open5e](https://open5e.com) search functionality, you can simply add the public bot [Oghma](https://github.com/shadowedlucario/oghma/tree/master) on top.gg!

Otherwise, the current method for installing __DnD-Assistant__ is from source. 

1. [Add a bot to your Discord account](https://discordpy.readthedocs.io/en/latest/discord.html) (it's recommended you use the bot name "DnD-Assistant")

2. Install [Python 3.8](https://www.python.org/downloads/)

3. Clone __dungeons__
```
git clone https://github.com/cadojo/dungeons/
```

4. Install the python3.8 dependencies
```
# CD into wherever you cloned dungeons
cd dungeons

# Install pipenv if you haven't already
python3.8 -m pip install --upgrade pip
python3.8 -m pip install pipenv

# Install all dependencies to a virtual environment
pipenv install
```

5. Add contents to `dungeons/assistant/.env`
```
# Environment variables for DnD-Assistant
DISCORD_TOKEN=your-token-id-here
DISCORD_GUILD=your-guild-name-here
TOP_LEVEL_PATH=/path/to/dungeons
AUTHOR=name-of-author
```

6. Run the bot!
```
# Load the virtual environment
pipenv shell

# Run the bot
python assistant/bot.py
```
