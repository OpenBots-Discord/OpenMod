import discord
from discord import embeds
from discord.ext import commands

import datetime
import json
from termcolor import cprint

from os.path import dirname
from os.path import abspath

from cogs.utils import Utils

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)


class Settings(commands.Cog, name='Settings'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Settings'

    @commands.command(aliases=['pref', 'setprefix'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx, prefix):
        with open(dirname(abspath(__file__)) + '/../data/settings.json', 'r') as f:
            settings = json.load(f)

        settings[str(ctx.guild.id)]['prefix'] = prefix

        with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

        await ctx.message.add_reaction(config['yes_emoji'])

    @commands.command(aliases=['lang', 'setlang', 'setlanguage'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def locale(self, ctx, locale: str):
        with open(dirname(abspath(__file__)) + '/../data/settings.json', 'r') as f:
            settings = json.load(f)

        with open(dirname(abspath(__file__)) + '/../data/locales.json', 'r') as f:
            locales = json.load(f)

        for _locale in [*locales]:
            if _locale == locale:
                settings[str(ctx.guild.id)]['locale'] = locale

                with open(dirname(abspath(__file__)) + '/../data/settings.json', 'w') as f:
                    json.dump(settings, f, indent=4)

                await ctx.message.add_reaction(config['yes_emoji'])
                return
        else:
            await ctx.send("нет такой локали какбы")


def setup(bot):
    bot.add_cog(Settings(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Settings').name)), 'green')
