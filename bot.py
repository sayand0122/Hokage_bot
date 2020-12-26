import discord
import os
import dotenv

from discord.ext import commands
from datetime import datetime
from dotenv.main import load_dotenv

load_dotenv()
TOKEN = os.environ.get('SECRET')

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    """
        Sends a message in terminal with start time.
        Primary use is just for logging.
    """
    launch_time = datetime.now()
    print(f"Started at {launch_time}")

# ping it and it returns your latency


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


bot.run(TOKEN)
