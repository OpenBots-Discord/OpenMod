import discord
from discord.ext import commands

import asyncio
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


filepath = dirname(abspath(__file__))


class Listeners(commands.Cog, name='Listeners'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Listeners'

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(color=0x00FF47, title=locales[config['default_locale']]['etc']['info']['name'],
                              description=locales[config['default_locale']]['general']['about'])
        embed.set_thumbnail(
            url=self.bot.user.avatar_url_as())

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

        with open(filepath + '/data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = config['defaul_prefix']

        with open(filepath + '/data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        now = datetime.datetime.now()
        time = now.strftime('%H:%M:%S')
        cprint(locales[config['default_locale']]['bot_log']
               ['log_cmd'].format(time, ctx.message.author, ctx.command.name, ctx.message.guild), 'green', attrs=['dark'])

    @commands.Cog.listener()
    async def on_message(self, message):
        lang = Utils.get_lang(None, message)

        if message.content == f'<@!{self.bot.user.id}>' or message.content == f'<@{self.bot.user.id}>' or message.content == f'@{self.bot.user}':
            await message.channel.send(locales[lang]['etc']['on_mention'].format(message.author.id,
                                                                                 Utils.get_prefix(None, message)))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        lang = Utils.get_lang(None, ctx.message)

        if isinstance(error, commands.CommandNotFound):
            return
        else:
            await ctx.message.add_reaction(config['no_emoji'])

        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.cog.name != 'Jishaku':
                msg = await ctx.send(embed=Utils.error_embed(locales[lang]['etc']['usage']
                                                             .format(cmds[lang][ctx.command.cog.name]
                                                                     ['commands'][ctx.command.name]['usage'].format(Utils.get_prefix(None, ctx.message)))))
                await asyncio.sleep(15)
                await msg.delete()
            else:
                pass

        elif isinstance(error, commands.MissingPermissions):
            embed = Utils.error_embed(
                locales[lang]['error']['missing_perms'])
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await msg.delete()

        elif isinstance(error, commands.BotMissingPermissions):
            embed = Utils.error_embed(
                locales[lang]['error']['missing_bot_perms'].format(' '.join(['+ ' + locales[lang]['etc']['permissions'][f'{perm}'] for perm in error.missing_perms])))
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await msg.delete()

        elif isinstance(error, commands.CommandOnCooldown):
            embed = Utils.error_embed(
                locales[lang]['error']['cooldown'].format(
                    error.retry_after))
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await msg.delete()

        else:
            now = datetime.datetime.now()
            time = now.strftime('%H:%M:%S')
            cprint(locales[config['default_locale']]['bot_log']
                   ['warn'].format(time, str(error)), 'red')
            embed = discord.Embed(title=locales[lang]['error']['on_error_title'],
                                  description=locales[lang]['error']['on_error_text'].format(str(error)), color=0xdd0000)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await msg.delete()


def setup(bot):
    bot.add_cog(Listeners(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Listeners').name)), 'green')
