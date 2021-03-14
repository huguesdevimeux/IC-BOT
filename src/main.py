from ICBOT import ICBOT
from dotenv import dotenv_values

TOKEN = dotenv_values(".env.secret")["TOKEN"]
ICBOT().run(TOKEN)
