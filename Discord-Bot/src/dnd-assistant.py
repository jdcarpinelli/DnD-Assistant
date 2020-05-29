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

# Imports 
import sys, os, time, random
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load token, server name from local file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Create bot
bot = commands.Bot(command_prefix='!')

# On startup
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

# On event error
@bot.event
async def on_error(event, *args, **kwargs):
    with open('../logs/err'+str(int(time.time()*10e3))+'.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# On command error
@bot.event
async def on_command_error(ctx, error):
    await ctx.send('Invalid argument. Use "!help command" to find the proper usage.')

# Silly function
@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

# Roll dice
@bot.command(name='roll', help='Rolls 4, 6, 8, 10, 12, or 20 sided die.\n Examples: !roll 20 or !roll 3d6')
async def roll(ctx, roll_cmd):
    '''
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
    '''
    
    

if __name__ == '__main__':
    bot.run(TOKEN)
