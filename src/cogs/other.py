from typing import NoReturn
from termcolor import cprint

from discord.ext import commands
import discord

from os.path import abspath
from os.path import dirname

import datetime
import json

from cogs.utils import Settings, Utils


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


class Other(commands.Cog, name='Other'):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = 'Other'

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx) -> NoReturn:
        """Shows host latency.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', config['default_locale'])
        latency = int(round(self.bot.latency * 100, 1))

        embed = Utils.done_embed(
            locales[lang]['other']['pong'].format(str(latency)))
        await ctx.send(embed=embed)


def setup(bot) -> NoReturn:
    bot.add_cog(Other(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Other').name)), 'green')
