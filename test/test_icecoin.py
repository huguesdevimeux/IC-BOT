import discord.ext.test as dpytest
import pytest

from ICBOT.constants.constants import ErrorMessages, Constants
from ICBOT.exceptions import InvalidArgument
from ICBOT.icecoin.commands import Help

help_message = Help().to_message()

PREFIX = Constants.PREFIX_ICECOIN


@pytest.mark.asyncio
async def test_no_command(bot):
    await dpytest.message(PREFIX)
    await Help.build_with_args()
    assert not dpytest.verify().message().nothing()
    m = dpytest.get_embed()
    assert dpytest.embed_eq(m, help_message)


@pytest.mark.asyncio
async def test_help(bot):
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
async def test_info(bot, michel):
    await dpytest.message(f"{PREFIX} infos")
    assert not dpytest.verify().message().nothing()
    assert (
        dpytest.verify()
            .message()
            .embed(InvalidArgument(ErrorMessages.NO_ONE_MENTIONED_INFOS).to_message())
    )

    await dpytest.message(f"{PREFIX} {michel.mention}")
    assert not dpytest.verify().message().nothing()


@pytest.mark.asyncio
def test_don(bot):
    # TODO
    pass
