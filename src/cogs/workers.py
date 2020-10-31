import asyncio
import glob
import json
import datetime

from os.path import dirname
from os.path import abspath

import discord
from discord.ext import commands

from termcolor import cprint

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)

result = glob.glob('./**/*.py', recursive=True)
lines = 0
for i in result:
    with open(i) as f:
        lines += sum(1 for _ in f)


class Workers(commands.Cog, name='Workers'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Workers'
        bot.loop.create_task(Workers.status_updater(self, bot))

    async def status_updater(self, bot):
        while True:
            try:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name=locales[config['default_locale']]['workers']['at_servers'].format(str(len(self.bot.guilds)))))
                await asyncio.sleep(10)
            except:
                pass

            try:
                members = 0
                for guilds in self.bot.guilds:
                    members += len(guilds.members)
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name=locales[config['default_locale']]['workers']['at_users'].format(members)))
                await asyncio.sleep(10)
            except:
                pass

            try:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name=locales[config['default_locale']]['workers']['at_commands'].format(len(self.bot.commands))))
                await asyncio.sleep(10)
            except:
                pass

            try:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name=locales[config['default_locale']]['workers']['at_lines'].format(lines)))
                await asyncio.sleep(10)
            except:
                pass

            try:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name="irwbot was here ;)"))
                await asyncio.sleep(10)
            except:
                pass


def setup(bot):
    bot.add_cog(Workers(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Workers').name)), 'green')
