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
import dice 

# Load token, server name from local file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TOP_LEVEL_PATH = os.getenv('TOP_LEVEL_PATH')

# Bot invalid command messages
INVALID_CMD = \
    'Whoops! The roll command wasn\'t used correctly.\n' \
    'Try using the same format as the examples in "!help roll".'
INTERNAL_BUG = \
    'Congrats! That command you just sent resulted in an internal bug!' \
    'Sorry about that, this was jodoca\'s first attempt at a Bot.' \
    'Sending jodoca a DM with the command you sent would be really helpful!'

## Helper functions

# Returns timestampt string for log messages
def get_timestamp():
    return str(int(time.time()*10e3))



# Create bot
bot = commands.Bot(command_prefix='')

# On startup
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    if guild is not None:
        print('Connection with guild established!')
        print(f'Bot username: {bot.user}')
        print(f'Guild name: {guild.name}')

# On event error
@bot.event
async def on_error(event, *args, **kwargs):
    with open(
        TOP_LEVEL_PATH + 'assistant/logs/errors/err' + get_timestamp() + '.log', 
        'a'
    ) as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# On command error
@bot.event
async def on_command_error(ctx, error):
    # Print to stderr
    print(INTERNAL_BUG, file=sys.stderr)
    
    # Log real error
    with open(
        TOP_LEVEL_PATH + 'assistant/logs/command_errors/err' + \
            get_timestamp() + '.log',
        'a'
    ) as err_file:
        err_file.write(
            f'Author: {ctx.author}\n\n'
            f'Message Metadata: {ctx.message}\n\n'
            f'Error: {str(error)}'
        )
        print('Error logged to ', err_file.name)
    
    await ctx.send(INTERNAL_BUG)

# Roll dice
@bot.command(
    name='roll', 
    help='Rolls 4, 6, 8, 10, 12, or 20 sided die.\n\n'
    'Examples:\n'
    'Roll a single 20-sided die:\troll 20\n'
    'Roll three 6-sided die:\t\troll 3d6\n')
async def roll(ctx, *args): 
    success, msg = dice.roll_request(args)

    if success:
        await ctx.send('Roll returned: ' + str(msg))
    else:
        await ctx.send(INVALID_CMD + '\n' + str(msg))

# Roll dice
@bot.command(
    name='r', 
    help='Alias for "roll" comand. Rolls 4, 6, 8, 10, 12, or 20 sided die.\n\n'
    'Examples:\n'
    'Roll a single 20-sided die:\troll 20\n'
    'Roll three 6-sided die:\t\troll 3d6\n')
async def roll(ctx, *args): 
    success, msg = dice.roll_request(args)

    if success:
        await ctx.send('Roll returned: ' + str(msg))
    else:
        await ctx.send(INVALID_CMD + '\n' + str(msg))


if __name__ == '__main__':
    bot.run(TOKEN)
