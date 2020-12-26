import asyncio

import youtube_dl as ydl

import discord
from discord.ext import commands

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
    
    @commands.command()
    async def play(self, ctx, playable):
        """
            Plays song passed as an arguemnet 'playbale'.
        """
        try:
            vc = ctx.author.voice.channel
            await vc.connect()
        except Exception as e:
            pass
        self.queue.append(playable)

    
    @commands.command()
    async def quit(self, ctx):
        """
            Leaves the vc in the server it was prompted in.
        """
        for vc in self.bot.voice_clients:
            if vc.guild.id == ctx.guild.id:
                self.queue = []
                await vc.disconnect()


def setup(bot):
    bot.add_cog(Music(bot)) 