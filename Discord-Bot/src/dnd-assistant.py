## Dungeons and Dragons Assistant
# Discord bot to handle...
# dice rolling,
# relaying messages,
# roll tracking,
# and (maybe) eventually more!
# 
# Copied and modified code from:
# https://realpython.com/how-to-make-a-discord-bot-python/
#
##

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)


print('Shutting down...')
