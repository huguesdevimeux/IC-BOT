import typing
from typing import Union

import discord
from discord.channel import GroupChannel
from discord.embeds import Embed
from discord.enums import ChannelType
from discord.errors import HTTPException
from discord.ext import tasks
from discord.message import Message

from .BotResponse import BotResponse
from .commands.command_manager import CommandManager
from .exceptions import AbstractICBOTException
from .constants import Constants, Messages
from .templates import EmebedWithFile
from .utils.cleaner import clean_message
from .utils.filter import filter_message
from .utils.logging import logger
from .channels import update_channels


def _load_channel(channels, name: str) -> ChannelType:
    temp = discord.utils.get(channels, name=name)
    if temp == None:
        raise Exception(f"Channel with name {name} not found.")
    return temp


class ICBOT(discord.Client):
    async def on_ready(self):
        assert len(self.guilds) == 1
        logger.info("BOT IS GETTING READY")
        for guild in self.guilds:
            logger.info(f"On {guild} (id {guild.id}")

        update_channels("memes", _load_channel(self.guilds[0].channels, "memes"))
        update_channels(
            "copie-pates", _load_channel(self.guilds[0].channels, "copie-pates")
        )

        await self.change_presence(
            activity=discord.Game("rien de particulier mais on est là quoi")
        )

        logger.info("\nBOT IS READY!\n")

    @filter_message
    async def on_message(self, message: Message):
        content = clean_message(message.content)
        args = content.split(" ")
        if args.pop(0) == Constants.PREFIX:
            logger.info(f"Recived command : {args}")
            try:
                resp = await CommandManager.parse_command(args, message)
            except AbstractICBOTException as e:
                resp = e
            await self._handle_send(message.channel, resp.to_message())
        elif self.user in message.mentions:
            await message.channel.send(Messages.BONSOIR_NON)

    async def _handle_send(
        self, channel: GroupChannel, message: typing.Union[Embed, str]
    ) -> None:
        if isinstance(message, Embed):
            await channel.send(embed=message)
        elif isinstance(message, str):
            await channel.send(message)
        elif isinstance(message, EmebedWithFile):
            await channel.send(embed=message.embed, file=message.file)
        logger.info(f"Sent message {message} on {channel}")
