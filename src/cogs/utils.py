import datetime
import json

import discord
from discord.ext import commands

from os.path import dirname
from os.path import abspath
from discord.ext.commands.bot import when_mentioned_or

from termcolor import cprint


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)


class Utils(commands.Cog, name='Utils'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Utils'

    def done_embed(msg):
        return discord.Embed(color=0x00FF47, description=msg)

    def warn_embed(msg):
        return discord.Embed(color=0xFFD600, description=msg)

    def error_embed(msg):
        return discord.Embed(color=0xED4242, description=msg)

    def get_prefix(bot, msg):
        with open(dirname(abspath(__file__)) + '/../data/settings.json', 'r') as f:
            settings = json.load(f)

        try:
            _ = settings[str(msg.guild.id)]

        except KeyError:
            settings[str(msg.guild.id)] = {}

            with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
                json.dump(settings, f, indent=4)

        try:
            if bot == None:
                return settings[str(msg.guild.id)]['prefix']
            else:
                return [bot.user.mention + ' ', '<@!%s> ' % bot.user.id, settings[str(msg.guild.id)]['prefix']]
        except KeyError:
            settings[str(msg.guild.id)
                     ]['prefix'] = config['default_prefix']

            with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
                json.dump(settings, f, indent=4)

            if bot == None:
                return settings[str(msg.guild.id)]['prefix']
            else:
                return [bot.user.mention + ' ', '<@!%s> ' % bot.user.id, settings[str(msg.guild.id)]['prefix']]

    def get_lang(bot, msg):
        with open(dirname(abspath(__file__)) + '/../data/settings.json', 'r') as f:
            settings = json.load(f)

        try:
            _ = settings[str(msg.guild.id)]

        except KeyError:
            settings[str(msg.guild.id)] = {}

            with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
                json.dump(settings, f, indent=4)

        try:
            return settings[str(msg.guild.id)]['locale']
        except KeyError:
            settings[str(msg.guild.id)
                     ]['locale'] = config['default_locale']
            with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
                json.dump(settings, f, indent=4)

            return settings[str(msg.guild.id)]['locale']

    def get_mute_role(bot, msg):
        with open(dirname(abspath(__file__)) + '/../data/settings.json', 'r') as f:
            settings = json.load(f)

        try:
            _ = settings[str(msg.guild.id)]

        except KeyError:
            settings[str(msg.guild.id)] = {}

            with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
                json.dump(settings, f, indent=4)

        try:
            return settings[str(msg.guild.id)]['mute_role']
        except KeyError:
            settings[str(msg.guild.id)
                     ]['mute_role'] = None
            with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            return settings[str(msg.guild.id)]['mute_role']


def setup(bot):
    bot.add_cog(Utils(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Utils').name)), 'green')
