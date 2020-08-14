""" Translations for russian language """


def logged_as(name):
    return 'Бот успешно запущен под тегом "{0}"!'.format(name)


def pong(count):
    return 'Понг! Задержка сервера: {0} мс.'.format(count)


def successfull_ban():
    return 'Пользователь успешно заблокирован.'


def dm_ban(guild="", reason=""):
    return 'Вы были заблокированы на сервере **{0}** по причине **{1}**'.format(guild, reason)


def missing_perms():
    return 'У вас недостаточно прав для выполнения этой команды.'


def missing_bot_perms():
    return 'У меня недостаточно прав для выполнения этой команды. Пожалуйста, предоставьте все права для роли, которые позволят выполнить данную команду.'


def cannot_ban_user():
    return 'Невозможно заблокировать пользователя, роль которого выше роли бота.'


def at_servers(count):
    return 'на {0} серверов'.format(count)


def cannot_ban_bots():
    return 'Невозможно заблокировать бота.'
