from aiofile import async_open
from asyncinit import asyncinit
import datetime
import json

import discord
from discord.ext import commands

from os.path import dirname
from os.path import abspath

from termcolor import cprint


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


@asyncinit
class Settings:
    guild_id = 0
    settings = None

    async def __init__(self, _guild_id):
        self.guild_id = _guild_id

        async with async_open(dirname(abspath(__file__)) + '/../data/settings.json', 'r') as f:
            self.settings = json.loads(await f.read())

    async def __save(self):
        async with async_open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
            await f.write(json.dumps(self.settings, indent=4))

    async def __create_guild_object(self):
        self.settings[str(str(self.guild_id))] = {}
        await self.__save()

    async def create_empty_field(self, field: str):
        try:
            self.settings[str(self.guild_id)][field] = None
            await self.__save()
        except:
            await self.__create_guild_object()
            self.settings[str(self.guild_id)][field] = None
            await self.__save()

    async def get_field(self, field: str, default_value=None):
        try:
            val = self.settings[str(self.guild_id)][field]
        except:
            await self.create_empty_field(field)
            val = self.settings[str(self.guild_id)][field]

        if val == None and default_value != None:
            await self.set_field(field, default_value)
            return default_value
        else:
            return self.settings[str(self.guild_id)][field]

    async def set_field(self, field: str, value):
        try:
            self.settings[str(self.guild_id)][field] = value
            await self.__save()
        except:
            await self.create_empty_field(field)
            self.settings[str(self.guild_id)][field] = value
            await self.__save()


class Utils(commands.Cog, name='Utils'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Utils'

    def done_embed(msg):
        return discord.Embed(color=0x00FF47, description=msg)

    def warn_embed(msg):
        return discord.Embed(color=0xFFD600, description=msg)

    def error_embed(msg):
        return discord.Embed(color=0xED4242, description=msg)

    async def get_prefix(bot, msg):
        s = await Settings(msg.guild.id)
        prefix = await s.get_field('prefix', config['default_prefix'])
        return [bot.user.mention + ' ', '<@!%s> ' % bot.user.id, prefix]


def setup(bot):
    bot.add_cog(Utils(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Utils').name)), 'green')
