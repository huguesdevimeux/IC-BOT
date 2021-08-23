from pathlib import Path

import discord
import discord.ext.test as dpytest
import pytest

from ICBOT import ICBOT


@pytest.fixture
async def bot(event_loop):
    intents = discord.Intents.default()
    intents.members = True
    bot: ICBOT = ICBOT(loop=event_loop, intents=intents)
    dpytest.configure(bot, num_members=2)

    config = dpytest.runner.get_config()

    # Copie-pates
    copie_pate_channel = dpytest.back.make_text_channel(
        "copie-pates", guild=config.guilds[0]
    )
    dpytest.message(content="Test1", channel=copie_pate_channel)

    # Memes
    meme_channel = dpytest.back.make_text_channel("memes", guild=config.guilds[0])
    dpytest.message(
        content="", channel=meme_channel, attachments=[Path(__file__) / "meme.jpeg"]
    )
    await dpytest.run_all_events()
    await bot._fetch_channels()
    return bot


@pytest.fixture
async def michel() -> discord.Member:
    michel: discord.Member = dpytest.get_config().guilds[0].members[-1]
    assert "FakeApp" in michel.display_name
    return michel
