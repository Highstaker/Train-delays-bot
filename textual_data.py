#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from os import path

SCRIPT_FOLDER = path.dirname(path.realpath(__file__))

##############
# FILENAMES###
##############

#A filename of a file containing Telegram bot token.
BOT_TOKEN_FILENAME = 'tokens/token'

with open(path.join(SCRIPT_FOLDER, BOT_TOKEN_FILENAME),'r') as f:
	BOT_TOKEN = f.read().replace("\n","")

# Subscribers database
SUBSCRIBERS_DATABASE_PATH = path.join(SCRIPT_FOLDER, "databases/users.save")

#############
# TEXTS######
#############

START_MESSAGE = {"EN": "Welcome! Type /help to get help.",
"RU": "Добро пожаловать! Наберите /help для получения помощи."}
PERSONAL_LIST_MESSAGE = {"EN":"Trains you've selected are:",
"RU": "Вы выбрали следующие поезда:"}
PERSONAL_LIST_IS_EMPTY_MESSAGE = {"EN":"Your list of trains is empty! Add some by typing the train number.",
"RU": "Ваш список поездов пуст! Введите номер поезда, чтобы добавить его в список."}
SECONDS_SINCE_LAST_UPDATE_MESSAGE = {"EN": "Seconds since last update: {0}",
"RU": "Секунд прошло с момента последнего обновления данных: {0}"}
USER_TRAINS_NOT_FOUND_MESSAGE = {"EN": """Could not find any data on trains from your list.
Maybe they're not off-schedule now?""",
"RU": """Нет данных по поездам в вашем списке. Возможно они идут по расписанию или не существуют"""}
TRAIN_ADDED_MESSAGE = {"EN": "Train {0} has been added to your personal list",
"RU": "Поезд номер {0} добавлен в ваш личный список."}
TRAIN_DELETED_MESSAGE = {"EN": "Train {0} has been deleted from your personal list",
"RU": "Поезд номер {0} удалён из вашего личного списка."}
TRAIN_NOT_ON_LIST_MESSAGE = {"EN": "Train {0} is not in your personal list",
"RU": "Поезд номер {0} отсутствует в вашем личном списке."}
TO_DELETE_INFO_MESSAGE = {"EN": "To delete a train from your list, press the respective /delXXXXX link",
"RU": "Для удаления поезда нажмите на соответствующую команду формата /delXXXXX"}
FULL_TABLE_HEADER = {"EN": "Full table",
"RU":"Полная таблица"}
PERSONAL_TABLE_HEADER = {"EN": "Your personal table",
"RU":"Ваша личная таблица"}

UNKNOWN_COMMAND_MESSAGE = {"EN": "Unknown command!",
"RU":"Неизвестная команда"}


################
### BUTTONS#####
################

EN_LANG_BUTTON = "🇬🇧 EN"
RU_LANG_BUTTON = "🇷🇺 RU"

ABOUT_BUTTON = {"EN":"ℹ️ About", "RU": "ℹ️ О программе"}
OTHER_BOTS_BUTTON = {"EN":"👾 My other bots", "RU": "👾 Другие мои боты"}
HELP_BUTTON = {"EN":"⁉️" + "Help", "RU": "⁉️ Помощь"}
GET_FULL_TABLE_BUTTON = {"EN": "Get full table", "RU": "Полное расписание опозданий"}
GET_USER_TRAINS_LIST_BUTTON = {"EN": "My train list", "RU": "Мой список поездов"}
GET_USER_TRAINS_DELAYS_BUTTON = {"EN": "Get delays for my trains", "RU": "Расписание опозданий моих поездов"}

##################
# BIG TEXTS#######
##################

ABOUT_MESSAGE = """*Stockholm train delays bot*
_Created by:_ Highstaker a.k.a. OmniSable.
Source: https://github.com/Highstaker/Train-delays-bot
Version: {0}
This bot uses the python-telegram-bot library.
https://github.com/leandrotoledo/python-telegram-bot
"""

HELP_MESSAGE = """Help message"""

OTHER_BOTS_MESSAGE = """*My other bots*:

@OmniCurrencyExchangeBot: a currency converter bot supporting past rates and graphs.

@multitran\_bot: a Russian-Whichever dictionary with support of 9 languages. Has transcriptions for English words.
"""
