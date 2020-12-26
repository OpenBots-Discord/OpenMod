# -*- coding: utf-8 -*-

from typing import NoReturn
from os.path import abspath, dirname

import discord
from discord import Guild, Message
from discord.ext import commands
from discord.ext.commands import Bot, Context

import asyncio
import datetime
import json
from termcolor import cprint

from cogs.utils import Settings, Utils


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)


class Listeners(commands.Cog, name='Listeners'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Listeners'

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild) -> NoReturn:
        """This function sends a welcome message from the bot to the first channel
                in which the bot has the permission to send messages.

        """
        embed = discord.Embed(color=0x00FF47, title=locales[config['default_locale']]['etc']['info']['name'],
                              description=locales[config['default_locale']]['general']['about'])
        embed.set_thumbnail(
            url=self.bot.user.avatar_url_as())

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

    @commands.Cog.listener()
    async def on_command(self, ctx: Context) -> NoReturn:
        """Logging commands to the console.

        """
        now = datetime.datetime.now()
        time = now.strftime('%H:%M:%S')
        cprint(locales[config['default_locale']]['bot_log']
               ['log_cmd'].format(time, ctx.message.author, ctx.command.name, ctx.message.guild), 'green', attrs=['dark'])

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> NoReturn:
        """Getting the bot prefix when it is mentioned.

        """
        try:
            s = await Settings(message.guild.id)
            lang = await s.get_field('locale', config['default_locale'])
            prefix = await s.get_field('prefix', config['default_prefix'])
        except AttributeError:
            pass
        else:
            if message.content == f'<@!{self.bot.user.id}>' or message.content == f'<@{self.bot.user.id}>' or message.content == f'@{self.bot.user}':
                await message.channel.send(locales[lang]['etc']['on_mention'].format(message.author.id, prefix))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception) -> NoReturn:
        """If an unexpected error occurs, it displays an... error message?

        Attributes:
        -----------
        - `error` - error information

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', config['default_locale'])

        if isinstance(error, commands.CommandNotFound):
            return
        else:
            await ctx.message.add_reaction(config['no_emoji'])

            if isinstance(error, commands.MissingRequiredArgument):
                prefix = await s.get_field('prefix', config['default_prefix'])

                if ctx.command.cog.name != 'Jishaku':
                    embed = Utils.error_embed(locales[lang]['etc']['usage']
                                              .format(cmds[lang][ctx.command.cog.name]['commands'][ctx.command.name]['usage']
                                                      .format(prefix)))
                else:
                    pass

            elif isinstance(error, commands.MissingPermissions):
                embed = Utils.error_embed(
                    locales[lang]['error']['missing_perms'])

            elif isinstance(error, commands.BotMissingPermissions):
                embed = Utils.error_embed(locales[lang]['error']['missing_bot_perms'].format(' '.join(
                    ['+ ' + locales[lang]['etc']['permissions'][f'{perm}'] for perm in error.missing_perms])))

            elif isinstance(error, commands.CommandOnCooldown):
                embed = Utils.error_embed(
                    locales[lang]['error']['cooldown']
                    .format(error.retry_after))

            else:
                now = datetime.datetime.now()
                time = now.strftime('%H:%M:%S')
                cprint(locales[config['default_locale']]['bot_log']
                       ['warn'].format(time, str(error)), 'red')

                embed = discord.Embed(color=0xdd0000)
                embed.title = locales[lang]['error']['on_error_title']
                embed.description = locales[lang]['error']['on_error_text'].format(
                    str(error))

            msg = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await msg.delete()


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Listeners(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Listeners').name)), 'green')
