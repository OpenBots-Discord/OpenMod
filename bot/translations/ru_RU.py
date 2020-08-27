""" Translations for russian language """

openmod = 'OpenMod'

help_titles = ['Общие', 'Модерация', 'Прочее']

help_texts = [
    '`{0}help` - вывести список команд; \n `{0}about` - информация о боте.',

    '`{0}ban [@пользователь] <причина>` - блокировка пользователя;\n`{0}unban [пользователь#1234]` - разблокировка пользователя\n\
    `{0}multiban [@польз.1] <польз.2> <польз...>` банит несколько пользователей подряд\n`{0}kick [@пользователь] <причина>` - кик пользователя\n`{0}purge [кол-во сообщений]` - очистка чата на определенное кол-во сообщений\n\
    `{0}setname [@пользователь] [имя]` - установить специальный никнейм для пользователя\n`{0}info <@пользователь>` - узнать информацию о пользователе',

    '`{0}ping` - задержка бота.\n`{0}prefix [префикс]` - установка префикса специально для сервера'
]


def on_invite_text():
    return 'Спасибо что выбрали меня. Я - OpenMod, бот, созданный специально для модерации серверов Дискорд, который имеет полностью открытый исходный код, буду рад, если вы проголосуете за меня на мониторинге: [бот на модерации, ссылки нет :)]'


def about_user():
    return 'Сведения о пользователе:'


def user_info(id, created_at, joined_at, color):
    return '**Айди:** {0}\n **Зарегистрировался:** {1}\n**Присоединился:** {2}\n**Цвет роли:** {3}'.format(
        id, created_at, joined_at, color)


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


def too_long_name():
    return 'Длина никнейма не должна превышать 32 символа.'


def at_servers(count):
    return 'на {0} серверов'.format(count)


def at_users(count):
    return 'на {0} пользователей'.format(count)


def at_commands(count):
    return 'на {0} команд'.format(count)


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


def successfull_name():
    return 'Никнейм успешно изменён.'


def log_cmd(time, user, command, guild):
    return '{0} @{1} использовал команду "{2}" на сервере "{3}"'.format(
        time, user, command, guild)
