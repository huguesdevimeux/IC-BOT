import typing
from typing import Union

import discord
from discord.channel import GroupChannel
from discord.embeds import Embed
from discord.enums import ChannelType
from discord.errors import HTTPException
from discord.ext import tasks
from discord.message import Message
from discord.utils import to_json

from .BotResponse import BotResponse
from .commands.command_manager import CommandManager
from .exceptions import AbstractICBOTException
from .constants import Constants, Messages
from .mail_fetcher import MailFetcher
from .templates import EmebedWithFile, Mail
from .utils.cleaner import clean_message
from .utils.filter import filter_message
from .utils.logging import logger


class ICBOT(discord.Client):
    async def on_ready(self):
        assert len(self.guilds) == 1
        logger.info("BOT IS READY")
        for guild in self.guilds:
            logger.info(f"On {guild} (id {guild.id}")
        
        self._mail_fetcher = MailFetcher()
        self._channels_mails = {}
        for section in Constants.SECTIONS:
            self._channels_mails[section] = discord.utils.get(self.guilds[0].channels, name=Constants.CHANNEL_MAILS_NAMES[section])
        if self._channels_mails[section] is None: 
            raise Exception(f"Couldn't find mail channel named {Constants.CHANNEL_MAILS_NAMES[section]}")
        logger.info(f"Found mail channels on {self.guilds[0]}")
        
        self.handle_mails.start()
        
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
            
    @tasks.loop(minutes=3)
    async def handle_mails(self): 
        logger.info("Refreshing mail.")
        # Fuck this code is ugly
        with self._mail_fetcher.fetched_email() as mails_section:
            for section in mails_section:
                if mails_section[section] is not None :
                    logger.info(f"Trying to send an email to {section}")
                    logger.info(f"Mail to send ('object') {mails_section[section]['object']}")
                    to_send = Mail(mails_section[section]["sender"], mails_section[section]["object"], mails_section[section]["content"])
                    try:
                        await self._handle_send(self._channels_mails[section], to_send)
                    except HTTPException as e: 
                        logger.warning(f"Could send mail {mails_section[section]['object']}")
                        logger.warning(e)
                        raise Exception()