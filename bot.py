import discord
from discord.ext import commands
import dotenv

from datetime import datetime

from dotenv.main import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    """
        Sends a message in terminal with start time.
        Primary use is just for logging.
    """
    launch_time = datetime.now()
    print(f"Started at {launch_time}")


bot.run(TOKEN)
