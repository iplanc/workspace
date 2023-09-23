import datetime
import json
import re
import requests

import botpy

class Client(botpy.Client):
    def hi(self):
        print("hello")

with open("./config.json", "r", encoding="UTF-8") as config_file:
    config = json.loads(config_file.read())

intents = botpy.Intents(public_guild_messages=True, guild_messages=True, guild_members=True)
client = Client(intents=intents)
client.hi()
coro = client.run(appid=config['AppID'], token=config['Token'], ret_coro=True)
