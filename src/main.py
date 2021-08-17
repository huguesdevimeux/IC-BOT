from pathlib import Path

from dotenv import dotenv_values

from ICBOT import ICBOT

env_path = Path(__file__).parents[1] / ".env.secret"
TOKEN = dotenv_values(env_path, verbose=True)["TOKEN"]
ICBOT().run(TOKEN)
