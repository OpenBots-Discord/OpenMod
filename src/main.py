# -*- coding: utf-8 -*-

import asyncio
import json
import os
import sqlite3
from os.path import abspath, dirname
from typing import NoReturn

import discord

# from scripts import db
from discord.ext import commands, tasks
from discord.ext.commands import AutoShardedBot
from discord_slash import SlashCommand
from dotenv import load_dotenv
from slashify import Slashify
from termcolor import cprint

from cogs.utils import Config, Logger, Strings, Utils

CONFIG = Config()
STRINGS = Strings(CONFIG["default_locale"])

filepath = dirname(abspath(__file__))

cprint(STRINGS["etc"]["info"]["art"], "white")

cprint("Default locale is {0}".format(CONFIG["default_locale"]), "green")

bot = AutoShardedBot(command_prefix=Utils.get_prefix, help_command=None)


@bot.event
async def on_ready() -> NoReturn:
    for filename in os.listdir(filepath + "/cogs/"):
        if filename.endswith(".py"):
            bot.load_extension("cogs.{0}".format(filename[:-3]))

    await bot.change_presence(activity=discord.Game(name="..."))
    bot.load_extension("jishaku")
    Logger.done(STRINGS["bot_log"]["logged_as"].format(bot.user))


bot.run(CONFIG["token"])
