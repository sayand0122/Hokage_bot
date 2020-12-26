import discord
import os
import dotenv

from discord.ext import commands
from datetime import datetime
from dotenv.main import load_dotenv
import os

"""
    Loads environment variables from .env.
    Initializes TOKEN as bot token.
"""
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


@bot.command()
async def hi(ctx):
    await ctx.send('hola')


"""
    Loads cogs from ./cogs directory.
    Make sure your file name starts with '_' if you dont want it to load just yet. 
"""
for cog in os.listdir(r"./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded\n{e}")


bot.run(TOKEN)
