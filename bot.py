import discord
from discord.ext import commands

from datetime import datetime
import dotenv
from dotenv.main import load_dotenv
import os

"""
    Loads environment variables from .env.
    Initializes TOKEN as bot token.
"""
load_dotenv()
TOKEN = os.environ.get('TOKEN')

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    """
        Sends a message in terminal with start time.
        Primary use is just for logging.
    """
    launch_time = datetime.now()
    print(f"Started at {launch_time}")
    

for cog in os.listdir(r"./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded\n{e}")


bot.run(TOKEN)