# -*- coding: utf-8 -*-

from typing import NoReturn
from os.path import abspath, dirname

from discord.ext import commands
from discord.ext.commands import Bot

import asyncio
import datetime
import json
import requests
from termcolor import cprint

from cogs.utils import Config


CONFIG = Config()

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)


class Workers(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Workers'
        bot.loop.create_task(Workers.sdc_updater(self, bot))

    async def sdc_updater(self, bot: Bot) -> NoReturn:
        """Updates bot information on bots.servers-discord.com

        """
        while True:
            requests.post(f'https://api.server-discord.com/v2/bots/{bot.user.id}/stats',
                          headers={
                              "Authorization": CONFIG['sdc_token']},
                          data={"servers": len(bot.guilds), "shards": 0})
            await asyncio.sleep(3600)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Workers(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[CONFIG['default_locale']]['bot_log']['info'].format(time, locales[CONFIG['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Workers').name)), 'green')
