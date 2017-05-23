#The Fresh Bot of Excelsior by Exanimem#3112 and Ned#5609
#Testing Github Webhook
import discord
import asyncio
import logging
import feedparser
import random

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler) #Logs errors and warnings, take from example in discord.py documentaion

client = discord.Client()

@client.event
async def on_ready(): #Logs in (?)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message): #Performs on message
    if message.author.id == client.user.id: #If message author is client
        return #Ignore

#rss commands

    elif message.content.startswith("[rss"):
        feed = message.content[4:].strip()
        a = feedparser.parse(feed).entries[1]
        await client.send_message(message.channel, '__***{0}***__ \n{1}'.format(a.title, a.link))

    elif message.content.startswith("[topnews"):
        a = feedparser.parse('http://feeds.reuters.com/reuters/topNews').entries[1] #Gets top entry from Reuters Top News RSS feed
        await client.send_message(message.channel, '__***{0}***__ \n{1}'.format(a.title, a.link)) #Formats message. Posts title, a line break then the link

    elif message.content.startswith("[randnews"):
        r = random.randint(1, 10) #Picks a random number between 1 and 10
        a = feedparser.parse('http://feeds.reuters.com/reuters/topNews').entries[r] #Gets a article in the order corresponding to the number randomly chosen from Reuters Top News RSS Feed
        await client.send_message(message.channel, '__***{0}***__ \n{1}'.format(a.title, a.link)) #Formats message. Posts title, a line break then the link

    elif message.content.startswith("[onion"):
        a = feedparser.parse('http://www.theonion.com/feeds/rss').entries[1] #Gets latest entry from Onion RSS feed
        await client.send_message(message.channel, '__***{0}***__ \n{1}'.format(a.title, a.link)) #Formats message. Posts title, a line break then the link

#rss commands end

    elif message.content.startswith("[setlog"): #Takes channel ID to post log messages. To Do: Save channel ID set for server
        if message.author.id != '95978401654919168': #If author isn't Exanimem. To Do: Make this customizable so the owner can choose who can use this command
            await client.send_message(message.channel, 'Sorry, certain bot commands are locked down for everyone except Exanimem due to exploits that need to be fixed')
            return
        global log_channel #Makes log_channel usable in other functions
        log_channel = message.content[4:].strip()
        log_channel = int(log_channel) #Turns log_channel into an interger
        return log_channel

    elif message.content.startswith("[say"): #Log who said what
        if message.author.id != '95978401654919168': #Temporary until pings can be disabled
            await client.send_message(message.channel, 'Sorry, certain bot commands are locked down for everyone except Exanimem due to exploits that need to be fixed')
            return
        say = message.content[4:].strip() #Cuts the first four characters of the content
        #if say.content.startswith == '@': #My attempt at disabling pings. Didn't work.
            #await client.send_message(message.channel, 'Fuck off')
        await client.send_message(message.channel, say)
        print('I was told by {0} to say "{1}"'.format(message.author, say)) #Logs who made it say what to catch exploiters who delete their messages. Temporary solution, need to disable pings
        em = discord.Embed(title="Say Command Used", color=0xFFFFFF) #Creates Rich Embed
        em.add_field(inline=True, name="Commander", value="{}".format(message.author)) #Adds field underneath title with the author of the command
        em.add_field(inline=True, name="Said Message", value="{}".format(say)) #Adds field next toe the previous with the message said
        em.set_footer(text="{}".format(message.timestamp)) #Sets timestamp as footer
        await client.send_message(discord.Object(id=log_channel), embed=em) #Sends Rich Embed to log_channel

    elif message.content.startswith("[info"):
        em = discord.Embed(title='Information', description='**[topnews** - Top news article by Reuters \n**[randnews** - Randomly picks one of the top 10 articles on Reuters \n**[onion** - Picks top onion article \n**[say** - Commands the bot to say whatever you want it to \n**[rss** - Paste a URL to any RSS feed and get the top article!\n**Github** - https://github.com/Exanimem/The-Fresh-Bot-of-Excelsior\n**Trello** - https://trello.com/b/Ehk9xZMx/the-fresh-bot-of-excelsior', colour=0x3366FF) #Defines em as an embed, creates embed title, descripton, and defines the color
        em.set_footer(text="Made by Exanimem#3112 using Discord.py") #Creates footer for embed
        await client.send_message(message.channel, embed=em)



@client.event
async def change_presence(game=None, idle=False): #Sets playing status. Doesn't currently work
    game='Chillin out maxin relaxin all cool' #Sets playing to said message

@client.event
async def on_member_update(before, after): #When a parameter of member updates. Doesn't currently work. Wanted result: Check if change is addition of active role, post message down below in #lounge
    if before.roles != after.roles: #If before roles is different than after roles
        for role in member.roles:
            if after.roles == "315622124494520320": #If after role is the active role
                await client.send_messsage(discord.Object(id='283294159685681152'), '{} became Active! Enjoy your time here where we drink fine wine and smoke ripe Cuban cigars'.format()) #Sends message in #lounge
