from typing import NoReturn
from discord.ext import commands

from os.path import abspath
from os.path import dirname

import asyncio
import datetime
import json
import requests
from termcolor import cprint


with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

filepath = dirname(abspath(__file__))


class Workers(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = 'Workers'
        bot.loop.create_task(Workers.sdc_updater(self, bot))

    async def sdc_updater(self, bot) -> NoReturn:
        """Updates bot information on bots.servers-discord.com

        """
        while True:
            requests.post(f'https://api.server-discord.com/v2/bots/{bot.user.id}/stats',
                          headers={
                              "Authorization": config['sdc_token']},
                          data={"servers": len(bot.guilds), "shards": 0})
            await asyncio.sleep(60)


def setup(bot) -> NoReturn:
    bot.add_cog(Workers(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Workers').name)), 'green')
