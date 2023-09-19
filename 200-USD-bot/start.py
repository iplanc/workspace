import botpy
from botpy import logger

class Client(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # TODO: 简单问答
        logger.info("接收到 @消息")
        await self.api.post_message(channel_id=message.channel_id, content="content")

    async def on_guild_member_add(self, member: Member):
        # TODO: 新人入群
        logger.info("监听到 新人入群")

intents = botpy.Intents(public_guild_messages=True, guild_members=True)
client = Client(intents=intents)
client.run(appid={""}, token={""})
