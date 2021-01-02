import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

import asyncio
from async_timeout import timeout
import itertools
from youtube_dl import YoutubeDL
from validator_collection import checkers
import pafy


class Audio():
    """Creates an audio object with relevant data."""
    
    def __init__(self, search, requester):
        self.requester = requester
        self.audio = None
        self.title = None   
        self.search = search
        self.embed = None
        self.gather_stream()
    
    def gather_stream(self):
        """Gathers audio stream and relevant info."""
        ffmpegopts = {
        'before_options': '-nostdin',
        'options': '-vn'
        }   
        ytdlopts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
        }
        
        ytdl = YoutubeDL(ytdlopts)
        
        data = ytdl.extract_info(self.search, download=False)
        
        if not checkers.is_url(self.search):
            data = data['entries'][0]
        
        self.audio = FFmpegPCMAudio(data['formats'][0]['url'], **ffmpegopts)
        thumbnail_url = data['thumbnail']
        webpage_url = data['webpage_url']
        self.title = data['title']
        uploader = data['uploader']
        channel_url = data['channel_url']      
        # youtube_dl doesnt give accurate view count above 100M (Havent checked for a lesser amount once I discovered this).
        video = pafy.new(webpage_url)
        views = video.viewcount
        duration = video.duration  
        
        song_embed = discord.Embed()
        song_embed.set_image(url=thumbnail_url)
        song_embed.add_field(name='\u200b', value=f'**[{self.title}]({webpage_url})**')
        song_embed.add_field(name='\u200b', value=f'**[{uploader}]({channel_url})**', inline=False)
        song_embed.add_field(name='Views', value=f'{views}')        
        song_embed.add_field(name='Duration', value=f'{duration}')      
        song_embed.add_field(name='Requested by', value=f'{self.requester.mention}')   
        self.embed = song_embed  


class MusicPlayer:
    """Player that is generated for each guild (one channel per guild).
    When the bot disconnects from the voice client it's instance will be destroyed.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        
        self.current = None

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        ctx.bot.loop.create_task(self.player_loop(self.ctx))

    async def player_loop(self, ctx):
        """Main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
                    self.current = source
            except asyncio.TimeoutError:
                return self.destroy(self._guild)
            
            self._guild.voice_client.play(source.audio, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            
            await self.next.wait()
            
    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass
            
    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send("`This command can not be used in Private Messages.`")
            except discord.HTTPException:
                pass
        else:
            pass

    def get_player(self, ctx):
        """Retrieve the guild player or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    async def connect(self, ctx):
        """Connect to voice the user is in."""
        channel = None
        
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            print('Connection failed')

        vc = ctx.voice_client


        if vc:
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                print('Connection failed')           
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                print('Connection failed')


    @commands.command(name='play', aliases=['sing'])
    async def play_(self, ctx, *search: str):
        """Requests a song and adds to queue.

        Args:
            search (str): keywords for querying the song on youtube.
        """
        search = ' '.join(search[:])
   
        vc = ctx.voice_client
        
        if not vc:        
            await self.connect(ctx)
            
        player = self.get_player(ctx)

        source = Audio(search, ctx.message.author)
        await ctx.send(embed=source.embed)  

        await player.queue.put(source)

    @commands.command(name='pause')
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return 
        elif vc.is_paused():
            return

        vc.pause()

    @commands.command(name='resume')
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return 
        elif not vc.is_paused():
            return

        vc.resume()

    @commands.command(name='skip')
    async def skip_(self, ctx):
        """Skip the current song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return 

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()

    @commands.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')

        # Queries upto 5 songs in the queue. 
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        desc = '\n'.join(f'**`{_.title}`**' for _ in upcoming)
        embed = discord.Embed(title='Upcoming - Next', description=desc)

        await ctx.send(embed=embed)

    @commands.command(name='stop')
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return 

        await self.cleanup(ctx.guild)
        
    @commands.command()
    async def current(self, ctx):
        """Displays current track."""
        vc = ctx.voice_client
        
        if not vc or not vc.is_connected():
            return
        
        player = self.get_player(ctx)
        
        desc = player.current.title
        if desc:
            embed = discord.Embed(title='Currently Playing', description=desc)
            await ctx.send(embed=embed)
             

def setup(bot):
    bot.add_cog(Music(bot))

