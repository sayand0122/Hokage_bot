import asyncio
from pprint import pprint

from youtube_dl import YoutubeDL

import validators

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
    
    @commands.command()
    async def play(self, ctx, playable):
        """
            Plays song passed as an arguemnet 'playable'.
        """
        try:   
            if validators.url(playable):
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playable, download=False) 
                URL = info['formats'][0]['url']
            else:
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playable, download=False)
                URL = info['entries'][0]['formats'][0]['url']
            print(f"url: {URL}")
            
            vc = ctx.author.voice.channel
            vc = await vc.connect()
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