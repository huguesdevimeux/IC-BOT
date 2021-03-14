from typing import Union
import typing
import discord
from discord.channel import GroupChannel
from discord.embeds import Embed
from discord.enums import ChannelType
from discord.message import Message

from ICBOT.commands.BotResponse import BotResponse

from .commands.command_manager import CommandManager
from .commands.exceptions import AbstractICBOTException
from .utils.cleaner import clean_message
from .utils.filter import filter_message
from .utils.logging import logger
from .constants import Constants


class ICBOT(discord.Client):
    async def on_ready(self):
        logger.info("BOT IS READY")
        for guild in self.guilds: 
            logger.info(f"On {guild} (id {guild.id}")

    @filter_message
    async def on_message(self, message: Message):
        content = clean_message(message.content)
        args = content.split(" ")
        if args.pop(0) == Constants.PREFIX:
            logger.info(f"Recived command : {args}")
            try:
                resp = CommandManager.parse_command(args, message)
            except AbstractICBOTException as e:
                resp = e
            await self._handle_send(message.channel, resp.to_message())
            logger.info(f"Sent message {resp}")

    async def _handle_send(
        self, channel: GroupChannel, message: typing.Union[Embed, str]
    ) -> None:
        if isinstance(message, Embed):
            await channel.send(embed=message)
        elif isinstance(message, str):
            await channel.send(message)
