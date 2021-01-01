import discord
import os
import dotenv
import pymongo

from discord.ext import commands
from datetime import datetime
from dotenv.main import load_dotenv
from pymongo import MongoClient

"""
    Loads environment variables from .env.
    Initializes TOKEN as bot token.
"""
load_dotenv()

DISCORD_TOKEN = os.environ.get('SECRET')

mongo_url = os.environ.get("mongo_url")

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    """
        Sends a message in terminal with start time.
        Primary use is just for logging.
    """
    launch_time = datetime.now()
    print(f"Started at {launch_time}")

    cluster = MongoClient(mongo_url)
    db = cluster['hokage-base']
    collection = db['data']


# maintaining cogs
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_exntension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(DISCORD_TOKEN)
