import discord
from discord.message import Message

from .commands.command_manager import CommandManager
from .commands.exceptions import AbstractICBOTException
from .utils.cleaner import clean_message
from .utils.filter import filter_message
from .utils.logging import logger
from .constants import Constants


class ICBOT(discord.Client):
    async def on_ready(self):
        logger.info("BOT IS READY")

    @filter_message
    async def on_message(self, message: Message):
        logger.debug(f"Message recieved {message.content} from {message.author}")
        content = clean_message(message.content)
        logger.debug(f"Cleaned message : {content}")
        args = content.split(" ")
        if args.pop(0) == Constants.PREFIX:
            try:
                resp = CommandManager.parse_command(args)
            except AbstractICBOTException as e:
                resp = e
            await message.channel.send(embed=resp.to_embed())
            logger.info(f"Sent message {resp}")
