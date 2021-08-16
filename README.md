# IC-BOT
A cool Discord bot made for the EPFL IC 2021 promotion 

## Contributing 
Contributions are welcome and encouraged. 
There are a few steps to follow before being able to work on the bot: 

- Clone the repository: 
  ```
  git clone git@github.com:huguesdevimeux/IC-BOT.git
  ```
- Install the requirements: 
  ```
  pip install -r requirements.txt
  ```
 - You'll now have to get a token to be allowed to run a discord bot. It's fairly easy, a tutorial can be found [here](https://realpython.com/how-to-make-a-discord-bot-python/#creating-an-application)
 - This repository uses `.env` files to ensure that secrets are not pushed. As you can see in `src/main.py`, you have to create at at the root a file named `.env.secret`, and put a single line `TOKEN = YOURTOKEN` inside it.

## Running the bot: 
Run `src/main.py`. That's all :D

### NOTE: 
> All the sensible informations are stored in `.env.shared`. Since this file is not pushed, all the variables normally extracted from this file are replaced with NON_LOADED_DATA. (See `ICBOT/var_env.py`). Feel free to ask that I share this file with you if you need it. The bot can work without these value, just not completly. 
