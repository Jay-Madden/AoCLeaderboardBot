import json

import discord

with open('config.json.template') as f:
    print('Loading Config')
    config = json.load(f.read())
client = discord.Client()



client.Run()