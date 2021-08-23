
import discord.ext.test as dpytest
import pytest

from ICBOT.channels import CHANNELS
from ICBOT.constants.constants import Constants, ErrorMessages
from ICBOT.icbot import ICBOT
from ICBOT.standard_commands.commands import Help

PREFIX = Constants.PREFIX_STANDARD


@pytest.fixture
async def help_message():
    return (await Help.build_with_args()).to_message()


@pytest.mark.asyncio
async def test_no_command(bot, help_message):
    await dpytest.message(PREFIX)
    await Help.build_with_args()
    assert dpytest.verify().message().embed(help_message)


@pytest.mark.asyncio
async def test_help(bot, help_message):
    await dpytest.message(f"{PREFIX} aide")
    assert (
            ErrorMessages.COMMAND_NOT_FOUND.format("aide")
            not in dpytest.get_embed(peek=True).description
    )
    assert not dpytest.verify().message().nothing()
    await Help.build_with_args()
    assert dpytest.verify().message().embed(help_message)


@pytest.mark.asyncio
async def test_wrong_command(bot):
    r = "qsddqsd"
    await dpytest.message(f"{PREFIX} {r}")
    message = dpytest.get_message(peek=False)
    assert len(message.embeds) == 1
    assert ErrorMessages.COMMAND_NOT_FOUND.format(r) in message.embeds[0].description


@pytest.mark.asyncio
async def test_bonsoir_non(bot):
    pass

@pytest.mark.asyncio
async def test_drive(bot):
    await dpytest.message(f"{PREFIX} drive")
    assert not dpytest.verify().message().nothing()
    message = dpytest.get_embed()

    from ICBOT.exceptions import NoArgument
    assert dpytest.embed_eq(message, NoArgument(StandardCommands.DRIVE.name).to_message())

    await dpytest.message(f"{PREFIX} drive test")
    from ICBOT.exceptions import InvalidArgument
    assert dpytest.embed_eq(dpytest.get_embed(), InvalidArgument(ErrorMessages.DRIVE_NO_FILE_SPECIFIED).to_message())


@pytest.mark.xfail(reason="dpytest does not support emoji addition")
@pytest.mark.asyncio
async def test_pandalea(bot):
    await dpytest.message(f"{PREFIX} pandalea")
    dpytest.get_message()


@pytest.mark.xfail(reason="dpytest fail.")
@pytest.mark.asyncio
async def test_random_meme(bot: ICBOT):
    await dpytest.message(f"{PREFIX} meme")
    assert "memes" in CHANNELS
    assert (
            ErrorMessages.COMMAND_NOT_FOUND.format("meme")
            not in dpytest.get_embed(peek=True).description
    )
    assert not dpytest.verify().message().peek().nothing()
    message = dpytest.get_embed()
    assert len(message.image) > 0


@pytest.mark.xfail(reason="dpytest fail.")
@pytest.mark.asyncio
async def test_random_mmeme(bot: ICBOT):
    await dpytest.message(f"{PREFIX} copiepate")
    assert "copie-pates" in CHANNELS
    assert (
            ErrorMessages.COMMAND_NOT_FOUND.format("copiepate")
            not in dpytest.get_embed(peek=True).description
    )
    assert not dpytest.verify().message().peek().nothing()
    message = dpytest.get_embed()
    assert len(message.image) > 0
