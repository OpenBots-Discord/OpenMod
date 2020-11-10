import discord
from discord.ext import commands

import json
import datetime

from termcolor import cprint

from cogs.utils import Utils

from os.path import dirname
from os.path import abspath

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)


class General(commands.Cog, name='General'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'General'

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, command=None):
        lang = Utils.get_lang(None, ctx.message)
        prefix = Utils.get_prefix(None, ctx.message)

        if command == None:
            embed = discord.Embed(
                title=locales[lang]['general']['commands_list'], description=locales[lang]['general']['help_list_description'].format(prefix), color=0xef940b)
            embed.set_thumbnail(
                url=self.bot.user.avatar_url_as())

            for i in cmds[lang]:
                title = cmds[lang][i]['title']

                description = ', '.join(
                    [f'`{j}`' for j in cmds[lang][i]['commands']])

                if self.bot.get_cog(i) != None:
                    embed.add_field(
                        name=title, value=description, inline=False)

            await ctx.send(embed=embed)

        elif command != '':
            for i in cmds[lang]:
                for j in cmds[lang][i]['commands']:
                    if command == j:
                        embed = discord.Embed(
                            title=locales[lang]['general']['help'].format(f'`{prefix}{j}`'), color=0xef940b)

                        embed.set_thumbnail(
                            url=self.bot.user.avatar_url_as())

                        embed.add_field(
                            name=locales[lang]['general']['description'], value=cmds[lang][i]['commands'][j]['description'], inline=False)

                        embed.add_field(
                            name=locales[lang]['general']['usage'], value=cmds[lang][i]['commands'][j]['usage'].format(prefix), inline=False)

                        if len(cmds[lang][i]['commands'][j]['aliases']) > 0:
                            aliases = ', '.join(
                                [f'`{alias}`' for alias in cmds[lang][i]['commands'][j]['aliases']])
                            embed.add_field(
                                name=locales[lang]['general']['aliases'], value=aliases, inline=False)

                        await ctx.send(embed=embed)
                        return
            else:
                await ctx.send(embed=Utils.error_embed(locales[lang]['error']['command_not_found']))

    @commands.guild_only()
    @commands.command()
    async def about(self, ctx):
        await ctx.send(embed=discord.Embed(description=locales[Utils.get_lang(
            None, ctx.message)]['general']['about'], color=0xef940b).set_thumbnail(url=self.bot.user.avatar_url_as()))


def setup(bot):
    bot.add_cog(General(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('General').name)), 'green')
