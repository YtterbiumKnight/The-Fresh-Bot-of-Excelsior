"""The Fresh Bot of Excelsior by Exanimem#3112 and Ned#5609 with discord.py."""
# Code Style Notes: " for messages posted in chat, ' for everything else.
# Comments will be up to date with the Stable branch, though may not be
# up to date with the Unstable branch.
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

server = discord.Server
#  -----------------------------RSS Start--------------------------------------

rss_entries_dict = {
                'RSS': list(range(0, 10)),
                'awwnime': list(range(0, 10)),
                'news': list(range(0, 10)),
                'onion': list(range(0, 10))
}
# Lists for each random RSS command so that one command doesn't remove entries
# of another


def get_random_rss_entry(rss_dict_entry):
    """Randomly selects a number from rss_entries_dict and sets auto-refresh of entry."""
    global random_rss_entry
    # Global needs to be removed!
    random_rss_entry = random.choice(rss_entries_dict[rss_dict_entry])
    rss_entries_dict[rss_dict_entry].remove(random_rss_entry)
    # Removes selected number to prevent duplicate entries being posted
    print(rss_entries_dict[rss_dict_entry])
    print(random_rss_entry)
    # For debugging
    if not rss_entries_dict[rss_dict_entry]:
        print('List is empty, refresh or wait')
        if min == 30:
            # 30 minute timer keeps the entries being posted fresh rather than
            # the same ones every refresh
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
    global random_rss_entry

    async def exclusive_command(dev=False, WIP=False, owner=False):
        if message.author.id != '95978401654919168' or message.author.id != '138001563158446081':
            # ID's are the devs ID's
            if dev is True:
                await client.send_message(message.channel,
                                          "This command is a dev tool and not"
                                          " avaliable to normal users")
                return False
                # Returns the function it's called in
            elif WIP is True:
                await client.send_message(message.channel,
                                          "This command is a work in progress"
                                          " thus unavaliable for the time"
                                          " being")
                return False
        elif message.author.id != message.server.owner.id:
            if owner is True:
                await client.send_message(message.channel, "This command"
                                          " is only for the server owner")
                return False
        else:
            pass

    if message.author.id == client.user.id:
        return
        # Prevents people abusing [say to make the bot trigger it's own commands

# ---------------------------RSS Commands Start--------------------------

    elif message.content.startswith("[rss"):
        get_random_rss_entry('RSS')
        feed = message.content[4:].strip()
        feed_entry = feedparser.parse(feed).entries[random_rss_entry]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[awwnime"):
        # Cannot get link post's link with current knowledge and research
        get_random_rss_entry('awwnime')
        continue_function = await exclusive_command(WIP=True)
        if continue_function is False:
            return
        feed_entry = feedparser.parse(
            'https://www.reddit.com/r/awwnime/.rss').entries[random_rss_entry]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[topnews"):
        feed_entry = feedparser.parse(
            'http://feeds.reuters.com/reuters/topNews').entries[0]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[news"):
        get_random_rss_entry('news')
        feed_entry = feedparser.parse(
            'http://feeds.reuters.com'
            '/reuters/topNews').entries[random_rss_entry]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[onion"):
        get_random_rss_entry('onion')
        feed_entry = feedparser.parse(
                'http://www.theonion.com'
                '/feeds/rss').entries[random_rss_entry]
        await client.send_message(message.channel, '***{0}*** \n{1}'
                                  .format(feed_entry.title, feed_entry.link))

    elif message.content.startswith("[refresh"):
        for key, values in rss_entries_dict.items():
            rss_entries_dict[key] = list(range(0, 10))
        await client.send_message(message.channel, "All RSS commands refreshed"
                                  "; 30 minute refresh rate bypassed")

# ---------------------------RSS Commands End---------------------------------
    elif message.content.startswith("[test"):
        # Just for testing ;)
        continue_function = await exclusive_command(False)
        if continue_function is False:
            return
        await client.send_message(message.channel, "Testing 1 2 3")

    elif message.content.startswith("[setlog"):
        # Takes channel ID to post log messages

        continue_function = await exclusive_command(owner=True)
        if continue_function is False:
            return
        try_log_channel = message.content[8:].strip()
        # Must be tested to see if it's an actual channel ID
        try:
            int(try_log_channel)
        except ValueError:
            # Channel IDs have no alphabetical characters
            print('Channel ID invalid, contains alphabetical characters')
            await client.send_message(message.channel, "That's an invalid "
                                      "channel ID, please try again")
            return
        if len(try_log_channel) != 18:
            # Channel IDs are exactly 18 characters in length
            await client.send_message(message.channel, "That's an invalid "
                                      "channel ID, please try again")
            raise ValueError('Channel ID invalid,'
                             ' incorrect amount of characters')
            return
        await client.send_message(message.channel, "Valid log channel ID"
                                  "accepted")
        log_channel = try_log_channel
        with open('data.txt', 'w') as save_log_id:
            save_log_id.write(str(message.server.id))
            save_log_id.write(str('\n'))
            save_log_id.write(str(log_channel))
            save_log_id.write(str('\n'))
        with open('data.txt', 'r') as testerino:
            print(testerino.read())
        print(log_channel)
        # For debugging

    elif message.content.startswith("[say"):  # WORK IN PROGRESS
        continue_function = await exclusive_command(WIP=True)
        if continue_function is False:
            return
        say_message = message.content[4:].strip()
        await client.send_message(message.channel, say_message)
        if not log_channel:
            return
        # ----------------------Logging Below----------------------------
        # Done to find abusers of the command. Done in Rich Embed format
        print('I was told by {0} to say "{1}"'
              .format(message.author, say_message))
        em = discord.Embed(title="Say Command Used", color=0xFFFFFF)
        em.add_field(inline=True, name="Commander", value="{}".format(
            message.author))
        em.add_field(inline=True, name="Said Message", value="{}"
                     .format(say_message))
        em.set_footer(text="{}".format(message.timestamp))
        await client.send_message(discord.Object(id=log_channel), embed=em)

    elif message.content.startswith("[removeentries"):
        # Work in Progress. Command for debugging.
        continue_function = await exclusive_command(dev=True)
        if continue_function is False:
            return
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
        em.set_footer(text="Made by Exanimem#3112 and Ned#5609 using"
                      " Discord.py")
        await client.send_message(message.channel, embed=em)
