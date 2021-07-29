__all__ = ["CHANNELS", "update_channels"]


from typing import Dict
from discord.channel import TextChannel


CHANNELS: Dict[str, TextChannel] = {}


def update_channels(name, channel):
    # Ggngng globals are bad gngng
    global CHANNELS
    CHANNELS[name] = channel
