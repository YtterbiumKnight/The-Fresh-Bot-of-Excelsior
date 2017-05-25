"""The Fresh Bot of Excelsior by Exanimem#3112 and Ned#5609 with discord.py."""
# Code Style Notes: " for messages posted in chat, ' for everything else
import discord
import logging
import random
import feedparser

#  ---------------------------Logging Start------------------------------------
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# Logs errors and warnings, taken from example in discord.py documentaion
#  ----------------------------Logging End-------------------------------------

client = discord.Client()

#  -----------------------------RSS Start--------------------------------------

global rss_dict_entry  # Entry in rss_entries_dict. Each random command has
#  this defined and is used to get definition from the dictonary
# [Global] Allows for use inside other functions
rss_dict_entry = 0

global rss_entries_dict
rss_entries_dict = {
                'RSS': list(range(0, 10)),
                'awwnime': list(range(0, 10)),
                'news': list(range(0, 10)),
                'onion': list(range(0, 10))
}
# Lists for each random RSS command using randomRssEntry to get entries from


def randomRssEntry():
    """Randomly selects a number from rss_entries_dict and sets auto-refresh of entry."""
    # Docstring ("""): Documents what an object does
    global rss_entries_dict
    global random_rss_entry  # Randomly chosen number
    random_rss_entry = random.choice(rss_entries_dict[rss_dict_entry])
    rss_entries_dict[rss_dict_entry].remove(random_rss_entry)
    # Removes selected number from selected rss_dict_entry
    print(rss_entries_dict[rss_dict_entry])  # For debugging
    print(random_rss_entry)
    if not rss_entries_dict[rss_dict_entry]:  # If nothing is in it
        print('List is empty, refresh or wait')
        if min == 30:  # After 30 minutes
            print('Auto-refreshed')
            rss_entries_dict[rss_dict_entry] = list(range(0, 10))
            # Sets back to original definition, effectively resetting it


# --------------------------------RSS End-------------------------------------


@client.event
async def on_ready():
    """Ran when data finished being recieved from Discord andd logged in."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='some b-ball '
                                                   'outside of the school'))
    # Changes playing status to name=


@client.event
async def on_message(message):
    """When a message is sent."""
    global rss_entries_dict
    global random_rss_entry
    global rss_dict_entry

    async def exclusiveCommand(dev=False, WIP=False):
        # For when a command is a work in progress or only for devs
        if message.author.id != '95978401654919168':
            if dev is True:
                await client.send_message(message.channel,
                                          "This command is dev tool and not"
                                          " avaliable to normal users")

            if WIP is True:
                await client.send_message(message.channel,
                                          "This command is a work in progress"
                                          " thus unavaliable for the time"
                                          " being")
            return

    if message.author.id == client.user.id:  # If message author is the bot
        return

# ---------------------------RSS Commands Start--------------------------

    elif message.content.startswith("[rss"):
        rss_dict_entry = "RSS"
        randomRssEntry()
        feed = message.content[4:].strip()  # Strip of first four letters
        feed_entry = feedparser.parse(feed).entries[random_rss_entry]
        # random_rss_entry is position in the feed
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[awwnime"):
        # Status: Waiting for comments on Reddit post to make it work
        # Cannot get link post's link with current knowledge and research
        rss_dict_entry = "awwnime"
        await exclusiveCommand(WIP=True)
        feed_entry = feedparser.parse(
            'https://www.reddit.com/r/awwnime/.rss').entries[0]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))
        print(feed_entry)

    elif message.content.startswith("[topnews"):
        feed_entry = feedparser.parse(
            'http://feeds.reuters.com/reuters/topNews').entries[0]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[news"):
        rss_dict_entry = "news"
        randomRssEntry()
        feed_entry = feedparser.parse(
            'http://feeds.reuters.com'
            '/reuters/topNews').entries[random_rss_entry]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[onion"):
        rss_dict_entry = "onion"
        randomRssEntry()
        feed_entry = feedparser.parse(
                'http://www.theonion.com'
                '/feeds/rss').entries[random_rss_entry]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[refresh"):
        global rss_entries_dict
        rss_entries_dict['RSS'] = list(range(0, 10))
        rss_entries_dict['awwnime'] = list(range(0, 10))
        rss_entries_dict['news'] = list(range(0, 10))
        rss_entries_dict['onion'] = list(range(0, 10))
        await client.send_message(message.channel, "All RSS commands refreshed"
                                  ", 30 minute refresh rate bypassed")

# ---------------------------RSS Commands End---------------------------------

    elif message.content.startswith("[setlog"):  # WORK IN PROGRESS
        # Takes channel ID to post log messages
        # To Do: Save channel ID set for server
        if message.author.id != message.server.owner.id:  # If not server owner
            await client.send_message(message.channel, "This command "
                                      "is only for the server owner")
            return
        global log_channel
        log_channel = message.content[4:].strip()
        log_channel = int(log_channel)  # Turns log_channel in  to an interger
        return log_channel

    elif message.content.startswith("[say"):  # WORK IN PROGRESS
        await exclusiveCommand()
        say_message = message.content[4:].strip()
        await client.send_message(message.channel, say_message)
        if not log_channel:
            return
        # ----------------------Logging Below----------------------------
        print('I was told by {0} to say "{1}"'
              .format(message.author, say_message))
        # Logs who made it say what
        em = discord.Embed(title="Say Command Used", color=0xFFFFFF)
        em.add_field(inline=True, name="Commander", value="{}".format(
            message.author))  # Adds commander field
        em.add_field(inline=True, name="Said Message", value="{}"
                     .format(say_message))
        # What message the bot was made to say
        em.set_footer(text="{}".format(message.timestamp))
        # Adds timestamp footer
        await client.send_message(discord.Object(id=log_channel), embed=em)
        # Sends Rich Embed to value specificed, in this case, the log channel

    elif message.content.startswith("[removeentries"):  # WORK IN PROGRES
        await exclusiveCommand()
        remove_entries_key = message.content[15:]
        if remove_entries_key == 'news':
            rss_entries_dict['news'].remove(range(0, 9))
            await client.send_message(message.channel, "News entries removed")

    elif message.content.startswith("[info"):
        em = discord.Embed(title="Information", description="**Expect"
                           " shit to be broken and not working. This bot "
                           "is a work in progres. Any bugs or exploits "
                           "are probably known, and this command may be "
                           "out of date. Any help would be appreciated**"
                           "\n**Refresh Rate** - Random RSS commands have a"
                           "Refresh Rate of 30 minutes to keep entries fresh"
                           "\n**[topnews** - Top news article by Reuters"
                           " \n**[news** - Randomly picks one of the"
                           " top 10 articles on Reuters \n**[onion** - "
                           "Randomly picks one of the top 10 articles on"
                           "the Onion\n**[rss** - Paste a URL to any RSS "
                           "feed and get any random top 10 entry!\n"
                           "**[refresh** - Bypasses 30 minute refresh rate"
                           "\n**Github** - https://github.com/Exanimem/"
                           "The-Fresh-Bot-of-Excelsior", colour=0x3366FF)
        # Defines em as an embed, creates embed title, descripton, and
        # defines the color
        em.set_footer(text="Made by Exanimem#3112 using Discord.py")
        # Creates footer for embed
        await client.send_message(message.channel, embed=em)
