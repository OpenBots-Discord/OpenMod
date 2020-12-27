# -*- coding: utf-8 -*-

from typing import NoReturn
from os.path import abspath, dirname

from discord.ext import commands
from discord.ext.commands import Bot, Context

import datetime
import json
from termcolor import cprint

from cogs.utils import Config, Strings, Utils


CONFIG = Config()
STRINGS = Strings(CONFIG['default_locale'])


class Admin(commands.Cog, name='Admin'):
    """A module required to administer the bot. Only works for its owners."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Admin'

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(CONFIG['no_emoji'])
            embed = Utils.error_embed('`{}`: {}'.format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: Context, *, module: str) -> NoReturn:
        """Unloads a module (cog). If the module is not found, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.unload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(CONFIG['no_emoji'])
            embed = Utils.error_embed('`{}`: {}'.format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:

            await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.reload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(CONFIG['no_emoji'])
            embed = Utils.error_embed('`{}`: {}'.format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction(CONFIG['yes_emoji'])


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Admin(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(STRINGS[CONFIG['default_locale']]['bot_log']['info'].format(time, STRINGS[CONFIG['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Admin').name)), 'green')
