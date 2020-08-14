import asyncio
import discord
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


def done_embed(msg):
    return discord.Embed(color=0x00FF47, description="✅⼁" + msg)


def warn_embed(msg):
    return discord.Embed(color=0xFFD600, description="⚠⼁" + msg)


def error_embed(msg):
    return discord.Embed(color=0xED4242, description="‼⼁" + msg)


bot = Bot(command_prefix=config.PREFIX, help_command=None)


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
async def ping(ctx):
    log.cmd('ping', ctx.author, ctx.guild)
    latency = int(round(bot.latency * 100, 1))
    embed = done_embed(pong(str(latency)))
    await ctx.send(embed=embed)


# Ban member
@bot.command()
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def ban(ctx, member: discord.User, *, reason="N/A"):
    if member.bot:
        embed = error_embed(cannot_ban_bots())
        await ctx.send(embed=embed)
    else:
        await member.ban(reason=reason)
        embed = done_embed(successfull_ban())
        await ctx.send(embed=embed)
        embed = error_embed(dm_ban(ctx.guild, reason))
        await member.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = error_embed(missing_perms())
        await ctx.send(embed=embed)
    if isinstance(error, commands.BotMissingPermissions):
        embed = error_embed(missing_bot_perms())
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandInvokeError):
        embed = error_embed(cannot_ban_user())
        await ctx.send(embed=embed)

bot.run(config.TOKEN)
