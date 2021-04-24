import logging

__all__ = ["logger"]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
# Tell the discord API logger to STFU
logging.getLogger("discord").setLevel(logging.WARNING)
logger = logging.getLogger("ICEBOT")# Vim sessions
logger.setLevel(logging.DEBUG)
