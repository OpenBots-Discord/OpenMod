# -*- coding: utf-8 -*-

from typing import Any, List, NoReturn
from aiofile import async_open
from asyncinit import asyncinit

from discord import Embed, Message
from discord.ext import commands
from discord.ext.commands import Bot

from os.path import abspath, dirname

from termcolor import cprint
import datetime
import json


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)


class Config:
    cfg = None

    def __new__(self) -> Any:
        with open(dirname(abspath(__file__)) + '/../data/config.json', 'r') as f:
            return json.load(f)


CONFIG = Config()


class Commands:
    cfg = None

    def __new__(self) -> Any:
        with open(dirname(abspath(__file__)) + '/../data/commands.json', 'r') as f:
            return json.load(f)


@asyncinit
class Settings:
    guild_id = 0
    settings = None

    async def __init__(self, _guild_id: int) -> None:
        self.guild_id = _guild_id

        async with async_open(dirname(abspath(__file__)) + '/../data/settings.json', 'r') as f:
            self.settings = json.loads(await f.read())

    async def __save(self) -> NoReturn:
        async with async_open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
            await f.write(json.dumps(self.settings, indent=4))

    async def __create_guild_object(self) -> NoReturn:
        self.settings[str(str(self.guild_id))] = {}
        await self.__save()

    async def create_empty_field(self, field: str) -> NoReturn:
        try:
            self.settings[str(self.guild_id)][field] = None
            await self.__save()
        except:
            await self.__create_guild_object()
            self.settings[str(self.guild_id)][field] = None
            await self.__save()

    async def get_field(self, field: str, default_value: Any = None) -> Any:
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

    async def set_field(self, field: str, value) -> NoReturn:
        try:
            self.settings[str(self.guild_id)][field] = value
            await self.__save()
        except:
            await self.create_empty_field(field)
            self.settings[str(self.guild_id)][field] = value
            await self.__save()


class Utils(commands.Cog, name='Utils'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Utils'

    def done_embed(msg: Message) -> Embed:
        return Embed(color=0x00FF47, description=msg)

    def warn_embed(msg: Message) -> Embed:
        return Embed(color=0xFFD600, description=msg)

    def error_embed(msg: Message) -> Embed:
        return Embed(color=0xED4242, description=msg)

    async def get_prefix(bot: Bot, msg: Message) -> List[str]:
        s = await Settings(msg.guild.id)
        prefix = await s.get_field('prefix', CONFIG['default_prefix'])
        return [bot.user.mention + ' ', 'f<@!bot.user.id> ', prefix, prefix + ' ']


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Utils(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[CONFIG['default_locale']]['bot_log']['info'].format(time, locales[CONFIG['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Utils').name)), 'green')
