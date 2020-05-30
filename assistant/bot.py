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
import sys, os, time, random, datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import dice 

# Load token, server name from local file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TOP_LEVEL_PATH = os.getenv('TOP_LEVEL_PATH')
AUTHOR = os.getenv('AUTHOR')

# Bot invalid command messages
INVALID_CMD = \
    'Whoops! The roll command wasn\'t used correctly.\n' \
    'Try using the same format as the examples in "!help roll".'
INTERNAL_BUG = \
    f'Congrats! That command you just sent resulted in an internal bug! ' \
    f'Sorry about that, this was {AUTHOR}\'s first attempt at a Bot. ' \
    f'Sending {AUTHOR} a DM with the command you sent would be really helpful!'

## Helper functions

# Returns timestampt string for log messages
def get_timestamp():
    return str(int(time.time()*10e3))



# Create bot
bot = commands.Bot(command_prefix='!')

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

# Print intro message
@bot.command(
    name='intro',
    help='Responds with Dnd-Assistant Introduction.'
)
async def intro(ctx, *args):
    # Ignore any arguments
    embed = discord.Embed(
        title='Hello, meet DnD-Assisant!', 
        description= \
            f'The primary feature is rolling dice, '
            f'but more features will be added soon. '
            f'Let {AUTHOR} know if you have any '
            f'features you want added!\n\n'
            f'You can run DnD-Assistant\'s commands '
            f'by typing "!" immediately followed by '
            f'the command. For example, to list all '
            f'possible commands, enter "!help". To '
            f'get help with a particular command, like '
            f'the "roll" command, enter "!help roll". '
            f'Finally, to roll three 6-sided die, enter '
            f'"!roll 3d6".\n\n'
            f'If you\'re interested, you can check out '
            f'the source code at https://github.com/jdcarpinelli/dungeons.', 
        color=0x000000)
    
    # Roll command
    embed.add_field(
        name='Command: roll', 
        value= \
            'Rolls 4, 6, 8, 10, 12, or 20 sided die.\n'
            'Usage: !roll 20, !roll 3d6, !r 2d20, etc.', 
        inline=False
    )

    # Help command
    embed.add_field(
        name='Command: help', 
        value= \
            'List all possible DnD-Assistant commands, or '
            'get help with one specific command.\n'
            'Usage: !help, or !help roll, !help r, !help intro, etc.', 
        inline=False
    )

    # Intro command
    embed.add_field(
        name='Command: intro', 
        value= \
            'Print out this introduction!\n'
            'Usage: !intro', 
        inline=False
    )

    await ctx.send(embed=embed)

# Roll dice
@bot.command(
    name='roll', 
    help='Rolls 4, 6, 8, 10, 12, or 20 sided die.\n\n'
    'Examples:\n'
    'Roll a single 20-sided die:\t\t!roll 20\n'
    'Roll three 6-sided die:\t\t\t!roll 3d6\n'
    '"!r" serves as a shortcut for "!roll:\t !r 20\n')
async def roll(ctx, *args): 
    success, msg = dice.roll_request(args)

    if success:
        await ctx.send('Roll returned: ' + str(msg))
    else:
        await ctx.send(INVALID_CMD + '\n' + str(msg))

# Roll dice
@bot.command(
    name='r', 
    help='Rolls 4, 6, 8, 10, 12, or 20 sided die.\n\n'
    'Examples:\n'
    'Roll a single 20-sided die:\t\t!roll 20\n'
    'Roll three 6-sided die:\t\t\t!roll 3d6\n'
    '"!r" serves as a shortcut for "!roll:\t !r 20\n')
async def roll(ctx, *args): 
    success, msg = dice.roll_request(args)

    if success:
        await ctx.send('Roll returned: ' + str(msg))
    else:
        await ctx.send(INVALID_CMD + '\n' + str(msg))


if __name__ == '__main__':
    bot.run(TOKEN)
