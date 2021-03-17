from .BotResponse import BotResponse
from abc import ABC, abstractmethod

from ICBOT.constants import Commands, ErrorMessages

from .templates import ErrorMessage


class AbstractICBOTException(Exception, BotResponse):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def to_message(self):
        return ErrorMessage(self.message, show_doc=True)


class NoCommand(AbstractICBOTException):
    def __init__(
        self,
    ) -> None:
        super().__init__(message=ErrorMessages.NO_COMMAND)


class NoArgument(AbstractICBOTException):
    def __init__(self, command_name) -> None:
        super().__init__(message=ErrorMessages.NO_ARGUMENT_GIVEN.format(command_name))


class InvalidArgument(AbstractICBOTException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidCommandName(AbstractICBOTException):
    pass
