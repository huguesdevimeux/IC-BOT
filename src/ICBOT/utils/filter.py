from discord.message import Message


def filter_message(func):
    async def wrapper(self, message: Message):
        if not (message.author == self.user):
            await func(self, message)

    return wrapper
