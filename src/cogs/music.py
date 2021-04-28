# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from enum import Enum
import typing as t
import wavelink
import asyncio
import random
import re
from cogs.utils import Logger, Settings, Config, Commands, Strings, Utils
from logging_files.music_log import logger

CONFIG = Config()

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

OPTIONS = {
    "1️⃣": 0,"2️⃣": 1,"3️⃣": 2,"4️⃣": 3,"5️⃣": 4,
}

class AlreadyConnectedToChannel(commands.CommandError):
    pass

class NoVoiceChannel(commands.CommandError):
    pass

class QueueIsEmpty(commands.CommandError):
    pass

class NoTracksFound(commands.CommandError):
    pass

class PlayerIsAlreadyPaused(commands.CommandError):
    pass

class PlayerIsAlreadyPlaying(commands.CommandError):
    pass

class NoMoreTracks(commands.CommandError):
    pass

class NoPreviousTracks(commands.CommandError):
    pass

class InvalidRepeatMode(commands.CommandError):
    pass

class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2

class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty
        self.position += 1
        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None
        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty
        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "Yok":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "Tümü":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel
        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        if not tracks:
            raise NoTracksFound
        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            playEmbed = discord.Embed(title=STRINGS['music']['embed_controler_title'], description=STRINGS['music']['embed_controler_desc'], color=0xff8000)
            playEmbed.add_field(name=STRINGS['music']['embed_controler_secdesc'], value=f"{tracks[0].title}", inline=True)
            playEmbed.add_field(name=STRINGS['music']['embed_controler_dur'], value=f"**({tracks[0].length//60000}:{str(tracks[0].length%60).zfill(2)})**",inline=True)
            playEmbed.add_field(name=STRINGS['music']['embed_controler_req'], value=f"{ctx.author}", inline=True)
            playEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])
            
            await ctx.send(embed=playEmbed)
            
            logger.info(f"Tracks added by {ctx.author} in {ctx.message.guild}")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                playEmbed_2 = discord.Embed(title="Parça Listeye Eklendi",description = f"Parça: **{track.title}**\nUzunluk: **({track.length//60000}:{str(track.length%60).zfill(2)})**",colour=0xffd500, timestamp=ctx.message.created_at)
                playEmbed_2.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.message.delete()
                
                await ctx.send(embed=playEmbed_2)
                
                logger.info(f"Tracks added by {ctx.author} in {ctx.message.guild}")
        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )
        chooseTrackEmbed = discord.Embed(description=("\n".join(f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"for i, t in enumerate(tracks[:5]))),colour=0xffd500,timestamp=ctx.message.created_at)
        chooseTrackEmbed.set_author(name="Arama Sonuçları")
        chooseTrackEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        msg = await ctx.send(embed=chooseTrackEmbed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        nodes = {
            "MAIN": {
                "host": "heroku-lavalink-heliaservice.herokuapp.com",
                "port": 80,
                "rest_uri": "https://heroku-lavalink-heliaservice.herokuapp.com",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "us",
            }
        }
        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)
    @commands.command(name="leave", brief = "L.",aliases=["fuck_off","buggerout","disconnect","lv"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        
        logger.info(f"Music | Leave | Tarafından: {ctx.author}")

    @commands.command(name="play", brief = "play music.",aliases=["p","pl"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)
        
        if not player.is_connected:
            await player.connect(ctx)
        
        if query is None:
            
            if player.queue.is_empty:
                raise QueueIsEmpty
            elif player.is_paused :
                await player.set_pause(False)
                playEmbed=discord.Embed(title="Çalmaya devam ettiriliyor.",colour=0xffd500)
                playEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
                
                await ctx.send(embed=playEmbed)
            else:
                raise PlayerIsAlreadyPlaying    
        else:
            query = query.strip("<>")
            
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"
            
            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPlaying):
            playEmbed_2=discord.Embed(title="Halihazırda çalan bir parça var.",colour=0xffd500)
            
            await ctx.send(embed=playEmbed_2)
        elif isinstance(exc, QueueIsEmpty):
            playEmbed_3=discord.Embed(title="Liste boş olduğundan çalınacak bir şarkı yok.",colour=0xffd500)
            
            await ctx.send(embed=playEmbed_3)

    @commands.command(name="pause", brief = "Pause playback.",aliases=["ps","pauza","пауза"])
    async def pause_command(self, ctx):
        player = self.get_player(ctx)
        
        if player.is_paused:
            raise PlayerIsAlreadyPaused
        await player.set_pause(True)
        pauseEmbed=discord.Embed(title="Parça duraklatıldı.",colour=0xffd500)
        pauseEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=pauseEmbed)
        
        logger.info(f"Music paused by {ctx.author} in {ctx.message.guild}")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            pauseer_embed=discord.Embed(title="Halihazırda duraklatılan bir şarkı var.",colour=0xffd500)
            
            await ctx.send(embed=pauseer_embed)

    @commands.command(name="Dur", brief = "Sesi durdurur ve listeyi temizler.",aliases=["dur","Stop","stop"])
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        stopEmbed=discord.Embed(title="Oynatıcı durduruldu ve liste temizlendi.",colour=0xffd500)
        stopEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=stopEmbed)
        
        logger.info(f"Music | Stop | Tarafından: {ctx.author}")

    @commands.command(name="Sıradaki", brief = "Listedeki bir sonraki şarkıya atlar.",aliases=["sıradaki","Skip","skip","Next","next"])
    async def next_command(self, ctx):
        player = self.get_player(ctx)
        
        if not player.queue.upcoming:
            raise NoMoreTracks
        await player.stop()
        nextEmbed=discord.Embed(title="Listedeki mevcut sıradan bir sonraki parça çalınıyor.",colour=0xffd500)
        nextEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=nextEmbed)
        
        logger.info(f"Music | Next | Tarafından: {ctx.author}")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            nextEmbed_2=discord.Embed(title="Liste boş.",colour=0xffd500)
            
            await ctx.send(embed=nextEmbed_2)
        elif isinstance(exc, NoMoreTracks):
            nextEmbed_3=discord.Embed(title="Listede başka parça yok.",colour=0xffd500)
            
            await ctx.send(embed=nextEmbed_3)

    @commands.command(name="Önceki", brief = "Listedeki bir önceki şarkıya döner.",aliases=["önceki","Previous","previous"])
    async def previous_command(self, ctx):
        player = self.get_player(ctx)
        
        if not player.queue.history:
            raise NoPreviousTracks
        player.queue.position -= 2
        await player.stop()
        previousEmbed=discord.Embed(title="Listedeki mevcut sıradan bir önceki parça çalınıyor.",colour=0xffd500)
        previousEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=previousEmbed)
        
        logger.info(f"Music | Previous | Tarafından: {ctx.author}")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            previousEmbed_2=discord.Embed(title="Liste boş.",colour=0xffd500)
            
            await ctx.send(embed=previousEmbed_2)
        elif isinstance(exc, NoPreviousTracks):
            previousEmbed_3=discord.Embed(title="Listede başka parça yok.",colour=0xffd500)
            
            await ctx.send(embed=previousEmbed_3)

    @commands.command(name="Karıştır", brief = "Listeyi karıştırır.",aliases=["karıştır","Shuffle","shuffle"])
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        shuffleEmbed=discord.Embed(title="Liste karıştırıldı.",colour=0xffd500)
        shuffleEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=shuffleEmbed)
        
        logger.info(f"Music | Shuffle | Tarafından: {ctx.author}")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            shuffleEmbed_2=discord.Embed(title="Liste şu anda boş.",colour=0xffd500)
            
            await ctx.send(embed=shuffleEmbed_2)

    @commands.command(name="Tekrarla", brief = "Mevcut parçayı veya listeyi tekrarlar.",aliases=["tekrarla","Repeat","repeat"])
    async def repeat_command(self, ctx, mode: str):
        mode = mode.title()
        if mode not in ("Yok", "1", "Tümü"):
            raise InvalidRepeatMode
        player = self.get_player(ctx)
        
        if player.queue.is_empty:
            raise QueueIsEmpty
        player.queue.set_repeat_mode(mode)
        repeatEmbed=discord.Embed(title=f"Tekrarlama modu {mode} olarak ayarlandı.",colour=0xffd500)
        repeatEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=repeatEmbed)
        
        logger.info(f"Music | Repeat | Tarafından: {ctx.author}")

    @repeat_command.error
    async def repeat_command_error(self, ctx, exc):
        if isinstance(exc, InvalidRepeatMode):
            repeatEmbed_2=discord.Embed(title="Hatalı Tekrarlama Modu",description="Tekrarlama Modları\n1-Yok\n2-1 (Mevcut Parça)\n3-Tümü",colour=0xffd500)
            
            await ctx.send(embed=repeatEmbed_2)
        elif isinstance(exc, QueueIsEmpty):
            repeatEmbed_3=discord.Embed(title="Liste boş.",colour=0xffd500)
            
            await ctx.send(embed=repeatEmbed_3)

    @commands.command(name="Liste", brief = "Listenin güncel durumunu görüntüler.",aliases=["liste","Queue","queue"])
    async def queue_command(self, ctx):
        player = self.get_player(ctx)
        
        if player.queue.is_empty:
            raise QueueIsEmpty
        queueEmbed = discord.Embed(title="Güncel Liste",colour=0xffd500)
        queueEmbed.add_field(name="Mevcut Parça", value=player.queue.current_track.title, inline=False)
        
        if upcoming := player.queue.upcoming:
            queueEmbed.add_field(name="Sıradaki Parçalar",value=("\n".join(f"**{i+2}.** {t.title}"for i, t in enumerate(upcoming[:19]))),inline=False)
        queueEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=queueEmbed)
        
        logger.info(f"Music | Queue | Tarafından: {ctx.author}")

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            queueEmbed_2=discord.Embed(title="Liste şu anda boş.",colour=0xffd500)
            
            await ctx.send(embed=queueEmbed_2)

    @commands.has_permissions(administrator=True)
    @commands.command(name="Düzey", brief = "Ses düzeyini ayarlar.",aliases=["düzey","Volume","volume"])
    async def volume_command(self,ctx,value:int):
        player = self.get_player(ctx)
        
        if player.queue.is_empty:
            raise QueueIsEmpty
        
        await player.set_volume(value)
        volumeEmbed=discord.Embed(title=f"Ses düzeyi {value} olarak ayarlandı.",description="Varsayılan ses düzeyi **100**'dür.",colour=0xffd500)
        volumeEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=volumeEmbed)
        
        logger.info(f"Music | Volume | Tarafından: {ctx.author}")

    @volume_command.error
    async def volume_command_error(self,ctx,exc):
        if isinstance(exc, QueueIsEmpty):
            volumeEmbed_2=discord.Embed(title="Liste şu anda boş.",colour=0xffd500)
            
            await ctx.send(embed=volumeEmbed_2)
        else :    
            volumeEmbed_3=discord.Embed(title="Lütfen 0 - 1000 aralığında bir tamsayı giriniz.",colour=0xffd500)
            
            await ctx.send(embed=volumeEmbed_3)

def setup(bot):
    bot.add_cog(Music(bot))