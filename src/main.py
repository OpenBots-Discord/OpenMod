# -*- coding: utf-8 -*-



from typing import NoReturn
from termcolor import cprint

import os

from os.path import dirname
from os.path import abspath

from cogs.utils import Config, Strings, Utils, Logger
from discord.ext import tasks, commands
from discord.ext.commands import AutoShardedBot
import json
from dotenv import load_dotenv
import asyncio
import sqlite3
#from scripts import db
from discord.ext import tasks, commands
from discord_slash import SlashCommand
from slashify import Slashify
import discord



CONFIG = Config()
STRINGS = Strings(CONFIG['default_locale'])

filepath = dirname(abspath(__file__))


cprint(STRINGS['etc']['info']['art'], 'white')

cprint('Default locale is {0}'.format(
    CONFIG['default_locale']), 'green')


bot = AutoShardedBot(command_prefix=Utils.get_prefix, help_command=None)


@bot.event
async def on_ready() -> NoReturn:
    for filename in os.listdir(filepath + '/cogs/'):
        if filename.endswith('.py'):
            bot.load_extension('cogs.{0}'.format(filename[:-3]))

    await bot.change_presence(activity=discord.Game(name='HELIA CANARY BRANCH - INTERNAL TEST ONLY'))
    bot.load_extension('jishaku')
    Logger.done(STRINGS['bot_log']['logged_as'].format(bot.user))


bot.run(CONFIG['token'])
