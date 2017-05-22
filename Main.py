import discord
import asyncio
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler) #Logs errors and warnings, take from example in discord.py documentaion

#The Fresh Bot of Excelsior by Exanimem#3112 and Ned#5609
client = discord.Client()

@client.event
async def on_ready(): #Logs in (?)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content == ('[info'):
        await client.send_message(message.channel, 'Made by Exanimem#3112')

@client.event
async def change_presence(game=None, idle=False): #Sets playing status
    game='Chillin out maxin relaxin all cool'

@client.event
async def add_roles(member, *roles):
    pass

client.run('') #Runs bot
