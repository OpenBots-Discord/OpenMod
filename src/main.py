import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.bot import when_mentioned_or
from cogs.utils import Utils

from os.path import abspath
from os.path import dirname

import os
import json
import datetime
from termcolor import cprint


with open(dirname(abspath(__file__)) + '/data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/data/config.json') as f:
    config = json.load(f)

filepath = dirname(abspath(__file__))


cprint(locales[config['default_locale']]['etc']['info']['art'], 'white')

cprint('Default locale is {0}'.format(
    config['default_locale']), 'green')


bot = Bot(command_prefix=Utils.get_prefix, help_command=None)


@bot.event
async def on_ready():
    for filename in os.listdir(filepath + '/ogs/'):
        if filename.endswith('.py'):
            bot.load_extension('cogs.{0}'.format(filename[:-3]))

    await bot.change_presence(activity=discord.Game(name='@mention me to get prefix'))

    bot.load_extension('jishaku')

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]
                                                                       ['bot_log']['logged_as'].format(bot.user)), 'green')


bot.run(config['token'])
