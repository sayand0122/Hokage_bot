import discord
import os
import dotenv
import pymongo

from discord.ext import commands
from datetime import datetime
from dotenv.main import load_dotenv


"""
Loads environment variables from .env.
Initializes TOKEN as bot token.
"""
load_dotenv()

DISCORD_TOKEN = os.environ.get('TOKEN')


bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    """
    Sends a message in terminal with start time.
    Primary use is just for logging.
    """
    launch_time = datetime.now()
    print(f"Started at {launch_time}")

    

# clear commands and its error handling
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass the amount to clear the number of data.")

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

