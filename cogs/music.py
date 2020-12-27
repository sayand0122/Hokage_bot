import asyncio

from youtube_dl import YoutubeDL

import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YDL_OPTIONS = {
            'format': 'bestaudio',
            'noplaylist': 'True',
            'nocheckcertificate': True,
            'default_search': 'auto'
        }

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music cog is ready')

    @commands.command()
    async def play(self, ctx, url):
        """
            Plays song passed as an arguemnet 'playbale'.
        """
        try:
            vc = ctx.author.voice.channel
            vc = await vc.connect()

            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)

            URL = info['formats'][0]['url']
            vc.play(FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS))
        except Exception as e:
            pass

    @commands.command()
    async def quit(self, ctx):
        """
            Leaves the vc in the server it was prompted in.
        """
        vc = get(self.bot.voice_clients, guild=ctx.message.guild)
        if vc:
            await vc.disconnect()


def setup(bot):
    bot.add_cog(Player(bot))
