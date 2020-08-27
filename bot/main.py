# TODO: extend logging


import asyncio
import discord
import datetime
import json
from os.path import dirname
from os.path import abspath
from discord.ext import commands
from discord.ext.commands import Bot
import config
import logger as log

filepath = dirname(abspath(__file__))

""" Setting language """
if config.LANGUAGE == "ru_RU":
    from translations.ru_RU import *
elif config.LANGUAGE == "en_EN":
    from translations.en_EN import *
else:
    log.warn(
        "Unable to load translations. Make sure you have entered the correct language.")
    exit()


class Utilities(commands.Cog, name='Utilities'):
    def __init__(self, bot):
        self.bot = bot

    def done_embed(msg):
        return discord.Embed(color=0x00FF47, description="✅⼁" + msg)

    def warn_embed(msg):
        return discord.Embed(color=0xFFD600, description="⚠⼁" + msg)

    def error_embed(msg):
        return discord.Embed(color=0xED4242, description="🚫⼁" + msg)

    def get_prefix(bot, message):
        with open(filepath + '/data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        try:
            return prefixes[str(message.guild.id)]

        except KeyError:
            prefixes[str(message.guild.id)] = config.DEFAULT_PREFIX

            with open(filepath + '/data/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)

            return prefixes[str(message.guild.id)]


bot = Bot(command_prefix=Utilities.get_prefix, help_command=None)


class General(commands.Cog, name='General'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):
        log.cmd('help', ctx.author, ctx.guild)
        prefix = Utilities.get_prefix(ctx, ctx)
        embed = discord.Embed(title='**Список команд**',
                              description='Синтаксис команд: `[об. аргумент] <необ. аргумент>`', color=0xff5757)

        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/738279888674357298/0a8114760177033f90ddfa2ac9b5c93d.png?size=256')

        for i in range(len(help_titles)):
            embed.add_field(
                name=help_titles[i], value=help_texts[i].format(prefix), inline=False)

        await ctx.message.add_reaction(emoji='📭')
        await ctx.message.author.send(embed=embed)


class Moderation(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason="N/A"):
        log.cmd('ban', ctx.author, ctx.guild)
        if member.bot:
            embed = Utilities.error_embed(cannot_ban_bots())
            await ctx.send(embed=embed)
        else:
            await member.ban(reason=reason)

            embed = Utilities.done_embed(successfull_ban())
            await ctx.send(embed=embed)

            embed = Utilities.error_embed(dm_ban(ctx.guild, reason))
            await member.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unban(self, ctx, *, member):
        log.cmd('unban', ctx.author, ctx.guild)
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = Utilities.done_embed(successfull_unban())
                await ctx.send(embed=embed)
                return

        embed = Utilities.error_embed(user_not_found())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def multiban(self, ctx, *members: discord.Member):
        log.cmd('multiban', ctx.author, ctx.guild)

        print(members)
        for i in members:
            await i.ban(reason="N/A")
            embed = Utilities.error_embed(dm_ban(ctx.guild, "N/A"))
            await i.send(embed=embed)

        embed = Utilities.done_embed(successfull_ban())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason="N/A"):
        log.cmd('kick', ctx.author, ctx.guild)
        await member.kick()

        embed = Utilities.done_embed(successfull_kick())
        await ctx.send(embed=embed)

        embed = Utilities.error_embed(dm_kick(ctx.guild, reason))
        await member.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx, arg: int):
        log.cmd('purge', ctx.author, ctx.guild)
        await ctx.channel.purge(limit=arg + 1)
        embed = Utilities.done_embed(successfull_clear(arg))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setname(self, ctx, member: discord.Member, *, name):
        if len(name) > 32:
            embed = Utilities.error_embed(too_long_name())
            await ctx.send(embed=embed)
        else:
            if ctx.message.author.guild_permissions.manage_nicknames or member == ctx.message.author:
                await member.edit(nick=name)
                embed = Utilities.done_embed(successfull_name())
                await ctx.send(embed=embed)
            else:
                embed = Utilities.error_embed(missing_perms())
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def info(self, ctx, member: discord.Member):
        id = str(member.id)
        hash = member.avatar
        joined_at = member.joined_at.strftime('%d.%m.%Y')
        created_at = member.created_at.strftime('%d.%m.%Y')
        color = member.color

        embed = discord.Embed(title=about_user(),
                              description=user_info(
            id, created_at, joined_at, color),
            color=0xff5757)

        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/{0}/{1}.png?size=64'.format(id, hash))

        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx, error):
        log.cmd('info', ctx.author, ctx.guild)
        if isinstance(error, commands.MissingRequiredArgument):
            id = str(ctx.message.author.id)
            hash = ctx.message.author.avatar
            joined_at = ctx.message.author.joined_at.strftime('%d.%m.%Y')
            created_at = ctx.message.author.created_at.strftime('%d.%m.%Y')
            color = ctx.message.author.color

            embed = discord.Embed(title=about_user(),
                                  description=user_info(
                id, created_at, joined_at, color),
                color=0xff5757)

            embed.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/{0}/{1}.png?size=512'.format(id, hash))

            await ctx.send(embed=embed)


class Other(commands.Cog, name='Other'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx, prefix):
        log.cmd('prefix', ctx.author, ctx.guild)
        with open(filepath + '/data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open(filepath + '/data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        embed = Utilities.done_embed(successfull_prefix())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        log.cmd('ping', ctx.author, ctx.guild)
        latency = int(round(bot.latency * 100, 1))
        embed = Utilities.done_embed(pong(str(latency)))
        await ctx.send(embed=embed)


class Workers(commands.Cog, name='Workers'):
    def __init__(self, bot):
        self.bot = bot

    async def status_updater():
        while True:
            try:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=at_servers(str(len(bot.guilds)))))
                await asyncio.sleep(10)
            except:
                pass

            try:
                members = 0
                for guilds in bot.guilds:
                    members += len(guilds.members)
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=at_users(members)))
                await asyncio.sleep(10)
            except:
                pass

            try:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=at_commands(len(bot.commands))))
                await asyncio.sleep(10)
            except:
                pass

            try:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name="irwbot was here ;)"))
                await asyncio.sleep(10)
            except:
                pass


@bot.event
async def on_ready():
    log.info(logged_as(bot.user))
    bot.add_cog(Utilities(bot))
    bot.add_cog(General(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(Other(bot))
    bot.add_cog(Workers(bot))
    bot.loop.create_task(Workers.status_updater())


@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(color=0x00FF47, title='**OpenMod**',
                          description=on_invite_text())
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/738279888674357298/0a8114760177033f90ddfa2ac9b5c93d.png?size=256')

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
            break

    with open(filepath + '/data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = config.DEFAULT_PREFIX

    with open(filepath + '/data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open(filepath + '/data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open(filepath + '/data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@Other.prefix.error
@Moderation.ban.error
@Moderation.multiban.error
@Moderation.kick.error
@Moderation.unban.error
@Moderation.purge.error
async def errors(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = Utilities.error_embed(missing_perms())
        await ctx.send(embed=embed)
    if isinstance(error, commands.BotMissingPermissions):
        embed = Utilities.error_embed(missing_bot_perms())
        await ctx.send(embed=embed)


bot.run(config.TOKEN)
