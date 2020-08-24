""" Translations for russian language """

help_titles = ['Общие', 'Модерация', 'Прочее']

help_texts = [
    '`{0}help` - вывести список команд; \n `{0}about` - информация о боте.',

    '`{0}ban [@пользователь] <причина>` - блокировка пользователя; \n `{0}unban [пользователь#1234]` - разблокировка пользователя \n \
     `{0}kick [@пользователь] <причина>` - кик пользователя \n `{0}purge [кол-во сообщений]` - очистка чата на определенное кол-во сообщений \n \
     `{0}info <@пользователь>` - узнать информацию о пользователе',

    '`{0}ping` - задержка бота. \n `{0}prefix [префикс]` - установка префикса специально для сервера'
]

type_user = 'Пользователь'
type_bot = 'Бот'


def about_user():
    return 'Сведения о пользователе:'


def user_info(id, tag, is_bot, created_at, joined_at):
    return '**Айди:** {0} \n **Тег:** {1} \n **Тип:** {2} \n **Зарегистрировался:** {3} \n **Присоединился:** {4}'.format(
        id, tag, is_bot, created_at, joined_at)


def logged_as(name):
    return 'Бот успешно запущен под тегом "{0}"!'.format(name)


def pong(count):
    return 'Понг! Задержка сервера: {0} мс.'.format(count)


def successfull_ban():
    return 'Пользователь успешно заблокирован.'


def dm_ban(guild="", reason=""):
    return 'Вы были заблокированы на сервере **{0}** по причине **{1}**'.format(guild, reason)


def successfull_kick():
    return 'Пользователь успешно выгнан с сервера.'


def dm_kick(guild="", reason=""):
    return 'Вы были выгнаны с сервера **{0}** по причине **{1}**'.format(guild, reason)


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


def user_not_found():
    return 'Пользватель не найден.'


def successfull_unban():
    return 'Пользователь успешно разблокирован.'


def successfull_clear(messages):
    return 'Успешно очищено {0} сообщений.'.format(messages)


def successfull_prefix():
    return 'Префикс сервера успешно изменён.'


def log_cmd(time, user, command, guild):
    return '{0} @{1} использовал команду "{2}" на сервере "{3}"'.format(
        time, user, command, guild)
