from termcolor import cprint
from discord.ext import commands
import discord
from os.path import abspath
from os.path import dirname
import datetime
import json

from cogs.utils import Utils


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)


class Other(commands.Cog, name='Other'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Other'

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        latency = int(round(self.bot.latency * 100, 1))
        embed = Utils.done_embed(locales[Utils.get_lang(
            None, ctx.message)]['other']['pong'].format(str(latency)))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Other(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Other').name)), 'green')
