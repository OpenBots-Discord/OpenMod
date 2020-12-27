# -*- coding: utf-8 -*-

from typing import NoReturn
from os.path import abspath, dirname

from discord.ext import commands
from discord.ext.commands import Bot, Context

import datetime
import json
from termcolor import cprint

from cogs.utils import Settings, Config, Utils


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

CONFIG = Config()


class Other(commands.Cog, name='Other'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Other'

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx: Context) -> NoReturn:
        """Shows host latency.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        latency = int(round(self.bot.latency * 100, 1))

        embed = Utils.done_embed(
            locales[lang]['other']['pong'].format(str(latency)))
        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Other(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[CONFIG['default_locale']]['bot_log']['info'].format(time, locales[CONFIG['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Other').name)), 'green')
