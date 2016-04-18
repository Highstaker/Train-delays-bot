#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

#check if the version of Python is correct
from python_version_check import check_version
check_version((3, 4, 3))

VERSION_NUMBER = (0, 0, 1)

from time import time

from telegramHigh import TelegramHigh
from textual_data import *
import delays_scraper
from button_handler import getMainMenu
from language_support import LanguageSupport
from userparams import SubscribersHandler
from logging_handler import LoggingHandler as lh

##############
###PARAMS#####
##############


#How often should the data be grabbed from the source
FILE_UPDATE_PERIOD = 60

INITIAL_SUBSCRIBER_PARAMS = {"lang": "EN",  # bot's langauge
							 "subscribed": 0, # has the user subscribed?
							 "last_update_time" : 0,
							 }


class MainBot:
	"""The main bot class"""
	def __init__(self, token):
		super(MainBot, self).__init__()

		self.bot = TelegramHigh(token)

		# the last time when the data was grabbed from server
		self.last_update_time = 1

		# the raw data about train delays
		self.data = None

		# handler of user data
		self.userparams = SubscribersHandler(savefile_path=SUBSCRIBERS_DATABASE_PATH,
											 initial_params=INITIAL_SUBSCRIBER_PARAMS)
		
		self.bot.start(processingFunction=self.processUpdate, periodicFunction=self.periodicRoutine)

	def periodicRoutine(self):

		if time() - self.last_update_time >FILE_UPDATE_PERIOD:

			lh.warning("Updating the trains data!")
			data = delays_scraper.get_data()

			if data:
				self.data = data
				self.last_update_time = time()


	def processUpdate(self, u):
		bot = self.bot
		Message = u.message
		message = Message.text
		message_id = Message.message_id
		chat_id = Message.chat_id
		subs = self.userparams

		# # initialize the user's params if they are not present yet
		subs.initializeUser(chat_id=chat_id)

		# language support class for convenience
		LS = LanguageSupport(subs.getEntry(chat_id=chat_id, param="lang"))
		lS = LS.languageSupport
		allv = LS.allVariants
		MMKM = lS(getMainMenu(subs.getEntry(chat_id=chat_id, param="subscribed")))

		if message == "/start":
			bot.sendMessage(chat_id=chat_id
				,message=lS(START_MESSAGE)
				,key_markup=MMKM
				)
		elif message == "/help" or message == HELP_BUTTON:
			bot.sendMessage(chat_id=chat_id
				,message=lS(HELP_MESSAGE)
				,key_markup=MMKM
				,markdown=True
				)
		elif message == "/about" or message == ABOUT_BUTTON:
			bot.sendMessage(chat_id=chat_id
				,message=lS(ABOUT_MESSAGE).format(".".join([str(i) for i in VERSION_NUMBER]))
				,key_markup=MMKM
				,markdown=True
				)
		elif message == "/otherbots" or message == lS(OTHER_BOTS_BUTTON):
			bot.sendMessage(chat_id=chat_id
				,message=lS(OTHER_BOTS_MESSAGE)
				,key_markup=MMKM
				,markdown=True
				)
		elif message == "/get" or message == lS(GET_FULL_TABLE_BUTTON):
			table = self.getDelaysTable()
			since_last_update = time()-self.last_update_time
			msg = table + "\n" + "Seconds since last update: {0}".format(int(since_last_update))
			bot.sendMessage(chat_id=chat_id
				,message=msg
				,key_markup=MMKM
				# ,markdown=True
				)
		else:
			bot.sendMessage(chat_id=chat_id,
				message="Unknown command!"
				,key_markup=MMKM
				)

	def getDelaysTable(self):
		data = self.data

		result = ""
		for train in data:
			result = result + "\t".join(train) + "\n"

		return result

def main():
	MainBot(BOT_TOKEN)

if __name__ == '__main__':
	main()