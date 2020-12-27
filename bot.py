import discord
import os
import dotenv

from discord.ext import commands
from datetime import datetime
from dotenv.main import load_dotenv

"""
    Loads environment variables from .env.
    Initializes TOKEN as bot token.
"""
load_dotenv()
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    """
        Sends a message in terminal with start time.
        Primary use is just for logging.
    """
    launch_time = datetime.now()
    print(f"Started at {launch_time}")

# maintaining cogs


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, cog=None):
    """
        Hot reloading of cogs.
    """
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        cog1 = f'cog `{cog}`'

    await ctx.send(f"Successfully reloaded {cog}")


bot.run(DISCORD_TOKEN)
