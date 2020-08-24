import asyncio
import discord
import datetime
import json
from discord.ext import commands
from discord.ext.commands import Bot
import config
import logger as log


""" Setting language """
if config.LANGUAGE == "ru_RU":
    from translations.ru_RU import *
elif config.LANGUAGE == "en_EN":
    from translations.en_EN import *
else:
    log.warn(
        "Unable to load translations. Make sure you have entered the correct language.")
    exit()


def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    try:
        return prefixes[str(message.guild.id)]

    except KeyError:
        prefixes[str(message.guild.id)] = config.DEFAULT_PREFIX

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        return prefixes[str(message.guild.id)]


def done_embed(msg):
    return discord.Embed(color=0x00FF47, description="✅⼁" + msg)


def warn_embed(msg):
    return discord.Embed(color=0xFFD600, description="⚠⼁" + msg)


def error_embed(msg):
    return discord.Embed(color=0xED4242, description="‼⼁" + msg)


bot = Bot(command_prefix=get_prefix, help_command=None)


async def status_updater():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name=at_servers(str(len(bot.guilds)))))
        await asyncio.sleep(30)


@bot.event
async def on_ready():
    log.info(logged_as(bot.user))
    bot.loop.create_task(status_updater())


@bot.command()
@commands.guild_only()
async def ping(ctx):
    log.cmd('ping', ctx.author, ctx.guild)
    latency = int(round(bot.latency * 100, 1))
    embed = done_embed(pong(str(latency)))
    await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
async def info(ctx, member: discord.Member):
    id = str(member.id)
    tag = member
    hash = member.avatar
    joined_at = member.joined_at.strftime('%d.%m.%Y')
    created_at = member.created_at.strftime('%d.%m.%Y')
    if member.bot:
        is_bot = type_bot
    else:
        is_bot = type_user

    embed = discord.Embed(title=about_user(),
                          description=user_info(
        id, tag, is_bot, created_at, joined_at),
        color=0xff5757)

    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/{0}/{1}.png?size=64'.format(id, hash))

    await ctx.send(embed=embed)


@info.error
async def info_error(ctx, error):
    log.cmd('info', ctx.author, ctx.guild)
    if isinstance(error, commands.MissingRequiredArgument):
        id = str(ctx.message.author.id)
        tag = ctx.message.author
        hash = ctx.message.author.avatar
        joined_at = ctx.message.author.joined_at.strftime('%d.%m.%Y')
        created_at = ctx.message.author.created_at.strftime('%d.%m.%Y')
        if ctx.message.author.bot:
            is_bot = type_bot
        else:
            is_bot = type_user

        embed = discord.Embed(title=about_user(),
                              description=user_info(
                                  id, tag, is_bot, created_at, joined_at),
                              color=0xff5757)

        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/{0}/{1}.png?size=64'.format(id, hash))

        await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
async def help(ctx):
    log.cmd('help', ctx.author, ctx.guild)
    prefix = get_prefix(ctx, ctx)
    embed = discord.Embed(title='**Список команд**',
                          description='Синтаксис команд: `[об. аргумент] <необ. аргумент>`', color=0xff5757)

    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/738279888674357298/0a8114760177033f90ddfa2ac9b5c93d.png?size=64')

    for i in range(len(help_titles)):
        embed.add_field(
            name=help_titles[i], value=help_texts[i].format(prefix), inline=False)

    await ctx.message.add_reaction(emoji='📭')
    await ctx.message.author.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = config.DEFAULT_PREFIX

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def ban(ctx, member: discord.Member, *, reason="N/A"):
    log.cmd('ban', ctx.author, ctx.guild)
    await member.ban(reason=reason)

    embed = done_embed(successfull_ban())
    await ctx.send(embed=embed)

    embed = error_embed(dm_ban(ctx.guild, reason))
    await member.send(embed=embed)


@bot.command()
@commands.guild_only()
@commands.bot_has_permissions(kick_members=True)
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def kick(ctx, member: discord.Member, *, reason="N/A"):
    log.cmd('kick', ctx.author, ctx.guild)
    await member.kick()

    embed = done_embed(successfull_kick())
    await ctx.send(embed=embed)

    embed = error_embed(dm_kick(ctx.guild, reason))
    await member.send(embed=embed)


@bot.command()
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def unban(ctx, *, member):
    log.cmd('unban', ctx.author, ctx.guild)
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = done_embed(successfull_unban())
            await ctx.send(embed=embed)
            return

    embed = error_embed(user_not_found())
    await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def purge(ctx, arg: int):
    log.cmd('purge', ctx.author, ctx.guild)
    await ctx.channel.purge(limit=arg + 1)
    embed = done_embed(successfull_clear(arg))
    await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
@commands.bot_has_permissions(administrator=True)
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def prefix(ctx, prefix):
    log.cmd('prefix', ctx.author, ctx.guild)
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    embed = done_embed(successfull_prefix())
    await ctx.send(embed=embed)


@ban.error
@kick.error
@unban.error
@purge.error
@prefix.error
async def errors(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = error_embed(missing_perms())
        await ctx.send(embed=embed)
    if isinstance(error, commands.BotMissingPermissions):
        embed = error_embed(missing_bot_perms())
        await ctx.send(embed=embed)


bot.run(config.TOKEN)
