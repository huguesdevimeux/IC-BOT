import typing

import discord
from discord.channel import GroupChannel
from discord.embeds import Embed
from discord.enums import ChannelType
from discord.ext.commands import ChannelNotFound
from discord.message import Message

from .abstract_templates import EmebedWithFile
from .channels import update_channels
from .command_manager import CommandManager
from .constants.constants import Constants, Messages
from .exceptions import AbstractICBOTException
from .icecoin.icecoin_command_manager import IcecoinCommandManager
from .standard_commands.standard_command_manager import StandardCommandManager
from .utils.cleaner import clean_message
from .utils.filter import filter_message
from .utils.logging import logger

__all__ = ["ICBOT"]


class _ChannelNotFound(Exception):
    pass


def _load_channel(channels, name: str) -> ChannelType:
    temp = discord.utils.get(channels, name=name)
    if temp == None:
        raise ChannelNotFound(f"Channel with name {name} not found.")
    return temp


class ICBOT(discord.Client):
    async def on_ready(self):
        assert len(self.guilds) == 1
        logger.info("BOT IS GETTING READY")
        for guild in self.guilds:
            logger.info(f"On {guild} (id {guild.id}")
        try:
            await self._fetch_channels()
        except _ChannelNotFound:
            # Tolerated. Mostly for testing, since we can't (I think, didn't check further) make the bot start on a
            # already set up server with dpytest.
            pass

        await self.change_presence(
            activity=discord.Game("rien de particulier mais on est là quoi")
        )

        logger.info("\nBOT IS READY!\n")

    @filter_message
    async def on_message(self, message: Message):
        if message.channel.type is discord.ChannelType.private:
            return await self.on_private_message(message)
        if self.user in message.mentions and not message.reference:
            return await message.channel.send(Messages.BONSOIR_NON)

        content = clean_message(message.content)
        args = content.split(" ")

        manager: typing.Type[CommandManager] = None
        if args[0] == Constants.PREFIX_STANDARD:
            logger.info(f"Received standard command: {args}")
            manager = StandardCommandManager
        elif args[0] == Constants.PREFIX_ICECOIN:
            logger.info(f"Received icécoin command: {args}")
            manager = IcecoinCommandManager
        else:
            return

        del args[0]

        try:
            resp = await manager.parse_command(args, message)
        except AbstractICBOTException as e:
            resp = e
        await self._handle_send(message.channel, resp.to_message())

    async def on_private_message(self, message: Message):
        await message.channel.send(Messages.PRIVATE_MESSAGE_ANSWER)

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

    async def _fetch_channels(self):
        """Fetches the channels that the bot needs to work (memes, copie-pates).

        Raises
        ------
        ChannelNotFound if one of the channel is not found.
        """
        update_channels("memes", _load_channel(self.guilds[0].channels, "memes"))
        update_channels(
            "copie-pates", _load_channel(self.guilds[0].channels, "copie-pates")
        )
