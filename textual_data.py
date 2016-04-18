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

################
### BUTTONS#####
################

ABOUT_BUTTON = "ℹ️ About"
HELP_BUTTON = "⁉️" + "Help"
OTHER_BOTS_BUTTON = "👾 My other bots"
GET_FULL_TABLE_BUTTON = "Get full table"


##################
# BIG TEXTS#######
##################

ABOUT_MESSAGE = """*Random Picture Bot*
_Created by:_ Highstaker a.k.a. OmniSable.
Source: https://github.com/Highstaker/Picture-sender-telegram-bot
Version: {0}
This bot uses the python-telegram-bot library.
https://github.com/leandrotoledo/python-telegram-bot
"""

HELP_MESSAGE = """Help message"""

OTHER_BOTS_MESSAGE = """*My other bots*:

@OmniCurrencyExchangeBot: a currency converter bot supporting past rates and graphs.

@multitran\_bot: a Russian-Whichever dictionary with support of 9 languages. Has transcriptions for English words.
"""
