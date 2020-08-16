""" Translations for english language """


def logged_as(name):
    return 'Successfully logged as "{0}"!'.format(name)


def pong(count):
    return 'Pong! Took: {0} ms.'.format(count)


def successfull_ban():
    return 'User successfully banned.'


def dm_ban(guild="", reason=""):
    return 'You were banned from the server **{0}** for reason **{1}**'.format(guild, reason)


def missing_perms():
    return 'You do not have sufficient rights to execute this command.'


def missing_bot_perms():
    return 'I do not have sufficient rights to execute this command. Please grant all rights to the role that will allow this command to run.'


def cannot_ban_user():
    return 'It is not possible to block a user whose role is higher than that of a bot.'


def at_servers(count):
    return 'to {0} servers'.format(count)


def cannot_ban_bots():
    return 'Unable to block the bot.'


def user_not_found():
    return 'User not found.'


def successfull_unban():
    return 'User successfully unbanned.'
