import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Game

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

bot = commands.Bot(command_prefix="c!")
client = discord.ext.commands.Bot(command_prefix = "c!")

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

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError, commands.Cog):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError, commands.Cog):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer, commands.Cog):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'```ini\n[{data["title"]} foi adicionado à fila.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'Título': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer(commands.Cog):
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'Ocorreu um erro em processar essa música.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**Tocando agora:** `{source.title}` . Solicitado por: '
                                               f'`{source.requester}`')
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Desconecta e limpa a fileira."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

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
                return await ctx.send('Esse comando não pode ser usado em DMs.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Erro ao conectar ao Voice Chat. '
                           'Tenha certeza que você tentou me conectar à um canal válido.')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='conectar', aliases=['entrar'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Conecta ao VC.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('Nenhum canal para entrar. Certifique se você está em um/me deu um canal válido.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Indo para o canal: <{channel}> algo deu errado.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Conectando ao canal: <{channel}> algo deu errado.')

        await ctx.send(f'Conectada em: **{channel}**', delete_after=20)

    @commands.command(name='play', aliases=['tocar'])
    async def play_(self, ctx, *, search: str):
        """Pede uma musica e adiciona para a fila.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
        await player.queue.put(source)

    @commands.command(name='pausar')
    async def pause_(self, ctx):
        """Pausa a musica atual."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('Eu ainda não estou tocando nada.', delete_after=20)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Pausou a música.')

    @commands.command(name='retomar')
    async def resume_(self, ctx):
        """Continua a música pausada"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Eu ainda não estou tocando nada.', delete_after=20)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: Retomou a música')

    @commands.command(name='pular')
    async def skip_(self, ctx):
        """Pula a música."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Eu ainda não estou tocando nada.', delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: Pulou a música')

    @commands.command(name='queue', aliases=['f', 'playlist', 'fila', 'fileira'])
    async def queue_info(self, ctx):
        """Mostra a fila."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Eu não estou conectada em um Voice Channel.', delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('Não há mais músicas na fila.')

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Próxima música: {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)

    @commands.command(name='agora', aliases=['tocando', 'atual', 'musicat'])
    async def now_playing_(self, ctx):
        """Infos sobre a música atual."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Eu não estou em nenhum Voice Channel.', delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('Eu não estou tocando nada.')

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass
        player.np = await ctx.send(f'**TOCANDO AGORA:** `{vc.source.title}` '
                                   f'Solicitado por `{vc.source.requester}`')


    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        """Muda o volume
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Eu não estou conectada em um VC!', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send('Entre um valor entre 0 e 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'**`{ctx.author}`**: Mudou o volume para **{vol}%**')

    @commands.command(name='parar')
    async def stop_(self, ctx):
        """Para a música e apaga a fila.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Eu não estou tocando nada!', delete_after=20)

        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))
