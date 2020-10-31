import re
from typing import Awaitable
from discord.channel import TextChannel
from termcolor import cprint

import datetime
import json

from os.path import abspath
from os.path import dirname

from cogs.utils import Utils
from discord.ext import commands
import discord

import asyncio

import discord
from discord.ext import commands


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/commands.json') as f:
    cmds = json.load(f)


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Utilities'

    @commands.command()
    @commands.guild_only()
    async def user(self, ctx, member: discord.Member = None):
        lang = Utils.get_lang(None, ctx.message)

        if member == None:
            id = str(ctx.message.author.id)
            name = ctx.message.author.name
            tag = ctx.message.author.discriminator
            joined_at = ctx.message.author.joined_at.strftime('%d.%m.%Y %H:%M')
            created_at = ctx.message.author.created_at.strftime(
                '%d.%m.%Y %H:%M')
            color = ctx.message.author.color
            avatar = ctx.message.author.avatar_url_as()
        else:
            id = str(member.id)
            name = member.name
            tag = member.discriminator
            joined_at = member.joined_at.strftime('%d.%m.%Y %H:%M')
            created_at = member.created_at.strftime('%d.%m.%Y %H:%M')
            color = member.color
            avatar = member.avatar_url_as()

        embed = discord.Embed(description=locales[lang]['utilities']['user_info'].format(
            id, created_at, joined_at, color), color=color)
        embed.set_author(
            name=locales[lang]['utilities']['user_info_title'].format(name, tag))
        embed.set_thumbnail(url=avatar)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def emoji(self, ctx, emoji: str):
        lang = Utils.get_lang(None, ctx.message)

        if re.sub('[\<]', '', emoji.split(':')[0]) == '':
            format = 'png'
        else:
            format = 'gif'

        name = emoji.split(':')[1]
        id = re.sub('[\>]', '', emoji.split(':')[2])

        embed = discord.Embed(
            title=locales[lang]['utilities']['emoji_info_title'].format(name), color=0xeda84e)
        embed.set_image(
            url=f'https://cdn.discordapp.com/emojis/{id}.{format}')
        embed.set_footer(text=locales[lang]
                         ['utilities']['emoji_info'].format(id))

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def channel(self, ctx, channel: str):
        lang = Utils.get_lang(None, ctx.message)

        if re.search('[@&\:]', channel) == None:

            channel = discord.utils.get(
                ctx.guild.channels, id=int(re.sub('[<#>]', '', channel)))

            if (channel.type == discord.ChannelType.text):
                type = locales[lang]['etc']['channel_type']['text']
            elif (channel.type == discord.ChannelType.voice):
                type = locales[lang]['etc']['channel_type']['voice']
            elif (channel.type == discord.ChannelType.news):
                type = locales[lang]['etc']['channel_type']['news']
            else:
                pass

            if channel.nsfw:
                is_nsfw = locales[lang]['etc']['other']['yes']
            else:
                is_nsfw = locales[lang]['etc']['other']['no']

            name = channel.name
            id = channel.id
            created_at = channel.created_at.strftime('%d.%m.%Y %H:%M')

            embed = discord.Embed(description=locales[lang]['utilities']['channel_info'].format(
                                  id, type, created_at, is_nsfw), color=0xeda84e)
            embed.set_author(
                name=locales[lang]['utilities']['channel_info_title'].format(name))
            await ctx.send(embed=embed)

        else:
            await ctx.send('чел, это не канал, ты что-то попутал')

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        lang = Utils.get_lang(None, ctx.message)

        if member == None:
            name = ctx.message.author.name
            tag = ctx.message.author.discriminator
            avatar = ctx.message.author.avatar_url_as()
            hash = ctx.message.author.avatar
        else:
            name = member.name
            tag = member.discriminator
            avatar = member.avatar_url_as()
            hash = member.avatar

        embed = discord.Embed(
            color=0xeda84e, title=locales[lang]['utilities']['avatar_info_title'].format(name, tag),
            description=locales[lang]['utilities']['avatar_info'].format(hash, avatar))
        embed.set_image(url=avatar)

        await ctx.send(embed=embed)

    @commands.command(aliases=['server'])
    @commands.guild_only()
    async def guild(self, ctx):
        lang = Utils.get_lang(None, ctx.message)

        guild = ctx.guild
        id = ctx.guild.id
        banner = guild.banner_url_as()
        icon = guild.icon_url_as()
        created_at = guild.created_at.strftime('%d.%m.%Y %H:%M')
        members = len(guild.members)
        owner = guild.owner

        if guild.verification_level == discord.VerificationLevel.none:
            verication_level = locales[lang]['etc']['levels']['none']
        elif guild.verification_level == discord.VerificationLevel.low:
            verication_level = locales[lang]['etc']['levels']['low']
        elif guild.verification_level == discord.VerificationLevel.medium:
            verication_level = locales[lang]['etc']['levels']['medium']
        elif guild.verification_level == discord.VerificationLevel.high:
            verication_level = locales[lang]['etc']['levels']['high']
        elif guild.verification_level == discord.VerificationLevel.extreme:
            verication_level = locales[lang]['etc']['levels']['extreme']
        else:
            verication_level = locales[lang]['etc']['levels']['unknown']

        if guild.explicit_content_filter == discord.ContentFilter.disabled:
            content_filter = locales[lang]['etc']['levels']['none']
        elif guild.explicit_content_filter == discord.ContentFilter.no_role:
            content_filter = locales[lang]['etc']['levels']['medium']
        elif guild.explicit_content_filter == discord.ContentFilter.all_members:
            content_filter = locales[lang]['etc']['levels']['high']
        else:
            content_filter = locales[lang]['etc']['levels']['unknown']

        embed = discord.Embed(
            description=locales[lang]['utilities']['guild_info'].format(
                id, created_at, members, f'<@!{owner.id}>', verication_level, content_filter), color=0xeda84e)
        embed.set_author(name=locales[lang]['utilities']
                         ['guild_info_title'].format(guild))
        embed.set_thumbnail(url=icon)
        embed.set_image(url=banner)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    cprint(locales[config['default_locale']]['bot_log']['info'].format(time, locales[config['default_locale']]['bot_log']
                                                                       ['cog_loaded'].format(bot.get_cog('Utilities').name)), 'green')
