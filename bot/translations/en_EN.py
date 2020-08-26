""" Translations for english language """

openmod = 'OpenMod'

help_titles = ['General', 'Moderation', 'Other']

help_texts = [
    '`{0}help` - display a list of commands;\n`{0}about` - information about the bot.',

    '`{0}ban [@user] <reason>` - blocking user;\n`{0}unban [user # 1234]` - unblocking user;\n\
    `{0}multiban [@user1] <user2> <user ...>` bans multiple users in a row\n`{0}kick [@user] <reason>` - kick the user;\n`{0}purge [number of messages]` - clear chat for a certain number of messages.\n\
    `{0}setname [@user] [nickname]` - set a special nickname for the user\n`{0}info <@user>` - get information about the user',

    '`{0}ping` - bot delay;\n`{0}prefix [prefix] `- set a prefix specifically for the server.'
]


def on_invite_text():
    return 'Thank you for choosing me. I am OpenMod, a bot created specifically for moderation of Discord servers, which is completely open source, I will be glad if you vote for me on monitoring: [bot on moderation, no link :)]'


def about_user():
    return 'User information:'


def user_info(id, created_at, joined_at, color):
    return '**ID:** {0}\n**Registered:** {1}\n**Joined:** {2}\n**Role Color:** {3}'.format(
        id, created_at, joined_at, color)


def logged_as(name):
    return 'Successfully logged as "{0}"!'.format(name)


def pong(count):
    return 'Pong! Took: {0} ms.'.format(count)


def successfull_ban():
    return 'User successfully banned.'


def dm_ban(guild="", reason=""):
    return 'You were banned from the server **{0}** for reason **{1}**'.format(guild, reason)


def successfull_kick():
    return 'The user has been successfully kicked from the server.'


def dm_kick(guild="", Reason=""):
    return 'You were kicked from the server **{0}** for **{1}**'.format(guild, reason)


def missing_perms():
    return 'You do not have sufficient rights to execute this command.'


def missing_bot_perms():
    return 'I do not have sufficient rights to execute this command. Please grant all rights to the role that will allow this command to run.'


def cannot_ban_user():
    return 'It is not possible to block a user whose role is higher than that of a bot.'


def too_long_name():
    return 'Nickname length must not exceed 32 characters.'


def at_servers(count):
    return 'to {0} servers'.format(count)


def at_users(count):
    return 'at {0} users'.format(count)


def cannot_ban_bots():
    return 'Unable to block the bot.'


def user_not_found():
    return 'User not found.'


def successfull_unban():
    return 'User successfully unbanned.'


def successfull_clear(messages):
    return '{0} messages cleared successfully.'.format(messages)


def successfull_prefix():
    return 'Server prefix changed successfully.'


def successfull_name():
    return 'Nickname changed successfully.'


def log_cmd(time, user, command, guild):
    return '{0} @{1} used command "{2}" on server "{3}"'.format(
        time, user, command, guild)
