# -*- coding: utf-8 -*-

"""
                   OpenMod
-----------------------------------------------
Open-Source bot for moderating Discord servers.

* Copyright: (c) 2020 arslee07
* E-mail: me@arslee.tk
* License: MIT, see LICENSE for more details.
-----------------------------------------------

"""

from typing import NoReturn
from termcolor import cprint

import datetime
import json
import os

from os.path import dirname
from os.path import abspath

from cogs.utils import Utils
from discord.ext.commands import AutoShardedBot
import discord


with open(dirname(abspath(__file__)) + '/data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/data/config.json') as f:
    config = json.load(f)

filepath = dirname(abspath(__file__))


cprint(locales[config['default_locale']]['etc']['info']['art'], 'white')

cprint('Default locale is {0}'.format(
    config['default_locale']), 'green')


bot = AutoShardedBot(command_prefix=Utils.get_prefix, help_command=None)


@bot.event
async def on_ready() -> NoReturn:
    for filename in os.listdir(filepath + '/cogs/'):
        if filename.endswith('.py'):
            bot.load_extension('cogs.{0}'.format(filename[:-3]))

    await bot.change_presence(activity=discord.Game(name='@mention me to get prefix'))

    bot.load_extension('jishaku')

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]
                                                                       ['bot_log']['logged_as'].format(bot.user)), 'green')


bot.run(config['token'])
