# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import json
import datetime

from termcolor import cprint

from cogs.utils import Settings, Utils

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
        """Shows help for a specific command, or displays a complete list of commands.

        Attributes:
        -----------
        - `command` - the command to display help for. 
            If `command` is empty, displays a complete list of commands.     
            If the command does not exist, writes that the command was not found.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', config['default_locale'])
        prefix = await s.get_field('prefix', config['default_prefix'])

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
        """Shows a short description of the bot.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', config['default_locale'])
        await ctx.send(embed=discord.Embed(description=locales[lang]['general']['about'], color=0xef940b)
                       .set_thumbnail(url=self.bot.user.avatar_url_as()))


def setup(bot):
    bot.add_cog(General(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('General').name)), 'green')
