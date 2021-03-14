import discord
from discord.message import Message

from ..var_env import ID_SERVER
from ..constants import Constants


def filter_message(func):
    async def wrapper(self, message: Message):
        if (Constants.TESTING and str(message.guild.id) == ID_SERVER): 
            return
        if not (
            message.author == self.user
            or message.channel.type is discord.ChannelType.private
        ):
            await func(self, message)

    return wrapper
