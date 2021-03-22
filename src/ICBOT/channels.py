__all__ = ["CHANNELS", "update_channels"]


CHANNELS = {}


def update_channels(name, channel):
    # Ggngng globals are bad gngng
    global CHANNELS
    CHANNELS[name] = channel
