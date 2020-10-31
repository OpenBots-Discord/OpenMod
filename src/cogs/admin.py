import discord
from discord import embeds
from discord.ext import commands

import datetime
import json
from termcolor import cprint
import re

from os.path import dirname
from os.path import abspath

from cogs.utils import Utils

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)


class Admin(commands.Cog, name='Admin'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Admin'

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        try:
            self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(config['no_emoji'])
            await ctx.send(embed=Utils.error_embed('`{}`: {}'.format(type(e).__name__, e)))
        else:
            await ctx.message.add_reaction(config['yes_emoji'])

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        try:
            self.bot.unload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(config['no_emoji'])
            await ctx.send(embed=Utils.error_embed('`{}`: {}'.format(type(e).__name__, e)))
        else:

            await ctx.message.add_reaction(config['yes_emoji'])

    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx, *, module: str):
        try:
            self.bot.reload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(config['no_emoji'])
            await ctx.send(embed=Utils.error_embed('`{}`: {}'.format(type(e).__name__, e)))
        else:
            await ctx.message.add_reaction(config['yes_emoji'])

    @commands.command(name='eval', aliases=['e'])
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        await ctx.send(f'```\n{eval(re.sub("[`]", "", code))}\n```')


def setup(bot):
    bot.add_cog(Admin(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Admin').name)), 'green')
