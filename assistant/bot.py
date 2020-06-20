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

# Imports from shadowedlucario/oghma:46128dc:bot.py
from query import *
import requests
import json

# Load token, server name from local file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TOP_LEVEL_PATH = os.getenv('TOP_LEVEL_PATH')
AUTHOR = os.getenv('AUTHOR')

# Bot invalid command messages
INVALID_ROLL_CMD = \
    'Whoops! The roll command wasn\'t used correctly.\n' \
    'Try using the same format as the examples in "!help roll".'
INVALID_TELL_CMD = \
    'Whoops! The tell command wasn\'t used correctly.\n' \
    'Try using the same format as the examples in "!help tell".'
INVALID_TELL_MSG = \
    'This command requires a non-blank message.'
INVALID_TELL_RECIPIENT = \
    'The user you requested was not found in the server.'
INTERNAL_BUG = \
    f'Congrats! That command you just sent resulted in an internal bug! ' \
    f'Sorry about that, this was {AUTHOR}\'s first attempt at a Bot. ' \
    f'Sending {AUTHOR} a DM with the command you sent would be really helpful!'

## Helper functions

# Returns timestampt string for log messages
def get_timestamp():
    return str(int(time.time()*10e3))

# Create bot
bot = commands.Bot(command_prefix='!', disable_everyone=False)

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
        TOP_LEVEL_PATH + '/assistant/logs/errors/err' + get_timestamp() + '.log', 
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
    print('\n\n' + INTERNAL_BUG + '\n\n')
    
    # Log real error
    with open(
        TOP_LEVEL_PATH + '/assistant/logs/command_errors/err' + \
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
        title='Hello, meet DnD-Assistant!', 
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
            f'the source code at https://github.com/cadojo/dungeons.', 
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
    aliases=['r'],
    help='Rolls 4, 6, 8, 10, 12, or 20 sided die.\n\n'
    'Examples:\n'
    'Roll a single 20-sided die:\t\t!roll 20\n'
    'Roll three 6-sided die:\t\t\t!roll 3d6\n'
    '"!r" serves as a shortcut for "!roll:\t!r 20\n')
async def roll(ctx, *args): 
    success, msg = dice.roll_request(args)

    if success:
        await ctx.send('Roll returned: ' + str(msg))
    else:
        await ctx.send(INVALID_ROLL_CMD + '\n' + str(msg))


# Relay a message
@bot.command(
    name = 'tell',
    help = \
    f'Relay a message to someone else on this server.\n\n'
    f'Examples:\n'
    f'Tell {AUTHOR} have a great day: !tell @jodoca have a great day!'
)
async def tell(ctx, recipient: str, *message):
    ## Argument checking
    #  Usage:
    #  !tell @user message without any quotes  

    guild = discord.utils.get(bot.guilds, name=GUILD)
    if guild is None:
        await ctx.send(INTERNAL_BUG)
        return
    
    ## Argument checking

    # Re-construct message
    msg = ''
    for m in message:
        msg += m + ' '
    
    # Recipient and message should not be empty
    if '@' not in recipient \
        or recipient == '' \
            or msg == '':
        await ctx.send(INVALID_TELL_CMD + '\n' + INVALID_TELL_MSG)

    # Check if recipient is @everyone or a user
    all_recipients = []
    if recipient == '@everyone':
        all_recipients = [user for user in guild.members if user != bot.user]
    else:
        # Remove special characters, left with id or name
        recipient_parsed = recipient\
            .replace('@','')\
            .replace('<','')\
            .replace('>','')\
            .replace('!','')

        for user in [user for user in guild.members if user != bot.user]:
            if (recipient_parsed == user.name) \
                or (recipient_parsed == str(user.id)):
                all_recipients.append(user)

    if len(all_recipients) == 0:
        await ctx.send(INVALID_TELL_RECIPIENT)
        return

    ## Context checking
    #  If command in DM, DM recipient
    if ctx.message.channel.type == discord.ChannelType.private:
        for user in all_recipients:
            await user.send('<@!' + str(ctx.author.id) + '> says: ' + msg)
        await ctx.send('Sent!')
        return

    #  Otherwise, just post wherever this was posted
    else:
        recipient_str = ''
        for user in all_recipients:
            recipient_str += ('<@!' + str(user.id) + '> ')
        await ctx.send(
            f'Hey {recipient_str}, {ctx.author.name} says: {msg}'
        )
        return

### Bot commands from shadowedlucario/oghma
###
# FUNC NAME: ?search [ENTITY]
# FUNC DESC: Queries the Open5e search API, basically searches the whole thing for the ENTITY.
# ENTITY: The DND entity you wish to get infomation on.
# FUNC TYPE: Command
###
@bot.command(
    name='search',
    help='Queries the Open5e API to get the entities infomation.',
    usage='?search [ENTITY]',
    aliases=["sea", "s", "S"]
)
async def search(ctx, *args):
    print(f"Executing: ?search {args}")

    # Import & reset globals
    global partialMatch
    partialMatch = False

    # Verify arg length isn't over limits
    if len(args) >= 201:
        argumentsEmbed = discord.Embed(
            color=discord.Colour.red(),
            title="Invalid argument length",
            description="This command does not support more than 200 words in a single message. Try splitting up your query."
        )
        argumentsEmbed.set_thumbnail(url="https://i.imgur.com/j3OoT8F.png")

        return await ctx.send(embed=argumentsEmbed)

    # Send directory contents if no search term given
    if len(args) <= 0:

        await ctx.send(embed=discord.Embed(
            color=discord.Colour.blue(),
            title="Searching...",
            description="This might take a few seconds!"
        ))

        # Get objects from directory, store in txt file
        directoryRequest = requests.get("https://api.open5e.com/search/?format=json&limit=10000")

        if directoryRequest.status_code != 200: 
            return await ctx.send(embed=codeError(
                directoryRequest.status_code,
                "https://api.open5e.com/search/?format=json&limit=10000"
                )
            )

        # Generate a unique filename and write to it
        entityFileName = generateFileName("entsearch")

        entityFile = open(entityFileName, "a+")
        for entity in directoryRequest.json()["results"]:
            if "title" in entity.keys():
                entityFile.write(f"{ entity['title'] }\n")
            else:
                entityFile.write(f"{ entity['name'] }\n")

        entityFile.close()

        # Send embed notifying start of the spam stream
        detailsEmbed = discord.Embed(
            colour=discord.Colour.orange(),
            title=f"See `{ entityFileName }` for all searchable entities in this endpoint", 
            description="Due to discord charecter limits regarding embeds, the results have to be sent in a file. Yes I know this is far from ideal but it's the best I can do!"
        )

        detailsEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")

        await ctx.send(embed=detailsEmbed)

        # Send entites file
        return await ctx.send(file=discord.File(entityFileName))

    # Filter input to remove whitespaces and set lowercase
    filteredInput = "".join(args).lower()

    # Search API
    await ctx.send(embed=discord.Embed(
        color=discord.Colour.blue(),
        title=f"Searching for { filteredInput }...",
        description="This might take a few seconds!"
    ))
    
    # Use first word to narrow search results down for quicker response on some directories
    match = requestOpen5e(f"https://api.open5e.com/search/?format=json&limit=10000&text={ str(args[0]) }", filteredInput, True)

    # An API Request failed
    if isinstance(match, dict) and "code" in match.keys():
        return await ctx.send(embed=codeError(match["code"], match["query"]))

    # Searching algorithm hit an invalid object
    elif match == "UNKNOWN":
        unknownMatchEmbed = discord.Embed(
            colour=discord.Colour.red(),
            title="ERROR", 
            description="I found an entity in the API database that doesn't contain a `name` or `docuement` attribute. Please report this to https://github.com/shadowedlucario/oghma/issues"
        )

        unknownMatchEmbed.set_thumbnail(url="https://i.imgur.com/j3OoT8F.png")

        return await ctx.send(embed=unknownMatchEmbed)

    # No entity was found
    elif match == None:
        noMatchEmbed = discord.Embed(
            colour=discord.Colour.orange(),
            title="ERROR", 
            description=f"No matches found for **{ filteredInput }** in the search endpoint"
        )

        noMatchEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")

        return await ctx.send(embed=noMatchEmbed)

    # Otherwise, construct & send responses
    else:
        responses = constructResponse(args, match["route"], match["matchedObj"])
        for response in responses:

            if isinstance(response, discord.Embed):

                # Set a thumbnail for relevent embeds and on successful Scyfall request, overwriting all other thumbnail setup
                image = requestScryfall(args, False)

                if (not isinstance(image, int)): response.set_thumbnail(url=image)

                # Note partial match in footer of embed
                if partialMatch: 
                    response.set_footer(text=f"NOTE: Your search term ({ filteredInput }) was a PARTIAL match to this entity.\nIf this isn't the entity you were expecting, try refining your search term or use ?searchdir instead")
                else:
                    response.set_footer(text="NOTE: If this isn't the entity you were expecting, try refining your search term or use `?searchdir` instead")

                print(f"SENDING EMBED: { response.title }...")
                await ctx.send(embed=response)

            elif ".txt" in response:
                print(f"SENDING FILE: { response }...")
                await ctx.send(file=discord.File(response))

###
# FUNC NAME: ?searchdir [RESOURCE] [ENTITY]
# FUNC DESC: Queries the Open5e RESOURCE API.
# RESOURCE:  Resource name (i.e. spells, monsters, etc.).
# ENTITY: The DND entity you wish to get infomation on.
# FUNC TYPE: Command
###
@bot.command(
    name='searchdir',
    help='Queries the Open5e API to get the entities infomation from the specified resource.',
    usage='!search [RESOURCE] [ENTITY]',
    aliases=["dir", "d", "D"]
)
async def searchdir(ctx, *args):
    print(f"EXECUTING: ?searchdir {args}")

    # Import & reset globals
    global partialMatch
    partialMatch = False

    # Get API Root
    rootRequest = requests.get("https://api.open5e.com?format=json")

    # Throw if Root request wasn't successfull
    if rootRequest.status_code != 200:
        return await ctx.send(embed=codeError(rootRequest.status_code, "https://api.open5e.com?format=json"))
    
    # Remove search endpoint from list (not used in this command)
    directories = list(rootRequest.json().keys())
    directories.remove("search")

    # Verify we have arguments
    if len(args) <= 0:
        usageEmbed = discord.Embed(
            colour=discord.Colour.red(),
            title="No directory was requested.\nUSAGE: `?searchdir [DIRECTORY] [D&D OBJECT]`", 
            description=f"**Available Directories**\n{ ', '.join(directories) }"
        )

        usageEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")

        return await ctx.send(embed=usageEmbed)

    # Filter the dictionary input
    filteredDictionary = f"{ args[0].lower() }/"

    # Filter input to remove whitespaces and set lowercase
    filteredInput = "".join(args[1:]).lower()

    # Verify arg length isn't over limits
    if len(args) >= 201:
        argumentsEmbed = discord.Embed(
            color=discord.Colour.red(),
            title="Invalid argument length",
            description="This command does not support more than 200 words in a single message. Try splitting up your query."
        )
        argumentsEmbed.set_thumbnail(url="https://i.imgur.com/j3OoT8F.png")

        return await ctx.send(embed=argumentsEmbed)

    # Verify resource exists
    if directories.count(args[0]) <= 0:

        noResourceEmbed = discord.Embed(
            colour=discord.Colour.orange(),
            title=f"Requested Directory (`{ str(args[0]) }`) is not a valid directory name", 
            description=f"**Available Directories**\n{ ', '.join(directories) }"
        )

        noResourceEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")

        return await ctx.send(embed=noResourceEmbed)

    # Send directory contents if no search term given
    if len(args) == 1:

        await ctx.send(embed=discord.Embed(
            color=discord.Colour.blue(),
            title=f"Searching for everything having to do this { filteredDictionary.upper() }!!",
            description="Sit back, this might take a minute."
        ))

        # Get objects from directory, store in txt file
        directoryRequest = requests.get(f"https://api.open5e.com/{ filteredDictionary }?format=json&limit=10000")

        if directoryRequest.status_code != 200: 
            return await ctx.send(embed=codeError(
                directoryRequest.status_code,
                f"https://api.open5e.com/{ filteredDictionary }?format=json&limit=10000"
                )
            )

        entityNames = []
        for entity in directoryRequest.json()["results"]:
            if "title" in entity.keys(): entityNames.append(entity['title'])
            else: entityNames.append(entity['name'])

        # Keep description word count low to account for names with lots of charecters
        if len(entityNames) <= 200:

            detailsEmbed = discord.Embed(
                colour=discord.Colour.orange(),
                title="All searchable entities in this endpoint", 
                description="\n".join(entityNames)
            )

            detailsEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")
            if "search" in filteredDictionary:
                detailsEmbed.set_footer(text="NOTE: The `search` endpoint is not searchable with `?searchdir`. Use `?search` instead for this.")

            return await ctx.send(embed=detailsEmbed)

        # Generate a unique filename and write to it
        entityDirFileName = generateFileName("entsearchdir")

        entityFile = open(entityDirFileName, "a+")
        entityFile.write("\n".join(entityNames))
        entityFile.close()

        # Send embed notifying start of the spam stream
        detailsEmbed = discord.Embed(
            colour=discord.Colour.orange(),
            title=f"See `{ entityDirFileName }` for all searchable entities in this endpoint", 
            description="Due to discord charecter limits regarding embeds, the results have to be sent in a file. Yes I know this is far from ideal but it's the best I can do!"
        )

        detailsEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")
        if "search" in filteredDictionary:
            detailsEmbed.set_footer(text="NOTE: The `search` endpoint is not searchable with `?searchdir`. Use `?search` instead for this.")

        await ctx.send(embed=detailsEmbed)

        # Send entites file
        return await ctx.send(file=discord.File(entityDirFileName))

    # search/ endpoint is best used with the dedicated ?search command
    if "search" in filteredDictionary:
        
        # Remove search endpoint from list
        directories = list(rootRequest.json().keys())
        directories.remove("search")

        searchEmbed = discord.Embed(
            colour=discord.Colour.orange(),
            title=f"Requested Directory (`{ str(args[0]) }`) is not a valid directory name", 
            description=f"**Available Directories**\n{ ', '.join(directories) }"
        )

        searchEmbed.add_field(name="NOTE", value="Use `?search` for searching the `search/` directory. This has been done to cut down on parsing errors.")
        searchEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")

        return await ctx.send(embed=searchEmbed)

    # Search API
    await ctx.send(embed=discord.Embed(
        color=discord.Colour.blue(),
        title=f"Searching all { filteredDictionary.upper() } for { filteredInput }...",
        description="This might take a few seconds!"
    ))
    
    # Determine filter type (search can only be used for some endpoints)
    filterType = "text"
    if args[0] in searchParamEndpoints: filterType = "search"

    # Use first word to narrow search results down for quicker response on some directories
    match = requestOpen5e(
        f"https://api.open5e.com/{ filteredDictionary }?format=json&limit=10000&{ filterType }={ str(args[1]) }",
        filteredInput,
        False
    )

    # An API Request failed
    if isinstance(match, dict) and "code" in match.keys():
        return await ctx.send(embed=codeError(match.code, match.query))

    # Searching algorithm hit an invalid object
    elif match == "UNKNOWN":
        unknownMatchEmbed = discord.Embed(
            colour=discord.Colour.red(),
            title="ERROR", 
            description="I found an entity in the API database that doesn't contain a `name` or `docuement` attribute. Please report this to https://github.com/shadowedlucario/oghma/issues"
        )

        unknownMatchEmbed.set_thumbnail(url="https://i.imgur.com/j3OoT8F.png")

        return await ctx.send(embed=unknownMatchEmbed)

    # No entity was found
    elif match == None:
        noMatchEmbed = discord.Embed(
            colour=discord.Colour.orange(),
            title="ERROR", 
            description=f"No matches found for **{ filteredInput.upper() }** in the { filteredDictionary } endpoint"
        )

        noMatchEmbed.set_thumbnail(url="https://i.imgur.com/obEXyeX.png")

        return await ctx.send(embed=noMatchEmbed)

    # Otherwise, construct & send responses
    else:
        responses = constructResponse(args, filteredDictionary, match)
        for response in responses:
            
            if isinstance(response, discord.Embed):

                # Set a thumbnail for relevent embeds and on successful Scyfall request, overwrites other thumbnail setup
                image = requestScryfall(args, True)

                if (not isinstance(image, int)): response.set_thumbnail(url=image)

                # Note partial match in footer of embed
                if partialMatch: 
                    response.set_footer(text=f"NOTE: Your search term ({ filteredInput }) was a PARTIAL match to this entity.\nIf this isn't the entity you were expecting, try refining your search term")

                print(f"SENDING EMBED: { response.title }...")
                await ctx.send(embed=response)

            elif ".txt" in response:
                print(f"SENDING FILE: { response }...")
                await ctx.send(file=discord.File(response))




if __name__ == '__main__':
    bot.run(TOKEN)
