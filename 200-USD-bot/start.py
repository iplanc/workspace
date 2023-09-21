import datetime
import json
import re
import requests

import botpy

class Client(botpy.Client):
    async def on_at_message_create(self, message: botpy.types.message):
        if "/签到" in message.content:
            await self.signin(message)
        elif "/信息" in message.content:
            await self.query(message)
        elif "/提问" in message.content:
            await self.question(message)
        elif "/频道" in message.content:
            botpy.logger.info(self.api.get_guild(guild_id=message.guild_id))
            await self.api.post_message(channel_id=message.channel_id, content="频道信息已写入logger", msg_id=message.id)

    async def on_guild_member_add(self, member: botpy.user.Member):
        botpy.logger.info("监听到 新人入群: %s", member)

    async def on_message_create(self, message: botpy.types.message):
        for each in explicit['words']:
            if re.match(each, message.content):
                botpy.logger.info("检测到违禁词: %s", message.content)
                await self.api.recall_message(channel_id=message.channel_id, message_id=message.id, hidetip=False)
    
    async def signin(self, message: botpy.types.message):
        database = {}
        with open("./signin.json", "r", encoding="UTF-8") as db:
            database = json.loads(db.read())

        with open("./signin.json", "w", encoding="UTF-8") as db:
            try:
                if (database[message.author.id]['lastSignInDate'] == datetime.date.today().strftime("%Y-%m-%d")):
                    await self.api.post_message(channel_id=message.channel_id, content="今日已签到", msg_id=message.id)
                    return
                database[message.author.id]['coin'] = database[message.author.id]['coin'] + 1
                await self.api.post_message(channel_id=message.channel_id, content="签到成功，金币+1", msg_id=message.id)
            except KeyError:
                database[message.author.id] = {}
                database[message.author.id]['coin'] = 10
                await self.api.post_message(channel_id=message.channel_id, content="首次签到成功，金币+10", msg_id=message.id)
            finally:
                database[message.author.id]['lastSignInDate'] = datetime.date.today().strftime("%Y-%m-%d")
                db.write(json.dumps(database, indent=4))
    
    async def query(self, message: botpy.types.message):
        with open("./signin.json", "r", encoding="UTF-8") as db:
            database = json.loads(db.read())
            try:
                coin = database[message.author.id]['coin']
                await self.api.post_message(channel_id=message.channel_id, content="金币为：" + coin, msg_id=message.id)
            except KeyError:
                await self.api.post_message(channel_id=message.channel_id, content="未查询到首次签到记录", msg_id=message.id)
    
    async def question(self, message: botpy.types.message):
        if (message.content == "你是谁"):
            await self.api.post_message(channel_id=message.channel_id, content="服务于成都中医药大学学生自建校园论坛的专属机器人｜CDUTCM BBS｜Chengdu University of Traditional Chinese Medicine BBS", msg_id=message.id)
        elif (message.content == "1+1等于几"):
            await self.api.post_message(channel_id=message.channel_id, content="1+1=2", msg_id=message.id)

with open("./explicit.json", "r", encoding="UTF-8") as explicit_file:
    explicit = json.loads(explicit_file.read())

with open("./config.json", "r", encoding="UTF-8") as config_file:
    config = json.loads(config_file.read())

intents = botpy.Intents(public_guild_messages=True, guild_messages=True, guild_members=True)
client = Client(intents=intents)
client.run(appid=config['AppID'], token=config['Token'])
