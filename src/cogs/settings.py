# -*- coding: utf-8 -*-

from typing import NoReturn
from os.path import abspath, dirname

from discord.ext import commands
from discord.ext.commands import Bot, Context

import datetime
import json
from termcolor import cprint

from cogs.utils import Settings


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


class Settings(commands.Cog, name='Settings'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Settings'

    @commands.command(aliases=['pref', 'setprefix'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx: Context, prefix: str) -> NoReturn:
        """Sets a custom prefix.

        Attributes:
        -----------
        - `prefix` - new prefix

        """
        s = await Settings(ctx.guild.id)
        await s.set_field('prefix', prefix)

        await ctx.message.add_reaction(config['yes_emoji'])

    @commands.command(aliases=['lang', 'setlang', 'setlanguage'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def locale(self, ctx: Context, locale: str) -> NoReturn:
        """Sets bot language. If not found, it throws an error.

        Attributes:
        -----------
        - `locale` - new locale

        """
        s = await Settings(ctx.guild.id)

        for _locale in [*locales]:
            if _locale == locale:
                await s.set_field('locale', locale)

                await ctx.message.add_reaction(config['yes_emoji'])
                return

        await ctx.send("нет такой локали какбы")


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Settings(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Settings').name)), 'green')
