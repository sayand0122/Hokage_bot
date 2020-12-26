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


# maintaining cogs
@client.command()
async def load(ctx, extension):
    client.load_exntension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_exntension(f'cogs.{extension}')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@bot.command(aliases=['slap', 'destroy'])
async def roast(ctx, *, link):
    embed = discord.Embed(title='Roast', color=0x11ad4b)
    embed.add_field(name='😈', value=f'{link} , {os.urandom.choice(roast)}')
    await ctx.send(embed=embed)

bot.run(TOKEN)
