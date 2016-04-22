#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

#check if the version of Python is correct
from python_version_check import check_version
check_version((3, 4, 3))

VERSION_NUMBER = (0, 0, 6)

from time import time
import re
from datetime import datetime

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
							 "trains" : [] 
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
		if time() - self.last_update_time > FILE_UPDATE_PERIOD:
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
		MM = getMainMenu(subs.getEntry(chat_id=chat_id, param="subscribed"))
		MMKM = lS(MM)

		def getDelaysTable(user=None, formatted=False):
			"""
			Returns a text representation of delays table
			:param user: a chat_id to read train numbers from. If None, returns the whole current table.
			:return: string table
			"""
			data = self.data


			#Inits
			result, user_trains = "", []

			if user:
				user_trains = self.userparams.getEntry(user,"trains")

			for train in data:
				# check data for each train
				if not user or (user and train["number"] in user_trains):
					if not formatted:
						result = result + "\t".join([i for i in train.values() if isinstance(i, str)]) + "\n"
					else:
						result = result + lS(TABLE_ENTRY_BEGINNING_MESSAGE).format(train["number"])\
						+ (lS(DEPARTED_FROM_APPENDIX).format(train["station"]) if train["departed"] else lS(ARRIVED_AT_APPENDIX).format(train["station"]))\
							+ (lS(COMES_ONTIME_APPENDIX) if train["delay"][1:] == "0"
								else lS(TABLE_ENTRY_ONOFFTIME_APPENDIX).format(
							train["delay"].replace("-","").replace("+",""),
							lS(COMES_EARLY_APPENDIX) if train["delay"][0] == "-" else lS(COMES_LATE_APPENDIX)
							)
							)\
							+ (lS(RED_LIGHT_APPENDIX) if train["red_light"] else "")\
							+ "\n"

			return result

		def sendTable(user=None):
			"""
			Sends a table of delays

			:param user: a chat_id to read train numbers from. If None, returns the whole current table.
			"""
			table = getDelaysTable(user, formatted=True) 

			if table:
				since_last_update = time()-self.last_update_time
				msg = (lS(PERSONAL_TABLE_HEADER) if user else lS(FULL_TABLE_HEADER) ) + "\n" \
				+ lS("Current time: ") + datetime.now().strftime("%H:%M") + "\n\n" \
				+ table \
				+ "\n" + lS(SECONDS_SINCE_LAST_UPDATE_MESSAGE).format(int(since_last_update))
			else:
				msg = lS(USER_TRAINS_NOT_FOUND_MESSAGE)

			bot.sendMessage(chat_id=chat_id
				,message=msg
				,key_markup=MMKM
				,markdown=True
				)

		if message == "/start":
			bot.sendMessage(chat_id=chat_id
				,message=lS(START_MESSAGE)
				,key_markup=MMKM
				)
		elif message == "/help" or message == lS(HELP_BUTTON):
			bot.sendMessage(chat_id=chat_id
				,message=lS(HELP_MESSAGE)
				,key_markup=MMKM
				,markdown=True
				)
		elif message == "/about" or message == lS(ABOUT_BUTTON):
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
			sendTable(user=None)
		elif message == "/getmy" or message == lS(GET_USER_TRAINS_DELAYS_BUTTON):
			sendTable(user=chat_id)
		elif message == "/mylist" or message == lS(GET_USER_TRAINS_LIST_BUTTON):
			trains = subs.getEntry(chat_id,"trains")
			if trains:
				msg = lS(PERSONAL_LIST_MESSAGE) + "\n" + "\n".join([i + "\t /del" + i for i in trains])\
					  + "\n" + lS(TO_DELETE_INFO_MESSAGE)
			else: 
				msg = lS(PERSONAL_LIST_IS_EMPTY_MESSAGE)
			bot.sendMessage(chat_id=chat_id
			,message=msg
			,key_markup=MMKM
			# ,markdown=True
			)
		elif re.fullmatch(r"^/del[0-9]+[A-Za-z]?$", message):
			train = message[4:]
			trains = subs.getEntry(chat_id,"trains")
			if train in trains:
				subs.setEntry(chat_id,"trains",list(filter(train.__ne__,trains)))
				msg = lS(TRAIN_DELETED_MESSAGE).format(train)
			else:
				msg = lS(TRAIN_NOT_ON_LIST_MESSAGE).format(train)

			bot.sendMessage(chat_id=chat_id
				,message=msg
				,key_markup=MMKM
				# ,markdown=True
				)
		elif re.fullmatch(r"^[0-9]+[A-Za-z]?$", message):
			train = message.upper()
			subs.setEntry(chat_id,"trains",train,append=True)
			bot.sendMessage(chat_id=chat_id
				,message=lS(TRAIN_ADDED_MESSAGE).format(train)
				,key_markup=MMKM
				# ,markdown=True
				)
			
		elif message == RU_LANG_BUTTON:
			subs.setEntry(chat_id, "lang", 'RU')
			LS = LanguageSupport("RU")
			bot.sendMessage(chat_id=chat_id
							, message="Сообщения бота будут отображаться на русском языке."
							, key_markup=LS.languageSupport(MM)
							)
		elif message == EN_LANG_BUTTON:
			subs.setEntry(chat_id, "lang", 'EN')
			LS = LanguageSupport("EN")
			bot.sendMessage(chat_id=chat_id
							, message="Bot messages will be shown in English."
							, key_markup=LS.languageSupport(MM)
							)
		else:
			bot.sendMessage(chat_id=chat_id,
				message=lS(UNKNOWN_COMMAND_MESSAGE)
				,key_markup=MMKM
				)

def main():
	MainBot(BOT_TOKEN)

if __name__ == '__main__':
	main()