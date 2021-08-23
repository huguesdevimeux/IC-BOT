from ICBOT.exceptions import AbstractICBOTException
from ICBOT.icecoin.templates import ErrorMessage


class IceCoinException(AbstractICBOTException):
    def to_message(self):
        return ErrorMessage(self.message, show_doc=True)


class NotEnoughMoney(IceCoinException):
    def __init__(self):
        super(NotEnoughMoney, self).__init__(message="T'as pas assez d'argent pauvre")


class CantMine(IceCoinException):
    def __init__(self):
        super(CantMine, self).__init__(message="Vous ne pouvez pas miner aussi vite !")
