# -*- coding: utf-8 -*-

from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from cogs.utils import Logger, Settings, Config, Commands, Strings, Utils


CONFIG = Config()


class General(commands.Cog, name='General'):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = 'General'

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx: Context, command: str = None) -> NoReturn:
        """Shows help for a specific command, or displays a complete list of commands.

        Attributes:
        -----------
        - `command` - the command to display help for. 
            If `command` is empty, displays a complete list of commands.     
            If the command does not exist, writes that the command was not found.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        prefix = await s.get_field('prefix', CONFIG['default_prefix'])
        STRINGS = Strings(lang)
        COMMANDS = Commands(lang)

        if command == None:
            embed = discord.Embed(
                title=STRINGS['general']['commands_list'], description=STRINGS['general']['help_list_description'].format(prefix), color=0xef940b)
            embed.set_thumbnail(
                url=self.bot.user.avatar_url_as())

            for i in COMMANDS:
                title = COMMANDS[i]['title']

                description = ', '.join(
                    [f'`{j}`' for j in COMMANDS[i]['commands']])

                if self.bot.get_cog(i) != None:
                    embed.add_field(
                        name=title, value=description, inline=False)

            await ctx.send(embed=embed)

        elif command != '':
            for i in COMMANDS:
                for j in COMMANDS[i]['commands']:
                    if command == j:
                        embed = discord.Embed(
                            title=STRINGS['general']['help'].format(f'`{prefix}{j}`'), color=0xef940b)

                        embed.set_thumbnail(
                            url=self.bot.user.avatar_url_as())

                        embed.add_field(
                            name=STRINGS['general']['description'], value=COMMANDS[i]['commands'][j]['description'], inline=False)

                        embed.add_field(
                            name=STRINGS['general']['usage'], value=COMMANDS[i]['commands'][j]['usage'].format(prefix), inline=False)

                        if len(COMMANDS[i]['commands'][j]['aliases']) > 0:
                            aliases = ', '.join(
                                [f'`{alias}`' for alias in COMMANDS[i]['commands'][j]['aliases']])
                            embed.add_field(
                                name=STRINGS['general']['aliases'], value=aliases, inline=False)

                        await ctx.send(embed=embed)
                        return
            else:
                await ctx.send(embed=Utils.error_embed(STRINGS['error']['command_not_found']))

    @commands.guild_only()
    @commands.command()
    async def about(self, ctx: Context) -> NoReturn:
        """Shows a short description of the bot.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)

        await ctx.send(embed=discord.Embed(description=STRINGS['general']['about'], color=0xef940b)
                       .set_thumbnail(url=self.bot.user.avatar_url_as()))


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(General(bot))
    Logger.cog_loaded(bot.get_cog('General').name)
