import re

from discord.utils import escape_mentions
from unidecode import unidecode


def remove_mentions(message_content):
    message_content = escape_mentions(message_content)
    return re.sub(
        r'(@([A-Za-z0-9`~!@#$%^&*()_|+\-=?;:\'",.<>\{\}\[\]\\\/]{2,32}))',
        "",
        message_content,
    ).strip()


def clean_message(message_content):
    # Remove urls
    message_content = re.sub(
        r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
        " ",
        message_content,
    ).strip()
    return unidecode(message_content)
