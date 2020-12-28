import asyncio

from youtube_dl import YoutubeDL
import pafy

import validators
from datetime import datetime
# from pprint import pprint

import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
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
    async def play(self, ctx, *playable):
        """
            Plays song passed as an arguemnet 'playable'.
        """
        
        # Joins song keywords exactly as user provided.
        playable = ' '.join(playable[:])
        views = 0
        
        try:   
            if validators.url(playable):
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playable, download=False) 
            else:
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playable, download=False)
                    info = info['entries'][0]
            
            url = info['formats'][0]['url']
            thumbnail_url = info['thumbnail']
            webpage_url = info['webpage_url']
            title = info['title']
            uploader = info['uploader']
            channel_url = info['channel_url'] 
            
            # youtube_dl doesnt give accurate view count above 100M (Havent checked for a lesser amount once I discovered this)
            video = pafy.new(webpage_url)
            views = video.viewcount
            duration = video.duration
            
            vc = ctx.author.voice.channel
            vc = await vc.connect()
            
            embed = discord.Embed()
            embed.set_image(url=thumbnail_url)
            embed.add_field(name='\u200b', value=f'**[{title}]({webpage_url})**')
            embed.add_field(name='\u200b', value=f'**[{uploader}]({channel_url})**', inline=False)
            embed.add_field(name='Views', value=f'{views}')        
            embed.add_field(name='Duration', value=f'{duration}')  
            await ctx.send(embed=embed)
            
            
            vc.play(FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS))
        except Exception as e:
            pass
            

    @commands.command(aliases=['leave', 'stop'])
    async def quit(self, ctx):
        """
            Leaves the vc in the server it was prompted in.
        """
        vc = get(self.bot.voice_clients, guild=ctx.message.guild)
        if vc:
            vc.stop()
            await vc.disconnect()
            
    
    @commands.command()
    async def pause(self, ctx):
        """
            Pauses vc in the server it was prompted in.
        """
        vc = get(self.bot.voice_clients, guild=ctx.message.guild)
        if vc:
            vc.pause()
            
    
    @commands.command()
    async def resume(self, ctx):
        """
            Resumes vc in the server it was prompted in.
        """
        vc = get(self.bot.voice_clients, guild=ctx.message.guild)
        if vc:
            vc.resume()


def setup(bot):
    bot.add_cog(Player(bot)) 