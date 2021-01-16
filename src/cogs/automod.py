# -*- coding: utf-8 -*-

from typing import NoReturn

import discord
from discord import Member, Role
from discord.ext import commands
from discord.ext.commands import Bot, Context

import asyncio

from cogs.utils import Settings, Config, Strings, Utils, Logger


CONFIG = Config()


class Automod(commands.Cog, name='Automod'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Automod'

    @commands.group()
    async def autorole(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('сет вообщето дебил!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    @autorole.command(name='set')
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(administrator=True)
    async def _set(self, ctx: Context, role: Role):
        s = await Settings(ctx.guild.id)

        await s.set_field('autorole', role.id)
        await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @autorole.command(name='set')
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx: Context):
        s = await Settings(ctx.guild.id)

        await s.set_field('autorole', None)
        await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        s = await Settings(member.guild.id)
        role_id = await s.get_field('autorole')

        if role_id != None:
            role = discord.utils.get(member.guild.roles, id=role_id)

            if role == None:
                await s.set_field('autorole', None)
            else:
                await member.add_roles(role)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Automod(bot))
    Logger.cog_loaded(bot.get_cog('Automod').name)
