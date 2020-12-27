import asyncio
from pprint import pprint

from youtube_dl import YoutubeDL
import pafy

import validators
from pprint import pprint

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
    async def play(self, ctx, *playable):
        """
            Plays song passed as an arguemnet 'playable'.
        """
        
        # Joins song keywords exactly as user provided.
        playable = ' '.join(playable[:])
        thumnail = None
        
        try:   
            if validators.url(playable):
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playable, download=False) 
            else:
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playable, download=False)
                    info = info['entries'][0]
            
            url = info['formats'][0]['url']
            thumbnail = info['thumbnail']
            webpage = info['webpage_url']
            title = info['title']
            uploader = info['uploader']
            channel_url = info['channel_url']
            views = pafy.new(webpage).viewcount
            print(views)
            # pprint(info)
            
            embed = discord.Embed()
            embed.set_thumbnail(url=thumbnail)
            embed.add_field(name='\u200b', value=f'**[{title}]({webpage})**')
            embed.add_field(name='\u200b', value=f'**[{uploader}]({channel_url})**', inline=False)
            embed.add_field(name='Views', value=f'{views}', inline=False)
            
            await ctx.send(embed=embed)
            
            # vc = ctx.author.voice.channel
            # vc = await vc.connect()
            # vc.play(FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS))
        except Exception as e:
            pass
            

    @commands.command(aliases=['leave'])
    async def quit(self, ctx):
        """
            Leaves the vc in the server it was prompted in.
        """
        vc = get(self.bot.voice_clients, guild=ctx.message.guild)
        if vc:
            await vc.disconnect()


def setup(bot):
    bot.add_cog(Player(bot)) 