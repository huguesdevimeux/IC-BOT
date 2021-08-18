from ICBOT.command_manager import CommandManager


class StandardCommandManager(CommandManager):
    _MAP_COMMANDS = {command.info.call_name: command for command in ALL_COMMANDS}
    def get_commmand(cls, key: typing.Union[str, int]) -> BotResponse:
        return _