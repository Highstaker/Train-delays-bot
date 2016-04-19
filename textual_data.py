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

START_MESSAGE = "Welcome! Type /help to get help."
PERSONAL_LIST_MESSAGE = "Trains you've selected are:"
PERSONAL_LIST_IS_EMPTY_MESSAGE = "Your list of trains is empty! Add some by typing the train number."
SECONDS_SINCE_LAST_UPDATE_MESSAGE = "Seconds since last update: {0}"
USER_TRAINS_NOT_FOUND_MESSAGE = """Could not find any data on trains from your list.
Maybe they're not off-schedule now?"""
TRAIN_ADDED_MESSAGE = "Train {0} has been added to your personal list"
TRAIN_DELETED_MESSAGE = "Train {0} has been deleted from your personal list"
TRAIN_NOT_ON_LIST_MESSAGE = "Train {0} is not in your personal list"
TO_DELETE_INFO_MESSAGE = "To delete a train from your list, press the respective /delXXXXX link"
FULL_TABLE_HEADER = "Full table"
PERSONAL_TABLE_HEADER = "Your personal table"

UNKNOWN_COMMAND_MESSAGE = "Unknown command!"

################
### BUTTONS#####
################

ABOUT_BUTTON = "ℹ️ About"
HELP_BUTTON = "⁉️" + "Help"
OTHER_BOTS_BUTTON = "👾 My other bots"
GET_FULL_TABLE_BUTTON = "Get full table"
GET_USER_TRAINS_LIST_BUTTON = "My train list"
GET_USER_TRAINS_DELAYS_BUTTON = "Get delays for my trains"


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
