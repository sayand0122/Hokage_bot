import re
import discord
import os
import dotenv
import random

from roast import insult

from discord.ext import commands
from datetime import datetime
from dotenv.main import load_dotenv

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


@bot.command(aliases=['slam'])
async def roast(ctx, *, link):
    embed = discord.Embed(title='Roast', color=0x11ad4b)
    embed.add_field(name='😈', value=f'{link} , {random.choice(insult)}')
    await ctx.send(embed=embed)

bot.run(TOKEN)
